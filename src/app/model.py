import asyncio
import logging
import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')
class Atom(ABC):
    @abstractmethod
    def encode(self) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes) -> None:
        pass

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        pass

@dataclass
class Event(Atom):
    id: str
    type: str
    detail_type: str
    message: List[Dict[str, Any]]

    def validate(self) -> bool:
        return all([
            isinstance(self.id, str),
            isinstance(self.type, str),
            isinstance(self.detail_type, str),
            isinstance(self.message, list)
        ])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "detail_type": self.detail_type,
            "message": self.message
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        return cls(
            id=data["id"],
            type=data["type"],
            detail_type=data["detail_type"],
            message=data["message"]
        )

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    def decode(self, data: bytes) -> None:
        obj = json.loads(data.decode())
        self.id = obj['id']
        self.type = obj['type']
        self.detail_type = obj['detail_type']
        self.message = obj['message']

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        # ...
        pass

@dataclass
class ActionRequest(Atom):
    action: str
    params: Dict[str, Any]
    self_info: Dict[str, Any]

    def validate(self) -> bool:
        return all([
            isinstance(self.action, str),
            isinstance(self.params, dict),
            isinstance(self.self_info, dict)
        ])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "params": self.params,
            "self": self.self_info
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionRequest':
        return cls(
            action=data["action"],
            params=data["params"],
            self_info=data["self"]
        )

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    def decode(self, data: bytes) -> None:
        obj = json.loads(data.decode())
        self.action = obj['action']
        self.params = obj['params']
        self.self_info = obj['self']

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        # ...
        pass

@dataclass
class ActionResponse(Atom):
    status: str
    retcode: int
    data: Dict[str, Any]
    message: str = ""

    def validate(self) -> bool:
        return all([
            isinstance(self.status, str),
            isinstance(self.retcode, int),
            isinstance(self.data, dict),
            isinstance(self.message, str)
        ])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "retcode": self.retcode,
            "data": self.data,
            "message": self.message
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionResponse':
        return cls(
            status=data["status"],
            retcode=data["retcode"],
            data=data["data"],
            message=data.get("message", "")
        )

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    def decode(self, data: bytes) -> None:
        obj = json.loads(data.decode())
        self.status = obj['status']
        self.retcode = obj['retcode']
        self.data = obj['data']
        self.message = obj['message']

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        # TODO: expose this to the user
        if self.status == "success":
            return self.data
        else:
            raise Exception(self.message)
        pass


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Any], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable[[Any], None]):
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(handler)

    def publish(self, event_type: str, data: Any):
        for handler in self._subscribers.get(event_type, []):
            handler(data)

