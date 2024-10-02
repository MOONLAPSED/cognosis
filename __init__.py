#!/usr/bin/env python
# -*- coding: utf-8 -*-
# STATE_START
{
  "current_step": 0
}
# STATE_END
import os
import sys
import io
import re
import dis
import ast
import tokenize
import importlib
import pathlib
import asyncio
import argparse
import uuid
import json
import struct
import time
import hashlib
import msgpack
import dis
import inspect
import threading
import logging
import time
import shlex
import shutil
import uuid
import argparse
import ctypes
import tracemalloc
from enum import Enum, auto
from typing import (
    Any, Dict, List, Optional, Union, Callable, TypeVar, Tuple, Generic, Set, Coroutine, Type, NamedTuple
)
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from asyncio import Queue as AsyncQueue
from queue import Queue, Empty
from functools import wraps
from enum import Enum, auto
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
tracemalloc.start()
tracefilter = ("<<frozen importlib._bootstrap>", "<frozen importlib._bootstrap_external>")
tracemalloc.Filter(False, trace for trace in tracemalloc.get_traced_memory() if trace.traceback[0].filename not in tracefilter)
def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(True, "<module>"),
    ))
    top_stats = snapshot.statistics(key_type)
    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print("#%s: %s:%s: %.1f KiB"
              % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)
    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))
snapshot = tracemalloc.take_snapshot()
display_top(snapshot)
class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: "\x1b[38;20m%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)\x1b[0m",
        logging.INFO: "\x1b[32;20m%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)\x1b[0m",
        logging.WARNING: "\x1b[33;20m%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)\x1b[0m",
        logging.ERROR: "\x1b[31;20m%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)\x1b[0m",
        logging.CRITICAL: "\x1b[31;1m%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)\x1b[0m",
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self._fmt)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
def setup_logger(name: str, level: int = logging.INFO, log_file: Optional[str] = None):
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger  # Avoid multiple handler additions

    formatter = CustomFormatter()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(level)
    return logger

@dataclass
class RuntimeState:
    current_step: int = 0
    variables: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    IS_POSIX = os.name == 'posix'
    IS_WINDOWS = not IS_POSIX  # Assume Windows if WSL is not detected
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
    allowed_root: Path = field(init=False)
    def __post_init__(self):
        try:
            self.allowed_root = Path(__file__).resolve().parent
            if not any(self.allowed_root.iterdir()):
                raise FileNotFoundError(f"Allowed root directory empty: {self.allowed_root}")
            logging.info(f"Allowed root directory found: {self.allowed_root}")
        except Exception as e:
            logging.error(f"Error initializing FilesystemState: {e}")
            raise

    def safe_remove(self, path: Path):
        """Safely remove a file or directory, handling platform-specific issues."""
        try:
            path = path.resolve()
            if not path.is_relative_to(self.allowed_root):
                logging.error(f"Attempt to delete outside allowed directory: {path}")
                return
            if path.is_dir():
                shutil.rmtree(path)
                logging.info(f"Removed directory: {path}")
            else:
                path.unlink()
                logging.info(f"Removed file: {path}")
        except (FileNotFoundError, PermissionError, OSError) as e:
            logging.error(f"Error removing path {path}: {e}")

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

    async def run_command_async(command: str, shell: bool = False, timeout: int = 120):
        logging.info(f"Running command: {command}")
        split_command = shlex.split(command, posix=(os.name == 'posix'))

        try:
            process = await asyncio.create_subprocess_exec(*split_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, shell=shell)
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)

            return {
                "return_code": process.returncode,
                "output": stdout.decode() if stdout else "",
                "error": stderr.decode() if stderr else "",
            }
        except asyncio.TimeoutError:
            logging.error(f"Command '{command}' timed out.")
            return {"return_code": -1, "output": "", "error": "Command timed out"}
        except Exception as e:
            logging.error(f"Error running command '{command}': {str(e)}")
            return {"return_code": -1, "output": "", "error": str(e)}

class preHomoiconic:
    # HOMOICONISTIC morphological source code displays 'modified quine' behavior
    # within a validated runtime, if and only if the valid python interpreter
    # has r/w/x permissions to the source code file and some method of writing
    # state to the source code file is available. Any interruption of the
    # '__exit__` method or misuse of '__enter__' will result in a runtime error
    # AP (Availability + Partition Tolerance): A system that prioritizes availability and partition tolerance may use a distributed architecture with eventual consistency (e.g., Cassandra or Riak). This ensures that the system is always available (availability), even in the presence of network partitions (partition tolerance). However, the system may sacrifice consistency, as nodes may have different views of the data (no consistency).
    # A homoiconic piece of source code is eventually consistent, assuming it is able to re-instantiated.
    # platforms: Ubuntu-22.04LTS (posix), Windows-11 (nt)
    def __init__(self):
        """All elements of homoiconism are setup with ADMIN-scoped access via __init__.py files, only. 
        to __enter__ a runtime, __init__ must run to do ADMIN-scoped instantiation."""
        self.set_permissions()
        def set_permissions(self):
            if os.name == 'nt':
                self.permissions_info = self.windows_permissions(sys.argv[0])
            elif os.name == 'posix':
                self.permissions_info = self.posix_permissions(sys.argv[0])
    
        if os.name == 'nt':
            from ctypes import windll
            # Function to check file permissions on Windows
            def windowsPermissions(filePath):
                GENERIC_READ = 0x80000000
                GENERIC_WRITE = 0x40000000
                GENERIC_EXECUTE = 0x20000000
                OPEN_EXISTING = 3
                FILE_ATTRIBUTE_NORMAL = 0x80
                # Open file for reading to get handle
                fileHandle = windll.kernel32.CreateFileW(filePath, GENERIC_READ, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
                if fileHandle == -1:
                    return None
                # Check file attributes using Windows API
                permissionsInfo = {
                    "readable": False,
                    "writable": False,
                    "executable": False}
                # GetFileSecurityW retrieves permissions (DACL - Discretionary Access Control List)
                # SECURITY_INFORMATION constants: https://docs.microsoft.com/en-us/windows/win32/secauthz/security-information
                READ_CONTROL = 0x00020000
                DACL_SECURITY_INFORMATION = 0x00000004
                # Allocate buffer to hold the security descriptor
                security_descriptor = ctypes.create_string_buffer(1024)
                sd_size = ctypes.c_ulong()
                # Fetch security info
                result = windll.advapi32.GetFileSecurityW(filePath, DACL_SECURITY_INFORMATION, security_descriptor, 1024, ctypes.byref(sd_size))
                if result == 0:
                    return permissionsInfo  # Failed to get security info
                # Check permissions by querying the file attributes
                fileAttributes = windll.kernel32.GetFileAttributesW(filePath)
                if fileAttributes == -1:
                    print("Failed to get file attributes")
                    return permissionsInfo
                # Modify permission status based on attributes
                permissionsInfo["readable"] = bool(fileAttributes & GENERIC_READ)
                permissionsInfo["writable"] = bool(fileAttributes & GENERIC_WRITE)
                permissionsInfo["executable"] = bool(fileAttributes & GENERIC_EXECUTE)
                # Close the file handle
                windll.kernel32.CloseHandle(fileHandle)
                return permissionsInfo
            self.permissions_info = self.windows_permissions(sys.argv[0])
            if permissionsInfo:
                print("File permissions:")
                print(f"Readable: {permissionsInfo['readable']}")
        elif os.name == 'posix':
            from ctypes import cdll
            def detailedPermissions(filePath):
                """Get detailed file permissions using stat."""
                fileStats = os.stat(filePath)
                mode = fileStats.st_mode
                permissionsInfo = {
                    "readable": bool(mode & stat.S_IRUSR),
                    "writable": bool(mode & stat.S_IWUSR),
                    "executable": bool(mode & stat.S_IXUSR),
                    "octal": oct(mode)}
                return permissionsInfo
            self.permissions_info = self.posix_permissions(sys.argv[0])
# Typing ----------------------------------------------------------
"""Homoiconism dictates that, upon runtime validation, all objects are code and data.
To fascilitate; we utilize first class functions and a static typing system."""
T = TypeVar('T', bound=any) # T for TypeVar, V for ValueVar. Homoicons are T+V.
V = TypeVar('V', bound=Union[int, float, str, bool, list, dict, tuple, set, object, Callable, type])
C = TypeVar('C', bound=Callable[..., Any])  # callable 'T'/'V' first class function interface
DataType = Enum('DataType', 'INTEGER FLOAT STRING BOOLEAN NONE LIST TUPLE') # 'T' vars (stdlib)
AtomType = Enum('AtomType', 'FUNCTION CLASS MODULE OBJECT') # 'C' vars (homoiconic methods or classes)
