# cognosis.uutils.py
import os
import sys
import json
import unittest
import datetime
import re


class Uutils_(object):
    def stat_(path):
        """
        Get the stat information for the given path.

        :param path: the path to the file or directory
        :return: a tuple containing the stat information (st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid, st_size, st_atime, st_mtime, st_ctime)
        """  # Use the `os.scandir()` function to get the stat information
        for info in os.scandir(path):
            if info.is_dir():
                # If the path is a directory, return the stat information for the directory
                return info.stat()
            elif info.is_file():  # If the path is a file, return the stat information for the file
                return info.stat()  # If the path is not a directory or a file, raise an exception
        raise IOError(f"{path} is not a directory or a file")
    """
    Usage:
    > u = Uutils_()
    > u.stat_('.')
os.stat_result(st_mode=16877, st_ino=250179, st_dev=2080, st_nlink=15, st_uid=1000, st_gid=1000, st_size=4096, st_atime=1701582419, st_mtime=1701582419, st_ctime=1701582419)
    """

    def get_file_size(path):
        """
        Get the size of the file or directory at the given path.
        """
        try:
            return stat_(path)[stat_.st_size]
        except:
            raise IOError(f"Could not get the size of {path}")
    def get_file_mtime(path):
        """
        Get the modification time of the file or directory at the given path.
        """
        try:
            return stat_(path)[stat_.st_mtime]
        except:
            raise IOError(f"Could not get the modification time of {path}")
    def find_files(path, pattern):
        """
        Find all files in the given path that match the given pattern.
        """
        try:
            for root, dirs, files in os.walk(path):
                for basename in files:
                    if re.search(pattern, basename):
                        filename = os.path.join(root, basename)
                        yield filename
            return True
        except:
            return False
            raise IOError(f"Could not find files in {path} matching {pattern}")
    def get_file_contents(path):
        """
        Get the contents of the file at the given path.
        """
        try:
            with open(path, 'r') as f:
                return f.read()
            return True
        except:
            return False
            raise IOError(f"Could not open {path} for reading")
    def get_file_contents_as_list(path):
        """
        Get the contents of the file at the given path.
        """
        try:
            with open(path, 'r') as f:
                return f.readlines()
            return True
        except:
            return False
            raise IOError(f"Could not open {path} for reading")
    def get_file_contents_as_json(path):
        """
        Get the contents of the file at the given path.
        """
        try:
            with open(path, 'r') as f:
                return json.load(f)
            return True
        except:
            return False
            raise IOError(f"Could not open {path} for reading")
    def write_file_contents(path, contents):
        """
        Write the given contents to the file at the given path.
        """
        try:
            with open(path, 'w') as f:
                f.write(contents)
            return True
        except:
            return False
            raise IOError(f"Could not open {path} for writing")
    def write_file_contents_as_json(path, contents):
        """
        Write the given contents to the file at the given path.
        """
        try:
            with open(path, 'w') as f:
                json.dump(contents, f)
            return True
        except:
            return False
            raise IOError(f"Could not open {path} for writing")
    def append_file_contents(path, contents):
        """
        Append the given contents to the file at the given path.
        """
        try:
            with open(path, 'a') as f:
                f.write(contents)
            return True
        except:
            return False
            raise IOError(f"Could not open {path} for appending")
    def append_file_contents_as_json(path, contents):
        """
        Append the given contents to the file at the given path.
        """
        try:
            with open(path, 'a') as f:
                json.dump(contents, f)
            return True
        except:
            return False
            raise IOError(f"Could not open {path} for appending")
    def create_file(path):
        """
        Create the file at the given path.
        """
        try:
            with open(path, 'x') as f:
                pass
            return True
        except:
            return False
    def create_dir(path):
        """
        Create the directory at the given path.
        """
        try:
            os.mkdir(path)
            return True
        except:
            return False

    def manage_daemon(self):
        """
        Manage system daemons.
        """
        # Example code: This is a placeholder for actual implementation
        print("Daemon managed")

    def process_info(self):
        """
        Get information about a running process.
        """
        # Example code: This is a placeholder for actual implementation
        print("Process information")

    def api_call(self, url, method='GET', data=None, headers=None):
        """
        Make a web API call to the specified URL with the given method, data, and headers.
        """
        # Example code: This is a placeholder for actual implementation
        print(f"API call to {url} with method {method}")
