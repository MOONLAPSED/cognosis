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
