import os
import sys
import inspect
from pathlib import Path
from typing import Union, Type, Callable, Tuple, Optional

def isModule(rawClsOrFn: Union[Type, Callable]) -> Optional[str]:
    pyModule = inspect.getmodule(rawClsOrFn)
    if hasattr(pyModule, "__file__"):
        return str(Path(pyModule.__file__).resolve())
    return None

def getModuleImportInfo(rawClsOrFn: Union[Type, Callable]) -> Tuple[Optional[str], str, str]:
    """
    Given a class or function in Python, get all the information needed to import it in another Python process.
    This version balances portability and optimization using camel case.
    """
    pyModule = inspect.getmodule(rawClsOrFn)
    
    if pyModule is None or pyModule.__name__ == '__main__':
        return None, 'interactive', rawClsOrFn.__name__

    modulePath = isModule(rawClsOrFn)

    if not modulePath:
        # Built-in or frozen module
        return None, pyModule.__name__, rawClsOrFn.__name__

    rootPath = str(Path(modulePath).parent)
    moduleName = pyModule.__name__
    clsOrFnName = getattr(rawClsOrFn, "__qualname__", rawClsOrFn.__name__)

    if getattr(pyModule, "__package__", None):
        try:
            package = __import__(pyModule.__package__)
            packagePath = str(Path(package.__file__).parent)
            if Path(packagePath) in Path(modulePath).parents:
                rootPath = str(Path(packagePath).parent)
            else:
                print(f"Warning: Module is not in the expected package structure. Using file parent as root path.")
        except Exception as e:
            print(f"Warning: Error processing package structure: {e}. Using file parent as root path.")

    return rootPath, moduleName, clsOrFnName

def demonstrateUsage():
    """Demonstrate the usage of getModuleImportInfo function."""
    # Example with a built-in function
    print("Built-in function (len):")
    print(getModuleImportInfo(len))

    # Example with this script's function
    print("\nFunction from this script (getModuleImportInfo):")
    print(getModuleImportInfo(getModuleImportInfo))

    # Example with a standard library module
    import json
    print("\nStandard library module (json.loads):")
    print(getModuleImportInfo(json.loads))

    # If you have numpy installed, uncomment the following:
    # import numpy as np
    # print("\nThird-party library function (numpy.array):")
    # print(getModuleImportInfo(np.array))

if __name__ == "__main__":
    demonstrateUsage()