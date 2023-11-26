import argparse
import unittest
from os import os
from sys import sys

import requests
from cognosis.main import Entity_
from logs.logdef import init_logging

#! /usr/bin/env python3


version = "0.1.10"
title = "cognosis/FSK_mono"
description = "cognosis RLHF kernel for FastStream_Kafka_Monolith"
broker = KafkaBroker()
app = FastStream(
    broker,
    title=title,
    version=version,
    description=description,
)
log_directory = 'logs'
log_file_path = os.path.join(log_directory, 'app.log')
logger = init_logging(log_directory, log_file_path)

PORT = 8080
server_main_url = 'http://localhost:{}'.format(PORT)


class TestServerStatus(unittest.TestCase):
    """
    TestServerStatus class for testing server status.
    """

    def test_server_is_running(self):
        """
        Test if the server is running and reachable.
        """
        try:
            response = requests.get(server_main_url)
            self.assertEqual(response.status_code, 200)
        except requests.ConnectionError as e:
            self.fail('Server is not running or not reachable.')


class Entity_:
    """
    The Entity_ class represents a general entity with a name and a description.

    Attributes:
    - name (str): The name of the entity.
    - description (str): The description of the entity.
    """

    def __init__(self, name: str, description: str):
        """
        The constructor for the Entity_ class. It initializes the name and description attributes.

        Parameters:
        - name (str): The name of the entity.
        - description (str): The description of the entity.
        """
        self.name = name
        self.description = description

    def subscriber(self, topic: str):
        """
        The subscriber decorator for the Entity_ class. It subscribes the entity to a topic.

        Parameters:
        - topic (str): The topic to subscribe to.
        """
        def decorator(func):
            """
            A decorator that wraps a function to provide additional functionality.

            Parameters:
            - func: The function to be decorated.

            Returns:
            - The decorated function.
            """
            async def wrapper():
                await func(self)
            return wrapper

        return decorator

    def publisher(self, topic: str):
        """
        The publisher decorator for the Entity_ class. It publishes the entity to a topic.

        Parameters:
        - topic (str): The topic to publish to.

        Returns:
        - The decorated function.
        """
        async def wrapper(message: str):
            print(f"Publishing message: {message}")
            await self.publish(topic, message)
        return wrapper

    def publish(self, topic: str, message: str):
        """
        The publish method for the Entity_ class. It publishes the entity to a topic.

        Parameters:
        - topic (str): The topic to publish to.
        - message (str): The message to publish.

        Returns:
        - None
        """
        print(f"Publishing message: {message}")
        return None


def run_tests():
    """
    Runs all the unit tests.

    Returns:
    - None
    """
    unittest.main()


def main():
    """
    Main function of the program.
    Parses command line arguments, runs unit tests, and starts the static file server.

    Returns:
    - None
    """
    try:
        parser = argparse.ArgumentParser(description='cognosis by MOONLAPSED@gmail.com MIT License')
        parser.add_argument('prompt', nargs='*', help='Enter the prompt here')
        args = parser.parse_args()

        if not args.prompt:
            args.prompt.append('Hello world!')

        prompt = ' '.join(args.prompt).strip()
        logger.info(f"Prompt: {prompt}")

        test_suite = unittest.TestLoader().discover(start_dir='.', pattern='test_*.py')
        result = unittest.TextTestRunner().run(test_suite)

        if result.wasSuccessful():
            logger.info("Tests passed successfully.")
        else:
            logger.error("Some tests failed.")
            sys.exit(1)

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
