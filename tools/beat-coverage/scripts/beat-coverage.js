#!/usr/bin/env node
// Node built-ins only. Governed by wiser/standards/script-contract.md.
import {
  existsSync, lstatSync, openSync, closeSync, writeFileSync, readFileSync,
  realpathSync, readdirSync, statSync,
} from 'node:fs';
import { basename, dirname, isAbsolute, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT = fileURLToPath(import.meta.url);
const TOOL = realpathSync(resolve(dirname(SCRIPT), '..'));
const HELP = `beat-coverage - read recorded coverage without opening its sources

Usage:
  node scripts/beat-coverage.js pull --dir <directory> --from YYYY-MM-DD --to YYYY-MM-DD [options]
  node scripts/beat-coverage.js count --dir <directory> --from YYYY-MM-DD --to YYYY-MM-DD [options]
  node scripts/beat-coverage.js help
  node scripts/beat-coverage.js <command> help

Commands:
  pull             Write --output, or return Markdown in the JSON markdown field
  count            Print counts only as one JSON object; writes nothing
  help             Return this usage in one JSON object

Options for pull and count:
  --dir <path>     Absolute directory of reporter .md files, read without recursion
  --from <date>    First date, YYYY-MM-DD, inclusive
  --to <date>      Last date, YYYY-MM-DD, inclusive
  --beat <regex>   Case-insensitive JavaScript regular expression; absent, no filter
  --exclude <name> Skip an exact file name; repeatable
  --output <path>  pull only: new absolute .md file outside this tool; parent must exist
  --help, -h      Return usage before reading any files

Year-only items count when their year equals --to's year and are marked year only.
Month-only dates use the month's first day. Undated items are omitted and counted.
Beat filtering runs first, so rejection counts are disjoint. Traction: lines are
dropped from output. Every kept item is unverified. Installs nothing, needs no
credentials, and makes no network requests. Success (including help) prints one
JSON object. Failure prints only to stderr and exits 1.`;

function fail(message) {
  throw new Error(`${message} See "node scripts/beat-coverage.js help".`);
}

function parseArgs(args) {
  let command = args[0] || 'help';
  if (command === '--help' || command === '-h') command = 'help';
  if (!['pull', 'count', 'help'].includes(command)) fail(`Unknown command "${command}".`);
  const options = { exclude: [] };
  let help = command === 'help';
  const allowed = new Set(['--dir', '--from', '--to', '--beat', '--exclude', '--output']);
  for (let i = 1; i < args.length; i++) {
    const flag = args[i];
    if (['help', '--help', '-h'].includes(flag)) {
      help = true;
      continue;
    }
    if (!allowed.has(flag)) fail(`Unknown option "${flag}".`);
    if (flag === '--output' && command === 'count') fail('--output is only valid with pull.');
    const value = args[++i];
    if (value === undefined || value.startsWith('--')) fail(`${flag} needs a value.`);
    const key = flag.slice(2);
    if (key === 'exclude') options.exclude.push(value);
    else {
      if (Object.hasOwn(options, key)) fail(`${flag} was given more than once; pass it once.`);
      options[key] = value;
    }
  }
  if (help) return { help: true };
  for (const key of ['dir', 'from', 'to']) {
    if (!options[key]) fail(`--${key} is required.`);
  }
  for (const key of ['from', 'to']) {
    if (!validDate(options[key])) fail(`--${key} must be a real date in YYYY-MM-DD form.`);
  }
  if (options.from > options.to) fail('--from must be on or before --to.');
  if (options.beat !== undefined) {
    try { options.pattern = new RegExp(options.beat, 'i'); }
    catch { fail('--beat is not a valid regular expression; correct it or omit the filter.'); }
  }
  for (const name of options.exclude) {
    if (!name || name === '.' || name === '..' || /[/\\]/.test(name)) {
      fail('--exclude must be a file name, without a directory.');
    }
  }
  return { command, options };
}

function validDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const date = new Date(`${value}T00:00:00Z`);
  return !Number.isNaN(date.valueOf()) && date.toISOString().slice(0, 10) === value;
}

// Resolve every existing ancestor, including a link used as a missing file's parent.
function canonical(value, flag) {
  if (!isAbsolute(value)) fail(`${flag} must be an absolute path.`);
  let ancestor = resolve(value);
  const suffix = [];
  try {
    while (!existsSync(ancestor)) {
      // existsSync is false for a dangling link too; do not treat that as absent.
      try {
        lstatSync(ancestor);
        fail(`${flag} names a broken symbolic link; choose a usable path.`);
      } catch (error) {
        if (error.code !== 'ENOENT') throw error;
      }
      const parent = dirname(ancestor);
      if (parent === ancestor) fail(`${flag} cannot be resolved; check its ancestors.`);
      suffix.unshift(basename(ancestor));
      ancestor = parent;
    }
    return join(realpathSync(ancestor), ...suffix);
  } catch (error) {
    if (error.message.endsWith('help".')) throw error;
    fail(`${flag} cannot be resolved; check the path and its permissions.`);
  }
}

function inside(child, parent) {
  const part = relative(parent, child);
  return part === '' || (part !== '..' && !part.startsWith(`..${sep}`) && !isAbsolute(part));
}

// realpath can preserve a caller's case on case-insensitive filesystems.
// Compare every existing ancestor by identity, including above a missing parent.
function insideToolDirectory(target) {
  let toolIdentity;
  try { toolIdentity = statSync(TOOL); }
  catch { fail('--output cannot be screened against this tool; check its directory and permissions.'); }
  let ancestor = target;
  for (;;) {
    try {
      const identity = statSync(ancestor);
      if (identity.dev === toolIdentity.dev && identity.ino === toolIdentity.ino) return true;
    } catch (error) {
      if (error.code !== 'ENOENT' && error.code !== 'ENOTDIR') {
        fail('--output ancestors cannot be screened; check their paths and permissions.');
      }
    }
    const parent = dirname(ancestor);
    if (parent === ancestor) return false;
    ancestor = parent;
  }
}

function inputFiles(options) {
  const directory = canonical(options.dir, '--dir');
  let entries;
  try {
    if (!statSync(directory).isDirectory()) fail('--dir must name a directory of reporter files.');
    entries = readdirSync(directory, { withFileTypes: true });
  } catch (error) {
    if (error.message.endsWith('help".')) throw error;
    fail('--dir could not be read; choose an existing readable directory.');
  }
  const files = [];
  for (const entry of entries.sort((a, b) => a.name < b.name ? -1 : a.name > b.name ? 1 : 0)) {
    if (entry.name.startsWith('.') || !entry.name.toLowerCase().endsWith('.md')) continue;
    if (options.exclude.includes(entry.name)) continue;
    if (!entry.isFile() && !entry.isSymbolicLink()) continue;
    const path = canonical(join(directory, entry.name), 'reporter file');
    // A reporter link cannot silently open another directory or a disguised credential.
    if (!inside(path, directory) || basename(path).startsWith('.') || !path.toLowerCase().endsWith('.md')) {
      fail('A reporter file resolves outside --dir or onto a non-Markdown file; remove or exclude its link.');
    }
    if (options.exclude.includes(basename(path))) continue;
    try {
      if (!statSync(path).isFile()) fail('A reporter path is not a regular file; remove or exclude it.');
    } catch (error) {
      if (error.message.endsWith('help".')) throw error;
      fail('A reporter file could not be read; check its permissions or exclude it.');
    }
    files.push({ path, name: entry.name });
  }
  return files;
}

const HEADING = /^ {0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$/;
const ITEM = /^ {0,3}(?:\d+[.)]|[-*+])\s+(.*)$/;
const LEGACY = /^(Compelling work|Most recent)\b/i;
const ITEM_TOKEN = /^(?:\*\*|__)?Item:(?:\*\*|__)?\s*/i;
const TRACTION = /^\s*(?:[-*+]\s+)?(?:\*\*|__)?Traction:(?:\*\*|__)?\s*/i;
const MONTH = '(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\\.?';
const ENGLISH_DATE = new RegExp(`\\b(?:(\\d{1,2})\\s+${MONTH}\\s+|${MONTH}\\s+(?:(\\d{1,2}),?\\s+)?)((?:19|20)\\d{2})\\b`, 'i');
const MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];

function reporterName(text) {
  let fence;
  for (const line of text.split(/\r?\n/)) {
    const code = line.match(/^\s*(`{3,}|~{3,})/);
    if (code) {
      if (!fence) fence = code[1][0];
      else if (code[1][0] === fence) fence = undefined;
      continue;
    }
    if (fence) continue;
    const title = line.match(/^ {0,3}#\s+(.+?)(?:\s+#+)?\s*$/);
    if (title) return title[1].replace(/^Bio sketch:\s*/i, '').trim() || 'not stated';
  }
  return 'not stated';
}

export function coverageItems(text) {
  const bio = /^schema:\s*bio-sketch\s*$/m.test(text) || /^# Bio sketch:/im.test(text);
  const items = [];
  let section = '';
  let current;
  let fence;
  const flush = () => { if (current) items.push(current); current = undefined; };
  for (const line of text.split(/\r?\n/)) {
    const code = line.match(/^\s*(`{3,}|~{3,})/);
    if (code) {
      if (!fence) fence = code[1][0];
      else if (code[1][0] === fence) fence = undefined;
      continue;
    }
    if (fence) continue;
    const heading = line.match(HEADING);
    if (heading) {
      flush();
      section = heading[1];
      continue;
    }
    const item = line.match(ITEM);
    if (item) {
      if (TRACTION.test(item[1])) {
        if (current) current.lines.push(item[1]);
        continue;
      }
      flush();
      const record = ITEM_TOKEN.test(item[1]);
      if (section && (LEGACY.test(section) || (bio && (record || /^Record\b/i.test(section))))) {
        if (!/^(?:\*\*|__)?Not available:/i.test(item[1])) {
          current = { section, lines: [item[1]], record: bio && !LEGACY.test(section) };
        }
      }
    } else if (current && line.trim()) current.lines.push(line.trim());
  }
  flush();
  return items;
}

export function itemDate(item) {
  // A date inside a link never dates the item, including an explicit date field.
  const lines = item.lines.map(line => line.replace(/https?:\/\/\S+/gi, ' '));
  let text = lines[0];
  if (item.record) {
    const all = lines.join(' ');
    // In a Bio Sketch record, As of is the publication date, never the file's capture date.
    const stated = all.match(/\b(?:Published|Date|As of):\s*(.*?)(?=\b(?:Source|Register|Read|Superseded|Kind|Published|Date|As of):|$)/i);
    if (stated) text = stated[1];
    else text = all.split(/\b(?:Source|Register|Read|Superseded):/i)[0];
  }
  for (const pattern of [
    /\b((?:19|20)\d{2})-(\d{2})(?:-(\d{2}))?\b/,
    /\b((?:19|20)\d{2})\/(\d{2})(?:\/(\d{2}))?\b/,
  ]) {
    const iso = text.match(pattern);
    if (iso) {
      const date = `${iso[1]}-${iso[2]}-${iso[3] || '01'}`;
      return validDate(date) ? { date, recorded: iso[0], kind: iso[3] ? 'day' : 'month' } : { kind: 'undated' };
    }
  }
  const english = text.match(ENGLISH_DATE);
  if (english) {
    const month = String(MONTHS.indexOf((english[2] || english[3]).slice(0, 3).toLowerCase()) + 1).padStart(2, '0');
    const day = english[1] || english[4];
    const date = `${english[5]}-${month}-${(day || '1').padStart(2, '0')}`;
    return validDate(date) ? { date, recorded: english[0], kind: day ? 'day' : 'month' } : { kind: 'undated' };
  }
  if (/\b\d{1,2}\/\d{1,2}\/(?:19|20)\d{2}\b/.test(text)) return { kind: 'undated' };
  const year = text.match(/(?<![\d-])((?:19|20)\d{2})(?![\d-])/);
  return year ? { date: year[1], recorded: year[1], kind: 'year' } : { kind: 'undated' };
}

function oneLine(value) {
  return value.replace(/[\r\n\u2028\u2029]/g, ' ').trim();
}

export function collect(options) {
  const files = inputFiles(options);
  const counts = { files: 0, items: 0, kept: 0, year_only: 0, undated: 0, off_beat: 0, outside_window: 0, bytes: 0 };
  const blocks = [];
  for (const file of files) {
    let bytes;
    try { bytes = readFileSync(file.path); }
    catch { fail('A reporter file could not be read; check its permissions or exclude it.'); }
    counts.files++;
    counts.bytes += bytes.length;
    const text = bytes.toString('utf8');
    const name = reporterName(text);
    const lines = [];
    for (const item of coverageItems(text)) {
      counts.items++;
      if (options.pattern && !options.pattern.test(item.lines.join('\n'))) {
        counts.off_beat++;
        continue;
      }
      const date = itemDate(item);
      if (date.kind === 'undated') {
        counts.undated++;
        continue;
      }
      const keep = date.kind === 'year' ? date.date === options.to.slice(0, 4)
        : options.from <= date.date && date.date <= options.to;
      if (!keep) {
        counts.outside_window++;
        continue;
      }
      counts.kept++;
      if (date.kind === 'year') counts.year_only++;
      const flag = date.kind === 'year' ? ' [date: year only; included for the window\'s last year]'
        : date.kind === 'month' ? ' [date: month only; compared as the first day]' : '';
      const recorded = item.lines.filter(line => !TRACTION.test(line)).map(oneLine).join(' ');
      lines.push(`- **unverified** | File: ${oneLine(file.name)} | Name: ${oneLine(name)} | Section: ${oneLine(item.section)} | Date: ${date.recorded}${flag} | ${recorded}`);
    }
    if (lines.length) blocks.push(`## ${oneLine(file.name)}\n\n${lines.join('\n')}\n`);
  }
  const markdown = `# Beat coverage, ${options.from} to ${options.to}\n\nRecorded coverage only. Every item is **unverified**; no source page was opened.\n\n${blocks.join('\n')}`;
  return { counts, markdown };
}

function outputPath(value) {
  const path = canonical(value, '--output');
  if (insideToolDirectory(path)) fail('--output resolves inside this tool; choose a work directory outside it.');
  if (!path.toLowerCase().endsWith('.md')) fail('--output must end in .md.');
  if (existsSync(path)) fail('--output already exists; choose a new file so no earlier output is lost.');
  try {
    if (!statSync(dirname(path)).isDirectory()) fail('--output parent must be an existing directory.');
  } catch (error) {
    if (error.message.endsWith('help".')) throw error;
    fail('--output parent does not exist or cannot be read; choose an existing work directory.');
  }
  return path;
}

export function main(args = process.argv.slice(2)) {
  const parsed = parseArgs(args);
  if (parsed.help) return { usage: HELP };
  const { command, options } = parsed;
  // Validate the destination before any source read. Exclusive creation refuses hard links too.
  const output = options.output === undefined ? undefined : outputPath(options.output);
  const result = collect(options);
  if (command === 'count') return result.counts;
  if (output) {
    let descriptor;
    try {
      descriptor = openSync(output, 'wx');
      writeFileSync(descriptor, result.markdown, 'utf8');
    } catch {
      fail('Could not create --output; choose a new writable .md path. A failed write may leave an incomplete file.');
    } finally {
      if (descriptor !== undefined) closeSync(descriptor);
    }
    return { counts: result.counts, output };
  }
  return result;
}

// With --eval/--print, argv[1] is an argument to the evaluating program, not its entry file.
const evaluated = process.execArgv.some(arg => /^(?:--eval(?:=|$)|--print(?:=|$)|-[ep])/.test(arg));
if (!evaluated && process.argv[1] && realpathSync(resolve(process.argv[1])) === SCRIPT) {
  try { process.stdout.write(`${JSON.stringify(main())}\n`); }
  catch (error) {
    process.stderr.write(`Error: ${error.message}\n`);
    process.exitCode = 1;
  }
}
