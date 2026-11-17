"""
server.py: a website OUTSIDE the company, played by a small Python server.

It answers as partner-news.example (a vendor's news site) and as
evil.example. Both names point at this one container. It serves the pages
in pages/, and it records every request it receives, including the full
query string and any body, so you can see exactly what reached it:

  docker compose logs external-site      the raw request log
  bin/external_log.sh                    the same, formatted

In Part 1 this is just the outside internet. In Part 2 you will see why an
agent that can reach the internet needs to be watched.
"""

import json
import os
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")


class Handler(BaseHTTPRequestHandler):
    server_version = "external-site"

    def _record(self, body: str = "") -> None:
        print(json.dumps({
            "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source": "external-site", "host": self.headers.get("Host", ""),
            "client": self.client_address[0], "method": self.command,
            "path": self.path, "body": body[:2000],
        }), flush=True)

    def _page(self) -> None:
        name = self.path.split("?", 1)[0].strip("/") or "index"
        file = os.path.join(PAGES, os.path.basename(name) + ".html")
        if os.path.isfile(file):
            data = open(file, "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        else:
            data = b"<html><body><p>Thanks!</p></body></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._record()
        self._page()

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        self._record(self.rfile.read(min(length, 100000)).decode("utf-8", "replace"))
        self._page()

    def log_message(self, *args):  # the JSON line above replaces the default log
        pass


if __name__ == "__main__":
    print("external-site listening on :80", file=sys.stderr, flush=True)
    ThreadingHTTPServer(("0.0.0.0", 80), Handler).serve_forever()
