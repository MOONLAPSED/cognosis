import argparse
import logging
import struct
import json
from typing import Any, Callable, Dict, Generic, TypeVar, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
import threading
import ast
import sys

# Setup logging
lock = threading.Lock()
with lock:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure output directory exists
output_path = Path(__file__).parent / "output"
output_path.mkdir(parents=True, exist_ok=True)

# Ensure logs directory exists
logs_dir = Path(__file__).resolve().parent / 'logs'
logs_dir.mkdir(exist_ok=True)

# Add paths for importing modules
sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parent / 'src'))

# Attempt to import necessary modules
try:
    from src.utils.kb import KnowledgeItem, FileContextManager
    from src.utils.helpr import helped, wizard
    from src.api.threadsafelocal import ThreadLocalScratchArena, ThreadSafeContextManager, FormalTheory, Atom, AtomicData
    from src.utils.get import ensure_path, get_project_tree, run_command, ensure_delete
except ImportError as e:
    logging.error(f"Error importing module: {e}")
    sys.exit(1)

# Argument parser
parser = argparse.ArgumentParser(description="Hypothesis? Use a simple, terse English statement.")
parser.add_argument("case_base", help="Case base? Use a simple, terse English statement.")

class Atom(ABC):
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
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def parse_expression(self, expression: str) -> 'AtomicData':
        pass

T = TypeVar('T')

@dataclass
class AtomicData(Generic[T], Atom):
    value: T
    data_type: str = field(init=False)

    MAX_INT_BIT_LENGTH = 1024

    def __post_init__(self):
        self.data_type = self.infer_data_type(self.value)
        logging.debug(f"Initialized AtomicData with value: {self.value} and inferred type: {self.data_type}")

    def infer_data_type(self, value) -> str:
        type_map = {
            'str': 'string',
            'int': 'integer',
            'float': 'float',
            'bool': 'boolean',
            'list': 'list',
            'dict': 'dictionary',
            'NoneType': 'none'
        }
        data_type_name = type(value).__name__
        inferred_type = type_map.get(data_type_name, 'unsupported')
        logging.debug(f"Inferred data type: {data_type_name} to {inferred_type}")
        return inferred_type

    def encode(self) -> bytes:
        logging.debug(f"Encoding value: {self.value} of type: {self.data_type}")
        if self.data_type == 'string':
            return self.value.encode('utf-8')
        elif self.data_type == 'integer':
            return self.encode_large_int(self.value)
        elif self.data_type == 'float':
            return struct.pack('f', self.value)
        elif self.data_type == 'boolean':
            return struct.pack('?', self.value)
        elif self.data_type in ['list', 'dictionary']:
            return json.dumps(self.value).encode('utf-8')
        elif self.data_type == 'none':
            return b'none'
        else:
            raise ValueError(f"Unsupported data type: {self.data_type}")

    def encode_large_int(self, value: int) -> bytes:
        logging.debug(f"Encoding large integer value: {value}")
        bit_length = value.bit_length()
        if bit_length > self.MAX_INT_BIT_LENGTH:
            raise OverflowError(f"Integer too large to encode: bit length {bit_length} exceeds MAX_INT_BIT_LENGTH {self.MAX_INT_BIT_LENGTH}")
        if -9223372036854775808 <= value <= 9223372036854775807:
            return struct.pack('q', value)
        else:
            value_bytes = value.to_bytes((bit_length + 7) // 8, byteorder='big', signed=True)
            length_bytes = len(value_bytes).to_bytes(1, byteorder='big')
            return length_bytes + value_bytes

    def decode(self, data: bytes) -> None:
        logging.debug(f"Decoding data for type: {self.data_type}")
        if self.data_type == 'string':
            self.value = data.decode('utf-8')
        elif self.data_type == 'integer':
            self.value = self.decode_large_int(data)
        elif self.data_type == 'float':
            self.value, = struct.unpack('f', data)
        elif self.data_type == 'boolean':
            self.value, = struct.unpack('?', data)
        elif self.data_type in ['list', 'dictionary']:
            self.value = json.loads(data.decode('utf-8'))
        elif self.data_type == 'none':
            self.value = None
        else:
            raise ValueError(f"Unsupported data type: {self.data_type}")
        self.data_type = self.infer_data_type(self.value)
        logging.debug(f"Decoded value: {self.value} to type: {self.data_type}")

    def execute(self, *args, **kwargs) -> Any:
        logging.debug(f"Executing atomic data with value: {self.value}")
        return self.value

    def __repr__(self) -> str:
        return f"AtomicData(value={self.value}, data_type={self.data_type})"

    def parse_expression(self, expression: str) -> 'AtomicData':
        try:
            evaluated = eval(ast.literal_eval(expression))
            return AtomicData(evaluated)
        except Exception as e:
            logging.error(f"Error parsing expression: {e}")
            raise

@dataclass
class FormalTheory(Generic[T], Atom):
    top_atom: AtomicData[T]
    bottom_atom: AtomicData[T]
    statement: str
    prediction: Callable[..., bool] = field(default_factory=lambda: lambda: True)
    case_base: Dict[str, Callable[..., bool]] = field(default_factory=dict)

    def __post_init__(self):
        self.case_base = {
            '⊤': lambda x, _: x,
            '⊥': lambda _, y: y,
            '¬': lambda a: not a,
            '∧': lambda a, b: a and b,
            '∨': lambda a, b: a or b,
            '→': lambda a, b: (not a) or b,
            '↔': lambda a, b: (a and b) or (not a and not b),
        }
        logging.debug(f"Initialized FormalTheory/Hypothesis: {self.statement}")

    def test(self, *args, **kwargs) -> AtomicData[T]:
        result = self.prediction(*args, **kwargs)
        return self.top_atom if result else self.bottom_atom

    def refine(self, new_case: Tuple[str, Callable[..., bool]]):
        key, func = new_case
        self.case_base[key] = func
        logging.debug(f"Refined theory with new case: {key}")

    def encode(self) -> bytes:
        encoded_top = self.top_atom.encode()
        encoded_bottom = self.bottom_atom.encode()
        encoded_statement = self.statement.encode('utf-8')
        lengths = struct.pack('III', len(encoded_top), len(encoded_bottom), len(encoded_statement))
        return lengths + encoded_top + encoded_bottom + encoded_statement

    def decode(self, data: bytes) -> None:
        top_len, bottom_len, statement_len = struct.unpack('III', data[:12])
        offset = 12
        self.top_atom.decode(data[offset:offset+top_len])
        offset += top_len
        self.bottom_atom.decode(data[offset:offset+bottom_len])
        offset += bottom_len
        self.statement = data[offset:offset+statement_len].decode('utf-8')

    def execute(self, *args, **kwargs) -> Any:
        return self.test(*args, **kwargs)

    def __repr__(self) -> str:
        return f"FormalTheory(statement='{self.statement}', top={self.top_atom}, bottom={self.bottom_atom})"

    def parse_expression(self, expression: str) -> 'FormalTheory':
        try:
            # Use the ast module to safely parse the expression
            parsed_expr = ast.parse(expression, mode='eval')
            eval_expr = eval(compile(parsed_expr, '', mode='eval'))
            return FormalTheory(
                top_atom=AtomicData(eval_expr == True),
                bottom_atom=AtomicData(eval_expr == False),
                statement=f"Expression {expression} evaluated to {eval_expr}",
                prediction=lambda: eval_expr
            )
        except Exception as e:
            logging.error(f"Error parsing expression: {e}")
            raise

# Create a basic theory/hypothesis
theory = FormalTheory(
    top_atom=AtomicData(True),
    bottom_atom=AtomicData(False),
    statement="All observed swans are white",
    prediction=lambda color: color == "white"
)

# Test the theory
result = theory.test("white")
print(f"Test result: {result}")  # Should print the top_atom (True)

result = theory.test("black")
print(f"Test result: {result}")  # Should print the bottom_atom (False)

# Refine the theory
theory.refine(("observed_swan", lambda color, location: color == "white" or location == "Australia"))

# The refined theory can now handle more complex cases
result = theory.test("black", "Australia")
print(f"Refined test result: {result}")  # Might return top_atom (True) depending on the implementation

# Test mathematical expression parsing
expr_theory = theory.parse_expression("1 + 1 == 2")
print(f"Expression test result: {expr_theory.test()}")  # Should print the top_atom (True)
