import argparse
import logging
import os
import sys
import unittest
import socketserver

# Import your modules here (make sure import paths are correct)
from src.dbase.pydbase import *
from src.utils.errors import *
from src.utils.logutils import *
from src.api.apidef import *
from api import CustomHandler  # Import CustomHandler from api.py

# Make sure the log file path is joining with the proper directory
log_directory = 'logs'
log_file_path = os.path.join(log_directory, 'app.log')
# Initialize logging
logger = init_logging(log_directory, log_file_path)

# Server configuration
PORT = 8080
server_main_url = 'http://localhost:{}'.format(PORT)

class TestServerStatus(unittest.TestCase):

    def test_server_is_running(self):
        """ Test if the server is running and reachable """
        try:
            response = requests.get(server_main_url)
            self.assertEqual(response.status_code, 200)
        except requests.ConnectionError as e:
            self.fail('Server is not running or not reachable.')
# A function to run all tests when this script is executed
def run_tests():
    unittest.main()


def main():
    """
    Main function of the program.
    Parses command line arguments, runs unit tests, and starts the static file server.
    """
    try:
        parser = argparse.ArgumentParser(description='cognosis by MOONLAPSED@gmail.com MIT License')
        parser.add_argument('prompt', nargs='*', help='Enter the prompt here')
        args = parser.parse_args()

        if not args.prompt:  # If the prompt is empty, provide a default
            args.prompt.append('Hello world!')

        # Construct the prompt as a single string
        prompt = ' '.join(args.prompt).strip()  # Remove leading/trailing spaces

        logger.info(f"Prompt: {prompt}")

        # Run tests
        test_suite = unittest.TestLoader().discover(start_dir='.', pattern='test_*.py')
        result = unittest.TextTestRunner().run(test_suite)

        if result.wasSuccessful():
            logger.info("Tests passed successfully.")
        else:
            logger.error("Some tests failed.")
            sys.exit(1)  # Exit if tests have failed

        # API or other logic can be executed here
        # NOTE: This section will only execute if tests pass
        
        # Start the static file server
        def run_static_server():
            with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
                logger.info(f"Serving files and handling API requests on port {PORT}")
                httpd.serve_forever()
        run_static_server()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    rlhf = RLHF('rlhf.db')
    rlhf.dbinitcall()
    run_tests()
    main()
