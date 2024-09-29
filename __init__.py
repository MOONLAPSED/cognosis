#!/usr/bin/env python
# -*- coding: utf-8 -*-
# STATE_START
{
  "current_step": 0
}
# STATE_END
import tracemalloc
import logging
tracemalloc.start()
tracefileter = ("<<frozen importlib._bootstrap>", "<frozen importlib._bootstrap_external>")
tracemalloc.Filter(False, tracefileter)
import ctypes
import os
import sys
import stat
# HOMOICONISTIC morphological source code displays 'modified quine' behavior
# within a validated runtime, if and only if the valid python interpreter
# has r/w/x permissions to the source code file and some method of writing
# state to the source code file is available. Any interruption of the
# '__exit__` method or misuse of '__enter__' will result in a runtime error
# platforms: Ubuntu-22.04LTS (posix), Windows-11 (nt)
if os.name == 'nt':
    from ctypes import windll
    # Function to check file permissions on Windows
    def windowsPermissions(filePath):
        GENERIC_READ = 0x80000000
        GENERIC_WRITE = 0x40000000
        GENERIC_EXECUTE = 0x20000000
        OPEN_EXISTING = 3
        FILE_ATTRIBUTE_NORMAL = 0x80
        # Open file for reading to get handle
        fileHandle = windll.kernel32.CreateFileW(filePath, GENERIC_READ, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
        if fileHandle == -1:
            return None
        # Check file attributes using Windows API
        permissionsInfo = {
            "readable": False,
            "writable": False,
            "executable": False}
        # GetFileSecurityW retrieves permissions (DACL - Discretionary Access Control List)
        # SECURITY_INFORMATION constants: https://docs.microsoft.com/en-us/windows/win32/secauthz/security-information
        READ_CONTROL = 0x00020000
        DACL_SECURITY_INFORMATION = 0x00000004
        # Allocate buffer to hold the security descriptor
        security_descriptor = ctypes.create_string_buffer(1024)
        sd_size = ctypes.c_ulong()
        # Fetch security info
        result = windll.advapi32.GetFileSecurityW(filePath, DACL_SECURITY_INFORMATION, security_descriptor, 1024, ctypes.byref(sd_size))
        if result == 0:
            return permissionsInfo  # Failed to get security info
        # Check permissions by querying the file attributes
        fileAttributes = windll.kernel32.GetFileAttributesW(filePath)
        if fileAttributes == -1:
            print("Failed to get file attributes")
            return permissionsInfo
        # Modify permission status based on attributes
        permissionsInfo["readable"] = bool(fileAttributes & GENERIC_READ)
        permissionsInfo["writable"] = bool(fileAttributes & GENERIC_WRITE)
        permissionsInfo["executable"] = bool(fileAttributes & GENERIC_EXECUTE)
        # Close the file handle
        windll.kernel32.CloseHandle(fileHandle)
        return permissionsInfo
    
    filePath = sys.argv[0]
    permissionsInfo = windowsPermissions(filePath)
    if permissionsInfo:
        print("File permissions:")
        print(f"Readable: {permissionsInfo['readable']}")
elif os.name == 'posix':
    from ctypes import cdll
    def detailedPermissions(filePath):
        """Get detailed file permissions using stat."""
        fileStats = os.stat(filePath)
        mode = fileStats.st_mode
        permissionsInfo = {
            "readable": bool(mode & stat.S_IRUSR),
            "writable": bool(mode & stat.S_IWUSR),
            "executable": bool(mode & stat.S_IXUSR),
            "octal": oct(mode)}
        return permissionsInfo
    filePath = sys.argv[0]
    permissionsInfo = detailedPermissions(filePath)
