import asyncio
import logging
import os
from pathlib import Path
import argparse
import subprocess
import sys
import uuid
import datetime
import threading
import json
import shutil
from functools import reduce
from typing import Callable, TypeVar, List, Optional, Union, Any, Tuple, Dict
from logging.config import dictConfig

from src.symbolic_kernel.kernel import SymbolicKernel
from src.symbolic_kernel.file_manager import FileSystemManager
from src.symbolic_kernel.memory_manager import MemoryManager
from src.symbolic_kernel.cpu_scheduler import CPUScheduler
from src.symbolic_kernel.llama_interface import LlamaInterface

T = TypeVar('T')

state = {
    "pipx_installed": False,
    "pdm_installed": False,
    "virtualenv_created": False,
    "dependencies_installed": False,
    "dev_mode": False,
    "lint_passed": False,
    "code_formatted": False,
    "tests_passed": False,
    "benchmarks_run": False,
    "pre_commit_installed": False,
}

def __timestamp__() -> str:
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    timestamp += f'_{str(uuid.uuid4())}'
    return timestamp.replace('-', '').replace(':', '').replace('.', '')

def introspect():
    """Introspect the current state and print results"""
    print("Introspection results:")
    for key, value in state.items():
        print(f"{key}: {'✅' if value else '❌'}")

def split_command(command):
    """A basic command splitting function for Windows"""
    return command.split()

def run_command(command, check=True, shell=False, verbose=False):
    """Utility to run a shell command and handle exceptions"""
    if verbose:
        command += " -v"
    
    try:
        if shell:
            result = subprocess.run(command, check=check, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            result = subprocess.run(split_command(command), check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        stdout = result.stdout.decode('utf-8', errors='replace')
        stderr = result.stderr.decode('utf-8', errors='replace')
        
        print(stdout)
        if stderr:
            print(f"Error: {stderr}", file=sys.stderr)
        
        return stdout, stderr
    
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode('utf-8', errors='replace') if e.stderr else 'Unknown error'
        print(f"Command '{command}' failed with error:\n{stderr}")
        if check:
            sys.exit(e.returncode)
        return '', stderr
    
    except Exception as e:
        print(f"An unexpected error occurred while running command '{command}': {str(e)}")
        if check:
            sys.exit(1)
        return '', str(e)

def _setup() -> logging.Logger:
    """Configures logging & paths for the app."""
    current_dir = Path(__file__).resolve().parent
    logs_dir = current_dir / "logs"

    # Find project root
    while not (current_dir / 'src').exists():
        current_dir = current_dir.parent
        if current_dir == Path('/'):
            raise Exception("Unable to find project root")

    logs_dir.mkdir(exist_ok=True)

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
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': 'INFO',
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(logs_dir / 'app.log'),
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

    try:
        output_path = current_dir / "output"
        output_path.mkdir(parents=True, exist_ok=True)
        media_path = current_dir / "media"
        media_path.mkdir(parents=True, exist_ok=True)
        kb_path = current_dir / "kb"
        kb_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Error creating directories: {e}")
        raise e

    logger.info(f"Timestamp: {__timestamp__()}")
    logger.info(f"Threading hash: {hash(threading)}")
    logger.info(f"Invocation dir: {current_dir}")
    logger.info(f"Src dir: {current_dir}")
    logger.info(f"Media dir # of items: {len(list(media_path.glob('*')))},  Output dir # of items: {len(list(output_path.glob('*')))}")
    logger.info(f"Media dir size: {media_path.__sizeof__()} bytes, Output dir size: {output_path.__sizeof__()} bytes")
    logger.info(f"KB # of items: {len(list(kb_path.glob('*')))}")
    logger.info(f"KB dir size: {kb_path.__sizeof__()} bytes")

    return logger

def parse_arguments():
    parser = argparse.ArgumentParser(description="Abraxus Project Setup")
    parser.add_argument('--mode', choices=['install', 'lint', 'format', 'test', 'bench', 'pre-commit'],
                        help="Mode of operation")
    parser.add_argument('--run_user_main', action='store_true',
                        help="Run user-defined main function if available")
    return parser.parse_args()

def update_path():
    os.environ["PATH"] = f"{os.path.dirname(os.path.abspath(__file__))}/.venv/bin:" + os.environ["PATH"]

def ensure_pipx():
    try:
        run_command("pipx --version", check=True)
        state['pipx_installed'] = True
    except subprocess.CalledProcessError:
        run_command(f"{sys.executable} -m pip install --user pipx", check=True)
        run_command(f"{sys.executable} -m pipx ensurepath", check=True)
        state['pipx_installed'] = True

def ensure_pdm():
    try:
        run_command("pdm --version", check=True)
        state['pdm_installed'] = True
    except subprocess.CalledProcessError:
        run_command("pipx install pdm", check=True)
        state['pdm_installed'] = True
    try:
        result = subprocess.run(
            ["python", "-m", "pdm", "self", "update"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while updating pdm: {e.stderr.decode()}")




def _init(mode):
    """Run initilization in the specified/current mode."""
    if mode == 'dev':
        run_command("pdm install", shell=True)
        state['dependencies_installed'], state['dev mode'] = True
    elif mode == 'install':
        try:
            stdout, stderr = run_command("pipx list")
            if "cognosis" in stdout:
                print("Cognosis is already installed with pipx.")
                raise Exception("Cognosis is already installed with pipx. No need to install it again.")
        except Exception as e:
            print(f"Error: {e}")
            raise
        run_command("pdm install", shell=True)
        state['dependencies_installed'] = True

    elif mode == 'lint':
        lint()
    elif mode == 'format':
        format_code()
    elif mode == 'test':
        test()
    elif mode == 'bench':
        bench()
    elif mode == 'pre-commit':
        pre_commit_install()
    else:
        raise ValueError(f"Invalid mode: {mode}")


def lint():
    if not state['lint_passed']:
        run_command("pdm run lint", check=True)
        state['lint_passed'] = True

def format_code():
    if not state['code_formatted']:
        run_command("pdm run format", check=True)
        state['code_formatted'] = True

def test():
    if not state['tests_passed']:
        run_command("pdm run test", check=True)
        state['tests_passed'] = True

def bench():
    if not state['benchmarks_run']:
        run_command("pdm run bench", check=True)
        state['benchmarks_run'] = True

def pre_commit_install():
    if not state['pre_commit_installed']:
        run_command("pdm add pre-commit && pdm run pre-commit install", shell=True)
        state['pre_commit_installed'] = True

async def async_main():
    args = parse_arguments()
    logger = _setup()
    logger.info("Starting cognosis project setup...")

    update_path()
    ensure_pipx()
    ensure_pdm()

    if args.mode:
        mode = args.mode
    else:
        mode = "install"

    _init(mode)

    if args.run_user_main:
        try:
            from user_main import main as user_main
            logger.info("Running user-defined main function.")
            await user_main()
        except ImportError:
            logger.error("user_main module not found. Ensure you have a user_main.py file with a main() function.")
    
    logger.info("cognosis project setup complete.")

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
