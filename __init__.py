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
"""
We can assume that imperative deterministic source code, such as this file written in Python, is capable of reasoning about non-imperative non-deterministic source code as if it were a defined and known quantity. This is akin to nesting a function with a value in an S-Expression.

In order to expect any runtime result, we must assume that a source code configuration exists which will yield that result given the input.

The source code configuration is the set of all possible configurations of the source code. It is the union of the possible configurations of the source code.

Imperative programming specifies how to perform tasks (like procedural code), while non-imperative (e.g., functional programming in LISP) focuses on what to compute. We turn this on its head in our imperative non-imperative runtime by utilizing nominative homoiconistic reflection to create a runtime where dynamical source code is treated as both static and dynamic.

"Nesting a function with a value in an S-Expression":
In the code, we nest the input value within different function expressions (configurations).
Each function is applied to the input to yield results, mirroring the collapse of the wave function to a specific state upon measurement.

This nominative homoiconistic reflection combines the expressiveness of S-Expressions with the operational semantics of Python. In this paradigm, source code can be constructed, deconstructed, and analyzed in real-time, allowing for dynamic composition and execution. Each code configuration (or state) is akin to a function in an S-Expression that can be encapsulated, manipulated, and ultimately evaluated in the course of execution.

To illustrate, consider a Python function as a generalized S-Expression. This function can take other functions and values as arguments, forming a nested structure. Each invocation changes the system's state temporarily, just as evaluating an S-Expression alters the state of the LISP interpreter.

In essence, our approach ensures that:

1. **Composition**: Functions (or code segments) can be composed at runtime, akin to how S-Expressions can nest functions and values.
2. **Evaluation**: Upon invocation, these compositions are evaluated, reflecting the current configuration of the runtime.
3. **Reflection and Modification**: The runtime can reflect on its structure and make modifications dynamically, which allows it to reason about its state and adapt accordingly.

This synthesis of static and dynamic code concepts is akin to the Copenhagen interpretation of quantum mechanics, where the observation (or execution) collapses the superposition of states (or configurations) into a definite outcome based on the input.

Ultimately, this model provides a flexible approach to managing and executing complex code structures dynamically while maintaining the clarity and compositional advantages traditionally seen in non-imperative, functional paradigms like LISP, drawing inspiration from lambda calculus and functional programming principles.

The most advanced concept of all in this ontology is the dynamic rewriting of source code at runtime. Source code rewriting is achieved with a special runtime `Atom()` class with 'modified quine' behavior. This special Atom, aside from its specific function and the functions obligated to it by polymorphism, will always rewrite its own source code but may also perform other actions as defined by the source code in the runtime which invoked it. They can be nested in S-expressions and are homoiconic with all other source code. These modified quines can be used to dynamically create new code at runtime, which can be used to extend the source code in a way that is not known at the start of the program. This is the most powerful feature of the system and allows for the creation of a runtime of runtimes dynamically limited by hardware and the operating system.
"""
# non-homoiconic pre-runtime "ADMIN-SCOPED" source code:

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

# Setup custom logging format for enhanced error messages and debugging
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

# DECORATORS =========================================================
def atom(cls: Type[{T, V, C}]) -> Type[{T, V, C}]: # homoicon decorator
    """Decorator to create a homoiconic atom."""
    original_init = cls.__init__
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        if not hasattr(self, 'id'):
            self.id = hashlib.sha256(self.__class__.__name__.encode('utf-8')).hexdigest()

    cls.__init__ = new_init
    return cls

def log(level=logging.INFO):
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            Logger.log(level, f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
            try:
                result = await func(*args, **kwargs)
                Logger.log(level, f"Completed {func.__name__} with result: {result}")
                return result
            except Exception as e:
                Logger.exception(f"Error in {func.__name__}: {str(e)}")
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            Logger.log(level, f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
            try:
                result = func(*args, **kwargs)
                Logger.log(level, f"Completed {func.__name__} with result: {result}")
                return result
            except Exception as e:
                Logger.exception(f"Error in {func.__name__}: {str(e)}")
                raise
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

def validate(cls: Type[T]) -> Type[T]:
    original_init = cls.__init__
    sig = inspect.signature(original_init)

    def new_init(self: T, *args: Any, **kwargs: Any) -> None:
        bound_args = sig.bind(self, *args, **kwargs)
        for key, value in bound_args.arguments.items():
            if key in cls.__annotations__:
                expected_type = cls.__annotations__.get(key)
                if not isinstance(value, expected_type):
                    raise TypeError(f"Expected {expected_type} for {key}, got {type(value)}")
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls

def encode(atom: 'Atom') -> bytes:
    data = {
        'tag': atom.tag,
        'value': atom.value,
        'children': [encode(child) for child in atom.children],
        'metadata': atom.metadata
    }
    return pickle.dumps(data)

def decode(data: bytes) -> 'Atom':
    data = pickle.loads(data)
    atom = Atom(data['tag'], data['value'], [decode(child) for child in data['children']], data['metadata'])
    return atom

# Typing ----------------------------------------------------------
"""Homoiconism dictates that, upon runtime validation, all objects are code and data.
To fascilitate; we utilize first class functions and a static typing system."""
T = TypeVar('T', bound=any) # T for TypeVar, V for ValueVar. Homoicons are T+V.
V = TypeVar('V', bound=Union[int, float, str, bool, list, dict, tuple, set, object, Callable, type])
C = TypeVar('C', bound=Callable[..., Any])  # callable 'T'/'V' first class function interface
DataType = Enum('DataType', 'INTEGER FLOAT STRING BOOLEAN NONE LIST TUPLE') # 'T' vars (stdlib)
AtomType = Enum('AtomType', 'FUNCTION CLASS MODULE OBJECT') # 'C' vars (homoiconic methods or classes)
# Base class for all Atoms to support homoiconism
class Atom:
    id: str = field(init=False)
    tag: str = ''
    children: List['Atom'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    reflexivity: Callable[[T], bool] = lambda x: x == x
    symmetry: Callable[[T, T], bool] = lambda x, y: x == y
    transitivity: Callable[[T, T, T], bool] = lambda x, y, z: (x == y and y == z)
    transparency: Callable[[Callable[..., T], T, T], T] = lambda f, x, y: f(True, x, y) if x == y else None
    case_base: Dict[str, Callable[..., bool]] = field(default_factory=dict)
    def __init__(self, id: str):
        self.id = id

    def __post_init__(self):
        self.case_base = {
            '⊤': lambda x, _: x,
            '⊥': lambda _, y: y,
            '¬': lambda a: not a,
            '∧': lambda a, b: a and b,
            '∨': lambda a, b: a or b,
            '→': lambda a, b: (not a) or b,
            '↔': lambda a, b: (a and b) or (not a and not b),
        }

    def encode(self) -> bytes:
        return json.dumps({
            'id': self.id,
            'attributes': self.attributes
        }).encode()

    @classmethod
    def decode(cls, data: bytes) -> 'Atom':
        decoded_data = json.loads(data.decode())
        return cls(id=decoded_data['id'], **decoded_data['attributes'])

    def introspect(self) -> str:
        """
        Reflect on its own code structure via AST.
        """
        source = inspect.getsource(self.__class__)
        return ast.dump(ast.parse(source))

    def __init__(self, value: Union[T, V, C], type: Union[DataType, AtomType]):
        self.value = value
        self.type = type
        self.hash = hashlib.sha256(repr(value).encode()).hexdigest()

    def __repr__(self):
        return f"{self.value} : {self.type}"

    def __str__(self):
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Atom) and self.hash == other.hash

    def __hash__(self) -> int:
        return int(self.hash, 16)

    def __buffer__(self, flags: int) -> memoryview:
        return memoryview(self.value)

    async def send_message(self, message: Any, ttl: int = 3) -> None:
        if ttl <= 0:
            logging.info(f"Message {message} dropped due to TTL")
            return
        logging.info(f"Atom {self.id} received message: {message}")
        for sub in self.subscribers:
            await sub.receive_message(message, ttl - 1)

    async def receive_message(self, message: Any, ttl: int) -> None:
        logging.info(f"Atom {self.id} processing received message: {message} with TTL {ttl}")
        await self.send_message(message, ttl)

    def subscribe(self, atom: 'Atom') -> None:
        self.subscribers.add(atom)
        logging.info(f"Atom {self.id} subscribed to {atom.id}")

    def unsubscribe(self, atom: 'Atom') -> None:
        self.subscribers.discard(atom)
        logging.info(f"Atom {self.id} unsubscribed from {atom.id}")
    # Use __slots__ for the rest of the methods to save memory
    __slots__ = ('value', 'type', 'hash')
    __getitem__ = lambda self, key: self.value[key]
    __setitem__ = lambda self, key, value: setattr(self.value, key, value)
    __delitem__ = lambda self, key: delattr(self.value, key)
    __len__ = lambda self: len(self.value)
    __iter__ = lambda self: iter(self.value)
    __contains__ = lambda self, item: item in self.value
    __call__ = lambda self, *args, **kwargs: self.value(*args, **kwargs)

    __add__ = lambda self, other: self.value + other
    __sub__ = lambda self, other: self.value - other
    __mul__ = lambda self, other: self.value * other
    __truediv__ = lambda self, other: self.value / other
    __floordiv__ = lambda self, other: self.value // other
@dataclass
class TaskAtom(Atom):  # Tasks are atoms that represent asynchronous potential actions
    task_id: int
    atom: Atom
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    result: Any = None

    async def run(self) -> Any:
        logging.info(f"Running task {self.task_id}")
        try:
            self.result = await self.atom.execute(*self.args, **self.kwargs)
            logging.info(f"Task {self.task_id} completed with result: {self.result}")
        except Exception as e:
            logging.error(f"Task {self.task_id} failed with error: {e}")
        return self.result

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    @classmethod
    def decode(cls, data: bytes) -> 'TaskAtom':
        obj = json.loads(data.decode())
        return cls.from_dict(obj)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'task_id': self.task_id,
            'atom': self.atom.to_dict(),
            'args': self.args,
            'kwargs': self.kwargs,
            'result': self.result
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskAtom':
        return cls(
            task_id=data['task_id'],
            atom=Atom.from_dict(data['atom']),
            args=tuple(data['args']),
            kwargs=data['kwargs'],
            result=data['result']
        )

class ArenaAtom(Atom):  # Arenas are threaded virtual memory Atoms appropriately-scoped when invoked
    def __init__(self, name: str):
        super().__init__(id=name)
        self.name = name
        self.local_data: Dict[str, Any] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.executor = ThreadPoolExecutor()
        self.running = False
        self.lock = threading.Lock()
    
    async def allocate(self, key: str, value: Any) -> None:
        with self.lock:
            self.local_data[key] = value
            logging.info(f"Arena {self.name}: Allocated {key} = {value}")
    
    async def deallocate(self, key: str) -> None:
        with self.lock:
            value = self.local_data.pop(key, None)
            logging.info(f"Arena {self.name}: Deallocated {key}, value was {value}")
    
    def get(self, key: str) -> Any:
        return self.local_data.get(key)
    
    def encode(self) -> bytes:
        data = {
            'name': self.name,
            'local_data': {key: value.to_dict() if isinstance(value, Atom) else value 
                           for key, value in self.local_data.items()}
        }
        return json.dumps(data).encode()

    @classmethod
    def decode(cls, data: bytes) -> 'ArenaAtom':
        obj = json.loads(data.decode())
        instance = cls(obj['name'])
        instance.local_data = {key: Atom.from_dict(value) if isinstance(value, dict) else value 
                               for key, value in obj['local_data'].items()}
        return instance
    
    async def submit_task(self, atom: Atom, args=(), kwargs=None) -> int:
        task_id = uuid.uuid4().int
        task = TaskAtom(task_id, atom, args, kwargs or {})
        await self.task_queue.put(task)
        logging.info(f"Submitted task {task_id}")
        return task_id
    
    async def task_notification(self, task: TaskAtom) -> None:
        notification_atom = AtomNotification(f"Task {task.task_id} completed")
        await self.send_message(notification_atom)
    
    async def run(self) -> None:
        self.running = True
        asyncio.create_task(self._worker())
        logging.info(f"Arena {self.name} is running")

    async def stop(self) -> None:
        self.running = False
        self.executor.shutdown(wait=True)
        logging.info(f"Arena {self.name} has stopped")
    
    async def _worker(self) -> None:
        while self.running:
            try:
                task: TaskAtom = await asyncio.wait_for(self.task_queue.get(), timeout=1)
                logging.info(f"Worker in {self.name} picked up task {task.task_id}")
                await self.allocate(f"current_task_{task.task_id}", task)
                await task.run()
                await self.task_notification(task)
                await self.deallocate(f"current_task_{task.task_id}")
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logging.error(f"Error in worker: {e}")

@dataclass
class AtomNotification(Atom):  # nominative async message passing interface
    message: str

    def encode(self) -> bytes:
        return json.dumps({'message': self.message}).encode()

    @classmethod
    def decode(cls, data: bytes) -> 'AtomNotification':
        obj = json.loads(data.decode())
        return cls(message=obj['message'])

class EventBus(Atom):  # Pub/Sub homoiconic event bus
    def __init__(self):
        super().__init__(id="event_bus")
        self._subscribers: Dict[str, List[Callable[[Atom], Coroutine[Any, Any, None]]]] = {}

    async def subscribe(self, event_type: str, handler: Callable[[Atom], Coroutine[Any, Any, None]]) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def unsubscribe(self, event_type: str, handler: Callable[[Atom], Coroutine[Any, Any, None]]) -> None:
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(handler)

    async def publish(self, event_type: str, event: Atom) -> None:
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                asyncio.create_task(handler(event))

    def encode(self) -> bytes:
        raise NotImplementedError("EventBus cannot be directly encoded")

    @classmethod
    def decode(cls, data: bytes) -> None:
        raise NotImplementedError("EventBus cannot be directly decoded")

@dataclass
class EventAtom(Atom):  # Events are network-friendly Atoms, associates with a type and an id (USER-scoped), think; datagram
    id: str
    type: str
    detail_type: Optional[str] = None
    message: Union[str, List[Dict[str, Any]]] = field(default_factory=list)
    source: Optional[str] = None
    target: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    @classmethod
    def decode(cls, data: bytes) -> 'EventAtom':
        obj = json.loads(data.decode())
        return cls.from_dict(obj)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "detail_type": self.detail_type,
            "message": self.message,
            "source": self.source,
            "target": self.target,
            "content": self.content,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EventAtom':
        return cls(
            id=data["id"],
            type=data["type"],
            detail_type=data.get("detail_type"),
            message=data.get("message"),
            source=data.get("source"),
            target=data.get("target"),
            content=data.get("content"),
            metadata=data.get("metadata", {})
        )

    def validate(self) -> bool:
        required_fields = ['id', 'type']
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"Missing required field: {field}")
        return True

@dataclass
class ActionRequestAtom(Atom):  # User-initiated action request
    action: str
    params: Dict[str, Any]
    self_info: Dict[str, Any]
    echo: Optional[str] = None

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    @classmethod
    def decode(cls, data: bytes) -> 'ActionRequestAtom':
        obj = json.loads(data.decode())
        return cls.from_dict(obj)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "params": self.params,
            "self_info": self.self_info,
            "echo": self.echo
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionRequestAtom':
        return cls(
            action=data["action"],
            params=data["params"],
            self_info=data["self_info"],
            echo=data.get("echo")
        )
class AntiAtom(Atom):
    def __init__(self, atom: Atom):
        super().__init__(id=f"anti_{atom.id}", value=None, attributes=atom.attributes)
        self.original_atom = atom

    def encode(self) -> bytes:
        return b'anti_' + self.original_atom.encode()

    def execute(self, *args, **kwargs) -> Any:
        return not self.original_atom.execute(*args, **kwargs)
class LiteralAtom(Atom):
    def __init__(self, tag: str, children: List[Atom]):
        super().__init__(tag=tag, children=children)

    async def evaluate(self) -> Any:
        """An async generator, which can't be directly used with sum(). Instead, we need to use 
        asyncio.gather() to collect all the results before summing them."""
        if self.tag == 'add':
            results = await asyncio.gather(*(child.evaluate() for child in self.children))
            return sum(results)
        elif self.tag == 'negate':
            return -await self.children[0].evaluate()
        else:
            raise NotImplementedError(f"Evaluation not implemented for tag: {self.tag}")

@atom
class ExternalRefAtom(Atom):
    async def evaluate(self):
        if "external_ref" in self.metadata:
            return self.metadata["external_ref"].resolve()
        return None

@atom
class MetaAtom(Atom):
    async def evaluate(self) -> Any:
        if self.tag == "reflect":
            target_atom = self.children[0]
            return target_atom
        elif self.tag == "transform":
            target_atom = self.children[0]
            transformation = self.children[1]
            return await transformation.apply(target_atom)
        else:
            raise NotImplementedError(f"Meta evaluation not implemented for tag: {self.tag}")

@dataclass
class FileAtom(Atom):
    file_path: Path
    file_content: str = field(init=False)

    def __post_init__(self):
        super().__init__(tag='file', value=self.file_path)
        self.file_content = self.read_file(self.file_path)

    def read_file(self, file_path: Path) -> str:
        with file_path.open('r', encoding='utf-8', errors='ignore') as file:
            return file.read()

    async def evaluate(self):
        return self.file_content

    def __repr__(self) -> str:
        return f"FileAtom(file_path={self.file_path}, file_content=...)"

@dataclass  # Theory combines atom behavior with task execution and memory allocation
class AtomicTheory(Atom):
    id: str
    local_data: Dict[str, Any] = field(default_factory=dict)
    task_queue: AsyncQueue = field(default_factory=AsyncQueue)
    running: bool = False
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    def __post_init__(self):
        super().__init__(id=self.id)

    async def submit_task(self, atom: Atom, args=(), kwargs=None) -> int:
        task_id = uuid.uuid4().int
        task = TaskAtom(task_id, atom, args, kwargs or {})
        await self.task_queue.put(task)
        logging.info(f"Submitted task {task_id}")
        return task_id

    async def allocate(self, key: str, value: Any) -> None:
        async with self.lock:
            self.local_data[key] = value
            logging.info(f"Allocated {key} = {value}")

    async def deallocate(self, key: str) -> None:
        async with self.lock:
            value = self.local_data.pop(key, None)
            logging.info(f"Deallocated {key}, value was {value}")

    def get(self, key: str) -> Any:
        return self.local_data.get(key)

    async def submit_task(self, atom: Atom, args=(), kwargs=None) -> int:
        task_id = uuid.uuid4().int
        task = TaskAtom(task_id, atom, args, kwargs or {})
        await self.task_queue.put(task)
        logging.info(f"Submitted task {task_id}")
        return task_id

    async def run(self) -> None:
        self.running = True
        asyncio.create_task(self._worker())
        logging.info(f"{self.id} is running")

    async def stop(self) -> None:
        self.running = False
        logging.info(f"{self.id} has stopped")

    async def _worker(self) -> None:
        while self.running:
            try:
                task: TaskAtom = await asyncio.wait_for(self.task_queue.get(), timeout=1)
                logging.info(f"Picked up task {task.task_id}")
                await self.allocate(f"current_task_{task.task_id}", task)
                await task.run()
                await self.deallocate(f"current_task_{task.task_id}")
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logging.error(f"Error in worker: {e}")
