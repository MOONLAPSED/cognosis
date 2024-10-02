from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, TypeVar, Union
from dataclasses import dataclass, field
import json
import hashlib
import struct
import msgpack
import marshal
import types

T = TypeVar('T')
V = TypeVar('V')
C = TypeVar('C')

@dataclass
class Atom(Generic[T, V, C]):
    type: Union[str, str]
    value: Union[T, V, C] = field(default=None)
    hash: str = field(init=False)

    def __post_init__(self):
        self.hash = hashlib.sha256(repr(self.value).encode()).hexdigest()


    @staticmethod
    def serialize_data(data: Any) -> bytes:
        return msgpack.packb(data, use_bin_type=True)

    @staticmethod
    def deserialize_data(data: bytes) -> Any:
        return msgpack.unpackb(data, raw=False)

    def __repr__(self):
        return f"{self.value} : {self.type}"

    def __str__(self):
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Atom) and self.hash == other.hash

    def __hash__(self) -> int:
        return int(self.hash, 16)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value

    def __delitem__(self, key):
        del self.value[key]

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        return iter(self.value)

    def __contains__(self, item):
        return item in self.value

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    @property
    def memory_view(self) -> memoryview:
        if isinstance(self.value, (bytes, bytearray)):
            return memoryview(self.value)
        raise TypeError("Unsupported type for memoryview")

@dataclass
class HypercubeEmbedding(Atom[T, V, C]):
    M: int
    K: int
    N: int
    hypercube: List[List[List[int]]] = field(init=False)

    def __post_init__(self):
        self.hypercube = [[[0 for _ in range(self.N)] for _ in range(self.K)] for _ in range(self.M)]
        super().__post_init__()

    def embed_bytecode(self, bytecode: bytes, stream_index: int, config_index: int):
        m_length = len(bytecode)
        for dim in range(self.M):
            self.hypercube[dim][stream_index][config_index] = bytecode[dim % m_length]

    def analyze_similarity(self, stream1: int, stream2: int) -> float:
        similarity = sum(
            sum(abs(self.hypercube[dim][stream1][config] - self.hypercube[dim][stream2][config])
                for config in range(self.N))
            for dim in range(self.M)
        )
        return 1 / (1 + similarity)

    def visualize(self):
        print("Visualizing the hypercube...(use your imagination)")

@dataclass
class FormalTheory(Atom, Generic[T]):
    reflexivity: Callable[[T], bool] = lambda x: x == x
    symmetry: Callable[[T, T], bool] = lambda x, y: x == y
    transitivity: Callable[[T, T, T], bool] = lambda x, y, z: (x == y) and (y == z) and (x == z)
    transparency: Callable[[Callable[..., T], T, T], T] = lambda f, x, y: f(x, y) if x == y else None
    case_base: Dict[str, Callable[..., bool]] = field(default_factory=dict)
    value: float = 0.0
    atom_count: int = 0
    completed_atoms: int = 0
    hypercube_embedding: HypercubeEmbedding = field(init=False)

    def __post_init__(self):
        self.hypercube_embedding = HypercubeEmbedding(10, 10, 100)
        self.update_value()
        self.case_base = {
            '⊤': lambda x, _: x,
            '⊥': lambda _, y: y,
            'a': self.if_else_a,
            '¬': lambda a: not a,
            '∧': lambda a, b: a and b,
            '∨': lambda a, b: a or b,
            '→': lambda a, b: (not a) or b,
            '↔': lambda a, b: (a and b) or (not a and not b),
            '¬∨': lambda a, b: not (a or b),  # NOR operation
            '¬∧': lambda a, b: not (a and b),  # NAND operation
            'contrapositive': self.contrapositive
        }
        super().__post_init__()

    def update_value(self):
        """Update the value based on completed atoms and total atoms."""
        if self.atom_count == 0:
            self.value = 1.0 if self.completed_atoms == 0 else 0.0
        else:
            self.value = self.completed_atoms / self.atom_count

    def add_atom(self, atom: Atom):
        """Add an atom and update the atom count."""
        self.atom_count += 1
        self.hypercube_embedding.embed_bytecode(atom.serialize_data(atom.value), self.atom_count % self.hypercube_embedding.K, self.atom_count % self.hypercube_embedding.N)
        self.update_value()

    def complete_atom(self):
        """Mark an atom as completed and update the completed atom count."""
        self.completed_atoms += 1
        self.update_value()

    def encode(self) -> bytes:
        # Encode FormalTheory attributes into bytes
        reflexivity_code = marshal.dumps(self.reflexivity.__code__)
        symmetry_code = marshal.dumps(self.symmetry.__code__)
        transitivity_code = marshal.dumps(self.transitivity.__code__)
        transparency_code = marshal.dumps(self.transparency.__code__)
        case_base_bytes = b''.join(marshal.dumps(func.__code__) for func in self.case_base.values())

        packed_data = struct.pack(
            '>3sB5I{}s{}s{}s{}s{}s'.format(
                len(reflexivity_code),
                len(symmetry_code),
                len(transitivity_code),
                len(transparency_code),
                len(case_base_bytes)
            ),
            b'THY', 1,
            len(reflexivity_code), len(symmetry_code),
            len(transitivity_code), len(transparency_code),
            len(case_base_bytes),
            reflexivity_code, symmetry_code,
            transitivity_code, transparency_code,
            case_base_bytes
        )
        hypercube_data = self.hypercube_embedding.encode()
        packed_data += hypercube_data

        return packed_data

    @classmethod
    def decode(cls, data: bytes) -> 'FormalTheory':
        offset = 4  # Skip the b'THY' part and version number
        lengths = struct.unpack_from('>5I', data, offset)
        offset += 4 * 5
        reflexivity_len, symmetry_len, transitivity_len, transparency_len, case_base_len = lengths

        reflexivity_code = data[offset:offset + reflexivity_len]
        offset += reflexivity_len
        symmetry_code = data[offset:offset + symmetry_len]
        offset += symmetry_len
        transitivity_code = data[offset:offset + transitivity_len]
        offset += transitivity_len
        transparency_code = data[offset:offset + transparency_len]
        offset += transparency_len
        case_base_bytes = data[offset:offset + case_base_len]
        offset += case_base_len

        hypercube_data = data[offset:]

        theory = cls()
        theory.reflexivity = cls.load_function(reflexivity_code)
        theory.symmetry = cls.load_function(symmetry_code)
        theory.transitivity = cls.load_function(transitivity_code)
        theory.transparency = cls.load_function(transparency_code)
        theory.case_base = cls.load_case_base(case_base_bytes)
        theory.hypercube_embedding = HypercubeEmbedding.decode(hypercube_data)

        return theory

    @staticmethod
    def load_function(bytecode: bytes) -> Callable:
        code = marshal.loads(bytecode)
        return types.FunctionType(code, globals())

    @staticmethod
    def load_case_base(case_base_bytes: bytes) -> Dict[str, Callable[..., bool]]:
        case_base = {}
        offset = 0
        while offset < len(case_base_bytes):
            length, = struct.unpack_from('>I', case_base_bytes, offset)
            offset += 4
            func_bytes = case_base_bytes[offset:offset + length]
            func = FormalTheory.load_function(func_bytes)
            case_base[func.__name__] = func
            offset += length
        return case_base

    
    def execute(self, *args, **kwargs) -> Any:
        return self.transparency(*args, **kwargs)

    def if_else_a(self, a, b):
        return a if a else b

    def contrapositive(self, a, b):
        return (not b) or (not a)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'reflexivity': marshal.dumps(self.reflexivity.__code__),
            'symmetry': marshal.dumps(self.symmetry.__code__),
            'transitivity': marshal.dumps(self.transitivity.__code__),
            'transparency': marshal.dumps(self.transparency.__code__),
            'case_base': {k: marshal.dumps(v.__code__) for k, v in self.case_base.items()},
            'value': self.value,
            'atom_count': self.atom_count,
            'completed_atoms': self.completed_atoms,
            'hypercube_embedding': self.hypercube_embedding.encode()  # Not implemented yet
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FormalTheory':
        theory = cls()
        theory.reflexivity = cls.load_function(data['reflexivity'])
        theory.symmetry = cls.load_function(data['symmetry'])
        theory.transitivity = cls.load_function(data['transitivity'])
        theory.transparency = cls.load_function(data['transparency'])
        theory.case_base = cls.load_case_base(data['case_base'])
        theory.value = data['value']
        theory.atom_count = data['atom_count']
        theory.completed_atoms = data['completed_atoms']
        theory.hypercube_embedding = HypercubeEmbedding.decode(data['hypercube_embedding'])
        return theory


# Example usage
if __name__ == "__main__":
    theory = FormalTheory()

    # Adding and completing atoms to see value update
    for _ in range(5):
        theory.add_atom(Atom(value=_, type='int'))  # Adding atoms

    for _ in range(3):
        theory.complete_atom()  # Completing atoms
    
    # Output the value after adding and completing atoms
    print(f"Theory Value after adding and completing atoms: {theory.value}")
    
    # Encode and decode the theory
    encoded_data = theory.encode()
    decoded_theory = FormalTheory.decode(encoded_data)
    print(f"Decoded Theory Value: {decoded_theory.value}")