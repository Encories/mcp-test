import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class MCPService(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        path_fragment = query_params.get('path', [''])[0]
        
        results = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if path_fragment in file:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    creation_time = os.path.getctime(file_path)
                    creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
                    
                    results.append({
                        "name": file,
                        "path": file_path,
                        "size": file_size,
                        "creation_date": creation_date
                    })
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(results).encode())

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MCPService)
    print("MCP сервис запущен на http://localhost:8000")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()