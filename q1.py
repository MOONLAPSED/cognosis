import ctypes
import uuid
import weakref
from typing import Any, Dict, List, Optional, Union, get_type_hints
import inspect


class Atom:
    __slots__ = ('_id', '_value', '_type', '_metadata', '_children', '_parent')

    def __init__(self, value: Any = None, atom_type: str = 'generic', metadata: Dict[str, Any] = None):
        self._id = str(uuid.uuid4())
        self._value = value
        self._type = atom_type
        self._metadata = metadata or {}
        self._children: List[weakref.ref] = []
        self._parent: Optional[weakref.ref] = None

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

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    def add_child(self, child: 'Atom'):
        self._children.append(weakref.ref(child))
        child._parent = weakref.ref(self)

    def remove_child(self, child: 'Atom'):
        self._children = [c for c in self._children if c() is not child]
        child._parent = None

    @property
    def children(self) -> List['Atom']:
        return [child() for child in self._children if child() is not None]

    @property
    def parent(self) -> Optional['Atom']:
        return self._parent() if self._parent is not None else None

    def __repr__(self):
        return f"Atom(id={self._id}, type={self._type}, value={self._value})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self._id,
            'type': self._type,
            'value': self._value,
            'metadata': self._metadata,
            'children': [child().id for child in self._children if child() is not None]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Atom':
        atom = cls(value=data['value'], atom_type=data['type'], metadata=data['metadata'])
        atom._id = data['id']
        return atom

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Atom):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

class AtomArray:
    def __init__(self, size: int):
        self._size = size
        self._array = (ctypes.py_object * size)()
        self._count = 0

    def append(self, atom: Atom):
        if self._count < self._size:
            self._array[self._count] = atom
            self._count += 1
        else:
            raise IndexError("AtomArray is full")

    def __getitem__(self, index: int) -> Atom:
        if 0 <= index < self._count:
            return self._array[index]
        raise IndexError("AtomArray index out of range")

    def __len__(self) -> int:
        return self._count

class AtomLinkedList:
    class Node:
        __slots__ = ('atom', 'next')
        def __init__(self, atom: Atom):
            self.atom = atom
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None
        self._count = 0

    def append(self, atom: Atom):
        new_node = self.Node(atom)
        if self.tail:
            self.tail.next = new_node
        else:
            self.head = new_node
        self.tail = new_node
        self._count += 1

    def __iter__(self):
        current = self.head
        while current:
            yield current.atom
            current = current.next

    def __len__(self):
        return self._count

class AtomArena:
    def __init__(self, size: int):
        self._array = AtomArray(size)
        self._linked_list = AtomLinkedList()

    def allocate(self, atom: Atom):
        try:
            self._array.append(atom)
        except IndexError:
            self._linked_list.append(atom)

    def __iter__(self):
        yield from self._array
        yield from self._linked_list

    def __len__(self):
        return len(self._array) + len(self._linked_list)


class DataclassAtom(Atom):
    def __init__(self, **kwargs):
        super().__init__(value=kwargs, atom_type='dataclass')
        self._fields = {}
        annotations = get_type_hints(self.__class__)
        
        for field_name, field_type in annotations.items():
            if field_name in kwargs:
                setattr(self, field_name, kwargs[field_name])
            elif hasattr(self.__class__, field_name):
                # Use class attribute as default if exists
                setattr(self, field_name, getattr(self.__class__, field_name))
            else:
                raise ValueError(f"Missing required field: {field_name}")

    def __setattr__(self, name: str, value: Any):
        if name in get_type_hints(self.__class__):
            expected_type = get_type_hints(self.__class__)[name]
            if not isinstance(value, expected_type):
                raise TypeError(f"Expected {expected_type} for {name}, got {type(value)}")
        super().__setattr__(name, value)

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict['fields'] = {
            field: getattr(self, field)
            for field in get_type_hints(self.__class__)
        }
        return base_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataclassAtom':
        atom = super().from_dict(data)
        for field, value in data['fields'].items():
            setattr(atom, field, value)
        return atom

# Example usage:
class User(DataclassAtom):
    name: str
    age: int
    email: str = "default@example.com"

# Create an AtomArena and allocate User instances
arena = AtomArena(100)
user1 = User(name="Alice", age=30)
user2 = User(name="Bob", age=25, email="bob@example.com")

arena.allocate(user1)
arena.allocate(user2)

# Iterate through the arena and print User information
for atom in arena:
    if isinstance(atom, User):
        print(f"User: {atom.name}, Age: {atom.age}, Email: {atom.email}")