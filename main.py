import argparse
import os
import requests
import sys
import unittest
import socketserver

from src.api.api import CustomHandler
from src.utils.logutils import LoggerManager

# Import the ErrorReporter class
from src.utils.errors import ErrorReporter

# Server configuration
PORT = 8069
server_main_url = 'http://localhost:{}'.format(PORT)

class TestServerStatus(unittest.TestCase):

    def test_server_is_running(self):
        """ Test if the server is running and reachable """
        try:
            response = requests.get(server_main_url)
            self.assertEqual(response.status_code, 200)
        except requests.ConnectionError as e:
            self.fail('Server is not running or not reachable.')


def main():
    """
    Main function of the program.
    Parses command line arguments, runs unit tests, and starts the static file server.
    """
    root_logger = None
    queue_listener = None
    try:
        parser = argparse.ArgumentParser(description='cognosis by MOONLAPSED@gmail.com MIT License')
        parser.add_argument('prompt', nargs='*', help='Enter the prompt here')
        args = parser.parse_args()

        if not args.prompt:  # If the prompt is empty, provide a default
            args.prompt.append('Hello world!')

        # Construct the prompt as a single string
        prompt = ' '.join(args.prompt).strip()  # Remove leading/trailing spaces

        # Initialize the LoggerManager
        log_file_path = '/path/to/log/app.log'
        logger_manager = LoggerManager(log_file_path, branch_name='my_branch', leaf_name='my_leaf')
        root_logger, branch_logger, leaf_logger, queue_listener = logger_manager.init_logging()

        root_logger.info(f"Prompt: {prompt}")

        # Run tests
        test_suite = unittest.TestLoader().discover(start_dir='.', pattern='test_*.py')
        result = unittest.TextTestRunner().run(test_suite)

        if result.wasSuccessful():
            root_logger.info("Tests passed successfully.")
        else:
            root_logger.error("Some tests failed.")
            sys.exit(1)  # Exit if tests have failed

        # API or other logic can be executed here
        # NOTE: This section will only execute if tests pass
        
        _, sub_logger = logger_manager.get_logger('my_branch', 'my_leaf')
        sub_logger.critical("This is a test log message.")
        print(f"Server running at http://localhost:{PORT}")

        # Start the static file server
        def run_static_server():
            with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
                root_logger.info(f"Serving files and handling API requests on port {PORT}")
                httpd.serve_forever()
        run_static_server()
    except Exception as e:
        # Create an ErrorReporter instance
        error_reporter = ErrorReporter(str(e), 1, e)
        # Log the error
        if root_logger is not None:
            error_reporter.log_error(root_logger)
        sys.exit(1)
    finally:
        if queue_listener is not None:
            queue_listener.stop()


if __name__ == "__main__":
    main()
