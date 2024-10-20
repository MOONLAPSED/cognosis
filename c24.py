import ctypes
import uuid
from typing import Any, Dict, Optional, List, TypeVar, Type
import weakref

class AtomicMemory:
    def __init__(self, size: int = 1024):
        self.memory = (ctypes.c_ubyte * size)()
        self.size = size
        self.free_list = [(0, size)]

    def allocate(self, size: int) -> Optional[int]:
        for i, (start, length) in enumerate(self.free_list):
            if length >= size:
                if length > size:
                    self.free_list[i] = (start + size, length - size)
                else:
                    del self.free_list[i]
                return start
        return None

    def deallocate(self, start: int, size: int):
        self.free_list.append((start, size))
        self.free_list.sort(key=lambda x: x[0])
        self._merge_free_blocks()

    def _merge_free_blocks(self):
        i = 0
        while i < len(self.free_list) - 1:
            current_start, current_size = self.free_list[i]
            next_start, next_size = self.free_list[i + 1]
            if current_start + current_size == next_start:
                self.free_list[i] = (current_start, current_size + next_size)
                del self.free_list[i + 1]
            else:
                i += 1

    def read(self, start: int, size: int) -> bytes:
        return bytes(self.memory[start:start+size])

    def write(self, start: int, data: bytes):
        self.memory[start:start+len(data)] = data

class Atom:
    def __init__(self, value: Any = None, atom_type: str = 'generic'):
        self.id = str(uuid.uuid4())
        self.value = value
        self.type = atom_type
        self.links = weakref.WeakSet()
        self.metadata = {}

    def link(self, other: 'Atom'):
        self.links.add(other)
        other.links.add(self)

    def unlink(self, other: 'Atom'):
        self.links.discard(other)
        other.links.discard(self)

    def get_links(self) -> List['Atom']:
        return list(self.links)

    def set_metadata(self, key: str, value: Any):
        self.metadata[key] = value

    def get_metadata(self, key: str) -> Any:
        return self.metadata.get(key)

    def __repr__(self):
        return f"Atom(id={self.id}, type={self.type}, value={self.value})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type': self.type,
            'value': self.value,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Atom':
        atom = cls(value=data['value'], atom_type=data['type'])
        atom.id = data['id']
        atom.metadata = data.get('metadata', {})
        return atom

class AtomicArena:
    def __init__(self, memory_size: int = 1024 * 1024):
        self.memory = AtomicMemory(memory_size)
        self.atom_locations: Dict[str, tuple[int, int]] = {}

    def store_atom(self, atom: Atom) -> bool:
        data = str(atom.to_dict()).encode()  # Change this line
        size = len(data)
        start = self.memory.allocate(size)
        if start is not None:
            self.memory.write(start, data)
            self.atom_locations[atom.id] = (start, size)
            return True
        return False

    def retrieve_atom(self, atom_id: str) -> Optional[Atom]:
        if atom_id in self.atom_locations:
            start, size = self.atom_locations[atom_id]
            data = self.memory.read(start, size)
            return Atom.from_dict(eval(data.decode()))
        return None

    def remove_atom(self, atom_id: str) -> bool:
        if atom_id in self.atom_locations:
            start, size = self.atom_locations[atom_id]
            self.memory.deallocate(start, size)
            del self.atom_locations[atom_id]
            return True
        return False

T = TypeVar('T', bound='RuntimeAtom')

class RuntimeAtom:
    def __init__(self, **data):
        self._atom = Atom(value=data, atom_type=self.__class__.__name__)
        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def from_atom(cls: Type[T], atom: Atom) -> T:
        if not isinstance(atom.value, dict):
            raise ValueError("Atom value must be a dictionary")
        return cls(**atom.value)

    def to_atom(self) -> Atom:
        return self._atom

    def dict(self) -> Dict[str, Any]:
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}

    def __repr__(self):
        attrs = ', '.join(f"{k}={v!r}" for k, v in self.dict().items())
        return f"{self.__class__.__name__}({attrs})"

# Example usage
class UserAtom(RuntimeAtom):
    def __init__(self, name: str, age: int, email: str = "default@example.com"):
        super().__init__(name=name, age=age, email=email)

# Create an AtomicArena
arena = AtomicArena()

# Create and store a UserAtom
user = UserAtom(name="Alice", age=30)
arena.store_atom(user.to_atom())

# Retrieve the UserAtom
retrieved_atom = arena.retrieve_atom(user.to_atom().id)
if retrieved_atom:
    retrieved_user = UserAtom.from_atom(retrieved_atom)
    print(retrieved_user)  # UserAtom(name='Alice', age=30, email='default@example.com')

# Remove the UserAtom
arena.remove_atom(user.to_atom().id)