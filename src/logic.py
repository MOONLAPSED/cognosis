import logging
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
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Tuple, Generic, Set, Coroutine, Type, ClassVar
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

def setup_logger(name: str, level: int = logging.INFO, handlers: List[logging.Handler] = None):
    if handlers is None:
        handlers = [logging.StreamHandler()]
    logger = logging.getLogger(name)
    logger.setLevel(level)
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
T = TypeVar('T', bound=type) # T for TypeVar, V for ValueVar. Homoicons are T+V.
V = TypeVar('V', bound=Union[int, float, str, bool, list, dict, tuple, set, object, Callable, type])
C = TypeVar('C', bound=Callable[..., Any])  # callable 'T'/'V' first class function interface

class DataType(Enum): # 'T' vars (stdlib)
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    NONE = auto()
    LIST = auto()
    TUPLE = auto()

class AtomType(Enum): # 'C' vars (homoiconic)
    FUNCTION = auto()
    CLASS = auto()
    MODULE = auto()
    OBJECT = auto()

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
    return Atom(data['tag'], data['value'], [decode(child) for child in data['children']], data['metadata'])

class DataType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    NONE = auto()
    LIST = auto()
    TUPLE = auto()

class AtomType(Enum):
    FUNCTION = auto()
    CLASS = auto()
    MODULE = auto()
    OBJECT = auto()

# Decorators
def calloc(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        tracemalloc.stop()
        tracecalloc = tracemalloc.get_traced_memory()
        return result
    return wrapper

def atom(cls: Type[Union[T, V, C]]) -> Type[Union[T, V, C]]:
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

# Encoding and Decoding Functions
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
    return Atom(data['tag'], data['value'], [decode(child) for child in data['children']], data['metadata'])

# Classes for Atom()(s) and Derived Types
@atom
@validate
@dataclass
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
    def encode(self) -> bytes:
        return json.dumps({
            'id': self.id,
            'attributes': self.attributes
        }).encode()
    @classmethod
    def decode(cls, data: bytes) -> 'Atom':
        decoded_data = json.loads(data.decode())
        return cls(id=decoded_data['id'], **decoded_data['attributes'])
    def validate(self) -> bool:
        return True
    def __getitem__(self, key: str) -> Any:
        return self.attributes[key]
    def __setitem__(self, key: str, value: Any) -> None:
        self.attributes[key] = value
    def __delitem__(self, key: str) -> None:
        del self.attributes[key]
    def __contains__(self, key: str) -> bool:
        return key in self.attributes
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, attributes={self.attributes})"
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

class AntiAtom(Atom):
    original_atom: Atom
    def encode(self) -> bytes:
        return b'anti_' + self.original_atom.encode()
    def execute(self, *args, **kwargs) -> Any:
        return not self.original_atom.execute(*args, **kwargs)

class LiteralAtom(Atom):
    def __init__(self, tag: str, children: List[Atom]):
        super().__init__(tag=tag, children=children)
    async def evaluate(self) -> Any:
        if self.tag == 'add':
            results = await asyncio.gather(*(child.evaluate() for child in self.children))
            return sum(results)
        elif self.tag == 'negate':
            return -await self.children[0].evaluate()
        else:
            raise NotImplementedError(f"Evaluation not implemented for tag: {self.tag}")

class ExternalRefAtom(Atom):
    async def evaluate(self):
        if "external_ref" in self.metadata:
            return self.metadata["external_ref"].resolve()
        return None
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
class AtomicData(Atom, ABC):
    def __init__(self, *atoms: Atom):
        super().__init__(tag='atomic_data')
        self.atoms = atoms
        self.data: Dict[str, Any] = {}
        self._extract_data()
    def _extract_data(self):
        for atom in self.atoms:
            self.data.update(atom.get_attributes())
    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__annotations__:
            expected_type = self.__annotations__[name]
            if not isinstance(value, expected_type):
                raise TypeError(f"Expected {expected_type} for {name}, got {type(value)}")
            validator = getattr(self.__class__, f'validate_{name}', None)
            if validator:
                validator(self, value)
        super().__setattr__(name, value)
    def get_attributes(self) -> Dict[str, Any]:
        return self.data
    def __repr__(self) -> str:
        return f"AtomicData(data={self.data})"
    def validate(self) -> bool:
        for key, value in self.data.items():
            if not isinstance(value, (int, float, str, bool, list, dict, tuple, set, Callable, type)):
                logging.error(f"Invalid type for {key}: {type(value)}")
                return False
        return True
class AtomicTheory(AtomicData):
    logic_rules: Dict[str, Callable[[Any], bool]] = field(default_factory=dict)
    local_data: Dict[str, Any] = field(default_factory=dict)
    task_queue: AsyncQueue = field(default_factory=AsyncQueue)
    running: bool = False
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
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
    def validate(self) -> bool:
        if not super().validate():
            return False
        for rule_name, rule in self.logic_rules.items():
            if not rule(self.data):
                logging.error(f"Logic rule '{rule_name}' failed for data {self.data}")
                return False
        return True
    def add_rule(self, rule_name: str, rule: Callable[[Any], bool]):
        self.logic_rules[rule_name] = rule
    def transform(self, transformer: Callable[[Any], Any]) -> None:
        self.data = transformer(self.data)
class TaskAtom(Atom): # Tasks are atoms that represent asynchronous potential actions
    task_id: int
    atom: Atom
    args: Tuple = field(default_factory=tuple)
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
class ArenaAtom(Atom):  # Arenas are threaded virtual memory Atoms appropriatly-scoped when invoked
    def __init__(self, name: str):
        super().__init__(id=name)
        self.name = name
        self.local_data: Dict[str, Any] = {}
        self.task_queue: Queue = Queue()
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
        notification_atom = AtomNotification(message=f"Task {task.task_id} completed")
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
class AtomNotification(Atom):
    message: str
    def encode(self) -> bytes:
        return json.dumps({'message': self.message}).encode()
    @classmethod
    def decode(cls, data: bytes) -> 'AtomNotification':
        obj = json.loads(data.decode())
        return cls(message=obj['message'])
class EventBus(Atom):
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
class Hypothesis(Atom):
    name: str
    logic: Callable[[Any], bool]
    experiment: Callable[[Any], Dict[str, Any]]
    def encode(self) -> bytes:
        data = {
            'name': self.name
        }
        return json.dumps(data).encode()
    @classmethod
    def decode(cls, data: bytes) -> 'Hypothesis':
        decoded_data = json.loads(data.decode())
        return cls(name=decoded_data['name'], logic=None, experiment=None)  # set actual logic and experiment callables
    async def __call__(self, input_data: Any) -> Any:
        return self.test(input_data)
    async def entangle(self, other: 'Hypothesis') -> 'Hypothesis':
        combined_name = self.name + "&" + other.name
        combined_logic = lambda input_data: self.logic(input_data) and other.logic(input_data)
        combined_experiment = lambda input_data: {**self.experiment(input_data), **other.experiment(input_data)}
        return Hypothesis(combined_name, combined_logic, combined_experiment)
    def test(self, input_data: Any) -> bool:
        return self.logic(input_data)
    def execute(self, input_data: Any) -> Any:
        return self.experiment(input_data)
    def __repr__(self) -> str:
        return f"Hypothesis(name={self.name})"
class AtomicElement(Atom, Generic[T]): # Generic runtime USER-scoped Atom()
    value: T
    data_type: str = field(init=False)
    MAX_INT_BIT_LENGTH = 1024
    def __post_init__(self):
        self.data_type = self.infer_data_type(self.value)
        logging.debug(f"Initialized AtomicElement with value: {self.value} and inferred type: {self.data_type}")
    def infer_data_type(self, value: T) -> str:
        type_map = {
            str: 'string',
            int: 'integer',
            float: 'float',
            bool: 'boolean',
            list: 'list',
            dict: 'dictionary',
            type(None): 'none'
        }
        inferred_type = type_map.get(type(value), 'unsupported')
        logging.debug(f"Inferred data type: {inferred_type}")
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
        elif self.data_type in ('list', 'dictionary'):
            return json.dumps(self.value).encode('utf-8')
        elif self.data_type == 'none':
            return b'none'
        else:
            raise ValueError(f"Unsupported data type: {self.data_type}")
    def encode_large_int(self, value: int) -> bytes:
        bit_length = value.bit_length()
        if bit_length > self.MAX_INT_BIT_LENGTH:
            raise OverflowError(f"Integer too large to encode: bit length {bit_length} exceeds MAX_INT_BIT_LENGTH {self.MAX_INT_BIT_LENGTH}")
        return value.to_bytes((bit_length + 7) // 8, byteorder='big', signed=True)
    def decode(self, data: bytes) -> None:
        logging.debug(f"Decoding data for type: {self.data_type}")
        if self.data_type == 'string':
            self.value = data.decode('utf-8')
        elif self.data_type == 'integer':
            self.value = self.decode_large_int(data)
        elif self.data_type == 'float':
            self.value = struct.unpack('f', data)[0]
        elif self.data_type == 'boolean':
            self.value = struct.unpack('?', data)[0]
        elif self.data_type in ('list', 'dictionary'):
            self.value = json.loads(data.decode('utf-8'))
        elif self.data_type == 'none':
            self.value = None
        else:
            raise ValueError(f"Unsupported data type: {self.data_type}")
        self.data_type = self.infer_data_type(self.value)
        logging.debug(f"Decoded value: {self.value} to type: {self.data_type}")
    def decode_large_int(self, data: bytes) -> int:
        return int.from_bytes(data, byteorder='big', signed=True)
# Model creation and runtime initialization functions
def create_model_from_file(file_path: pathlib.Path) -> Tuple[Optional[str], Optional[FileAtom]]:
    """Create a FileModel instance from a file."""
    try:
        with file_path.open('r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        model_name = file_path.stem.capitalize() + 'Model'
        model_class = type(model_name, (FileAtom,), {})
        instance = model_class(file_path=file_path, file_content=content)
        logging.info(f"Created {model_name} from {file_path}")
        return model_name, instance
    except Exception as e:
        logging.error(f"Failed to create model from {file_path}: {e}")
        return None, None
def load_files_as_models(root_dir: pathlib.Path, file_extensions: List[str]) -> Dict[str, Atom]:
    """Load files from a directory and create models."""
    models = {}
    for file_path in root_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix in file_extensions:
            model_name, instance = create_model_from_file(file_path)
            if model_name and instance:
                models[model_name] = instance
                sys.modules[model_name] = instance
    return models
def register_models(models: Dict[str, Atom]) -> None:
    """Register models in the global namespace."""
    for model_name, instance in models.items():
        globals()[model_name] = instance
        logging.info(f"Registered {model_name} in the global namespace")
def runtime(root_dir: pathlib.Path) -> None:
    """Initialize the runtime environment."""
    file_models = load_files_as_models(root_dir, ['.md', '.txt'])
    register_models(file_models)