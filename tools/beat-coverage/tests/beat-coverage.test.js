import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import {
  cpSync, existsSync, linkSync, mkdirSync, mkdtempSync, readFileSync,
  realpathSync, rmSync, statSync, symlinkSync, writeFileSync,
} from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { coverageItems, itemDate } from '../scripts/beat-coverage.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const TOOL = resolve(HERE, '..');
const SCRIPT = join(TOOL, 'scripts', 'beat-coverage.js');
const FIXTURES = join(HERE, 'fixtures', 'reporters');
const WINDOW = ['--from', '2026-01-01', '--to', '2026-11-05'];
const EXCLUSIONS = ['--exclude', 'excluded.md', '--exclude', 'excluded-again.md'];
const FILTER = ['--beat', '\\bagent'];
const EXPECTED = { files: 2, items: 10, kept: 6, year_only: 1, undated: 2, off_beat: 1, outside_window: 1 };

function run(args) {
  return spawnSync(process.execPath, [SCRIPT, ...args], { encoding: 'utf8' });
}

function success(result) {
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, '');
  // JSON.parse rejects additional objects, Markdown, or logging on stdout.
  const body = JSON.parse(result.stdout);
  assert.ok(body && !Array.isArray(body) && typeof body === 'object');
  return body;
}

function refusal(args, message) {
  const result = run(args);
  assert.equal(result.status, 1);
  assert.equal(result.stdout, '');
  assert.match(result.stderr, message);
  assert.match(result.stderr, /help/);
}

function scratch(t) {
  // All test writes stay in the checkout, outside the tool's protected directory.
  const path = mkdtempSync(join(dirname(TOOL), 'beat-coverage-test-'));
  t.after(() => rmSync(path, { recursive: true, force: true }));
  return path;
}

function standard(command = 'count', directory = FIXTURES) {
  return [command, '--dir', directory, ...WINDOW, ...EXCLUSIONS, ...FILTER];
}

test('both shapes yield exact counts, byte totals, and one count-only JSON object', () => {
  const body = success(run(standard()));
  const bytes = ['legacy.md', 'bio.md'].reduce((sum, name) => sum + readFileSync(join(FIXTURES, name)).length, 0);
  assert.deepEqual(body, { ...EXPECTED, bytes });
  assert.equal(body.items, body.kept + body.undated + body.off_beat + body.outside_window);
});

test('pull prints Markdown in JSON, groups files, and preserves recorded fields on one line per item', () => {
  const body = success(run(standard('pull')));
  assert.deepEqual(Object.keys(body).sort(), ['counts', 'markdown']);
  assert.equal(body.counts.kept, 6);
  const lines = body.markdown.split('\n');
  const items = lines.filter(line => line.startsWith('- '));
  assert.equal(items.length, 6);
  for (const line of items) {
    assert.match(line, /\*\*unverified\*\*/);
    assert.match(line, /File: (bio|legacy)\.md \| Section: .+ \| Date: 2026/);
    assert.match(line, /Fixture Desk [ABC]/);
  }
  assert.match(body.markdown, /Section: Compelling work \(recorded examples\)/);
  assert.match(body.markdown, /Section: Most recent coverage/);
  assert.match(body.markdown, /Section: Selected investigations/);
  assert.match(body.markdown, /Agent yearly survey.*2026/);
  assert.match(body.markdown, /Date: 2026 \[date: year only; included for the window's last year\]/);
  assert.match(body.markdown, /Date: 2026-07 \[date: month only; compared as the first day\]/);
  assert.match(body.markdown, /Agent rollback evidence/);
  assert.match(body.markdown, /Agent dispatch notes, Fixture Desk B/);
  assert.match(body.markdown, /As of: 2026-02-28/);
  assert.doesNotMatch(body.markdown, /Traction:|REMOVE|excluded record|Agent archive|Baking notes|publication date|scheduling notes|Role statement:|Beat:/);
  assert.ok(body.markdown.indexOf('## bio.md') < body.markdown.indexOf('## legacy.md'));
});

test('pull writes the same Markdown to a new absolute output and returns its resolved path', t => {
  const directory = scratch(t);
  const output = join(directory, 'coverage.md');
  const body = success(run([...standard('pull'), '--output', output]));
  assert.deepEqual(Object.keys(body).sort(), ['counts', 'output']);
  assert.equal(body.output, realpathSync(output));
  const printed = success(run(standard('pull')));
  assert.equal(readFileSync(output, 'utf8'), printed.markdown);
  assert.deepEqual(body.counts, printed.counts);
});

test('absent beat filter keeps otherwise eligible off-beat coverage', () => {
  const body = success(run(['count', '--dir', FIXTURES, ...WINDOW, ...EXCLUSIONS]));
  assert.equal(body.kept, 7);
  assert.equal(body.off_beat, 0);
  assert.equal(body.undated, 2);
});

test('repeatable exclusions skip whole files before item and byte counts', () => {
  const all = success(run(['count', '--dir', FIXTURES, ...WINDOW, ...FILTER]));
  const excluded = success(run(standard()));
  assert.equal(all.files - excluded.files, 2);
  assert.equal(all.items - excluded.items, 2);
  assert.equal(all.kept - excluded.kept, 2);
  assert.equal(all.bytes - excluded.bytes,
    readFileSync(join(FIXTURES, 'excluded.md')).length + readFileSync(join(FIXTURES, 'excluded-again.md')).length);
});

test('inclusive dates, month dates, invalid dates, and last-year-only inclusion', t => {
  const directory = scratch(t);
  writeFileSync(join(directory, 'window.md'), `# Fixture\n## Most recent\n
- Agent lower boundary (Fixture Desk, 2026-05-05).
- Agent upper boundary (Fixture Desk, 2026-11-05).
- Agent before window (Fixture Desk, 2026-05-04).
- Agent after window (Fixture Desk, 2026-11-06).
- Agent month before boundary (Fixture Desk, 2026-05).
- Agent last year only (Fixture Desk, 2026).
- Agent earlier year only (Fixture Desk, 2025).
- Agent impossible day (Fixture Desk, 2026-02-30).
`);
  const body = success(run(['count', '--dir', directory, '--from', '2026-05-05', '--to', '2026-11-05']));
  assert.deepEqual({ ...body, bytes: 0 }, { files: 1, items: 8, kept: 3, year_only: 1, undated: 1, off_beat: 0, outside_window: 4, bytes: 0 });
});

test('off-beat undated records count only as off-beat', () => {
  const body = success(run(['count', '--dir', FIXTURES, ...WINDOW, ...EXCLUSIONS, '--beat', '^does-not-match$']));
  assert.equal(body.off_beat, 10);
  assert.equal(body.undated, 0);
  assert.equal(body.outside_window, 0);
  assert.equal(body.kept, 0);
});

test('unrelated file types, hidden files and nested directories are not read', t => {
  const directory = scratch(t);
  cpSync(FIXTURES, join(directory, 'input'), { recursive: true });
  const input = join(directory, 'input');
  mkdirSync(join(input, 'nested'));
  writeFileSync(join(input, 'nested', 'nested.md'), '## Most recent\n- Agent nested (Fixture Desk, 2026-06-01).');
  writeFileSync(join(input, 'ignored.txt'), '## Most recent\n- Agent text (Fixture Desk, 2026-06-01).');
  writeFileSync(join(input, '.hidden.md'), '## Most recent\n- Agent hidden (Fixture Desk, 2026-06-01).');
  assert.deepEqual(success(run(standard('count', input))), success(run(standard())));
});

test('empty directories yield zero counts and a valid Markdown document', t => {
  const directory = scratch(t);
  const body = success(run(['pull', '--dir', directory, ...WINDOW]));
  assert.deepEqual(body.counts, { files: 0, items: 0, kept: 0, year_only: 0, undated: 0, off_beat: 0, outside_window: 0, bytes: 0 });
  assert.match(body.markdown, /^# Beat coverage/);
});

test('code examples, unavailable records and dated non-work facts do not count', () => {
  const text = '# Bio sketch: Fixture\n## Record\n- Not available: not supplied. As of: 2026-01-01.\n```md\n- Item: Agent example, Fixture Desk. As of: 2026-02-01.\n```\n## Role\n- Role statement: Agent editor. As of: 2026-02-01.\n## Other work\n- Item: Agent actual, Fixture Desk. As of: 2026-02-01.\n';
  assert.equal(coverageItems(text).length, 1);
  assert.equal(coverageItems(text)[0].section, 'Other work');
});

test('Traction lines in plain, bold and bulleted forms are removed without extra items', t => {
  const directory = scratch(t);
  writeFileSync(join(directory, 'traction.md'), '## Most recent\n- Traction: remove-orphan\n- Agent fixture (Fixture Desk, 2026-02-01).\n  Traction: remove-one\n  **Traction:** remove-two\n  - **Traction:** remove-three\n    Why it matters: recorded context.\n');
  const body = success(run(['pull', '--dir', directory, ...WINDOW]));
  assert.equal(body.counts.items, 1);
  assert.equal(body.counts.kept, 1);
  assert.doesNotMatch(body.markdown, /Traction|remove-/);
  assert.match(body.markdown, /recorded context/);
});

test('Bio Sketch publication date wins over a source URL; undated URL does not supply a date', () => {
  const items = coverageItems(readFileSync(join(FIXTURES, 'bio.md'), 'utf8'));
  assert.equal(itemDate(items[0]).date, '2026-02-28');
  assert.deepEqual(itemDate(items[1]), { kind: 'undated' });
});

test('help is a JSON object before configuration or file checks', () => {
  for (const args of [[], ['help'], ['--help'], ['-h'], ['pull', 'help'], ['count', '--help'], ['pull', '-h', '--dir', '/missing-reporter-directory', '--from', 'bad']]) {
    const body = success(run(args));
    assert.deepEqual(Object.keys(body), ['usage']);
    for (const word of ['pull', 'count', 'help', '--dir', '--from', '--to', '--beat', '--output', '--exclude', '--help', '-h']) {
      assert.ok(body.usage.includes(word), word);
    }
  }
});

test('unknown flags, duplicate options and discarded count output are refused before reads', () => {
  refusal(['count', '--dir', '/missing-reporter-directory', '--typo', 'x'], /Unknown option "--typo"/);
  refusal(['count', '--install'], /Unknown option "--install"/);
  refusal(['pull', '--env', '/missing-config'], /Unknown option "--env"/);
  refusal([...standard(), '--from', '2026-02-01'], /--from was given more than once/);
  refusal([...standard(), '--output', '/missing-output.md'], /--output is only valid with pull/);
  refusal(['help', '--typo'], /Unknown option "--typo"/);
});

test('bad windows, bad regular expressions and missing values fail with empty stdout', () => {
  refusal(['count'], /--dir is required/);
  refusal(['count', '--dir', FIXTURES, '--from', '2026-02-30', '--to', '2026-11-05'], /--from must be a real date/);
  refusal(['count', '--dir', FIXTURES, '--from', '2026-11-06', '--to', '2026-11-05'], /--from must be on or before/);
  refusal([...standard(), '--beat'], /--beat needs a value/);
  refusal(['count', '--dir', FIXTURES, ...WINDOW, '--beat', '['], /--beat is not a valid regular expression/);
  refusal([...standard(), '--exclude', '../other.md'], /--exclude must be a file name/);
});

test('relative or unreadable inputs fail with empty stdout', () => {
  refusal(['count', '--dir', '.', ...WINDOW], /--dir must be an absolute path/);
  refusal(['count', '--dir', '/missing-reporter-directory', ...WINDOW], /--dir could not be read/);
  refusal(['count', '--dir', join(FIXTURES, 'bio.md'), ...WINDOW], /--dir must name a directory/);
});

test('destinations are checked before reads; existing files and hard links are never replaced', t => {
  const directory = scratch(t);
  const output = join(directory, 'occupied.md');
  writeFileSync(output, 'Keep this earlier output.');
  const linked = join(directory, 'linked.md');
  linkSync(output, linked);
  for (const path of [output, linked]) {
    refusal(['pull', '--dir', '/missing-reporter-directory', ...WINDOW, '--output', path], /--output already exists/);
  }
  assert.equal(readFileSync(output, 'utf8'), 'Keep this earlier output.');
  refusal([...standard('pull'), '--output', 'relative.md'], /--output must be an absolute path/);
  refusal([...standard('pull'), '--output', join(directory, 'coverage.txt')], /--output must end in .md/);
  refusal([...standard('pull'), '--output', join(directory, 'missing', 'coverage.md')], /--output parent does not exist/);
});

test('an output parent symlink cannot bypass protection of the tool directory', t => {
  const directory = scratch(t);
  symlinkSync(TOOL, join(directory, 'tool-link'), 'dir');
  const protectedPath = join(TOOL, 'must-not-be-written.md');
  refusal([...standard('pull'), '--output', join(directory, 'tool-link', 'must-not-be-written.md')], /--output resolves inside this tool/);
  assert.equal(existsSync(protectedPath), false);
});

test('a different case of the tool directory cannot bypass output protection', t => {
  const variant = join(dirname(TOOL), 'BEAT-COVERAGE');
  if (!existsSync(variant)) {
    t.skip('This filesystem is case-sensitive; the case variant does not name the tool.');
    return;
  }
  const actual = statSync(TOOL);
  const spelled = statSync(variant);
  assert.equal(spelled.dev, actual.dev);
  assert.equal(spelled.ino, actual.ino);
  for (const parent of ['', 'scripts', 'missing-parent']) {
    const name = 'case-guard-must-not-be-written.md';
    const protectedPath = join(TOOL, parent, name);
    assert.equal(existsSync(protectedPath), false);
    t.after(() => rmSync(protectedPath, { force: true }));
    refusal([...standard('pull'), '--output', join(variant, parent, name)], /--output resolves inside this tool/);
    assert.equal(existsSync(protectedPath), false);
  }
});

test('source symlinks are screened and exclusions also use the resolved basename', t => {
  const directory = scratch(t);
  const input = join(directory, 'input');
  mkdirSync(input);
  writeFileSync(join(input, 'target.md'), '## Most recent\n- Agent link (Fixture Desk, 2026-02-01).');
  symlinkSync(join(input, 'target.md'), join(input, 'alias.md'));
  assert.equal(success(run(['count', '--dir', input, ...WINDOW, '--exclude', 'target.md'])).files, 0);
  symlinkSync(join(FIXTURES, 'bio.md'), join(input, 'outside.md'));
  refusal(['count', '--dir', input, ...WINDOW], /resolves outside --dir/);
  writeFileSync(join(input, 'non-markdown.txt'), 'Synthetic non-Markdown input.');
  symlinkSync(join(input, 'non-markdown.txt'), join(input, 'disguised.md'));
  refusal(['count', '--dir', input, ...WINDOW, '--exclude', 'outside.md'], /non-Markdown file/);
});

test('importing the entry script has no CLI output or process exit', () => {
  const result = spawnSync(process.execPath, ['--input-type=module', '-e', 'await import(process.argv[1]); process.stdout.write("imported");', SCRIPT], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, '');
  assert.equal(result.stdout, 'imported');
});
