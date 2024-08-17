from dataclasses import dataclass, field
from typing import Any, Dict, Callable, Coroutine, List, Optional, Union
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
import uuid
import logging
import ast
import inspect

# Base class for all Atoms to support homoiconism
class Atom:
    def __init__(self, id: str):
        self.id = id

    def encode(self) -> bytes:
        raise NotImplementedError("Must be implemented in subclasses")

    @classmethod
    def decode(cls, data: bytes) -> 'Atom':
        raise NotImplementedError("Must be implemented in subclasses")

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("Must be implemented in subclasses")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Atom':
        raise NotImplementedError("Must be implemented in subclasses")

    def introspect(self) -> str:
        """
        Reflect on its own code structure via AST.
        """
        source = inspect.getsource(self.__class__)
        return ast.dump(ast.parse(source))

@dataclass
class TaskAtom(Atom):  # Tasks are atoms that represent asynchronous potential actions
    task_id: int
    atom: Atom
    args: tuple = field(default_factory=tuple)
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

class ArenaAtom(Atom):  # Arenas are threaded virtual memory Atoms appropriately-scoped when invoked
    def __init__(self, name: str):
        super().__init__(id=name)
        self.name = name
        self.local_data: Dict[str, Any] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
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
        notification_atom = AtomNotification(f"Task {task.task_id} completed")
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

@dataclass
class AtomNotification(Atom):  # nominative async message passing interface
    message: str

    def encode(self) -> bytes:
        return json.dumps({'message': self.message}).encode()

    @classmethod
    def decode(cls, data: bytes) -> 'AtomNotification':
        obj = json.loads(data.decode())
        return cls(message=obj['message'])

class EventBus(Atom):  # Pub/Sub homoiconic event bus
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

@dataclass
class EventAtom(Atom):  # Events are network-friendly Atoms, associates with a type and an id (USER-scoped), think; datagram
    id: str
    type: str
    detail_type: Optional[str] = None
    message: Union[str, List[Dict[str, Any]]] = field(default_factory=list)
    source: Optional[str] = None
    target: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    @classmethod
    def decode(cls, data: bytes) -> 'EventAtom':
        obj = json.loads(data.decode())
        return cls.from_dict(obj)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "detail_type": self.detail_type,
            "message": self.message,
            "source": self.source,
            "target": self.target,
            "content": self.content,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EventAtom':
        return cls(
            id=data["id"],
            type=data["type"],
            detail_type=data.get("detail_type"),
            message=data.get("message"),
            source=data.get("source"),
            target=data.get("target"),
            content=data.get("content"),
            metadata=data.get("metadata", {})
        )

    def validate(self) -> bool:
        required_fields = ['id', 'type']
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"Missing required field: {field}")
        return True

@dataclass
class ActionRequestAtom(Atom):  # User-initiated action request
    action: str
    params: Dict[str, Any]
    self_info: Dict[str, Any]
    echo: Optional[str] = None

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    @classmethod
    def decode(cls, data: bytes) -> 'ActionRequestAtom':
        obj = json.loads(data.decode())
        return cls.from_dict(obj)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "params": self.params,
            "self_info": self.self_info,
            "echo": self.echo
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionRequestAtom':
        return cls(
            action=data["action"],
            params=data["params"],
            self_info=data["self_info"],
            echo=data.get("echo")
        )
