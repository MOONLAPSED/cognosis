#! /usr/bin/env python3
"""
The main.py module is responsible for the orchestration and initialization
of the FastStream application. It sets up server configurations, initializes
logging, and provides a test server status to ensure all components of
the application are functioning correctly before deployment.

This module is the entry point to the application and contains the command-line
interface (CLI) logic for command processing and handling all necessary startup
procedures.

Defines:
- Server configuration and status testing.
- Initiation of the logging system.
- Execution of unittests when the script is run.
"""
# Import necessary modules for network communication, data handling, and application functionality.
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
import sys
import threading
import unittest

import requests
from cognosis.FSK_mono.mono import *
from cognosis.FSK_mono.monoTypes import *
from faststream.kafka import KafkaBroker
from logs.logdef import *

version = "0.1.10"
title = "cognosis/FSK_mono"
description = "cognosis RLHF kernel for FastStream_Kafka_Monolith"
# Basemodels: Name, UUID, tbd  # ========================>mono.py
# Subscribers: bs_Name, bs_UUID, tbd  # ========================>mono.py
# Publishers: to_Name, to_UUID, to_UFS, tbd  # ========================>mono.py
broker = KafkaBroker()  # Initialize KafkaBroker
app = FastStream(  # Create the FastStream app with the broker
    broker,
    title=title,
    version=version,
    description=description,
)  # The FastStream app instance provides the framework for defining subscribers, publishers, and other application components.
# main.py is for orchestration and initialization of the FastStream application.
# /cognosis/application.py is for the actual application logic.
# Make sure the log file path is joining with the proper directory
log_directory = 'logs'
log_file_path = os.path.join(log_directory, 'app.log')
# Initialize logging
logger = init_logging(log_directory, log_file_path)

# Server configuration
PORT = 8080
server_main_url = 'http://localhost:{}'.format(PORT)


# Unit test case to verify that the server is up and responding to requests.
class TestServerStatus(unittest.TestCase):
    def test_server_is_running(self):
        """ Test if the server is running and reachable """
        try:
            response = requests.get(server_main_url)
            self.assertEqual(response.status_code, 200)
        except requests.ConnectionError as e:
from cognosis.main import Entity_

            self.fail('Server is not running or not reachable.')
# A function to run all tests when this script is executed

# Callable function to execute all the unit tests for the application.
def run_tests():
    """
    Runs all the unit tests.

    Returns:
    None
    """
    unittest.main()
    """
    Runs all the unit tests.
    """
    unittest.main()
    """Execute all unit tests for the application."""
    unittest.main()

    unittest.main()


# List of test cases for Entity_ instances, each with a unique name and description.
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

# Iterate over test cases to create and process Entity_ instances.
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
                """A decorator that wraps a function to provide additional functionality."""
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
        def publish(self, topic: str, message: str):
            """
            The publish method for the Entity_ class. It publishes the entity to a topic.
        def publisher(self, topic: str):
            """
            The publisher decorator for the Entity_ class. It publishes the entity to a topic.
            """
            async def wrapper(message: str):
                print(f"Publishing message: {message}")
                await self.publish(topic, message)
            return wrapper
        def publisher(self, topic: str):
            """
            The publisher decorator for the Entity_ class. It publishes the entity to a topic.
            """
            async def wrapper(message: str):
                print(f"Publishing message: {message}")
                await self.publish(topic, message)
            return wrapper
        
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
        """
        Runs all the unit tests.
        """
        unittest.main()
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
            """
            Launches a static file server which listens on a designated port, serving files as well as
            handling API requests.
        
            This server runs indefinitely once activated and logs its presence and available port to the terminal.
            """
            with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
                logger.info(f"Serving files and handling API requests on port {PORT}")
                httpd.serve_forever()
        run_static_server()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

def main():
    """
    This function acts as the primary entry point of the program.

    It parses command-line arguments, runs unit tests, starts the static file server, and contains
    the core execution logic required to initialize and run the application.
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
        """
        Runs all the unit tests.
        """
        unittest.main()
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
            """Starts a static file server that can serve files and handle API requests on a specified port."""
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
