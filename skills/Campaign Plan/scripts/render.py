#!/usr/bin/env python3
"""Print local campaign HTML through Wiser's existing Node Playwright runtime."""

import base64
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


SKILL = Path(__file__).resolve().parent.parent
HELP = """Print a Campaign Plan HTML file to a new sibling Letter PDF.
Usage: python3 render.py --html <absolute.html> --footer <text>
                        --wiser <absolute base-plugin directory>
       python3 render.py --self-test
       python3 render.py help
Options:
  --html <path>    Local HTML; local or embedded assets only (no remote requests).
  --footer <text>  Nonempty single-line footer, escaped as text; page number right.
  --wiser <path>   Composed Wiser root containing tools/lib/browser-runtime/.
  --self-test     Offline print lifecycle test with an in-memory browser double.
  --help, -h      Help before dependency or configuration access.
Python 3.9+ and Node 18+ are required; checks: python3 --version, node --version.
Reuses only the installed version-matched Playwright runtime (copy-local first,
then person-scoped), as wiser/tools/RUNNING.md describes. Missing Playwright or
Chromium stops and names that install. Nothing is installed or downloaded.
All paths absolute. Existing PDF destinations and outputs inside this skill
are refused. Protected .env and memory paths are refused. No credentials or
configuration. Only the sibling .pdf is written, with exclusive creation.
An interrupted write may leave an incomplete new PDF; inspect it and retry
with a fresh HTML/PDF version. Self-test writes nothing and needs no browser.
Success: one JSON object on stdout, exit 0. Failure: JSON on stderr only,
exit 1. Unknown and duplicate flags are refused; see --help.
"""

# Python drives one synchronous subprocess. The shared runtime supplies Node
# Playwright, so there is no second, unpinned Python Playwright dependency.
NODE_PROGRAM = r"""
import { readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';

const escape = value => String(value).replace(/[&<>"']/g,
  ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const MISSING_PLAYWRIGHT = 'Missing Playwright install in Wiser\'s version-matched browser runtime. Check tools/lib/browser-runtime/browser-runtime.js activeRuntimeDir(); arrange the browser-tool install separately, then retry. This script installs nothing.';

async function printDocument(request, runtime) {
  if (!runtime.activeRuntimeDir()) throw Error(MISSING_PLAYWRIGHT);
  let chromium;
  try {
    const module = await runtime.loadPlaywright();
    chromium = module.chromium || module.default?.chromium;
    if (!chromium) throw Error('no Chromium export');
  } catch {
    throw Error('The existing Playwright install cannot load; check its package.json and restore the version-matched runtime before retrying. Nothing was installed.');
  }
  let browser;
  try {
    try {
      browser = await chromium.launch({headless: true, timeout: 30000});
    } catch (error) {
      if (/executable doesn't exist|browser.*not found|ENOENT/i.test(String(error.message)))
        throw Error('Missing Chromium install for the active Playwright version. Check a headless chromium.launch(); arrange that browser build separately, then retry. This script installs nothing.');
      throw Error('Chromium cannot launch; check headless chromium.launch() in the active runtime and this host\'s browser permissions and system libraries. Nothing was installed.');
    }
    const context = await browser.newContext({serviceWorkers: 'block', javaScriptEnabled: false});
    const remote = new Set();
    await context.route('**/*', route => {
      const url = route.request().url();
      if (/^(file|data|about|blob):/i.test(url)) return route.continue();
      remote.add(new URL(url).protocol);
      return route.abort();
    });
    const page = await context.newPage();
    const failed = [];
    page.on('requestfailed', () => failed.push('resource'));
    page.on('response', response => { if (!response.ok()) failed.push('response'); });
    await page.emulateMedia({media: 'print'});
    await page.goto(request.uri, {waitUntil: 'networkidle', timeout: 30000});
    await page.evaluate(() => document.fonts.ready);
    const assets = await page.evaluate(() => ({
      fonts: document.fonts.status === 'loaded' && [...document.fonts].every(font => font.status === 'loaded'),
      images: [...document.images].every(image => image.complete && image.naturalWidth > 0),
      font: getComputedStyle(document.body).fontFamily,
    }));
    if (remote.size) throw Error('Remote resources refused; embed or supply local bound-design assets, then retry.');
    if (failed.length || !assets.fonts || !assets.images)
      throw Error('A local font, image or resource did not load; restore the bound-design asset before rendering.');
    const footer = `<div style="font-size:9px;font-family:${escape(assets.font)};width:100%;padding:0 0.55in;box-sizing:border-box;display:flex;justify-content:space-between"><span>${escape(request.footer)}</span><span class="pageNumber"></span></div>`;
    const pdf = await page.pdf({
      format: 'Letter', printBackground: true, preferCSSPageSize: true,
      displayHeaderFooter: true, headerTemplate: '<div></div>', footerTemplate: footer,
      margin: {top:'0.5in',right:'0.55in',bottom:'0.65in',left:'0.55in'},
    });
    if (!Buffer.isBuffer(pdf) || !pdf.subarray(0,5).equals(Buffer.from('%PDF-')) ||
        !pdf.subarray(-1024).toString('latin1').includes('%%EOF'))
      throw Error('Chromium returned incomplete PDF bytes; retry with a fresh version.');
    return pdf;
  } finally {
    if (browser) await browser.close();
  }
}

async function selfTest() {
  const calls = [];
  let handler, blocked = false, failPdf = false, closed = 0;
  const page = {
    on() {},
    async emulateMedia(value) { assert.equal(value.media,'print'); calls.push('print'); },
    async goto(uri, value) { assert.equal(uri,'file:///example.html'); assert.equal(value.waitUntil,'networkidle'); calls.push('navigate'); },
    async evaluate(fn) {
      if (String(fn).includes('document.fonts.ready')) { calls.push('fonts'); return; }
      return {fonts:true,images:true,font:'Example Face'};
    },
    async pdf(value) {
      calls.push('pdf');
      assert.equal(value.format,'Letter');
      for (const key of ['printBackground','preferCSSPageSize','displayHeaderFooter']) assert.equal(value[key],true);
      assert.equal(value.headerTemplate,'<div></div>');
      assert.match(value.footerTemplate,/A &amp; B &lt;draft&gt;/);
      assert.match(value.footerTemplate,/class="pageNumber"/);
      assert.match(value.footerTemplate,/Example Face/);
      assert.equal(value.margin.bottom,'0.65in');
      if (failPdf) throw Error('planted PDF failure');
      return Buffer.from('%PDF-1.7\nsynthetic test bytes\n%%EOF\n');
    },
  };
  const context = {async route(pattern, callback) { handler=callback; }, async newPage() {
    if (blocked) await handler({request:()=>({url:()=> 'https://example.invalid/asset'}),abort:()=>calls.push('blocked'),continue:()=>assert.fail('remote request escaped')});
    return page;
  }};
  const runtime = {activeRuntimeDir:()=> 'installed',async loadPlaywright() {return {chromium:{async launch(options) {
    assert.equal(options.headless,true);
    return {async newContext(options) {assert.equal(options.serviceWorkers,'block');assert.equal(options.javaScriptEnabled,false);return context;},async close() {closed++;}};
  }}};}};
  const request = {uri:'file:///example.html',footer:'A & B <draft>'};
  await printDocument(request,runtime);
  assert.deepEqual(calls,['print','navigate','fonts','pdf']);
  assert.equal(closed,1);
  failPdf=true;
  await assert.rejects(printDocument(request,runtime),/planted PDF failure/);
  assert.equal(closed,2);
  failPdf=false; blocked=true;
  await assert.rejects(printDocument(request,runtime),/Remote resources refused/);
  assert.ok(calls.includes('blocked'));
  await assert.rejects(printDocument(request,{activeRuntimeDir:()=> null}),/Missing Playwright install/);
  await assert.rejects(printDocument(request,{activeRuntimeDir:()=> 'installed',async loadPlaywright() {return {chromium:{async launch() {throw Error("Executable doesn't exist");}}};}}),/Missing Chromium install/);
  assert.equal(escape('"<&\''),'&quot;&lt;&amp;&#39;');
  return {status:'passed',tests:['Letter print settings and page-numbered escaped footer','print media, network-idle and fonts-ready order','browser closed on success and failure','remote requests blocked','missing Playwright stops','missing Chromium stops']};
}

try {
  if (Number(process.versions.node.split('.')[0]) < 18) throw Error('Node 18 or newer required; check node --version.');
  const request = JSON.parse(readFileSync(0,'utf8'));
  if (request.self_test) {
    process.stdout.write(JSON.stringify(await selfTest())+'\n');
  } else {
    const runtime = await import(pathToFileURL(request.runtime).href);
    // activeRuntimeDir checks the package marker/version before any package import.
    const active = runtime.activeRuntimeDir();
    if (!active) throw Error(MISSING_PLAYWRIGHT);
    if (!statSync(join(active,'node_modules','playwright','package.json')).isFile()) throw Error(MISSING_PLAYWRIGHT);
    const pdf = await printDocument(request,runtime);
    process.stdout.write(JSON.stringify({pdf:pdf.toString('base64')})+'\n');
  }
} catch (error) {
  process.stderr.write(JSON.stringify({error:String(error.message).split('\n')[0],fix:'See render.py --help; repair the named dependency or input, then retry.'})+'\n');
  process.exitCode=1;
}
"""


def options(argv):
    values = {}
    value_flags = {"--html", "--footer", "--wiser"}
    allowed = value_flags | {"--self-test", "--help", "-h"}
    if not argv or argv == ["help"]:
        return {"--help": True}
    index = 0
    while index < len(argv):
        flag = argv[index]
        if flag not in allowed:
            raise ValueError(f"Unknown option {flag}; see render.py --help")
        if flag in values:
            raise ValueError(f"Duplicate option {flag}; use it once; see --help")
        index += 1
        if flag in value_flags:
            if index == len(argv) or argv[index].startswith("--"):
                raise ValueError(f"{flag} needs a value; see --help")
            values[flag] = argv[index]
            index += 1
        else:
            values[flag] = True
    if values.get("--self-test") and set(values) != {"--self-test"}:
        raise ValueError("--self-test must be used alone; see --help")
    return values


def screened(value, destination=False):
    path = Path(value)
    if not path.is_absolute():
        raise ValueError("Path must be absolute; see --help")
    if any(part.casefold() == "memory" or
           re.match(r"^\.env(?:\.|$)", part, re.I) for part in path.parts):
        raise ValueError("Protected path; supply a work-product path")
    try:
        resolved = path.resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise ValueError("Path cannot be canonicalized; repair links or permissions") from error
    if any(part.casefold() == "memory" or
           re.match(r"^\.env(?:\.|$)", part, re.I) for part in resolved.parts):
        raise ValueError("Protected path; supply a work-product path")
    if destination:
        if resolved == SKILL or SKILL in resolved.parents:
            raise ValueError("PDF output resolves inside this skill; use the owning root's work directory")
        if path.exists() or path.is_symlink() or resolved.exists():
            raise ValueError("PDF destination already exists; choose a fresh HTML/PDF version")
    return resolved


def invoke_node(request):
    node = shutil.which("node")
    if not node:
        raise ValueError("Missing Node interpreter; check node --version (18 or newer required)")
    process = subprocess.run([node, "--input-type=module", "-e", NODE_PROGRAM],
                             input=json.dumps(request), text=True, capture_output=True,
                             timeout=120)
    if process.returncode != 0:
        try:
            message = json.loads(process.stderr)["error"]
        except (ValueError, KeyError, TypeError):
            message = "Node renderer failed; check Node 18+, the shared runtime and Chromium"
        raise ValueError(message)
    if process.stderr:
        raise ValueError("Node renderer emitted diagnostics; check its runtime before retrying")
    try:
        return json.loads(process.stdout)
    except ValueError as error:
        raise ValueError("Node renderer returned no complete JSON result; check its runtime") from error


def main(argv=None):
    try:
        args = options(sys.argv[1:] if argv is None else argv)
        if args.get("--help") or args.get("-h"):
            print(HELP, end="")
            return 0
        if args.get("--self-test"):
            print(json.dumps(invoke_node({"self_test": True})))
            return 0
        if not {"--html", "--footer", "--wiser"}.issubset(args):
            raise ValueError("--html, --footer and --wiser are required; see --help")
        footer = args["--footer"]
        if not footer.strip() or any(ord(char) < 32 or char in "\u2028\u2029" for char in footer):
            raise ValueError("--footer requires nonempty single-line text; see --help")
        html = screened(args["--html"])
        if html.suffix.lower() not in {".html", ".htm"} or not html.is_file():
            raise ValueError("--html must name a readable regular HTML file; see --help")
        pdf = screened(str(html.with_suffix(".pdf")), destination=True)
        wiser = screened(args["--wiser"])
        runtime = screened(str(wiser / "tools/lib/browser-runtime/browser-runtime.js"))
        if not runtime.is_file():
            raise ValueError("Shared browser runtime module is missing; pass the composed Wiser root as --wiser")
        result = invoke_node({"uri": html.as_uri(), "footer": footer, "runtime": str(runtime)})
        data = base64.b64decode(result["pdf"], validate=True)
        if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-1024:]:
            raise ValueError("Renderer returned incomplete PDF bytes; retry with a fresh version")
        # Exclusive creation also catches a destination created after screening.
        with pdf.open("xb") as handle:
            handle.write(data)
        if pdf.stat().st_size != len(data):
            raise ValueError("PDF write was incomplete; inspect it and retry with a fresh version")
        print(json.dumps({"status": "rendered", "html": str(html), "pdf": str(pdf),
                          "bytes": len(data), "format": "Letter"}))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"error": str(error),
                          "fix": "Check the named input or dependency; see render.py --help"}),
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
