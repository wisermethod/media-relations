#!/usr/bin/env python3
"""Print local campaign HTML through Wiser's existing Node browser runtime."""

import base64
import json
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this script's own folder, also under python -I
from paths import screen_path, self_test as path_self_test


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
  --self-test     Offline DOM, lifecycle, result and path tests; no browser needed.
  --help, -h      Help before dependency or configuration access.
Python 3.9+ and Node 18+ are required; checks: python3 --version, node --version.
Reuses only the installed version-matched Playwright runtime (copy-local first,
then person-scoped), as wiser/tools/RUNNING.md describes. Shared runtime.launch
supplies container flags, compatibility shims and the preinstalled-build retry;
each launch has its 180-second bound. Missing Playwright or Chromium stops and
names that dependency. Nothing is installed or downloaded; the shared runtime
may compile its documented Linux compatibility shims in its own package cache.
Paper is always Letter, overriding a different CSS paper size. Margins: top
0.5in, left/right 0.55in, bottom 0.65in. Match these in @page; add no second
body-margin or padding inset. Reserve bottom space for the page-numbered footer.
Unused unloaded fonts, complete zero-width SVGs and unrelated favicon failures
are accepted. Font errors, incomplete used images, page errors and failed
requests referenced by the document stop rendering. Remote requests are blocked.
All paths absolute and canonicalized. Destination ancestry is compared by device
and inode; existing PDFs and outputs inside this skill are refused. Protected
.env and memory paths are refused. No credentials or configuration. Only the
sibling .pdf is written, with exclusive creation. An interrupted write may leave
an incomplete new PDF; inspect it and retry with a fresh HTML/PDF version.
Self-test writes nothing. Success: one JSON object on stdout, exit 0. Failure:
JSON on stderr only, exit 1. Node diagnostics alone do not fail a zero-exit
complete success object. Unknown and duplicate flags are refused; see --help.
"""

# Python drives one subprocess. No separate Python Playwright dependency.
NODE_PROGRAM = r"""
import { readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';

const escape = value => String(value).replace(/[&<>"']/g,
  ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const MISSING_PLAYWRIGHT = 'Missing Playwright install in Wiser\'s version-matched browser runtime. Check tools/lib/browser-runtime/browser-runtime.js activeRuntimeDir(); arrange the browser-tool install separately, then retry. This script installs nothing.';
const resourceKey = url => { const value = new URL(url); value.hash = ''; return value.href; };

// Runs inside the print document. The self-test executes this same function,
// with DOM objects, rather than returning a precomputed all-true asset result.
function documentAssets() {
  const references = new Set([document.URL]);
  const add = value => {
    if (!value) return;
    try { const url = new URL(value, document.baseURI); url.hash = ''; references.add(url.href); }
    catch { /* a malformed URL cannot identify a completed request */ }
  };
  const cssUrls = (text, base) => {
    for (const match of text.matchAll(/url\(\s*(?:"([^"]*)"|'([^']*)'|([^\s)]+))\s*\)/gi)) {
      try { add(new URL(match[1] ?? match[2] ?? match[3], base).href); }
      catch { /* no resolvable URL */ }
    }
  };
  const rules = (list, base) => {
    for (const rule of list) {
      if (rule.href) add(new URL(rule.href, base).href);
      cssUrls(rule.cssText || '', base);
      if (rule.cssRules) rules(rule.cssRules, base);
      if (rule.styleSheet) sheet(rule.styleSheet);
    }
  };
  const sheet = value => {
    const base = value.href || document.baseURI;
    add(value.href);
    try { rules(value.cssRules, base); }
    catch { /* unreadable sheets still have their requested href recorded */ }
  };
  for (const value of document.styleSheets) sheet(value);
  for (const node of document.querySelectorAll('style,[style]'))
    cssUrls(node.tagName === 'STYLE' ? node.textContent : node.getAttribute('style') || '', document.baseURI);
  for (const node of document.querySelectorAll('link[rel~="stylesheet"],iframe[src],object[data],embed[src],video[src],video[poster],audio[src],source[src],image[href],image[xlink\\:href],use[href],input[type="image"][src]'))
    for (const attr of ['href','xlink:href','src','data','poster']) add(node.getAttribute(attr));
  const usedImages = [...document.images].filter(image => {
    const style = getComputedStyle(image);
    return (image.currentSrc || image.src) && image.getClientRects().length &&
      style.display !== 'none' && !['hidden','collapse'].includes(style.visibility);
  });
  for (const image of usedImages) add(image.currentSrc || image.src);
  return {
    fontError: [...document.fonts].some(font => font.status === 'error'),
    incompleteImage: usedImages.some(image => !image.complete),
    references: [...references],
    font: getComputedStyle(document.body).fontFamily,
  };
}

async function printDocument(request, runtime) {
  if (!runtime.activeRuntimeDir()) throw Error(MISSING_PLAYWRIGHT);
  let browser;
  try {
    try {
      // Do not call chromium.launch directly or shorten the runtime's bound.
      browser = await runtime.launch({headless:true, timeout:180000});
    } catch (error) {
      if (/executable doesn't exist|browser.*not found|ENOENT/i.test(String(error.message)))
        throw Error('Missing or inaccessible Chromium build for the active Playwright version. Check shared runtime.launch({headless:true}); arrange or repair that build separately, then retry. This script installs nothing.');
      throw Error('Shared browser runtime launch failed; check runtime.launch({headless:true}), the installed Playwright package and host browser permissions and system libraries. Nothing was installed.');
    }
    const context = await browser.newContext({serviceWorkers:'block', javaScriptEnabled:false});
    const failed = [];
    const recordFailure = request => {
      // A redirected asset can fail at a URL different from its document reference.
      for (let current = request; current; current = current.redirectedFrom())
        failed.push(resourceKey(current.url()));
    };
    await context.route('**/*', route => {
      const request = route.request();
      if (/^(file|data|about|blob):/i.test(request.url())) return route.continue();
      recordFailure(request);
      return route.abort();
    });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', () => errors.push('page error'));
    page.on('crash', () => errors.push('page crash'));
    page.on('requestfailed', recordFailure);
    page.on('response', response => { if (response.status() >= 400) recordFailure(response.request()); });
    await page.emulateMedia({media:'print'});
    await page.goto(request.uri, {waitUntil:'networkidle', timeout:30000});
    await page.evaluate(() => document.fonts.ready);
    const assets = await page.evaluate(documentAssets);
    const references = new Set(assets.references);
    if (errors.length || assets.fontError || assets.incompleteImage ||
        failed.some(url => references.has(url)))
      throw Error('A page error, font error, incomplete used image or failed document-referenced resource prevents rendering; restore that input before retrying.');
    const footer = `<div style="font-size:9px;font-family:${escape(assets.font)};width:100%;padding:0 0.55in;box-sizing:border-box;display:flex;justify-content:space-between"><span>${escape(request.footer)}</span><span class="pageNumber"></span></div>`;
    const pdf = await page.pdf({
      format:'Letter', printBackground:true, preferCSSPageSize:false,
      displayHeaderFooter:true, headerTemplate:'<div></div>', footerTemplate:footer,
      margin:{top:'0.5in',right:'0.55in',bottom:'0.65in',left:'0.55in'},
      timeout:30000,
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
  const fixture = (settings = {}) => {
    const calls = [], handlers = {};
    let closed = 0, handler;
    const image = (src, complete, visible = true) => ({src, currentSrc:src, complete,
      naturalWidth:0, getClientRects:() => visible ? [1] : [], style:{display:visible ? 'block':'none',visibility:'visible'}});
    const fonts = [{status:'loaded'}, {status:'unloaded'}, ...(settings.fontError ? [{status:'error'}] : [])];
    fonts.ready = Promise.resolve();
    const document = {
      URL:'file:///example.html', baseURI:'file:///example.html', fonts, body:{},
      images:[image('file:///logo.svg', !settings.incomplete), image('file:///hidden.png',false,false)],
      styleSheets:[{href:'file:///design.css', cssRules:[{cssText:'@font-face { src: url("font.woff2"); }'}]}],
      querySelectorAll(selector) { return selector.startsWith('link') ?
        [{getAttribute:attr => attr === 'href' ? 'file:///design.css' : null},
         ...(settings.remote ? [{getAttribute:attr => attr === 'href' ? 'https://example.invalid/design.css' : null}] : [])] : []; },
    };
    const page = {
      on(event, callback) { handlers[event] = callback; },
      async emulateMedia(value) { assert.equal(value.media,'print'); calls.push('print'); },
      async goto(uri, value) {
        assert.equal(uri,document.URL); assert.equal(value.waitUntil,'networkidle'); calls.push('navigate');
        const request = (url, prior = null) => ({url:() => url, redirectedFrom:() => prior});
        for (const url of settings.failures || []) handlers.requestfailed(request(url));
        for (const url of settings.responses || []) handlers.response({status:() => 404,request:() => request(url)});
        if (settings.redirected) handlers.requestfailed(request('file:///new-logo.svg', request('file:///logo.svg')));
        if (settings.pageError) handlers.pageerror(Error('planted page error'));
        if (settings.remote) await handler({request:() => request('https://example.invalid/design.css'),
          abort:() => calls.push('blocked'),continue:() => assert.fail('remote request escaped')});
      },
      async evaluate(fn) {
        if (fn === documentAssets) calls.push('assets'); else calls.push('fonts');
        globalThis.document = document;
        globalThis.getComputedStyle = node => node.style || {fontFamily:'Example Face'};
        try { return await fn(); }
        finally { delete globalThis.document; delete globalThis.getComputedStyle; }
      },
      async pdf(value) {
        calls.push('pdf');
        assert.equal(value.format,'Letter'); assert.equal(value.preferCSSPageSize,false);
        for (const key of ['printBackground','displayHeaderFooter']) assert.equal(value[key],true);
        assert.equal(value.headerTemplate,'<div></div>');
        assert.match(value.footerTemplate,/A &amp; B &lt;draft&gt;/);
        assert.match(value.footerTemplate,/class="pageNumber"/); assert.match(value.footerTemplate,/Example Face/);
        assert.deepEqual(value.margin,{top:'0.5in',right:'0.55in',bottom:'0.65in',left:'0.55in'});
        if (settings.failPdf) throw Error('planted PDF failure');
        return Buffer.from(settings.badPdf ? 'incomplete' : '%PDF-1.7\nsynthetic test bytes\n%%EOF\n');
      },
    };
    const context = {async route(pattern, callback) {assert.equal(pattern,'**/*');handler=callback;},async newPage() {return page;}};
    const runtime = {activeRuntimeDir:() => 'installed', async launch(options) {
      assert.deepEqual(options,{headless:true,timeout:180000}); calls.push('launch');
      return {async newContext(options) {assert.deepEqual(options,{serviceWorkers:'block',javaScriptEnabled:false});return context;},async close() {closed++;}};
    }};
    return {runtime, calls, closed:() => closed};
  };
  const request = {uri:'file:///example.html',footer:'A & B <draft>'};
  const good = fixture({failures:['file:///favicon.ico','file:///hidden.png'],responses:['file:///favicon.ico']});
  await printDocument(request,good.runtime);
  assert.deepEqual(good.calls,['launch','print','navigate','fonts','assets','pdf']); assert.equal(good.closed(),1);
  for (const settings of [{fontError:true},{incomplete:true},{pageError:true},{failures:['file:///logo.svg']},
    {responses:['file:///design.css']},{failures:['file:///font.woff2']},{redirected:true},{remote:true}]) {
    const bad = fixture(settings);
    await assert.rejects(printDocument(request,bad.runtime),/prevents rendering/);
    assert.equal(bad.closed(),1); assert.ok(!bad.calls.includes('pdf'));
    if (settings.remote) assert.ok(bad.calls.includes('blocked'));
  }
  for (const settings of [{failPdf:true},{badPdf:true}]) {
    const bad = fixture(settings);
    await assert.rejects(printDocument(request,bad.runtime),/planted PDF failure|incomplete PDF/);
    assert.equal(bad.closed(),1);
  }
  await assert.rejects(printDocument(request,{activeRuntimeDir:() => null}),/Missing Playwright install/);
  await assert.rejects(printDocument(request,{activeRuntimeDir:() => 'installed',async launch() {throw Error("Executable doesn't exist");}}),/Chromium build/);
  assert.equal(escape('"<&\''),'&quot;&lt;&amp;&#39;');
  return {status:'passed',tests:[
    'shared runtime launch and 180-second bound',
    'Letter overrides CSS size; margins and escaped page-numbered footer',
    'print, network-idle, fonts-ready and actual DOM asset predicate',
    'unused unloaded font, complete zero-width SVG and unrelated favicon accepted',
    'font error, incomplete used image, page error and referenced failures refused',
    'redirected referenced failures refused; remote requests blocked',
    'browser closed on success, asset failure and PDF failure',
    'missing Playwright and Chromium stop without installing',
  ]};
}

try {
  if (Number(process.versions.node.split('.')[0]) < 18) throw Error('Node 18 or newer required; check node --version.');
  const request = JSON.parse(readFileSync(0,'utf8'));
  if (request.self_test) {
    process.stdout.write(JSON.stringify(await selfTest())+'\n');
  } else {
    const runtime = await import(pathToFileURL(request.runtime).href);
    const active = runtime.activeRuntimeDir();
    if (!active || !statSync(join(active,'node_modules','playwright','package.json')).isFile()) throw Error(MISSING_PLAYWRIGHT);
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


def invoke_node(request):
    node = shutil.which("node")
    if not node:
        raise ValueError("Missing Node interpreter; check node --version (18 or newer required)")
    process = subprocess.run([node, "--input-type=module", "-e", NODE_PROGRAM],
                             input=json.dumps(request), text=True, capture_output=True,
                             timeout=480)
    if process.returncode != 0:
        try:
            message = json.loads(process.stderr)["error"]
        except (ValueError, KeyError, TypeError):
            message = "Node renderer failed; check Node 18+, the shared runtime and Chromium"
        raise ValueError(message)
    try:
        result = json.loads(process.stdout)
    except ValueError as error:
        raise ValueError("Node renderer returned no complete JSON success object; check its runtime") from error
    if not isinstance(result, dict) or "error" in result:
        raise ValueError("Node renderer returned no complete JSON success object; check its runtime")
    if request.get("self_test"):
        if result.get("status") != "passed" or not isinstance(result.get("tests"), list):
            raise ValueError("Node self-test returned no passed result; check its runtime")
    else:
        decode_pdf(result)
    # A valid structured success at exit 0 wins over diagnostic stderr.
    return result


def decode_pdf(result):
    try:
        data = base64.b64decode(result["pdf"], validate=True)
    except (KeyError, ValueError, TypeError) as error:
        raise ValueError("Node renderer returned no complete PDF success object; check its runtime") from error
    if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-1024:]:
        raise ValueError("Renderer returned incomplete PDF bytes; retry with a fresh version")
    return data


def self_test():
    from types import SimpleNamespace
    from unittest.mock import patch

    result = invoke_node({"self_test": True})
    good = json.dumps({"pdf": base64.b64encode(b"%PDF-1.7\n%%EOF\n").decode()})
    for code, stdout, stderr, success in [
        (0, good, "diagnostic warning\n", True),
        (1, good, '{"error":"planted failure"}', False),
        (0, "", "diagnostic warning\n", False),
        (0, '{"pdf":"aW5jb21wbGV0ZQ=="}', "", False),
        (0, '{"error":"not success"}', "", False),
    ]:
        with patch.object(subprocess, 'run', return_value=SimpleNamespace(returncode=code, stdout=stdout, stderr=stderr)):
            try:
                invoke_node({"uri": "file:///example.html"})
            except ValueError:
                assert not success, "Valid zero-exit success rejected for diagnostic stderr"
            else:
                assert success, "Missing success or nonzero exit accepted"
    result["tests"].extend([
        "zero-exit success with diagnostic stderr accepted; nonzero or missing success refused",
        path_self_test(),
    ])
    return result


def main(argv=None):
    try:
        args = options(sys.argv[1:] if argv is None else argv)
        if args.get("--help") or args.get("-h"):
            print(HELP, end="")
            return 0
        if args.get("--self-test"):
            print(json.dumps(self_test()))
            return 0
        if not {"--html", "--footer", "--wiser"}.issubset(args):
            raise ValueError("--html, --footer and --wiser are required; see --help")
        footer = args["--footer"]
        if not footer.strip() or any(ord(char) < 32 or char in "\u2028\u2029" for char in footer):
            raise ValueError("--footer requires nonempty single-line text; see --help")
        html = screen_path(args["--html"], file=True)
        if html.suffix.lower() not in {".html", ".htm"}:
            raise ValueError("--html must name a readable regular HTML file; see --help")
        pdf = screen_path(str(html.with_suffix(".pdf")), destination=SKILL)
        wiser = screen_path(args["--wiser"], directory=True)
        runtime = screen_path(str(wiser / "tools/lib/browser-runtime/browser-runtime.js"), file=True)
        result = invoke_node({"uri": html.as_uri(), "footer": footer, "runtime": str(runtime)})
        data = decode_pdf(result)
        # Exclusive creation also catches a destination created after screening.
        with pdf.open("xb") as handle:
            handle.write(data)
        if pdf.stat().st_size != len(data):
            raise ValueError("PDF write was incomplete; inspect it and retry with a fresh version")
        print(json.dumps({"status": "rendered", "html": str(html), "pdf": str(pdf),
                          "bytes": len(data), "format": "Letter"}))
        return 0
    except (OSError, ValueError, KeyError, TypeError, AssertionError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"error": str(error) or "Self-test assertion failed",
                          "fix": "Check the named input or dependency; see render.py --help"}),
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
