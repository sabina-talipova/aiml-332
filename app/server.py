from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from Docker Python server!")

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 7860
    server = HTTPServer((host, port), SimpleHandler)
    print(f"Server running on {host}:{port}")
    server.serve_forever()
