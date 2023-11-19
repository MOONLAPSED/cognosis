import http.server
import socketserver

PORT = 8080
DIRECTORY = "static"

handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), handler) as httpd:
    """
    This will start a simple HTTP server on port 8080. You can then access your static files by opening a web browser and navigating to http://localhost:8080/
    To access the index.html file, you would go to http://localhost:8080/index.html.
    """
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
            print("help - help")
            print("exit - exit")

    """
    This will start a simple HTTP server on port 8080. You can then access your static files by opening a web browser and navigating to http://localhost:8080/
    To access the index.html file, you would go to http://localhost:8080/index.html.
    """
    print(f"Serving static files from {DIRECTORY} on port {PORT}")
    httpd.serve_forever()
