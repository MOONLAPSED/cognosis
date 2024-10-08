from abc import ABC, abstractmethod
from dataclasses import asdict, astuple, dataclass, field
from struct import Struct
from types import (
    CodeType,
    FrameType,
    FunctionType,
    MethodType,
    ModuleType,
    TracebackType,
)
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)


@dataclass
class GrammarRule:
    """
    Represents a single grammar rule in a context-free grammar.
    
    Attributes:
        lhs (str): Left-hand side of the rule.
        rhs (List[Union[str, 'GrammarRule']]): Right-hand side of the rule, which can be terminals or other rules.
    """
    lhs: str
    rhs: List[Union[str, 'GrammarRule']]
    
    def __repr__(self):
        """
        Provide a string representation of the grammar rule.
        
        Returns:
            str: The string representation.
        """
        rhs_str = ' '.join([str(elem) for elem in self.rhs])
        return f"{self.lhs} -> {rhs_str}"


class Atom(ABC):
    """
    Abstract Base Class for all Atom types.
    
    Atoms are the smallest units of data or executable code, and this interface
    defines common operations such as encoding, decoding, execution, and conversion
    to data classes.
    
    Attributes:
        grammar_rules (List[GrammarRule]): List of grammar rules defining the syntax of the Atom.
    """
    grammar_rules: List[GrammarRule] = field(default_factory=list)
    
    @abstractmethod
    def encode(self) -> bytes:
        """
        Encode the Atom instance into bytes.
        """
        pass

    @abstractmethod
    def decode(self, data: bytes) -> None:
        """
        Decode the provided bytes into the Atom instance.
        """
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the Atom instance with the provided arguments.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Provide a string representation of the Atom instance.
        """
        pass

    @abstractmethod
    def to_dataclass(self) -> 'AtomDataclass':
        """
        Convert the Atom instance to a dataclass.
        """
        pass

    @abstractmethod
    def parse_tree(self) -> 'ParseTreeAtom':
        """
        Generate a parse tree representation of the Atom instance.
        """
        pass

    @abstractmethod
    def define_grammar(self) -> None:
        """
        Define the context-free grammar for the Atom.
        """
        pass

@dataclass
class AtomDataclass(Generic[T], Atom):
    """
    A concrete implementation of Atom representing various primitive data types.
    
    Attributes:
        value (T): The value of the atom, which can be of any type.
        data_type (str): The type of the value, determined during initialization.
    """
    value: T
    data_type: str = field(init=False)
    
    def __post_init__(self):
        """
        Initialize the data type based on the type of the value.
        """
        type_map = {
            'str': 'string',
            'int': 'integer',
            'float': 'float',
            'bool': 'boolean',
            'list': 'list',
            'dict': 'dictionary'
        }
        data_type_name = type(self.value).__name__
        object.__setattr__(self, 'data_type', type_map.get(data_type_name, 'unsupported'))
        self.define_grammar()

    def encode(self) -> bytes:
        """
        Encode the AtomDataclass instance into bytes.
        
        Returns:
            bytes: Encoded bytes of the AtomDataclass.
        """
        data_type_bytes = self.data_type.encode('utf-8')
        data_bytes = self._encode_data()
        header = struct.pack('!I', len(data_type_bytes))
        return header + data_type_bytes + data_bytes

    def _encode_data(self) -> bytes:
        """
        Encode the value into bytes based on its data type.
        
        Returns:
            bytes: Encoded value bytes.
        """
        if self.data_type == 'string':
            return self.value.encode('utf-8')
        elif self.data_type == 'integer':
            return struct.pack('!q', self.value)
        elif self.data_type == 'float':
            return struct.pack('!d', self.value)
        elif self.data_type == 'boolean':
            return struct.pack('?', self.value)
        elif self.data_type == 'list':
            return b''.join([AtomDataclass(element).encode() for element in self.value])
        elif self.data_type == 'dictionary':
            return b''.join(
                [AtomDataclass(key).encode() + AtomDataclass(value).encode() for key, value in self.value.items()]
            )
        else:
            raise ValueError(f"Unsupported data type: {self.data_type}")

    def decode(self, data: bytes) -> None:
        """
        Decode the provided bytes into the AtomDataclass instance.
        
        Args:
            data (bytes): The bytes to decode.
        """
        header_length = struct.unpack('!I', data[:4])[0]
        data_type_bytes = data[4:4 + header_length]
        data_type = data_type_bytes.decode('utf-8')
        data_bytes = data[4 + header_length:]
        
        type_map_reverse = {
            'string': 'str',
            'integer': 'int',
            'float': 'float',
            'boolean': 'bool',
            'list': 'list',
            'dictionary': 'dict'
        }

        if data_type == 'string':
            value = data_bytes.decode('utf-8')
        elif data_type == 'integer':
            value = struct.unpack('!q', data_bytes)[0]
        elif data_type == 'float':
            value = struct.unpack('!d', data_bytes)[0]
        elif data_type == 'boolean':
            value = struct.unpack('?', data_bytes)[0]
        elif data_type == 'list':
            value = []
            offset = 0
            while offset < len(data_bytes):
                element = AtomDataclass(None)
                element.decode(data_bytes[offset:])
                value.append(element.value)
                offset += len(element.encode())
        elif data_type == 'dictionary':
            value = {}
            offset = 0
            while offset < len(data_bytes):
                key = AtomDataclass(None)
                key.decode(data_bytes[offset:])
                offset += len(key.encode())
                val = AtomDataclass(None)
                val.decode(data_bytes[offset:])
                offset += len(val.encode())
                value[key.value] = val.value
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

        self.value = value
        object.__setattr__(self, 'data_type', type_map_reverse.get(data_type, 'unsupported'))

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the AtomDataclass instance. This is a placeholder for further implementation.
        """
        pass

    def __repr__(self):
        """
        Provide a string representation of the AtomDataclass instance.
        
        Returns:
            str: The string representation.
        """
        return f"AtomDataclass(id={id(self)}, value={self.value}, data_type='{self.data_type}')"

    def to_dataclass(self):
        """
        Convert the AtomDataclass instance to a dataclass.
        
        Returns:
            AtomDataclass: The instance itself.
        """
        return self

    def parse_tree(self) -> 'ParseTreeAtom':
        """
        Generate a parse tree representation of the AtomDataclass.
        
        Returns:
            ParseTreeAtom: The parse tree representation.
        """
        return ParseTreeAtom(str(self.value))

    def define_grammar(self) -> None:
        """
        Define the context-free grammar for the AtomDataclass.
        """
        if self.data_type == 'string':
            self.grammar_rules = [GrammarRule("STRING", ["\".*\""])]
        elif self.data_type == 'integer':
            self.grammar_rules = [GrammarRule("INTEGER", ["-?[0-9]+"])]
        elif self.data_type == 'float':
            self.grammar_rules = [GrammarRule("FLOAT", ["-?[0-9]*\\.[0-9]+"])]
        elif self.data_type == 'boolean':
            self.grammar_rules = [GrammarRule("BOOLEAN", ["true", "false"])]
        elif self.data_type == 'list':
            self.grammar_rules = [GrammarRule("LIST", ["[", "ELEMENTS", "]"])]
        elif self.data_type == 'dictionary':
            self.grammar_rules = [GrammarRule("
