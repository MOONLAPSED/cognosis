import datetime
import json
import logging
import logging.config
import logging.handlers
import operator
import os
import shutil
import subprocess
import sys
import threading
import uuid
from pathlib import Path
from functools import reduce
from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging.config import dictConfig
from typing import Callable, TypeVar, List, Optional, Union, Any, Tuple, Dict, NamedTuple, Set
from threading import Thread, current_thread, Semaphore
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser



from src.utils.kb import KnowledgeItem, FileContextManager
from src.utils.helpr import helped, wizard
from src.api.threadsafelocal import ThreadLocalScratchArena, ThreadSafeContextManager, FormalTheory, Atom, AtomicData
from src.utils.get import ensure_path, get_project_tree, run_command, ensure_delete

# Setup paths
output_path = Path(__file__).parent / "output"
output_path.mkdir(parents=True, exist_ok=True)
_lock = threading.Lock()
# Find the current directory for logging
current_dir = Path(__file__).resolve().parent
while not (current_dir / 'logs').exists():
    current_dir = current_dir.parent
    if current_dir == Path('/'):
        break
# Ensure the logs directory exists
logs_dir = Path(__file__).resolve().parent.joinpath('logs')
logs_dir.mkdir(exist_ok=True)
# Add paths for importing modules
sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parent.joinpath('src')))

def main(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> logging.Logger:
    """Configures logging for the app.
    Args:
        *args: Positional arguments to be passed to the function.
        **kwargs: Keyword arguments to be passed to the function.
    Returns:
        logging.Logger: The logger for the module.
    """
    try:
        run_id = os.getenv("GITHUB_RUN_ID")
        if run_id:
            print(f"Workflow run ID: {run_id}")
    except: pass
    try:
        with _lock:
            logging_config = {
                'version': 1,
                'disable_existing_loggers': False,
                'formatters': {
                    'default': {
                        'format': '[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
                        'datefmt': '%Y-%m-%d~%H:%M:%S%z'
                    },
                },
                'handlers': {
                    'console': {
                        'level': 'INFO',  # Explicitly set level to 'INFO'
                        'class': 'logging.StreamHandler',
                        'formatter': 'default',
                        'stream': 'ext://sys.stdout'
                    },
                    'file': {
                        'level': 'INFO',  # Explicitly set level to 'INFO'
                        'formatter': 'default',
                        'class': 'logging.handlers.RotatingFileHandler',
                        'filename': str(logs_dir / 'app.log'),  # Convert Path object to string for compatibility
                        'maxBytes': 10485760,  # 10MB
                        'backupCount': 10
                    }
                },
                'root': {
                    'level': logging.INFO,
                    'handlers': ['console', 'file']
                }
            }

            dictConfig(logging_config)

            logger = logging.getLogger(__name__)
            logger.info(f'Logging_dir {logs_dir}|'
                        f'\nSource_file: {__file__}|'
                        f'\nInvocation_dir: {Path(__file__).resolve().parent}|'
                        f'\nWorking_dir: {current_dir}||')

            arguments = [_ for _ in str(sys.argv).lower().strip().split(' ') if len(_) > 0]
            if len(arguments) > 1:
                logger.debug(f'Arguments: {arguments}')
                runtime_arguments = {}
                for arg in arguments:
                    if arg == '-h':
                        helped()
                        sys.exit()
                    elif str(arg).startswith('-'):
                        print(f'Unrecognized argument: {arg}')
                    elif len(str(arg).strip()) >= 5_000:
                        print(f'Argument is too long: {arg}')
                    # '--h' for args and flags of invocations of cognosis
                    elif arg.startswith('~'):
                        print(f'Argument starts with tilde: {arg}')
                    # '--v' verbose debugging for invocations of cognosis, their args, flags, and curried/runtime args
                    elif arg.startswith('!'):
                        print(f'Argument starts with exclamation point: {arg}')
                    else:
                        # Generate a timestamp as the key
                        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                        timestamp += f'_{str(uuid.uuid4())}'
                        timestamp = timestamp.replace('-', '')
                        timestamp = timestamp.replace(':', '')
                        timestamp = timestamp.replace('.', '')
                        hash_key = f'{timestamp}_{arg}'
                        runtime_arguments[hash_key] = arg
                        logger.debug(f'Argument: {arg}|{hash_key}')
                    rtjson_path = os.path.join(output_path, 'runtime_arguments.json')
                    with open(str(rtjson_path), 'w') as f:
                        json.dump(runtime_arguments, f, indent=4)
            else:
                logger.debug(f'No arguments provided.')

            return logger, runtime_arguments; _lock.release()
    except:
        logger = logging.getLogger(__name__).exception(f'Error in main(): {e}')
        sys.exit(1)
    finally:
        if _lock.locked(): _lock.release()  # cleanup routines
        return logger, runtime_arguments



state = {
    "pipx_installed": False,
    "pdm_installed": False,
    "virtualenv_created": False,
    "dependencies_installed": False,
    "lint_passed": False,
    "code_formatted": False,
    "tests_passed": False,
    "benchmarks_run": False,
    "pre_commit_installed": False,
}


#def state_load():  # provides a value for a 'loading bar' function, for the various stages

def ensure_pipx():
    """Ensure pipx is installed"""
    global state
    try:
        subprocess.run("pipx --version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        state['pipx_installed'] = True
    except subprocess.CalledProcessError:
        print("pipx not found, installing pipx...")
        run_command("pip install pipx", shell=True)
        run_command("pipx ensurepath", shell=True)
        state['pipx_installed'] = True

def ensure_pdm():
    """Ensure pdm is installed via pipx"""
    global state
    try:
        output = subprocess.run("pipx list", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if b'pdm' not in output.stdout:
            raise KeyError('pdm not found in pipx list')
        print("pdm is already installed.")
        state['pdm_installed'] = True
    except (subprocess.CalledProcessError, KeyError):
        print("pdm not found, installing pdm...")
        run_command("pipx install pdm", shell=True)
        state['pdm_installed'] = True


def create_virtualenv():
    """Create a virtual environment and activate it using pdm"""
    global state
    os.environ["PDM_VENV_IN_PROJECT"] = "1"
    venv_path = ".venv"
    if os.path.exists(venv_path):
        choice = input("Virtual environment already exists. Overwrite? (y/n): ").lower()
        if choice == 'y':
            print("Deactivating and deleting existing virtual environment...")
            ensure_delete(venv_path)
            print("Virtual environment deleted.")
            run_command("pdm venv create", shell=True)
        else:
            print("Reusing the existing virtual environment.")
    else:
        run_command("pdm venv create", shell=True)
    run_command("pdm lock", shell=True)
    run_command("pdm install", shell=True, verbose=True)
    state['virtualenv_created'] = True
    state['dependencies_installed'] = True


def prompt_for_mode():
    """Prompt the user to choose between development and non-development setup"""
    while True:
        choice = input("Choose setup mode: [d]evelopment or [n]on-development? ").lower()
        if choice in ['d', 'n']:
            return choice
        print("Invalid choice, please enter 'd' or 'n'.")


def install():
    """Run installation"""
    run_command("pdm install", shell=True, verbose=True)

def lint():
    """Run linting tools"""
    global state
    run_command("pdm run flake8 .", shell=True)
    run_command("pdm run black --check .", shell=True)
    run_command("pdm run mypy .", shell=True)
    state['lint_passed'] = True

def format_code():
    """Format the code"""
    global state
    run_command("pdm run black .", shell=True)
    run_command("pdm run isort .", shell=True)
    state['code_formatted'] = True

def test():
    """Run tests"""
    global state
    run_command("pdm run pytest", shell=True)
    state['tests_passed'] = True

def bench():
    """Run benchmarks"""
    global state
    run_command("pdm run python src/bench/bench.py", shell=True)
    state['benchmarks_run'] = True

def pre_commit_install():
    """Install pre-commit hooks"""
    global state
    run_command("pdm run pre-commit install", shell=True)
    state['pre_commit_installed'] = True

def introspect():
    """Introspect the current state and print results"""
    print("Introspection results:")
    for key, value in state.items():
        print(f"{key}: {'✅' if value else '❌'}")


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            try:
                wizard()
                helped()
                pmain = sys.argv[1+len(sys.argv)//2]
                main(pmain)
                sys.argv.pop(1)
                pass
            except Exception as e:
                logger=logging.getLogger(__name__).exception(f'Error in parallel execution: {e}')
                print(e)
                sys.exit(1)
        else:
            # No arguments provided, call main() without arguments
            wizard()
            helped()
            main()
    except:
        ArgumentParser(description='Run the main function in parallel for each argument.')

    try:
        atom = AtomicData(data=b"Some data")
        print(atom.encode())

        theory = FormalTheory()
        print(theory.encode())

        context_manager = ThreadSafeContextManager()
        with context_manager:
            print("Thread-safe operation")

        arena = ThreadLocalScratchArena()
        arena.set(AtomicData(data="Thread-local data"))
        print(arena.get())
    except Exception as e:
        print(e)
        raise e
    finally:
        pass