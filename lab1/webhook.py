#!/usr/bin/env python3

import subprocess
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8080
WORKSPACE = "/home/da/Рабочий стол/lab1_OIS1"
DEPLOY_SCRIPT = f"{WORKSPACE}/deploy.sh"

class WebhookHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length)

        try:
            data = json.loads(raw.decode('utf-8'))
            event = self.headers.get('X-GitHub-Event', '')

            if event == 'push':
                self._handle_push(data)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')

        except Exception as e:
            print(f"Error: {e}")
            self.send_response(400)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Webhook server is running')

    def _handle_push(self, data):
        branch = data.get('ref', '').replace('refs/heads/', '')
        commit = data.get('after')

        print(f"Push. Branch: {branch}. Commit: {commit}")

        if not commit:
            print("No commit SHA")
            return

        print("Running deploy script...")
        result = subprocess.run([DEPLOY_SCRIPT, branch], cwd=WORKSPACE)

        if result.returncode != 0:
            print("Deploy failed")
            return

        print("Deploy complete")

if __name__ == '__main__':
    print(f"Webhook server on port {PORT}")
    HTTPServer(('0.0.0.0', PORT), WebhookHandler).serve_forever()
