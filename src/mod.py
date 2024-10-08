import json
import struct
import json
import logging
import struct
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, List, Optional
from typing import Generic, TypeVar, Tuple, Type

# Generic typing
T = TypeVar('T')
# --- NEW AtomicData class to replace the old #
P = TypeVar('P')
class BaseModel:
    def dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def parse_obj(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls(**data)

    @classmethod
    def parse_json(cls: Type[T], json_str: str) -> T:
        return cls.parse_obj(json.loads(json_str))

# Define custom Field for dynamic models
class Field:
    def __init__(self, type_: Type, default: Any = None, required: bool = True):
        self.type = type_
        self.default = default
        self.required = required

def create_model(name: str, **field_definitions: Field) -> Type[BaseModel]:
    fields = {}
    annotations = {}
    defaults = {}

    for field_name, field in field_definitions.items():
        annotations[field_name] = field.type
        if not field.required:
            defaults[field_name] = field.default

    def __init__(self, **data):
        for field_name, field in field_definitions.items():
            if field.required and field_name not in data:
                raise ValueError(f"Field {field_name} is required")
            value = data.get(field_name, field.default)
            if not isinstance(value, field.type):
                raise TypeError(f"Expected {field.type} for {field_name}, got {type(value)}")
            setattr(self, field_name, value)

    fields['__annotations__'] = annotations
    fields['__init__'] = __init__

    return type(name, (BaseModel,), fields)