"""Build the site in Docker and run JavaScript inside a built page in headless Chrome.

Needs the local ``jekyll-site`` image, network access for the remote theme, and
``google-chrome``. Run all tests with: python3 -m unittest discover -s tests -v
"""
import atexit
import functools
import html
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# Analytics never runs in tests. Its inline script also has a known, older syntax
# error under `layout: compress` that would hide errors in the code under test.
ANALYTICS = re.compile(r"<script>(?:(?!</script>).)*?googletagmanager(?:(?!</script>).)*</script>", re.S)
SKIP_TOP_LEVEL = {".git", "_site", "vendor", "bak", ".specstory", ".vscode", ".superpowers"}

ERROR_HOOK = (
    "<script>window.__errors=[];addEventListener('error',function(e){"
    "if(e.message){window.__errors.push(e.message);}});</script>"
)

WRAPPER = """<!doctype html><meta charset="utf-8">
<iframe id="frame" style="border:0;width:%(width)dpx;height:900px"></iframe>
<pre id="result"></pre>
<script>
var frame = document.getElementById('frame');
frame.addEventListener('load', function () {
  setTimeout(function () {
    var win = frame.contentWindow, out;
    try {
      var value = win.eval('(function () {' + %(js)s + '\\n})()');
      out = {value: value === undefined ? null : value, errors: win.__errors || []};
    } catch (e) {
      out = {value: null, errors: (win.__errors || []).concat(String(e))};
    }
    document.getElementById('result').textContent = JSON.stringify(out);
  }, 300);
});
frame.src = %(url)s;
</script>
"""


def _temp_dir(prefix):
    path = Path(tempfile.mkdtemp(prefix=prefix))
    atexit.register(shutil.rmtree, path, ignore_errors=True)
    return path


def build(extra_files=None):
    """Return the output folder of a production build of a copy of the repo."""
    src = _temp_dir("site-src-")
    out = _temp_dir("site-out-")

    def ignore(folder, names):
        return SKIP_TOP_LEVEL & set(names) if Path(folder) == REPO else set()

    shutil.copytree(REPO, src, ignore=ignore, dirs_exist_ok=True)
    for relative, text in (extra_files or {}).items():
        target = src / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    command = [
        "docker", "run", "--rm", "--user", f"{os.getuid()}:{os.getgid()}",
        "-e", "JEKYLL_ENV=production", "-e", "HOME=/tmp",
        "-e", "LANG=C.UTF-8", "-e", "LC_ALL=C.UTF-8",
        "-e", "BUNDLE_GEMFILE=/srv/jekyll/Gemfile",
        "-e", "BUNDLE_PATH=/srv/jekyll/vendor/bundle",
        "-v", f"{src}:/usr/src/app", "-v", f"{out}:/out", "-w", "/usr/src/app",
        "jekyll-site", "bundle", "exec", "jekyll", "build",
        "--config", "_config.yml,_config_docker.yml", "-d", "/out",
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if result.returncode != 0 or not (out / "index.html").exists():
        raise RuntimeError("Jekyll build failed:\n" + (result.stdout + result.stderr)[-3000:])
    return out


class _Handler(SimpleHTTPRequestHandler):
    wrapper = b""

    def log_message(self, *args):
        pass

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/__wrapper":
            return self._send(self.wrapper)
        file = Path(self.translate_path(path))
        if file.is_dir():
            file = file / "index.html"
        if file.suffix == ".html" and file.is_file():
            page = ANALYTICS.sub("", file.read_text(encoding="utf-8"))
            return self._send(page.replace("<head>", "<head>" + ERROR_HOOK, 1).encode("utf-8"))
        return super().do_GET()

    def _send(self, body):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def query(site, url, js, width=1280):
    """Run ``js`` (a function body) in the built page at ``url`` and return its value."""
    def embed(text):
        return json.dumps(text).replace("</", "<\\/")

    wrapper = WRAPPER % {"width": width, "js": embed(js), "url": embed(url)}
    handler = type("Handler", (_Handler,), {"wrapper": wrapper.encode("utf-8")})
    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(handler, directory=str(site)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        command = [
            "google-chrome", "--headless=new", "--disable-gpu", "--dump-dom",
            "--virtual-time-budget=5000",
            "--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1",
            f"--user-data-dir={_temp_dir('chrome-')}",
            f"--window-size={max(width, 500) + 50},1000",
            f"http://127.0.0.1:{server.server_address[1]}/__wrapper",
        ]
        dom = subprocess.run(command, capture_output=True, text=True, timeout=90).stdout
    finally:
        server.shutdown()
        server.server_close()

    found = re.search(r'<pre id="result">(.*?)</pre>', dom, re.S)
    if not found or not found.group(1):
        raise RuntimeError(f"No result from {url}")
    out = json.loads(html.unescape(found.group(1)))
    if out["errors"]:
        raise RuntimeError(f"Script error on {url}: {out['errors']}")
    return out["value"]
