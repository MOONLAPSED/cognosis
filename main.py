# ~/main.py - Runtime for Cognosis, curryable (usermain())
import asyncio
import logging
import platform
from dataclasses import dataclass, field
from functools import partial
from struct import Struct
from typing import Any, Callable, Dict, TypeVar, List, Tuple
from typing import Union, Type, Optional, ClassVar, Generic
from enum import Enum, auto
from abc import ABC, abstractmethod
import argparse
import os
import subprocess
import sys
import logging
import pathlib

state: Dict[str, bool] = {
    k: False for k in [
        "pdm_installed", "virtualenv_created", "dependencies_installed",
        "lint_passed", "code_formatted", "tests_passed",
        "benchmarks_run", "pre_commit_installed"
    ]
}

def run_command(command: str, check: bool = True, shell: bool = False, timeout: int = 120) -> Dict[str, Any]:
    try:
        process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=timeout)

        if check and process.returncode != 0:
            logging.error(f"Command '{command}' failed with return code {process.returncode}")
            logging.error(f"Error output: {stderr.decode('utf-8')}")
            return {
                "return_code": process.returncode,
                "output": stdout.decode("utf-8"),
                "error": stderr.decode("utf-8")
            }

        logging.info(f"Command '{command}' completed successfully")
        logging.debug(f"Output: {stdout.decode('utf-8')}")

    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        logging.error(f"Command '{command}' timed out and was killed.")
        return {
            "return_code": -1,
            "output": stdout.decode("utf-8"),
            "error": "Command timed out"
        }
    except Exception as e:
        logging.error(f"An error occurred while running command '{command}': {str(e)}")
        return {
            "return_code": -1,
            "output": "",
            "error": str(e)
        }

    return {
        "return_code": process.returncode,
        "output": stdout.decode("utf-8"),
        "error": stderr.decode("utf-8")
    }

class Logger:
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        if not self.logger.handlers:
            for handler in [logging.StreamHandler(), logging.FileHandler(f"{name}.log")]:
                handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
                self.logger.addHandler(handler)
            self.logger.info(f"Logger {name} initialized.")

    def log(self, message: str, level: int = logging.INFO):
        try:
            self.logger.log(level, message)
        except Exception as e:
            logging.error(f"Failed to log message: {e}")

    def debug(self, message: str):
        self.log(message, logging.DEBUG)

    def info(self, message: str):
        self.log(message, logging.INFO)

    def warning(self, message: str):
        self.log(message, logging.WARNING)

    def error(self, message: str, exc_info=None):
        self.logger.error(message, exc_info=exc_info)

logger = Logger("MainLogger")
def log_error(error: Exception): #usermain() logger wrapper
    logger.error(f"Error occurred: {error}")

def setup_app():
    """Setup the application"""
    global state
    if not state["pdm_installed"]:
        ensure_pdm()
    if not state["virtualenv_created"]:
        ensure_virtualenv()
    if not state["dependencies_installed"]:
        ensure_dependencies()

    mode = prompt_for_mode()
    if mode == "dev":
        ensure_lint()
        ensure_format()
        ensure_tests()
        ensure_benchmarks()
        ensure_pre_commit()
    introspect()

def ensure_pdm():
    """Ensure pdm is installed"""
    if not state["pdm_installed"]:
        try:
            subprocess.run("pdm --version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            state["pdm_installed"] = True
            logging.info("pdm is already installed.")
        except subprocess.CalledProcessError:
            logging.info("pdm not found, installing pdm...")
            run_command("pip install pdm", shell=True)
            state["pdm_installed"] = True

def ensure_virtualenv():
    """Ensure the virtual environment is created"""
    if not state["virtualenv_created"]:
        if not os.path.exists(".venv"):
            run_command("pdm venv create", shell=True)
        state["virtualenv_created"] = True
        logging.info("Virtual environment already exists.")

def ensure_dependencies():
    """Install dependencies"""
    run_command("pdm install --project ./", shell=True)
    state["dependencies_installed"] = True

def ensure_lint():
    """Run linting tools"""
    run_command("pdm run flake8 .", shell=True)
    run_command("pdm run black --check .", shell=True)
    run_command("pdm run mypy .", shell=True)
    state["lint_passed"] = True

def ensure_format():
    """Format the code"""
    run_command("pdm run black .", shell=True)
    run_command("pdm run isort .", shell=True)
    state["code_formatted"] = True

def ensure_tests():
    """Run tests"""
    run_command("pdm run pytest", shell=True)
    state["tests_passed"] = True

def ensure_benchmarks():
    """Run benchmarks"""
    run_command("pdm run python src/bench/bench.py", shell=True)
    state["benchmarks_run"] = True

def ensure_pre_commit():
    """Install pre-commit hooks"""
    run_command("pdm run pre-commit install", shell=True)
    state["pre_commit_installed"] = True

def prompt_for_mode():
    """Prompt the user to choose between development and non-development setup"""
    while True:
        choice = input("Choose setup mode: [d]evelopment or [n]on-development? ").lower()
        if choice in ["d", "n"]:
            return choice
        logging.info("Invalid choice, please enter 'd' or 'n'.")

def introspect():
    """Introspect the current state and print results"""
    logging.info("Introspection results:")
    for key, value in state.items():
        logging.info(f"{key}: {'✅' if value else '❌'}")


logger.info(f"Starting main.py on {platform.system()}")

async def usermain(failure_threshold=10) -> bool:
    user_logger = logging.getLogger("UserMainLogger")
    user_logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    user_logger.addHandler(ch)

    async def rtkernel() -> bool:
        user_logger.info("The user has control of the application kernel.")
        # logic that requires a thread, etc.
        return True

    try:
        result = await rtkernel()
        if result:
            user_logger.info("usermain successful, returns True")
            return True
    except Exception as e:
        user_logger.error(f"Failed with error: {e}")
        return False

    failure_count = sum(1 for _ in range(failure_threshold) if not await rtkernel())
    failure_rate = failure_count / failure_threshold
    user_logger.info(f"Failure rate: {failure_rate:.2%}")
    return failure_rate < 1.0

CurriedUsermain = partial(usermain, failure_threshold=10)

async def main():
    try:
        if isinstance(CurriedUsermain, partial):
            try:
                await asyncio.wait_for(CurriedUsermain(), timeout=60)
            except asyncio.TimeoutError:
                logger.error("CurriedUsermain timed out")
            except Exception as e:
                log_error(e)
        else:
            await CurriedUsermain()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
    finally:
        logger.info("Exiting...")

if __name__ == "__main__":
    asyncio.run(main())

async def run_usermain():
    try:
        await usermain()  # Ensure usermain is run as async function
    except ImportError:
        logging.error("No user-defined main function found. Please add a main.py file and define a usermain() function.")
    except Exception as e:
        logging.error(f"An error occurred while running usermain: {str(e)}", exc_info=True)

def rtmain():
    ensure_pdm()
    ensure_virtualenv()
    parser = argparse.ArgumentParser(description="Setup and run cognosis project")
    parser.add_argument("-m", "--mode", choices=["dev", "non-dev"], help="Setup mode: 'dev' or 'non-dev'")
    parser.add_argument("-u", "--skip-user-main", action="store_true", help="Skip running the user-defined main function")
    args = parser.parse_args()
    mode = args.mode
    if not mode:
        choice = prompt_for_mode()
        mode = "dev" if choice == "d" else "non-dev"

    ensure_dependencies()

    if mode == "dev":
        ensure_lint()
        ensure_format()
        ensure_tests()
        ensure_benchmarks()
        ensure_pre_commit()

    if not args.skip_user_main:
        try:
            asyncio.run(run_usermain())
        except Exception as e:
            logging.error(f"An error occurred while running usermain: {str(e)}", exc_info=True)

    introspect()

if __name__ == "__main__":
    rtmain()