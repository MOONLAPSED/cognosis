import asyncio
import ctypes
from ctypes import CDLL
import uuid
import logging
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import wraps
import inspect
import os
import sys

from __init__ import Logger, setup_logger

if not Logger.root:
    Logger.root = setup_logger("ApplicationBus", logging.DEBUG, "%Y-%m-%d %H:%M:%S", [logging.StreamHandler()])

def log(level=logging.INFO):
    def decorator(func):
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

class AtomType(Enum):
    VALUE = auto()
    FUNCTION = auto()
    CLASS = auto()
    MODULE = auto()

class Atom(ABC):
    def __init__(self, tag: str, value: Any = None, children: List['Atom'] = None, metadata: Dict[str, Any] = None, **attributes):
        self.id = uuid.uuid4()
        self.tag = tag
        self.value = value
        self.children = children or []
        self.metadata = metadata or {}
        self.attributes = attributes
        self.atom_type = self._infer_atom_type()

    def _infer_atom_type(self) -> AtomType:
        if callable(self.value):
            return AtomType.FUNCTION
        elif inspect.isclass(self.value):
            return AtomType.CLASS
        elif inspect.ismodule(self.value):
            return AtomType.MODULE
        else:
            return AtomType.VALUE

    @abstractmethod
    async def evaluate(self) -> Any:
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, tag={self.tag}, value={self.value})"

class Element(Atom):
    def __post_init__(self):
        super().__init__(tag=self.__class__.__name__, value=self)

    def __setattr__(self, name, value):
        if name in self.__annotations__:
            expected_type = self.__annotations__[name]
            if not isinstance(value, expected_type):
                raise TypeError(f"Expected {expected_type} for {name}, got {type(value)}")
        super().__setattr__(name, value)

    async def evaluate(self) -> Any:
        return self

class FFILoader(Atom):
    def __init__(self, lib_path: str, **attributes):
        super().__init__(tag="FFI", **attributes)
        self.lib_path = lib_path
        self.lib = self._load_library()

    def _load_library(self):
        try:
            if sys.platform.startswith('linux'):
                return CDLL(self.lib_path)
            elif sys.platform == 'darwin':
                # For macOS, you may need to adjust this path
                return CDLL(self.lib_path)
            elif sys.platform == 'win32':
                # Adjust for Windows (assumes `.dll` file extension)
                return CDLL(self.lib_path)
            else:
                raise OSError(f"Unsupported platform: {sys.platform}")
        except OSError as e:
            Logger.error(f"Failed to load shared library {self.lib_path}: {e}")
            raise

    def get_function(self, func_name: str, argtypes=None, restype=ctypes.c_int):
        try:
            func = getattr(self.lib, func_name)
            func.argtypes = argtypes or []
            func.restype = restype
            return func
        except AttributeError:
            Logger.error(f"Function {func_name} not found in {self.lib_path}")
            raise

    async def evaluate(self) -> Any:
        return self.lib

class UniversalCompiler(Atom):
    def __init__(self):
        super().__init__(tag="UniversalCompiler")
        self.ffi_loaders: Dict[str, FFILoader] = {}
        self.lock = asyncio.Lock()

    @log()
    async def load_library(self, lib_name: str, lib_path: str):
        async with self.lock:
            if lib_name not in self.ffi_loaders:
                self.ffi_loaders[lib_name] = FFILoader(lib_path)
                Logger.info(f"Loaded library: {lib_name}")

    @log()
    async def call_foreign_function(self, lib_name: str, func_name: str, *args, **kwargs):
        if lib_name not in self.ffi_loaders:
            raise ValueError(f"Library {lib_name} not loaded")

        ffi_loader = self.ffi_loaders[lib_name]
        func = ffi_loader.get_function(func_name)

        c_args = [self._convert_to_ctype(arg) for arg in args]
        result = await asyncio.get_running_loop().run_in_executor(None, func, *c_args)
        return result

    def _convert_to_ctype(self, value: Any) -> Any:
        if isinstance(value, int):
            return ctypes.c_int(value)
        elif isinstance(value, float):
            return ctypes.c_double(value)
        elif isinstance(value, str):
            return ctypes.c_char_p(value.encode('utf-8'))
        elif isinstance(value, bool):
            return ctypes.c_bool(value)
        elif isinstance(value, list):
            return (ctypes.c_int * len(value))(*value)
        return value

    async def evaluate(self) -> Any:
        return self.ffi_loaders

@dataclass
class AtomicTheory(Atom):
    theory_id: str
    local_data: Dict[str, Any] = field(default_factory=dict)
    task_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    running: bool = False
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    def __post_init__(self):
        super().__init__(tag="AtomicTheory", value=self)

    @log()
    async def submit_task(self, atom: Atom, args=(), kwargs=None) -> str:
        task_id = str(uuid.uuid4())
        await self.task_queue.put((task_id, atom, args, kwargs or {}))
        Logger.info(f"Submitted task {task_id} to theory {self.theory_id}")
        return task_id

    @log()
    async def allocate(self, key: str, value: Any) -> None:
        async with self.lock:
            self.local_data[key] = value
            Logger.info(f"Allocated {key} = {value}")

    @log()
    async def deallocate(self, key: str) -> None:
        async with self.lock:
            value = self.local_data.pop(key, None)
            Logger.info(f"Deallocated {key}, value was {value}")

    async def get(self, key: str) -> Any:
        async with self.lock:
            return self.local_data.get(key)

    @log()
    async def run(self) -> None:
        self.running = True
        asyncio.create_task(self._worker())
        Logger.info(f"{self.theory_id} is running")

    @log()
    async def stop(self) -> None:
        self.running = False
        Logger.info(f"{self.theory_id} has stopped")

    async def _worker(self) -> None:
        while self.running:
            try:
                task_id, atom, args, kwargs = await asyncio.wait_for(self.task_queue.get(), timeout=1)
                Logger.info(f"Processing task {task_id}")
                await self.allocate(f"current_task_{task_id}", atom)
                result = await atom.evaluate(*args, **kwargs)
                await self.deallocate(f"current_task_{task_id}")
                Logger.info(f"Completed task {task_id} with result: {result}")
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                Logger.error(f"Error in worker: {e}")

    async def evaluate(self) -> Any:
        return self.local_data

class RuntimeManager(Atom):
    _instance: Optional['RuntimeManager'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'): 
            super().__init__(tag="RuntimeManager")
            self.universal_compiler = UniversalCompiler()
            self.theories: Dict[str, AtomicTheory] = {}
            self.initialized = True

    @log()
    async def create_theory(self, theory_id: str):
        if theory_id in self.theories:
            raise ValueError(f"Theory {theory_id} already exists")
        self.theories[theory_id] = AtomicTheory(theory_id)
        Logger.info(f"Created theory {theory_id}")

    @log()
    async def get_theory(self, theory_id: str) -> AtomicTheory:
        if theory_id not in self.theories:
            raise ValueError(f"Theory {theory_id} does not exist")
        return self.theories[theory_id]

    @log()
    async def run_theory(self, theory_id: str):
        theory = await self.get_theory(theory_id)
        await theory.run()

    @log()
    async def stop_theory(self, theory_id: str):
        theory = await self.get_theory(theory_id)
        await theory.stop()

    @log()
    async def call_function(self, lib_name: str, func_name: str, *args):
        return await self.universal_compiler.call_foreign_function(lib_name, func_name, *args)

    async def evaluate(self) -> Any:
        return self.theories
