# /cognosis/main.py
import os
import unittest

from uutils_ import Uutils_


def main():
    utils = Uutils_()
    if not os.path.exists("logs"):
        utils.create_dir("logs")
    else:
        print("Logs directory already exists.")
    if not os.path.exists("tests"):
        utils.create_dir("tests")
    else:
        print("Tests directory already exists.")
    
    try:
        utils.manage_daemon()
        process_info = utils.process_info()
        print(f"Process information: {process_info}")
        api_response = utils.api_call('https://example.com')
        print(f"API response: {api_response}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print(f"cognosis main in {os.getcwd()}")
    unittest.main()

if __name__ == '__main__':
    main()
