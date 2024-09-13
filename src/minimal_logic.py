import hashlib
from abc import ABC
from typing import Type, Any, List, Dict, Set, TypeVar

T = TypeVar('T', bound='Atom')

# Enum for DataType
from enum import Enum, auto

class DataType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto()
    NONE = auto()
    LIST = auto()
    TUPLE = auto()
    DICT = auto()
    CALLABLE = auto()
    OBJECT = auto()

# Atom decorator to assign a unique ID to each Atom class
def atom(cls: Type[T]) -> Type[T]:
    cls.id = hashlib.sha256(cls.__name__.encode('utf-8')).hexdigest()
    return cls

@atom
class Atom(ABC):
    def __init__(self, tag: str = '', value: Any = None, children: List['Atom'] = None, metadata: Dict[str, Any] = None):
        self.tag = tag
        self.value = value
        self.children = children if children else []
        self.metadata = metadata if metadata else {}
        self.subscribers: Set['Atom'] = set()
        self.data_type: DataType = self._infer_data_type()

    def _infer_data_type(self) -> DataType:
        if isinstance(self.value, int):
            return DataType.INTEGER
        elif isinstance(self.value, float):
            return DataType.FLOAT
        elif isinstance(self.value, str):
            return DataType.STRING
        elif isinstance(self.value, bool):
            return DataType.BOOLEAN
        elif self.value is None:
            return DataType.NONE
        elif isinstance(self.value, list):
            return DataType.LIST
        elif isinstance(self.value, tuple):
            return DataType.TUPLE
        elif isinstance(self.value, dict):
            return DataType.DICT
        elif callable(self.value):
            return DataType.CALLABLE
        else:
            return DataType.OBJECT

    def add_child(self, atom: 'Atom'):
        self.children.append(atom)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, tag={self.tag}, value={self.value}, data_type={self.data_type})"

# Example usage
@atom
class NumberAtom(Atom):
    def __init__(self, value):
        super().__init__('number', value)

@atom
class ComplexAtom(Atom):
    def __init__(self, tag: str, value: Any, children: List[Atom] = None, metadata: Dict[str, Any] = None):
        super().__init__(tag, value, children, metadata)

# Create some atoms
num_atom = NumberAtom(42)
complex_atom = ComplexAtom('complex', None, [num_atom])

print(num_atom)  # Output a representation of the NumberAtom
print(complex_atom)  # Output a representation of the ComplexAtom with NumberAtom as a child