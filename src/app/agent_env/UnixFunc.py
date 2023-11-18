import os
import subprocess
from xonsh.built_ins import XSH

class UnixFunctionality:
    def __init__(self):
        self.xonsh_shell = XSH

    def execute_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        return output, error

    def get_filesystem_info(self):
        filesystem_info = os.statvfs('/')
        return filesystem_info

    def get_system_info(self):
        system_info = os.uname()
        return system_info

    def get_process_info(self):
        process_info = os.system('ps -aux')
        return process_info

    def get_network_info(self):
        network_info = os.system('ifconfig')
        return network_info

    def get_xonsh_shell_info(self):
        xonsh_info = self.xonsh_shell
        return xonsh_info

unix_functionality = UnixFunctionality()