import json
import logging
import struct
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Generic, TypeVar

# Define typing variables
T = TypeVar('T')

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define validation and logging decorators
def validate_atom(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> T:
        if not self.validate():
            raise ValueError(f"Invalid {self.__class__.__name__} object")
        return func(self, *args, **kwargs)
    return wrapper

def log_execution(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        logging.info(f"Executing {func.__name__} with args: {args} and kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"{func.__name__} executed successfully")
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

# Base Atom Class
class Atom(ABC):
    def __init__(self, metadata: Optional[Dict[str, Any]] = None):
        self.metadata = metadata or {}

    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value
        
    def get_metadata(self, key: str) -> Optional[Any]:
        return self.metadata.get(key)

    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def encode(self) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes) -> None:
        pass

    @abstractmethod
    @log_execution
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Atom':
        return cls(metadata=data.get("metadata", {}))

@dataclass
class Token(Atom):
    def __init__(self, value: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(metadata)
        self.value = value

    def validate(self) -> bool:
        return isinstance(self.value, str) and isinstance(self.metadata, dict)

    @validate_atom
    def encode(self) -> bytes:
        data = {
            'type': 'token',
            'value': self.value,
            'metadata': self.metadata
        }
        json_data = json.dumps(data)
        return struct.pack('>I', len(json_data)) + json_data.encode()

    @validate_atom
    def decode(self, data: bytes) -> None:
        size = struct.unpack('>I', data[:4])[0]
        json_data = data[4:4+size].decode()
        parsed_data = json.loads(json_data)
        self.value = parsed_data.get('value', '')
        self.metadata = parsed_data.get('metadata', {})

    @validate_atom
    @log_execution
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return self.value

@dataclass
class Event(Atom):
    id: str
    type: str
    detail_type: str
    message: List[Dict[str, Any]]

    def __init__(self, id: str, type: str, detail_type: str, message: List[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None):
        super().__init__(metadata)
        self.id = id
        self.type = type
        self.detail_type = detail_type
        self.message = message

    def validate(self) -> bool:
        return all([
            isinstance(self.id, str),
            isinstance(self.type, str),
            isinstance(self.detail_type, str),
            isinstance(self.message, list)
        ])

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "id": self.id,
            "type": self.type,
            "detail_type": self.detail_type,
            "message": self.message
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        return cls(
            id=data["id"],
            type=data["type"],
            detail_type=data["detail_type"],
            message=data["message"],
            metadata=data.get("metadata", {})
        )

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    def decode(self, data: bytes) -> None:
        obj = json.loads(data.decode())
        self.id = obj['id']
        self.type = obj['type']
        self.detail_type = obj['detail_type']
        self.message = obj['message']
        self.metadata = obj.get('metadata', {})

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        logging.info(f"Executing event: {self.id}")
        # Implement necessary functionality here

@dataclass
class ActionRequest(Atom):
    action: str
    params: Dict[str, Any]
    self_info: Dict[str, Any]

    def __init__(self, action: str, params: Dict[str, Any], self_info: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None):
        super().__init__(metadata)
        self.action = action
        self.params = params
        self.self_info = self_info

    def validate(self) -> bool:
        return all([
            isinstance(self.action, str),
            isinstance(self.params, dict),
            isinstance(self.self_info, dict)
        ])

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "action": self.action,
            "params": self.params,
            "self_info": self.self_info
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionRequest':
        return cls(
            action=data["action"],
            params=data["params"],
            self_info=data["self_info"],
            metadata=data.get("metadata", {})
        )

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    def decode(self, data: bytes) -> None:
        obj = json.loads(data.decode())
        self.action = obj['action']
        self.params = obj['params']
        self.self_info = obj['self_info']
        self.metadata = obj.get('metadata', {})

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        logging.info(f"Executing action: {self.action}")
        # Implement action-related functionality here

@dataclass
class ActionResponse(Atom):
    status: str
    retcode: int
    data: Dict[str, Any]
    message: str = ""

    def __init__(self, status: str, retcode: int, data: Dict[str, Any], message: str = "", metadata: Optional[Dict[str, Any]] = None):
        super().__init__(metadata)
        self.status = status
        self.retcode = retcode
        self.data = data
        self.message = message

    def validate(self) -> bool:
        return all([
            isinstance(self.status, str),
            isinstance(self.retcode, int),
            isinstance(self.data, dict),
            isinstance(self.message, str)
        ])

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "status": self.status,
            "retcode": self.retcode,
            "data": self.data,
            "message": self.message
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionResponse':
        return cls(
            status=data["status"],
            retcode=data["retcode"],
            data=data["data"],
            message=data.get("message", ""),
            metadata=data.get("metadata", {})
        )

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    def decode(self, data: bytes) -> None:
        obj = json.loads(data.decode())
        self.status = obj['status']
        self.retcode = obj['retcode']
        self.data = obj['data']
        self.message = obj['message']
        self.metadata = obj.get('metadata', {})

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        logging.info(f"Executing response with status: {self.status}")
        if self.status == "success":
            return self.data
        else:
            raise Exception(self.message)

@dataclass
class MultiDimensionalAtom(Atom):
    dimensions: List[Atom] = field(default_factory=list)

    def add_dimension(self, atom: Atom):
        self.dimensions.append(atom)
    
    def validate(self) -> bool:
        if not all(isinstance(atom, Atom) for atom in self.dimensions):
            logging.error("Invalid Atom in dimensions")
            return False
        return True

    @validate_atom
    def encode(self) -> bytes:
        encoded_dims = [atom.encode() for atom in self.dimensions]
        lengths = struct.pack(f'>{len(encoded_dims)}I', *map(len, encoded_dims))
        return struct.pack('>I', len(encoded_dims)) + lengths + b''.join(encoded_dims)

    @validate_atom
    def decode(self, data: bytes) -> None:
        num_dims = struct.unpack('>I', data[:4])[0]
        lengths = struct.unpack(f'>{num_dims}I', data[4:4 + 4 * num_dims])
        offset = 4 + 4 * num_dims
        self.dimensions = []
        for length in lengths:
            atom_data = data[offset:offset + length]
            atom = Token()  # Initialize as Token by default, can be replaced dynamically
            atom.decode(atom_data)
            self.dimensions.append(atom)
            offset += length

    @validate_atom
    @log_execution
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return [atom.execute(*args, **kwargs) for atom in self.dimensions]
