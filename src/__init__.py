# src/__init__.py

import sys
import importlib
from importlib.util import module_from_spec
import pathlib

try:
    mixins = []
    for path in pathlib.Path(__file__).parent.glob("*.py"):
        if path.name.startswith("_"):
            continue
        module_name = path.stem
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        mixins.append(module)
except Exception as e:
    print(f"Error importing internal modules: {e}")
    sys.exit(1)

if mixins:
    __all__ = [mixin.__name__ for mixin in mixins]
else:
    __all__ = []

import asyncio
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import contextmanager
import json
import logging
import struct
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Generic, TypeVar
import threading
import queue
import time
import pathlib
import sys
import importlib.util

# Explicitly define what is exposed when the package is imported
__all__ = [
    "asyncio", "Future", "ThreadPoolExecutor", "contextmanager", "json", "logging", 
    "struct", "ABC", "abstractmethod", "dataclass", "field", "wraps", "Any", 
    "Callable", "Dict", "List", "Optional", "Generic", "TypeVar", "threading", 
    "queue", "time", "pathlib", "importlib"
]

# Import internal modules and submodules
try:
    from .app.llama import *
    from .app.kernel import *
except ModuleNotFoundError as e:
    print(f"Error importing internal modules: {e}")
    sys.exit(1)

__all__.extend([
    # Add the names of the imported symbols from the internal modules here
])

# Set the root directory to scan
root_dir = pathlib.Path(__file__).parent.parent

# Create an array to store the files to load
files_to_load = []

# Recursively traverse the directory tree and collect files
for file in root_dir.rglob('*'):
    if file.is_file():
        # Store the file path and contents in the array
        files_to_load.append((file, file.read_text()))

# Create a module for each file
for file_path, file_contents in files_to_load:
    # Create a module name based on the file name
    module_name = file_path.stem

    # Use importlib to load the contents into the namespace as a module
    spec = module_from_spec(importlib.util.Loader(file_path))
    module = sys.modules[module_name] = spec.load_module()

"""This code uses `pathlib` to recursively traverse the directory tree, collects files in an array, and then creates
a module for each file using `importlib`. The contents of each file are loaded into the namespace as a module."""
