import argparse
import asyncio
import datetime
import json
import logging
import os
import shutil
import subprocess
import sys
import threading
import uuid
from functools import reduce
from logging.config import dictConfig
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union

from runtime import main as runtime

T = TypeVar("T")


def main():
    try:
        runtime()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        logging.info("Exiting...")


def usermain():
    # some code that might fail
    def do_something():
        # some operation that might raise an exception
        return True
    try:
        # some operation that might raise an exception
        result = do_something()
    except Exception as e:
        logging.error(f"Failed with error: {e}")
        return False  # or whatever failure indication you want

failure_count = 0
for _ in range(10):  # or however many times you want to run the function
    if not usermain():
        failure_count += 1

failure_rate = failure_count / 10  # calculate the failure rate as a percentage
print(f"Failure rate: {failure_rate:.2f}%")


if __name__ == "__main__":
    main()
