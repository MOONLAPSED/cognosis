from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Generic, List, NamedTuple, Optional, Tuple, Type, TypeVar, Union
from types import ModuleType, FunctionType, MethodType, CodeType, FrameType, TracebackType
from dataclasses import dataclass, field, asdict, astuple
from struct import Struct


class Atom(ABC):
    """
    An abstract base class that defines the common interface for all Atom types.
    
    Atom represents a polymorphic data structure that can encode, decode, execute,
    represent itself as a string, be converted to a dataclass, and parse its structure
    into a tree representation.
    """

    @abstractmethod
    def encode(self) -> bytes:
        """
        Encodes the Atom instance into a bytes representation.
        
        Returns:
            bytes: The encoded bytes representation of the Atom instance.
        """
        pass

    @abstractmethod
    def decode(self, data: bytes) -> None:
        """
        Decodes the Atom instance from a bytes representation.
        
        Args:
            data (bytes): The bytes representation to be decoded.
        """
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Executes the Atom instance with the provided arguments.
        
        This method is expandable to support execution in different contexts
        (e.g., execute_py, execute_js, execute_c, etc.).
        
        Args:
            *args: Positional arguments for the execution.
            **kwargs: Keyword arguments for the execution.
            
        Returns:
            Any: The result of the execution.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Returns a string representation of the Atom instance.
        
        Returns:
            str: The string representation of the Atom instance.
        """
        pass

    @abstractmethod
    def to_dataclass(self) -> 'AtomDataclass':
        """
        Converts the Atom instance to an AtomDataclass instance.
        
        Returns:
            AtomDataclass: The AtomDataclass instance representing the Atom instance.
        """
        pass

    @abstractmethod
    def parse_tree(self) -> 'ParseTreeAtom':
        """
        Parses the structure of the Atom instance into a ParseTreeAtom representation.
        
        This method is expandable to support different parsing strategies
        (e.g., parse_tree_bnf, parse_tree_xml, etc.).
        
        Returns:
            ParseTreeAtom: The ParseTreeAtom representation of the Atom instance.
        """
        pass



