"""
Load content in file with reasonable runtime constraints.
"""
from typing import Any, Optional, List
import sys
import os
import subprocess
import shutil

def load_file_content(file_name: str, start_line: int = 0, end_line: int = 1000) -> str:
    """
    Load content in file from start_line to end_line.
    If start_line and end_line are not provided, load the whole file.
    """
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if start_line < 0 or end_line <= start_line:
                sys.stderr.write("Error: start line must be greater than or equal to 0 and end line must be greater than start line.\n")
                sys.exit(1)
            content = "".join(lines[int(start_line):int(end_line)])
            if len(content.split('\n')) > 500:
                sys.stderr.write("Error: The content is too large, please set a reasonable reading range.\n")
                sys.exit(1)
            return content
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)


def get_project_tree() -> List[str]:
    """
    Get project files by "git ls-files" command

    :return: list of relative file paths of the project
    """
    try:
        output: List[str] = subprocess.check_output(["git", "ls-files"]).decode("utf-8").split("\n")
        if len(output) > 100:
            sys.stderr.write("Error: Too many files, you need to view the files and directory structure in each directory through the 'ls' command.\n")
            sys.exit(1)
        return output
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")



def run_command(command, check=True, shell=False, verbose=False):
    """Utility to run a shell command and handle exceptions"""
    if verbose:
        command += " -v"
    try:
        result = subprocess.run(command, check=check, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error:\n{e.stderr.decode()}")
        if check:
            sys.exit(e.returncode)

def ensure_delete(path):
    """Ensure that a file or directory can be deleted"""
    try:
        os.chmod(path, 0o777)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    except Exception as e:
        print(f"Failed to delete {path}. Reason: {e}")

def ensure_path():
    """Ensure that the PATH is set correctly"""
    path = os.getenv('PATH')
    if 'desired_path_entry' not in path:
        os.environ['PATH'] = f'/desired_path_entry:{path}'
        print('Updated PATH environment variable.')





if __name__ == "__main__":
    file_name = sys.argv[1] if len(sys.argv) > 1 else "."
    start_line = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != '${startLine}' else 0
    end_line = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] != '${endLine}' else 1000

    print(get_project_tree())
    print(load_file_content(file_name, start_line, end_line))
    sys.exit(0)