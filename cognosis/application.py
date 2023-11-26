# Cognosis Application Logic
import asyncio
from sys import sys

from main import PORT, argparse, logger, socketserver, unittest


def main():
    # Main function of the program.
    # Parses command line arguments, runs unit tests, and starts the static file server.
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

