import http.server
import socketserver


PORT = 8080
DIRECTORY = 'static'

handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(('', PORT), handler) as httpd:
    print(f'Serving static files from {DIRECTORY} on port {PORT}')
    httpd.serve_forever()
"""This will start a simple HTTP server on port 8080. You can then access your static files by opening a web browser and navigating to http://localhost:8080/
To access the index.html file, you would go to http://localhost:8080/index.html."""

"""
def help(self):
    print("start - start server")
    print("stop - stop server")
    print("restart - restart server")
    print("status - status server")
    print("help - help")
    print("exit - exit")
    """