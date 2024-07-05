import subprocess
import sys
import argparse
import os
import shutil
import platform
from typing import Any, Dict, List, Union, Optional, Tuple, Callable, Any, Generic, TypeVar, Type
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass, field
import struct
import json
import re
import ast
import astunparse
import astor
import datetime
import json
import logging
import logging.config
import logging.handlers
import operator
import threading
import uuid
from pathlib import Path
from functools import reduce
from dataclasses import dataclass
from logging.config import dictConfig
from typing import Callable, TypeVar, List, Optional, Union, Any, Tuple, Dict, NamedTuple, Set
from threading import Thread, current_thread, Semaphore
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser


lock = threading.Lock()
with lock:
    try:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        # Setup paths
        output_path = Path(__file__).parent / "output"
        output_path.mkdir(parents=True, exist_ok=True)
        # Find the current directory for logging
        current_dir = Path(__file__).resolve().parent
        while not (current_dir / 'logs').exists():
            current_dir = current_dir.parent
            if current_dir == Path('/'):
                break
        # Ensure the logs directory exists
        logs_dir = Path(__file__).resolve().parent.joinpath('logs')
        logs_dir.mkdir(exist_ok=True)
        # Add paths for importing modules
        sys.path.append(str(Path(__file__).resolve().parent))
        sys.path.append(str(Path(__file__).resolve().parent.joinpath('src')))

        T = TypeVar('T')
        for type in ['Atom', 'AtomicData', 'FormalTheory']:
            logging.debug(f"Loading {type}")
            logging.debug("Initial Atom, 'T' is initialized as the core type.")
    except:
        logging.error(f"Error loading {type}")
    finally:
        with lock:
            try:
                from src.utils.kb import KnowledgeItem, FileContextManager
                from src.utils.helpr import helped, wizard
                from src.api.threadsafelocal import ThreadLocalScratchArena, ThreadSafeContextManager, FormalTheory, Atom, AtomicData
                from src.utils.get import ensure_path, get_project_tree, run_command, ensure_delete
            except ImportError as e:
                print(f"Error importing module: {e}")
                sys.exit(1)
# Argument parser
args = argparse.ArgumentParser(description="Hypothesis? Use a simple, terse english statement.")
args.add_argument("case_base", help="Case base? Use a simple, terse english statement.")

class Atom(ABC):
    """
    Abstract Base Class for all Atom types.
    An Atom represents a polymorphic data structure that can encode and decode data,
    execute specific behaviors, and convert its representation.
    """
    @abstractmethod
    def encode(self) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes) -> None:
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def parse_expression(self, expression: str) -> 'AtomicData':
        pass

@dataclass
class AtomicData(Generic[T], Atom):
    """
    Concrete Atom class representing Python runtime objects.
    Attributes:
        value (T): The value of the Atom.
    """
    value: T
    data_type: str = field(init=False)

    # Define a maximum bit length for encoding large integers
    MAX_INT_BIT_LENGTH = 1024  # Adjust this value as needed

    def __post_init__(self):
        self.data_type = self.infer_data_type(self.value)
        logging.debug(f"Initialized AtomicData with value: {self.value} and inferred type: {self.data_type}")

    def infer_data_type(self, value):
        type_map = {
            'str': 'string',
            'int': 'integer',
            'float': 'float',
            'bool': 'boolean',
            'list': 'list',
            'dict': 'dictionary',
            'NoneType': 'none'
        }
        data_type_name = type(value).__name__
        inferred_type = type_map.get(data_type_name, 'unsupported')
        logging.debug(f"Inferred data type: {data_type_name} to {inferred_type}")
        return inferred_type

    def encode(self) -> bytes:
        logging.debug(f"Encoding value: {self.value} of type: {self.data_type}")
        if self.data_type == 'string':
            return self.value.encode('utf-8')
        elif self.data_type == 'integer':
            return self.encode_large_int(self.value)
        elif self.data_type == 'float':
            return struct.pack('f', self.value)
        elif self.data_type == 'boolean':
            return struct.pack('?', self.value)
        elif self.data_type == 'list' or self.data_type == 'dictionary':
            return json.dumps(self.value).encode('utf-8')
        elif self.data_type == 'none':
            return b'none'
        else:
            raise ValueError(f"Unsupported data type: {self.data_type}")

    def encode_large_int(self, value: int) -> bytes:
        logging.debug(f"Encoding large integer value: {value}")
        bit_length = value.bit_length()
        if bit_length > self.MAX_INT_BIT_LENGTH:
            raise OverflowError(f"Integer too large to encode: bit length {bit_length} exceeds MAX_INT_BIT_LENGTH {self.MAX_INT_BIT_LENGTH}")
        if -9223372036854775808 <= value <= 9223372036854775807:
            return struct.pack('q', value)
        else:
            # Use multiple bytes to encode the integer
            value_bytes = value.to_bytes((bit_length + 7) // 8, byteorder='big', signed=True)
            length_bytes = len(value_bytes).to_bytes(1, byteorder='big')  # Store the length in the first byte
            return length_bytes + value_bytes  # Prefix the length of the encoded value

    def decode(self, data: bytes) -> None:
        logging.debug(f"Decoding data for type: {self.data_type}")
        if self.data_type == 'string':
            self.value = data.decode('utf-8')
        elif self.data_type == 'integer':
            self.value = self.decode_large_int(data)
        elif self.data_type == 'float':
            self.value, = struct.unpack('f', data)
        elif self.data_type == 'boolean':
            self.value, = struct.unpack('?', data)
        elif self.data_type == 'list' or self.data_type == 'dictionary':
            self.value = json.loads(data.decode('utf-8'))
        elif self.data_type == 'none':
            self.value = None
        else:
            raise ValueError(f"Unsupported data type: {self.data_type}")
        self.data_type = self.infer_data_type(self.value)
        logging.debug(f"Decoded value: {self.value} to type: {self.data_type}")

    def execute(self, *args, **kwargs) -> Any:
        logging.debug(f"Executing atomic data with value: {self.value}")
        return self.value

    def __repr__(self) -> str:
        return f"AtomicData(value={self.value}, data_type={self.data_type})"

    def parse_expression(self, expression: str) -> 'AtomicData':
        raise NotImplementedError("Expression parsing is not implemented yet.")

# End of AtomicData Class Definition

# Start of FormalTheory Class Definition
@dataclass
class FormalTheory(Generic[T], Atom):
    """
    Concrete Atom class representing formal logical theories.
    Attributes:
        top_atom (AtomicData[T]): Top atomic data.
        bottom_atom (AtomicData[T]): Bottom atomic data.
    """
    top_atom: AtomicData[T]
    bottom_atom: AtomicData[T]
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
        logging.debug(f"Initialized FormalTheory with top_atom: {self.top_atom}, bottom_atom: {self.bottom_atom}")

    def encode(self) -> bytes:
        logging.debug("Encoding FormalTheory")
        encoded_top = self.top_atom.encode()
        encoded_bottom = self.bottom_atom.encode()
        encoded_data = struct.pack(f'{len(encoded_top)}s{len(encoded_bottom)}s', encoded_top, encoded_bottom)
        logging.debug("Encoded FormalTheory to bytes")
        return encoded_data

    def decode(self, data: bytes) -> None:
        logging.debug("Decoding FormalTheory")
        top_length = len(self.top_atom.encode())
        encoded_top, encoded_bottom = struct.unpack(f'{top_length}s{len(data) - top_length}s', data)
        self.top_atom.decode(encoded_top)
        self.bottom_atom.decode(encoded_bottom)
        logging.debug(f"Decoded FormalTheory with top_atom: {self.top_atom}, bottom_atom: {self.bottom_atom}")

    def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Execution of FormalTheory is not implemented yet.")

    def __repr__(self) -> str:
        return f"FormalTheory(top_atom={self.top_atom}, bottom_atom={self.bottom_atom})"

    def parse_expression(self, expression: str) -> 'FormalTheory':
        raise NotImplementedError("Expression parsing for FormalTheory is not implemented yet.")
