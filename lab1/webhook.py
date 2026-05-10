#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import json

PORT = 8080
WORKSPACE = "/home/da/Рабочий стол/lab1_OIS1"
DEPLOY_SCRIPT = f"{WORKSPACE}/deploy.sh"

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        
        event = self.headers.get('X-GitHub-Event', '')
        
        if event == 'push':
            try:
                data = json.loads(body.decode('utf-8'))
                branch = data.get('ref', '').replace('refs/heads/', '')
                print(f"Push в ветку: {branch}")
                
                result = subprocess.run([DEPLOY_SCRIPT, branch], cwd=WORKSPACE)
                if result.returncode == 0:
                    print("Deploy successful")
                else:
                    print("Deploy failed")
            except Exception as e:
                print(f"Error: {e}")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Webhook server is running')

if __name__ == '__main__':
    print(f"Webhook on port {PORT}")
    HTTPServer(('0.0.0.0', PORT), WebhookHandler).serve_forever()
