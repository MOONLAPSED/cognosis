import subprocess
import sys
from typing import List

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

if __name__ == "__main__":
    print(get_project_tree())
    sys.exit(0)