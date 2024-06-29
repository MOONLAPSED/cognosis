import http.server
import json
import datetime
import sys
import logging
from logging.config import dictConfig
from pathlib import Path
import importlib
import types
from abc import ABC, abstractmethod
import builtins
from types import SimpleNamespace


all_modules = sys.modules
runtime_modules = [module for module in all_modules if "__" not in module]
dunder_modules = [module for module in all_modules if "__" in module] 


class REPLProxy(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # ...
        raise
    pass

class RuntimeModules(ABC):
    def __init__(self, *args, **kwargs):
        # ...
        raise
    pass

class ConcreteModules(ABC):
    def __init__(self, *args, **kwargs):
        # ...
        raise
    pass

class VersionedModules(ABC):
    def __init__(self, *args, **kwargs):
        # ...
        raise
    pass

class AssociativeModule(RuntimeModules, ConcreteModules, VersionedModules):
    def __init__(self, *args, **kwargs):
        # ...
        raise
    pass