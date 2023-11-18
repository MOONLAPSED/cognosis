import http.server
import socketserver
import os, sys, json, argparse, logging, unittest
from src.utils.errors import *  # Import the error classes
from src.utils.logutils import *  # Check and create the log directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
log_directory = 'logs'
log_file_path = os.path.join(log_directory, 'app.log')
# Initialize logging using logging_utils module
logger = init_logging(log_directory, log_file_path)



def main():
    try:
        prompt = []
        parser = argparse.ArgumentParser(description='cognosis by MOONLAPSED@gmail.com MIT License')
        parser.add_argument('prompt', nargs='*', help='Enter the prompt here')
        args = parser.parse_args()
        prompt.extend(args.prompt)
        if len(prompt) == 0:
            prompt.append('Hello world!')
        else:
            for line in args.prompt:
                prompt.append(line)
                prompt.append('\n')  # Append newline after each line
        if prompt[-1] == '\n':  # Remove the last newline if present
            prompt.pop()
        prompt = ''.join(prompt)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    print(prompt)
    test_suite = unittest.defaultTestLoader.discover(start_dir='.', pattern='test_*.py')
    unittest.TextTestRunner().run(test_suite)

# TODO ~/static/.server/statserv.py integration      
"""
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith(".html"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(self.path[1:], "r") as f:
                self.copyfile(f, self.wfile)
        else:
            super().do_GET()

port = 8000
server = socketserver.TCPServer(("localhost", port), MyHandler)
server.serve_forever()
"""