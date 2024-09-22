import asyncio
import inspect
import json
import logging
import os
import hashlib
import platform
import pathlib
import struct
import sys
import threading
import time
import shlex
import shutil
import uuid
import argparse
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Tuple, Generic, Set, Coroutine, Type, ClassVar, Protocol
from queue import Queue, Empty
import ctypes
import tracemalloc
tracemalloc.start()
# platforms: Ubuntu-22.04LTS, Windows-11
if os.name == 'posix':
    from ctypes import cdll
elif os.name == 'nt':
    from ctypes import windll

@dataclass
class AppState:
    pdm_installed: bool = False
    virtualenv_created: bool = False
    dependencies_installed: bool = False
    lint_passed: bool = False
    code_formatted: bool = False
    tests_passed: bool = False
    benchmarks_run: bool = False
    pre_commit_installed: bool = False

@dataclass
class FilesystemState:
    def __init__(self):
        try:
            self.allowed_root: Path = Path(__file__).resolve().parent
        except Exception as e:
            logging.error(f"Error initializing FilesystemState: {e}")
            raise
        finally:
            if not self.allowed_root.walk():
                logging.error(f"Allowed root directory not found: {self.allowed_root}")
                raise FileNotFoundError(f"Allowed root directory not found: {self.allowed_root}")
            else:
                logging.info(f"Allowed root directory found: {self.allowed_root}")

    def safe_remove(self, path: Path):
        """Safely remove a file or directory, handling platform-specific issues."""
        try:
            # Normalize and check if the path is within the allowed directory
            path = path.resolve()
            if not path.is_relative_to(self.allowed_root):
                logging.error(f"Attempt to delete outside allowed directory: {path}")
                return
            if path.is_dir():
                shutil.rmtree(path)
                logging.info(f"Removed directory: {path}")
            else:
                path.unlink()  # Removes a single file
                logging.info(f"Removed file: {path}")
        except (FileNotFoundError, PermissionError, OSError) as e:
            logging.error(f"Error removing path {path}: {str(e)}")
    
    def _on_error(self, func, path, exc_info):
        """Error handler for handling removal of read-only files on Windows."""
        logging.error(f"Error deleting {path}, attempting to fix permissions.")
        # Attempt to change the file's permissions and retry removal
        os.chmod(path, 0o777)
        func(path)
    
    async def execute_runtime_tasks(self):
        for task in self.tasks:
            try:
                await task()
            except Exception as e:
                logging.error(f"Error executing task: {e}")

    async def run_command_async(self, command: str, shell: bool = False, timeout: int = 120):
        logging.info(f"Running command: {command}")
        
        # Check for platform-specific adjustments
        if platform.system() == 'Windows':
            shell = False  # Ensure shell is false for subprocess on Windows
            command = shlex.split(command, posix=False) # Split command safely for Windows
            # Normalize paths if the command includes paths
            command = [os.path.normpath(arg) for arg in command]
        else:
            command = shlex.split(command)

        try:
            process = await asyncio.create_subprocess_exec(
                *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, shell=shell
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            stdout = stdout.decode() if stdout else ""
            stderr = stderr.decode() if stderr else ""
            return {
                "return_code": process.returncode,
                "output": stdout,
                "error": stderr,
            }
        except asyncio.TimeoutError:
            logging.error(f"Command '{command}' timed out.")
            return {"return_code": -1, "output": "", "error": "Command timed out"}
        except Exception as e:
            logging.error(f"Error running command '{command}': {str(e)}")
            return {"return_code": -1, "output": "", "error": str(e)}

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;20m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.format)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger(name: str, level: int, datefmt: str, handlers: list):
    """
    Setup logger with custom formatter.
    :param name: logger name
    :param level: logging level
    :param datefmt: date format
    :param handlers: list of logging handlers
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    for handler in handlers:
        if not isinstance(handler, logging.Handler):
            raise ValueError(f"Invalid handler provided: {handler}")
        handler.setLevel(level)
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)

    return logger

Logger = setup_logger("ApplicationBus", logging.DEBUG, "%Y-%m-%d %H:%M:%S", [logging.StreamHandler()])
