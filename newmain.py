# main.py
# This script is part of "cognosis - cognitive coherence coroutines" project,
# which is a pythonic implementation of a model cognitive system,
# utilizing concepts from signal processing, cognitive theories,
# and machine learning to create adaptive systems.

import subprocess
import sys
import argparse
import os
import shutil
import platform
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, TypeVar, Generic, Optional, List
import logging
import json
import struct

T = TypeVar('T')  # Type Variable to allow type-checking, linting,.. of Generic "T" and "V"

# | Cognitive Comment: Define Atom Class |

class Atom(ABC):
    """
    Abstract Base Class for all Atom types.
    An Atom represents a polymorphic data structure that can encode and decode data,
    execute specific behaviors, and convert its representation.
    """
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

# | Cognitive Comment: Define AtomicData Class |

@dataclass
class AtomicData(Generic[T], Atom):
    """
    Concrete Atom class representing Python runtime objects.
    Attributes:
        value (T): The value of the Atom.
    """
    value: T
    data_type: str = field(init=False)

    MAX_INT_BIT_LENGTH = 1024  # Adjust this value as needed

    def __post_init__(self):
        self.data_type = self.infer_data_type(self.value)
        logging.debug(f"Initialized AtomicData with value: {self.value} and inferred type: {self.data_type}")

    def infer_data_type(self, value):
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
        elif self.data_type == 'list' or self.data_type == 'dictionary':
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
        elif self.data_type == 'list' or self.data_type == 'dictionary':
            self.value = json.loads(data.decode('utf-8'))
        elif self.data_type == 'none':
            self.value = None
        else:
            raise ValueError(f"Unsupported data type: {self.data_type}")
        self.data_type = self.infer_data_type(self.value)
        logging.debug(f"Decoded value: {self.value} to type: {self.data_type}")

    def decode_large_int(self, data: bytes) -> int:
        logging.debug(f"Decoding large integer from data: {data}")
        if len(data) == 8:
            return struct.unpack('q', data)[0]
        else:
            length = data[0]
            value_bytes = data[1:length+1]
            return int.from_bytes(value_bytes, byteorder='big', signed=True)

    def execute(self, *args, **kwargs) -> Any:
        logging.debug(f"Executing atomic data with value: {self.value}")
        return self.value

    def __repr__(self) -> str:
        return f"AtomicData(value={self.value}, data_type={self.data_type})"

    def parse_expression(self, expression: str) -> 'AtomicData':
        raise NotImplementedError("Expression parsing is not implemented yet.")

# | Cognitive Comment: Define FormalTheory Class |

@dataclass
class FormalTheory(Generic[T], Atom):
    """
    Concrete Atom class representing formal logical theories.
    Attributes:
        top_atom (AtomicData[T]): Top atomic data.
        bottom_atom (AtomicData[T]): Bottom atomic data.
    """
    top_atom: AtomicData[T]
    bottom_atom: AtomicData[T]
    reflexivity: Callable[[T], bool] = lambda x: x == x
    symmetry: Callable[[T, T], bool] = lambda x, y: x == y
    transitivity: Callable[[T, T, T], bool] = lambda x, y, z: (x == y and y == z)
    transparency: Callable[[Callable[..., T], T, T], T] = lambda f, x, y: f(True, x, y) if x == y else None
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
        logging.debug(f"Initialized FormalTheory with top_atom: {self.top_atom}, bottom_atom: {self.bottom_atom}")

    def encode(self) -> bytes:
        logging.debug("Encoding FormalTheory")
        encoded_top = self.top_atom.encode()
        encoded_bottom = self.bottom_atom.encode()
        encoded_data = struct.pack(f'{len(encoded_top)}s{len(encoded_bottom)}s', encoded_top, encoded_bottom)
        logging.debug("Encoded FormalTheory to bytes")
        return encoded_data

    def decode(self, data: bytes) -> None:
        logging.debug("Decoding FormalTheory from bytes")
        split_index = len(data) // 2
        encoded_top = data[:split_index]
        encoded_bottom = data[split_index:]
        self.top_atom.decode(encoded_top)
        self.bottom_atom.decode(encoded_bottom)
        logging.debug(f"Decoded FormalTheory to top_atom: {self.top_atom}, bottom_atom: {self.bottom_atom}")

    def execute(self, operation: str, *args, **kwargs) -> Any:
        logging.debug(f"Executing FormalTheory operation: {operation} with args: {args}")
        if operation in self.case_base:
            result = self.case_base[operation](*args)
            logging.debug(f"Operation result: {result}")
            return result
        else:
            raise ValueError(f"Operation {operation} not supported in FormalTheory.")

    def __repr__(self) -> str:
        return f"FormalTheory(top_atom={self.top_atom}, bottom_atom={self.bottom_atom})"

    def parse_expression(self, expression: str) -> 'AtomicData':
        raise NotImplementedError("Formal logical expression parsing is not implemented yet.")

# | Cognitive Comment: Define Utility Functions |

def run_command(command, check=True, shell=False, verbose=False):
    """Utility to run a shell command and handle exceptions"""
    if verbose:
        command += " -v"
    try:
        result = subprocess.run(command, check=check, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error:\n{e.stderr.decode()}")
        if check:
            sys.exit(e.returncode)

def ensure_delete(path):
    """Ensure that a file or directory can be deleted"""
    try:
        os.chmod(path, 0o777)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    except Exception as e:
        print(f"Failed to delete {path}. Reason: {e}")

def ensure_path():
    """Ensure that the PATH is set correctly"""
    path = os.getenv('PATH')
    if 'desired_path_entry' not in path:
        os.environ['PATH'] = f'/desired_path_entry:{path}'
        print('Updated PATH environment variable.')

# | Cognitive Comment: Define State Dictionary |

state = {
    "pipx_installed": False,
    "pdm_installed": False,
    "virtualenv_created": False,
    "dependencies_installed": False,
    "lint_passed": False,
    "code_formatted": False,
    "tests_passed": False,
    "benchmarks_run": False,
    "pre_commit_installed": False,
}

# | Cognitive Comment: Define Pipx and PDM Functions |

def ensure_pipx():
    """Ensure pipx is installed"""
    global state
    try:
        subprocess.run("pipx --version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        state['pipx_installed'] = True
    except subprocess.CalledProcessError:
        print("pipx not found, installing pipx...")
        run_command("pip install pipx", shell=True)
        run_command("pipx ensurepath", shell=True)
        state['pipx_installed'] = True

def ensure_pdm():
    """Ensure pdm is installed via pipx"""
    global state
    try:
        output = subprocess.run("pipx list", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if b'pdm' not in output.stdout:
            raise KeyError('pdm not found in pipx list')
        print("pdm is already installed.")
        state['pdm_installed'] = True
    except (subprocess.CalledProcessError, KeyError):
        print("pdm not found, installing pdm...")
        run_command("pipx install pdm", shell=True)
        state['pdm_installed'] = True

# | Cognitive Comment: Define Virtual Environment Creation Function |

def create_virtualenv():
    """Create a virtual environment and activate it using pdm"""
    global state
    os.environ["PDM_VENV_IN_PROJECT"] = "1"
    venv_path = ".venv"
    if os.path.exists(venv_path):
        choice = input("Virtual environment already exists. Overwrite? (y/n): ").lower()
        if choice == 'y':
            print("Deactivating and deleting existing virtual environment...")
            ensure_delete(venv_path)
            print("Virtual environment deleted.")
            run_command("pdm venv create", shell=True)
        else:
            print("Reusing the existing virtual environment.")
    else:
        run_command("pdm venv create", shell=True)
    run_command("pdm lock", shell=True)
    run_command("pdm install", shell=True, verbose=True)
    state['virtualenv_created'] = True
    state['dependencies_installed'] = True

# | Cognitive Comment: Define Mode Prompt Function |

def prompt_for_mode():
    """Prompt the user to choose between development and non-development setup"""
    while True:
        choice = input("Choose setup mode: [d]evelopment or [n]on-development? ").lower()
        if choice in ['d', 'n']:
            return choice
        print("Invalid choice, please enter 'd' or 'n'.")

# | Cognitive Comment: Define Install, Lint, Format, Test, Bench, Pre-commit Functions |

def install():
    """Run installation"""
    run_command("pdm install", shell=True, verbose=True)

def lint():
    """Run linting tools"""
    global state
    run_command("pdm run flake8 .", shell=True)
    run_command("pdm run black --check .", shell=True)
    run_command("pdm run mypy .", shell=True)
    state['lint_passed'] = True

def format_code():
    """Format the code"""
    global state
    run_command("pdm run black .", shell=True)
    run_command("pdm run isort .", shell=True)
    state['code_formatted'] = True

def test():
    """Run tests"""
    global state
    run_command("pdm run pytest", shell=True)
    state['tests_passed'] = True

def bench():
    """Run benchmarks"""
    global state
    run_command("pdm run python src/bench/bench.py", shell=True)
    state['benchmarks_run'] = True

def pre_commit_install():
    """Install pre-commit hooks"""
    global state
    run_command("pdm run pre-commit install", shell=True)
    state['pre_commit_installed'] = True

# | Cognitive Comment: Define Introspect Function |

def introspect():
    """Introspect the current state and print results"""
    print("Introspection results:")
    for key, value in state.items():
        print(f"{key}: {'✅' if value else '❌'}")

# | Cognitive Comment: Define Main Function |

def main():
    ensure_pipx()
    ensure_pdm()
    create_virtualenv()
    parser = argparse.ArgumentParser(description="Setup and run Abraxus project")
    parser.add_argument('-m', '--mode', choices=['dev', 'non-dev'], help="Setup mode: 'dev' or 'non-dev'")
    args = parser.parse_args()
    mode = args.mode
    if not mode:
        choice = prompt_for_mode()
        mode = 'dev' if choice == 'd' else 'non-dev'
    if mode == 'dev':
        install()
        lint()
        format_code()
        test()
        bench()
        pre_commit_install()
        run_command("pdm run python src/bench/bench.py", shell=True)
    else:
        install()
        run_command("pdm run python main.py", shell=True)
    introspect()

if __name__ == "__main__":
    main()

# | Cognitive Comment: Define User-defined Main Function and Associated Routines |

def usermain(arg=None):
    import src.app
    from src.app import FormalTheory, AtomicData
    from src.app import ScopeLifetimeGarden, ThreadSafeContextManager
    if arg:
        print(f"Main called with argument: {arg}")
    else:
        print("Main called with no arguments")
    top = AtomicData(value=True)
    bottom = AtomicData(value=False)
    formal_theory = FormalTheory[int](top_atom=top, bottom_atom=bottom)
    encoded_ft = formal_theory.encode()
    print("Encoded FormalTheory:", encoded_ft)
    new_formal_theory = FormalTheory[int](top_atom=top, bottom_atom=bottom)
    new_formal_theory.decode(encoded_ft)
    print("Decoded FormalTheory:", new_formal_theory)
    try:
        result = formal_theory.execute('∧', True, True)
        print("Execution Result:", result)
    except NotImplementedError:
        print("Execution logic not implemented for FormalTheory.")
    atomic_data = AtomicData(value="Hello World")
    encoded_data = atomic_data.encode()
    print("Encoded AtomicData:", encoded_data)
    new_atomic_data = AtomicData(value=None)
    new_atomic_data.decode(encoded_data)
    print("Decoded AtomicData:", new_atomic_data)
    print("Using ThreadSafeContextManager")
    with ThreadSafeContextManager():
        pass
    garden = ScopeLifetimeGarden()
    garden.set(AtomicData(value="Initial Data"))
    print("Garden Data:", garden.get())
    with garden.scope():
        garden.set(AtomicData(value="New Data"))
        print("Garden Data:", garden.get())
    print("Garden Data:", garden.get())
