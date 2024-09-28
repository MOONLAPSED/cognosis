#!/usr/bin/env python3
# /src/utils/cleanup.py

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"Successfully ran command: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e}")


def remove_path(path):
    path = Path(path)
    try:
        if path.is_dir():
            shutil.rmtree(path)
            print(f"Removed directory: {path}")
        elif path.is_file() or path.is_symlink():
            path.unlink()
            print(f"Removed file: {path}")
        else:
            print(f"Path not found: {path}")
    except PermissionError:
        print(f"Permission denied: {path}")
    except Exception as e:
        print(f"Error removing {path}: {e}")


def cleanup():
    # Get the project root directory
    project_root = Path(__file__).resolve().parents[2]

    # List of paths to remove
    paths_to_remove = [
        ".venv",
        "build",
        "dist",
        ".pytest_cache",
        ".mypy_cache",
        ".tox",
        "cognosis.egg-info",
        ".pdm.toml",
        ".pdm-build",
        ".pdm-python",
        "pdm.lock",
    ]

    # Remove paths
    for path in paths_to_remove:
        remove_path(project_root / path)

    # Remove __pycache__ directories and .pyc files
    for root, dirs, files in os.walk(project_root, topdown=False):
        for name in dirs:
            if name == "__pycache__":
                remove_path(Path(root) / name)
        for name in files:
            if name.endswith(".pyc"):
                remove_path(Path(root) / name)

    # Uninstall the project using pipx
    run_command("pipx uninstall cognosis")

    # Remove PDM installation (if installed via pipx)
    run_command("pipx uninstall pdm")

    print("Cleanup completed.")


def remove_conda_env():
    try:
        conda_env_path = Path(os.environ.get("CONDA_PREFIX", ""))
        if not conda_env_path:
            print("No active conda environment detected.")
            return

        env_name = conda_env_path.name

        # Check if it's a base environment
        base_env_names = ["base", "miniconda", "anaconda"]
        if any(base_name in env_name.lower() for base_name in base_env_names):
            print(f"Cannot remove the base conda environment: {env_name}")
            return

        # Deactivate the current environment
        run_command("conda deactivate")

        # Remove the environment
        run_command(f"conda env remove -n {env_name} --yes")
        print(f"Removed conda environment: {env_name}")

    except KeyError as e:
        print(f"Error accessing environment variable: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while removing conda environment: {e}")


def main():
    confirm = input(
        "This will remove all project artifacts and installations. Are you sure? (y/N): "
    )
    if confirm.lower() == "y":
        cleanup()
        try:
            remove_conda_env()
        except Exception as e:
            print(f"Failed to remove conda environment: {e}")
    else:
        print("Cleanup aborted.")
    sys.exit(0)


if __name__ == "__main__":
    main()
