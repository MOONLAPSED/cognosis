
"""
This file contains the main orchestration and initialization logic for the FastStream application.
"""

import argparse
import asyncio
import datetime
import http.server
import json
import logging
import os
import re
import socketserver
import sqlite3
import subprocess
#! /usr/bin/env python3
import sys
import threading

import requests
from cognosis.FSK_mono.mono import *
from cognosis.FSK_mono.monoTypes import *
from cognosis.UFS import *
from logs.logdef import *

# main.py is for orchestration and initialization of the FastStream application.
# /cognosis/application.py is for the actual application logic.
version = "0.1.10"
title = "cognosis/FSK_mono"
description = "cognosis RLHF kernel for FastStream_Kafka_Monolith"
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

entity_test_cases = [
    {
        "name": "Entity 1",
        "description": "Description 1"
    },
    {
        "name": "Entity 2",
        "description": "Description 2"
    }
]
for test_case in entity_test_cases:
    entity = Entity_(test_case["name"], test_case["description"])
    class Entity_:
        """
        The Entity_ class represents a general entity with a name and a description.
    
        Attributes:
        name (str): The name of the entity.
        description (str): The description of the entity.
        """
        def __init__(self, name: str, description: str):
            """
            The constructor for the Entity_ class. It initializes the name and description attributes.
    
            Parameters:
            name (str): The name of the entity.
            description (str): The description of the entity.
            """
            self.name = name
            self.description = description
        def subscriber(self, topic: str):
            """
            The subscriber decorator for the Entity_ class. It subscribes the entity to a topic.
            """
        def decorator(func):
            async def wrapper():
                await func(self)
            return wrapper
            return decorator
        def publisher(self, topic: str):
            """
            The publisher decorator for the Entity_ class. It publishes the entity to a topic.
            """
            async def wrapper(message: str):
                print(f"Publishing message: {message}")
                await self.publish(topic, message)
                return wrapper
            return wrapper
        def publish(self, topic: str, message: str):
            """
            The publish method for the Entity_ class. It publishes the entity to a topic.

            Parameters:
            topic (str): The topic to publish to.
            message (str): The message to publish.
            """
            print(f"Publishing message: {message}")
            return None
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