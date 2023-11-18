import os
import subprocess
from threading_core_utils import ThreadingCoreUtils
from docker_configuration import DockerConfiguration
from LLM_Framework import LLM_Framework

class ServerAdministration:
    def __init__(self):
        self.threading_core_utils = ThreadingCoreUtils()
        self.docker_configuration = DockerConfiguration()
        self.llm_framework = LLM_Framework()

    def run_llm_model(self):
        self.llm_framework.run_model()

    def start_docker_container(self):
        self.docker_configuration.start_container()

    def stop_docker_container(self):
        self.docker_configuration.stop_container()

    def execute_shell_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        return output

    def get_server_hardware_info(self):
        command = "lshw -short"
        return self.execute_shell_command(command)

    def get_file_system_info(self):
        command = "df -h"
        return self.execute_shell_command(command)

    def get_running_processes(self):
        command = "ps aux"
        return self.execute_shell_command(command)

    def get_network_info(self):
        command = "ifconfig"
        return self.execute_shell_command(command)

    def get_docker_info(self):
        command = "docker info"
        return self.execute_shell_command(command)

    def get_llm_model_info(self):
        return self.llm_framework.get_model_info()

if __name__ == "__main__":
    server_admin = ServerAdministration()
    server_admin.run_llm_model()
    server_admin.start_docker_container()
    print(server_admin.get_server_hardware_info())
    print(server_admin.get_file_system_info())
    print(server_admin.get_running_processes())
    print(server_admin.get_network_info())
    print(server_admin.get_docker_info())
    print(server_admin.get_llm_model_info())
    server_admin.stop_docker_container()