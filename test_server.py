import http.server
import socketserver
import threading
import time

PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Server started at http://localhost:{PORT}")

# Start server in a separate thread so we can see output
server_thread = threading.Thread(target=httpd.serve_forever)
server_thread.daemon = True
server_thread.start()

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down server...")
    httpd.shutdown()