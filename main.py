#!/usr/bin/env python3
import asyncio
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from functools import partial, wraps
from struct import Struct
from typing import Any, Callable, Dict, Generic, List, Type, TypeVar, Union

import runtime


# Set up logger
def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
    return logger


logger = setup_logger("MainLogger")


# Base Model and Field
class BaseModel:
    def dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def json(self) -> str:
        return json.dumps(self.dict())

    @classmethod
    def parse_obj(cls, data: Dict[str, Any]) -> "BaseModel":
        return cls(**data)

    @classmethod
    def parse_json(cls, json_str: str) -> "BaseModel":
        return cls.parse_obj(json.loads(json_str))


class Field:
    def __init__(self, type_: Type, default: Any = None, required: bool = True):
        self.type = type_
        self.default = default
        self.required = required


# Create Model
def create_model(model_name: str, **field_definitions: Field) -> Type[BaseModel]:
    annotations = {name: field.type for name, field in field_definitions.items()}
    defaults = {
        name: field.default
        for name, field in field_definitions.items()
        if not field.required
    }

    def __init__(self, **data):
        for name, field in field_definitions.items():
            value = data.get(name, field.default)
            if field.required and name not in data:
                raise ValueError(f"Field {name} is required")
            if not isinstance(value, field.type):
                raise TypeError(f"Expected {field.type} for {name}, got {type(value)}")
            setattr(self, name, value)

    fields = {"__annotations__": annotations, "__init__": __init__}

    return type(model_name, (BaseModel,), fields)


User = create_model("User", ID=Field(int), name=Field(str))


# Event Bus
class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type: str, handler: Callable[[Any], None]):
        self._subscribers.setdefault(event_type, []).append(handler)

    def unsubscribe(self, event_type: str, handler: Callable[[Any], None]):
        self._subscribers.get(event_type, []).remove(handler)

    def publish(self, event_type: str, data: Any):
        for handler in self._subscribers.get(event_type, []):
            handler(data)


event_bus = EventBus()

# Validation
validate_type = lambda value, expected_type: isinstance(value, expected_type)


class Atom(ABC):
    grammar_rules: List["GrammarRule"] = field(default_factory=list)

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
    def to_dataclass(self) -> "AtomDataclass":
        pass

    @abstractmethod
    def parse_tree(self) -> "ParseTreeAtom":
        pass

    @abstractmethod
    def define_grammar(self) -> None:
        pass


@dataclass
class GrammarRule:
    lhs: str
    rhs: List[Union[str, "GrammarRule"]]

    def __repr__(self):
        return f"{self.lhs} -> {' '.join(map(str, self.rhs))}"


T = TypeVar("T")


@dataclass
class AtomDataclass(Generic[T], Atom):
    value: T
    data_type: str = field(init=False)

    def __post_init__(self):
        type_map = {
            "str": "string",
            "int": "integer",
            "float": "float",
            "bool": "boolean",
            "list": "list",
            "dict": "dictionary",
        }
        self.data_type = type_map.get(type(self.value).__name__, "unsupported")
        self.define_grammar()

    def encode(self) -> bytes:
        return (
            Struct("!I").pack(len(self.data_type.encode("utf-8")))
            + self.data_type.encode("utf-8")
            + self._encode_data()
        )

    def _encode_data(self) -> bytes:
        encoders = {
            "string": lambda x: x.encode("utf-8"),
            "integer": lambda x: Struct("!q").pack(x),
            "float": lambda x: Struct("!d").pack(x),
            "boolean": lambda x: Struct("?").pack(x),
            "list": lambda x: b"".join(AtomDataclass(elem).encode() for elem in x),
            "dictionary": lambda x: b"".join(
                AtomDataclass(k).encode() + AtomDataclass(v).encode()
                for k, v in x.items()
            ),
        }
        return encoders.get(self.data_type, lambda x: b"")(self.value)

    def decode(self, data: bytes) -> None:
        header_length = Struct("!I").unpack(data[:4])[0]
        data_type = data[4 : 4 + header_length].decode("utf-8")
        data_bytes = data[4 + header_length :]

        decoders = {
            "string": lambda x: x.decode("utf-8"),
            "integer": lambda x: Struct("!q").unpack(x)[0],
            "float": lambda x: Struct("!d").unpack(x)[0],
            "boolean": lambda x: Struct("?").unpack(x)[0],
            "list": lambda x: self._decode_list(x),
            "dictionary": lambda x: self._decode_dict(x),
        }

        if data_type in decoders:
            self.value = decoders[data_type](data_bytes)
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

        self.data_type = data_type

    def _decode_list(self, data_bytes: bytes) -> List[Any]:
        value, offset = [], 0
        while offset < len(data_bytes):
            element = AtomDataclass(None)
            element.decode(data_bytes[offset:])
            value.append(element.value)
            offset += len(element.encode())
        return value

    def _decode_dict(self, data_bytes: bytes) -> Dict[Any, Any]:
        value, offset = {}, 0
        while offset < len(data_bytes):
            key = AtomDataclass(None)
            key.decode(data_bytes[offset:])
            offset += len(key.encode())
            val = AtomDataclass(None)
            val.decode(data_bytes[offset:])
            offset += len(val.encode())
            value[key.value] = val.value
        return value

    def execute(self, *args, **kwargs) -> Any:
        pass

    def __repr__(self):
        return f"AtomDataclass(id={id(self)}, value={self.value}, data_type='{self.data_type}')"

    def to_dataclass(self):
        return self

    def parse_tree(self) -> "ParseTreeAtom":
        return ParseTreeAtom(str(self.value))

    def define_grammar(self) -> None:
        rules = {
            "string": [GrammarRule("STRING", ['".*"'])],
            "integer": [GrammarRule("INTEGER", ["-?[0-9]+"])],
            "float": [GrammarRule("FLOAT", ["-?[0-9]*\\.[0-9]+"])],
            "boolean": [GrammarRule("BOOLEAN", ["true", "false"])],
            "list": [GrammarRule("LIST", ["[", "ELEMENTS", "]"])],
            "dictionary": [GrammarRule("DICTIONARY", ["{", "KEY_VALUES", "}"])],
        }
        self.grammar_rules = rules.get(self.data_type, [])


@dataclass
class ParseTreeAtom:
    value: str


async def usermain(failure_threshold=10) -> bool:
    user_logger = setup_logger("UserMainLogger")

    async def do_something() -> bool:
        return True

    try:
        result = await do_something()
        if result:
            user_logger.info("usermain successful, returns True")
            return True
    except Exception as e:
        user_logger.error(f"Failed with error: {e}")
        return False

    failure_count = sum(
        1 for _ in range(failure_threshold) if not await usermain(failure_threshold)
    )
    user_logger.info(f"Failure rate: {failure_count / failure_threshold:.2%}")
    return failure_count < failure_threshold


CurriedUsermain = partial(usermain, failure_threshold=10)


async def main():
    try:
        logger.info("Starting runtime")
        runtime.main()
        await CurriedUsermain()
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        logger.info("Exiting...")


if __name__ == "__main__":
    asyncio.run(main())
