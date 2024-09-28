#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import importlib
import pathlib
import asyncio
import argparse
import uuid
import json
import struct
import time
import hashlib
import pickle
import dis
import inspect
import threading
import logging
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
tracemalloc.start()
IS_POSIX = os.name == 'posix'
IS_WINDOWS = not IS_POSIX  # Assume Windows if WSL is not detected
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
def setupLogger(
    name: str, 
    level: int = logging.INFO, 
    log_file: Optional[str] = None, 
    handlers: Optional[List[logging.Handler]] = None
) -> logging.Logger:
    """
    Setup and return a logger with a custom name and configuration.
    
    Arguments:
    name -- the name of the logger
    level -- logging level (default INFO)
    log_file -- path to the log file (default None)
    handlers -- list of logging handlers (default to console stream handler)
    
    Returns:
    Configured logger instance
    """
    if handlers is None:
        handlers = [logging.StreamHandler()]
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Clear any previous handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()
    for handler in handlers:
        handler.setLevel(level)
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)
    return logger
# Typing ----------------------------------------------------------
"""Homoiconism dictates that, upon runtime validation, all objects are code and data.
To fascilitate; we utilize first class functions and a static typing system."""
T = TypeVar('T', bound=any) # T for TypeVar, V for ValueVar. Homoicons are T+V.
V = TypeVar('V', bound=Union[int, float, str, bool, list, dict, tuple, set, object, Callable, type])
C = TypeVar('C', bound=Callable[..., Any])  # callable 'T'/'V' first class function interface
DataType = Enum('DataType', 'INTEGER FLOAT STRING BOOLEAN NONE LIST TUPLE') # 'T' vars (stdlib)
AtomType = Enum('AtomType', 'FUNCTION CLASS MODULE OBJECT') # 'C' vars (homoiconic methods or classes)
class Atom(Generic[T, V, C]):
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
    def __getitem__(self, key):
        return self.value[key]
    def __setitem__(self, key, value):
        self.value[key] = value
    def __delitem__(self, key):
        del self.value[key]
    def __len__(self):
        return len(self.value)
    def __iter__(self):
        return iter(self.value)
    def __contains__(self, item):
        return item in self.value
    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)
    def __add__(self, other):
        return self.value + other
    def __sub__(self, other):
        return self.value - other
    def __mul__(self, other):
        return self.value * other
    def __truediv__(self, other):
        return self.value / other
    def __floordiv__(self, other):
        return self.value // other
    def get_memory_view(atom: Atom) -> memoryview:
        if isinstance(atom.value, (bytes, bytearray)):
            return memoryview(atom.value)
        raise TypeError("Unsupported type for memoryview")