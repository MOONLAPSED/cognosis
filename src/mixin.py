import inspect
import logging
from enum import Enum, auto
from typing import Any, Dict, List, Tuple, Union, Callable, TypeVar, Type
from functools import wraps
import asyncio
import time
import pathlib
"""Type Variables to allow type-checking, linting,.. of Generic...
    "T"((t)ypes and classes),
    "V"((v)ariables and functions),
    "C"((c)allable(reflective functions))"""
T = TypeVar('T', bound=Type)  # type is synonymous for class: T = type(class()) or vice-versa
V = TypeVar('V', bound=Union[int, float, str, bool, list, dict, tuple, set, object, Callable, Enum, Type[Any]])
C = TypeVar('C', bound=Callable[..., Any])  # callable 'T' class/type variable

# Data types
datum = Union[int, float, str, bool, None, List[Any], Tuple[Any, ...]]

class DataType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    NONE = auto()
    LIST = auto()
    TUPLE = auto()

# Logging decorator
def _log(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = await func(*args, **kwargs)
        logging.info(f"Completed {func.__name__} with result: {result}")
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"Completed {func.__name__} with result: {result}")
        return result

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

# Benchmarking decorator
def _bench(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        logging.info(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# Introspection function
def _introspection(obj: Any):
    logging.info(f"Introspecting: {obj.__class__.__name__}")
    for name, value in inspect.getmembers(obj):
        if not name.startswith('_'):
            if inspect.isfunction(value) or inspect.ismethod(value):
                logging.info(f"  Method: {name}")
            elif isinstance(value, property):
                logging.info(f"  Property: {name}")
            else:
                logging.info(f"  Attribute: {name} = {value}")

# Base Model
class BaseModel:
    __slots__ = ('__dict__', '__weakref__')

    def __init__(self, **data):
        for name, value in data.items():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        if name in self.__annotations__:
            expected_type = self.__annotations__[name]
            if not isinstance(value, expected_type):
                raise TypeError(f"Expected {expected_type} for {name}, got {type(value)}")
            
            # Apply validation if defined
            validator = getattr(self.__class__, f'validate_{name}', None)
            if validator:
                validator(self, value)
        
        super().__setattr__(name, value)

    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs)

    def dict(self):
        return {name: getattr(self, name) for name in self.__annotations__}

    def __repr__(self):
        attrs = ', '.join(f"{name}={getattr(self, name)!r}" for name in self.__annotations__)
        return f"{self.__class__.__name__}({attrs})"

# Frozen Model
def frozen(cls):
    original_setattr = cls.__setattr__

    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError(f"Cannot modify frozen attribute '{name}'")
        original_setattr(self, name, value)
    
    cls.__setattr__ = __setattr__
    return cls

# Validator decorator
def validate(validator: Callable[[Any], None]):
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            return validator(value)
        return wrapper
    return decorator

# Generate __all__ dynamically
__all__ = [name for name, obj in globals().items() if inspect.isclass(obj) or inspect.isfunction(obj) and obj.__module__ == __name__]

# Example usage
@frozen
class Runtime(BaseModel):
    name: str
    # Set the root directory to scan
    root_dir = pathlib.Path(__file__).parent.parent

    # Create an array to store the files to load
    files_to_load = []


    @validate(lambda x: x >= 0)
    def _permissions(self, value):
        return value
