import array
import weakref
import uuid
from typing import Any, Dict, Type, TypeVar, get_type_hints, Optional, Union, List
import inspect

T = TypeVar('T', bound='RuntimeAtom')

class Atom:
    __slots__ = ('_id', '_value', '_type', '_links', '_metadata')

    def __init__(self, value: Any = None, atom_type: str = 'generic'):
        self._id = str(uuid.uuid4())
        self._value = value
        self._type = atom_type
        self._links = weakref.WeakSet()
        self._metadata = {}

    @property
    def id(self) -> str:
        return self._id

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, new_value: Any):
        self._value = new_value

    @property
    def type(self) -> str:
        return self._type

    def link(self, other: 'Atom'):
        self._links.add(other)
        other._links.add(self)

    def unlink(self, other: 'Atom'):
        self._links.discard(other)
        other._links.discard(self)

    def get_links(self) -> List['Atom']:
        return list(self._links)

    def set_metadata(self, key: str, value: Any):
        self._metadata[key] = value

    def get_metadata(self, key: str) -> Any:
        return self._metadata.get(key)

    def __repr__(self):
        return f"Atom(id={self._id}, type={self._type}, value={self._value})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self._id,
            'type': self._type,
            'value': self._value,
            'metadata': self._metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Atom':
        atom = cls(value=data['value'], atom_type=data['type'])
        atom._id = data['id']
        atom._metadata = data.get('metadata', {})
        return atom

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Atom):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

class AtomicMemory:
    def __init__(self, size: int = 1024):
        self._memory = array.array('Q', [0] * size)
        self._free_list = [(0, size)]

    def allocate(self, size: int) -> Optional[int]:
        for i, (start, length) in enumerate(self._free_list):
            if length >= size:
                if length > size:
                    self._free_list[i] = (start + size, length - size)
                else:
                    del self._free_list[i]
                return start
        return None

    def deallocate(self, start: int, size: int):
        self._free_list.append((start, size))
        self._free_list.sort(key=lambda x: x[0])
        self._merge_free_blocks()

    def _merge_free_blocks(self):
        i = 0
        while i < len(self._free_list) - 1:
            current_start, current_size = self._free_list[i]
            next_start, next_size = self._free_list[i + 1]
            if current_start + current_size == next_start:
                self._free_list[i] = (current_start, current_size + next_size)
                del self._free_list[i + 1]
            else:
                i += 1

    def read(self, start: int, size: int) -> array.array:
        return self._memory[start:start+size]

    def write(self, start: int, data: array.array):
        self._memory[start:start+len(data)] = data

class AtomicArena:
    def __init__(self, memory_size: int = 1024 * 1024):
        self._memory = AtomicMemory(memory_size)
        self._atom_locations: Dict[str, Tuple[int, int]] = {}

    def store_atom(self, atom: Atom) -> bool:
        data = array.array('Q', atom.to_dict().values())
        size = len(data)
        start = self._memory.allocate(size)
        if start is not None:
            self._memory.write(start, data)
            self._atom_locations[atom.id] = (start, size)
            return True
        return False

    def retrieve_atom(self, atom_id: str) -> Optional[Atom]:
        if atom_id in self._atom_locations:
            start, size = self._atom_locations[atom_id]
            data = self._memory.read(start, size)
            return Atom.from_dict(dict(zip(Atom.to_dict(Atom()).keys(), data)))
        return None

    def remove_atom(self, atom_id: str) -> bool:
        if atom_id in self._atom_locations:
            start, size = self._atom_locations[atom_id]
            self._memory.deallocate(start, size)
            del self._atom_locations[atom_id]
            return True
        return False

class RuntimeAtom:
    def __init__(self, **data):
        self._atom = Atom(value=data, atom_type=self.__class__.__name__)
        self._initialize_fields(data)

    def _initialize_fields(self, data: Dict[str, Any]):
        annotations = get_type_hints(self.__class__)
        for name, field_type in annotations.items():
            if name in data:
                setattr(self, name, data[name])
            elif hasattr(self.__class__, name):
                default_value = getattr(self.__class__, name)
                if inspect.isfunction(default_value):
                    setattr(self, name, default_value())
                else:
                    setattr(self, name, default_value)
            else:
                raise ValueError(f"Missing required field: {name}")

    @classmethod
    def from_atom(cls: Type[T], atom: Atom) -> T:
        if not isinstance(atom.value, dict):
            raise ValueError("Atom value must be a dictionary")
        return cls(**atom.value)

    def to_atom(self) -> Atom:
        return self._atom

    def dict(self) -> Dict[str, Any]:
        return {name: getattr(self, name) for name in get_type_hints(self.__class__)}

    def __repr__(self):
        attrs = ', '.join(f"{k}={v!r}" for k, v in self.dict().items())
        return f"{self.__class__.__name__}({attrs})"

# Example usage:
class UserAtom(RuntimeAtom):
    name: str
    age: int
    email: str = "default@example.com"

# Create a UserAtom instance
user = UserAtom(name="Alice", age=30)
print(user)  # UserAtom(name='Alice', age=30, email='default@example.com')

# Convert to base Atom
base_atom = user.to_atom()
print(base_atom)  # Atom(id=..., type='UserAtom', value={'name': 'Alice', 'age': 30, 'email': 'default@example.com'})

# Create UserAtom from base Atom
recovered_user = UserAtom.from_atom(base_atom)
print(recovered_user)  # UserAtom(name='Alice', age=30, email='default@example.com')