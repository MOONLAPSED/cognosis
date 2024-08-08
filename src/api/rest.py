# /src/api/rest.py
import json
from http.server import SimpleHTTPRequestHandler, HTTPStatus, HTTPServer
from urllib.parse import urlparse

STATIC_DIR = "output"  # Define your static directory


class CustomHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/generate":
            self.handle_generate()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Endpoint not found")

    def handle_generate(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data)
            instruct = data.get('instruct', '')
            # Here is where you'd process the `instruct`. Let's assume `markdown_to_html` is the processor.
            result = markdown_to_html(instruct)

            response_dict = {
                "status": "success",
                "message": result
            }
        except json.JSONDecodeError as e:
            response_dict = self.handle_error(BadRequestError("Invalid JSON format received."))
        except Exception as e:
            response_dict = self.handle_error(e)

        self.send_json_response(response_dict)

    def send_json_response(self, response_dict):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response_json = json.dumps(response_dict)
        self.wfile.write(response_json.encode('utf-8'))

    def handle_error(self, error):
        # Add specific custom error handling as necessary
        error_response = {"status": "error", "message": str(error)}
        if isinstance(error, BadRequestError):
            self.send_response(HTTPStatus.BAD_REQUEST)
        elif isinstance(error, UnsupportedActionError):
            self.send_response(HTTPStatus.NOT_IMPLEMENTED)
        else:
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        return error_response


def markdown_to_html(markdown_text):
    # Placeholder for Markdown to HTML conversion, replace with your logic
    # For instance, using a markdown library: return markdown.markdown(markdown_text)
    return f"<p>{markdown_text}</p>"  # Example: Wrap the text with paragraph tags


def run_server(port=8080):
    server = HTTPServer(('localhost', port), CustomHandler)
    print(f"Starting server on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()