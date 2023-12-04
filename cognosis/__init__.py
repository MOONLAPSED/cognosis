# cognosis.__init__.py
# declares the module 'cognosis'
# =================xGLOBAL_IMPORTS
import sys
import os
import json
import unittest
import datetime
import re
import logging
import typing
import typing_extensions
# ===================GLOBAL_VARIABLES
# ===================GLOBAL_CLASSES
# =================xLOGGING
from logs.exceptions_ import ErrorHandler_
from logs.logging_ import Logger_
from uutils_ import Uutils_

l_ = Logger_()
e_ = ErrorHandler_()
u_ = Uutils_()
SafeDir_ = ['/cognosis/', '/COGNOSIS/']
__all__ = ['e_', 'l_', 'u_', 'SafeDir_', 'log_dir_', 'Logger_', 'ErrorHandler_', 'Uutils_']

# ===================GLOBAL_FUNCTIONS
from main import main
print(f"cognosis init in {os.getcwd()}")
sys.path.append(os.getcwd())
main()
