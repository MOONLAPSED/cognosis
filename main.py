import http.server
import socketserver
import os
import sys
import argparse
import logging
import unittest
import json


from src.dbase.pydbase import *  # Import the database module and its classes
from src.utils.errors import *  # Import the error classes
from src.utils.logutils import *  # Check and create the log directory
from src.api.apidef import *  # Import the api module and its classes

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
log_directory = 'logs'
log_file_path = os.path.join(log_directory, 'app.log')
# Initialize logging using logging_utils module
logger = init_logging(log_directory, log_file_path)


def main():
    """
    Main function of the program.
    Parses command line arguments and executes the program accordingly.
    """
    try:
        parser = argparse.ArgumentParser(description='cognosis by MOONLAPSED@gmail.com MIT License')
        parser.add_argument('prompt', nargs='*', help='Enter the prompt here')
        args = parser.parse_args()

        if not args.prompt:  # If prompt is empty, provide a default
            args.prompt.append('Hello world!')

        # Construct the prompt as a single string
        prompt = ' '.join(args.prompt)

        # Remove the last newline if present
        if prompt.endswith('\n'):
            prompt = prompt[:-1]
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

    logger.info(f"Prompt: {prompt}")

    # Run tests
    test_suite = unittest.defaultTestLoader.discover(start_dir='.', pattern='test_*.py')
    result = unittest.TextTestRunner().run(test_suite)

    if result.wasSuccessful():
        logger.info("Tests passed successfully.")
    else:
        logger.error("Some tests failed.")

    # Instantiate API and call the API with the prompt
    # api_instance = API()
    # api_instance.call_api(prompt)


if __name__ == "__main__":
    rlhf = RLHF('rlhf.db')
    rlhf.dbinitcall() 
    main()
