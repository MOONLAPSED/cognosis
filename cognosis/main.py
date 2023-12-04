# /cognosis/main.py
import os
from uutils_ import Uutils_
import unittest


def main():
    if not os.path.exists("logs"):
        Uutils_.create_dir("logs")
        pass
    else:
        pass
    if not os.path.exists("tests"):
        Uutils_.create_dir("tests")
        pass
    else:
        pass
    
    print(f"cognosis main in {os.getcwd()}")
    unittest.main()

if __name__ == '__main__':
    main()
