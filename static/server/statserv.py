import http.server
import os
import socketserver

PORT = 8080
DIRECTORY = "static"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

handler = MyHttpRequestHandler
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Serving static files from {DIRECTORY} on port {PORT}")
    httpd.serve_forever()

def help(self):
    """
    Print available commands:
    - start: start server
    - stop: stop server
    - restart: restart server
    - status: status server
    - help: help
    - exit: exit
    """
    print("start - start server")
    print("stop - stop server")
    print("restart - restart server")
    print("status - status server")
