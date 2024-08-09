import json
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPStatus, ThreadingHTTPServer
from urllib.parse import urlparse


STATIC_DIR = "output"


class AsyncHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        asyncio.run(self.handle_post())

    async def handle_post(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/generate":
            await self.handle_generate()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Endpoint not found")

    async def handle_generate(self):
        content_length = int(self.headers['Content-Length'])
        post_data = await self.read_async(content_length)

        try:
            data = json.loads(post_data)
            instruct = data.get('instruct', '')
            result = markdown_to_html(instruct)

            response_dict = {
                "status": "success",
                "message": result
            }
        except json.JSONDecodeError:
            response_dict = self.handle_error(BadRequestError("Invalid JSON format received."))
        except Exception as e:
            response_dict = self.handle_error(e)

        self.send_json_response(response_dict)

    async def read_async(self, content_length):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.rfile.read, content_length)

    def send_json_response(self, response_dict):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response_json = json.dumps(response_dict)
        self.wfile.write(response_json.encode('utf-8'))

    def handle_error(self, error):
        error_response = {"status": "error", "message": str(error)}
        if isinstance(error, BadRequestError):
            self.send_response(HTTPStatus.BAD_REQUEST)
        elif isinstance(error, UnsupportedActionError):
            self.send_response(HTTPStatus.NOT_IMPLEMENTED)
        else:
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        return error_response


def markdown_to_html(markdown_text):
    return f"<p>{markdown_text}</p>"


def run_server(port=8080):
    server = ThreadingHTTPServer(('localhost', port), AsyncHTTPRequestHandler)
    print(f"Starting server on http://localhost:{port}")
    server.serve_forever()


class BadRequestError(Exception):
    pass


class UnsupportedActionError(Exception):
    pass


if __name__ == "__main__":
    run_server()
