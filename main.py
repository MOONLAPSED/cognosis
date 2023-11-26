#! /usr/bin/env python3
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
import typer
from cognosis.Chunk_ import TextChunker
from cognosis.FSK_mono.mono import *
from cognosis.FSK_mono.mono import UUID
from cognosis.FSK_mono.monoTypes import *
from faststream import FastStream
from faststream.kafka import KafkaBroker

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


@broker.publisher("to_Name")
@broker.publisher(
    "to_UUID"
)  # This indicates that the decorated function will be called whenever a message is published to any of these topics.
@broker.publisher("to_UFS")
@app.after_startup  # This line decorates a function as the after_startup event handler. The after_startup event is triggered once the FastStream application has been fully initialized.


# =====async-section============
async def my_async_function(*args, **kwargs):
    pass  # The decorated function is called when the application starts up.


async def publish_UUID():
    await broker.publish(UUID(uuid="1234567890"), "greetings")
    pass  # The decorated function publishes a UUID object with the value "1234567890" to the "greetings" topic when the application starts up.


async def main(arg1, arg2):
    await app.run()


if __name__ == "__main__":
    arg1 = {"hello", str}
    arg2 = {"world", str}
    asyncio.run(main(arg1, arg2))
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

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    rlhf = RLHF('rlhf.db')
    rlhf.dbinitcall()
    run_tests()
    main()
