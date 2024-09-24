# src/__init__.py

import sys
import importlib
from importlib.util import spec_from_file_location, module_from_spec
import pathlib
import logging
import argparse

import uuid
import json
import struct
import time
import os
import logging
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Tuple, Generic, Set, Coroutine, Type, ClassVar
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import asyncio
from asyncio import Queue as AsyncQueue
from queue import Queue, Empty
import threading
from functools import wraps
import hashlib
import pickle
import dis
import inspect
import tracemalloc
import pytest
tracemalloc.start()
# Detect platform
IS_POSIX = os.name == 'posix'

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

T = TypeVar('T', bound=Type)
C = TypeVar('C', bound=Callable[..., Any])  # callable 'T' class/type variable

class DataType(Enum): # 'T' vars (stdlib)
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    NONE = auto()
    LIST = auto()
    TUPLE = auto()

class AtomType(Enum): # 'C' vars (cust)
    FUNCTION = auto()
    CLASS = auto()
    MODULE = auto()
    OBJECT = auto()

# DECORATORS =========================================================
def atom(cls: Type[T]) -> Type[T]:
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

@atom
class Atom(ABC):
    id: str = field(init=False)
    tag: str = ''
    children: List['Atom'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    reflexivity: Callable[[T], bool] = lambda x: x == x
    symmetry: Callable[[T, T], bool] = lambda x, y: x == y
    transitivity: Callable[[T, T, T], bool] = lambda x, y, z: (x == y and y == z)
    transparency: Callable[[Callable[..., T], T, T], T] = lambda f, x, y: f(True, x, y) if x == y else None
    case_base: Dict[str, Callable[..., bool]] = field(default_factory=dict)

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
def frozen(cls):
    original_setattr = cls.__setattr__

    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError(f"Cannot modify frozen attribute '{name}'")
        original_setattr(self, name, value)
    
    cls.__setattr__ = __setattr__
    return cls
