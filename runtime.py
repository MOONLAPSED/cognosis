import argparse
import logging
import os
import platform
import subprocess
import sys
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

state = {
    "pdm_installed": False,
    "virtualenv_created": False,
    "dependencies_installed": False,
    "lint_passed": False,
    "code_formatted": False,
    "tests_passed": False,
    "benchmarks_run": False,
    "pre_commit_installed": False,
}


def run_command(
    command: str, check: bool = True, shell: bool = False
) -> Dict[str, Any]:
    """Utility to run a shell command and handle exceptions"""
    try:
        process = subprocess.Popen(
            command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        if check and process.returncode != 0:
            raise Exception(
                f"Command '{command}' failed with return code {process.returncode}"
            )

        logging.info(
            f"Command '{command}' returned {process.returncode}. Output: {stdout.decode('utf-8')}, Error: {stderr.decode('utf-8')}"
        )

    except FileNotFoundError as e:
        logging.error(f"Error running command '{command}': {str(e)}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{command}' failed with return code {e.returncode}.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

    return {
        "return_code": process.returncode,
        "output": stdout.decode("utf-8"),
        "error": stderr.decode("utf-8"),
    }


def update_path():
    home = os.path.expanduser("~")
    local_bin = os.path.join(home, ".local", "bin")
    if local_bin not in os.environ["PATH"]:
        os.environ["PATH"] = f"{local_bin}:{os.environ['PATH']}"
        logging.info(f"Added {local_bin} to PATH")


def ensure_pdm():
    """Ensure pdm is installed"""
    global state
    try:
        subprocess.run(
            "pdm --version",
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        state["pdm_installed"] = True
        logging.info("pdm is already installed.")
    except subprocess.CalledProcessError:
        logging.info("pdm not found, installing pdm...")
        run_command("pip install pdm", shell=True)
        state["pdm_installed"] = True


def prompt_for_mode():
    """Prompt the user to choose between development and non-development setup"""
    while True:
        choice = input(
            "Choose setup mode: [d]evelopment or [n]on-development? "
        ).lower()
        if choice in ["d", "n"]:
            return choice
        logging.info("Invalid choice, please enter 'd' or 'n'.")


def install(mode):
    """Run installation"""
    run_command("pdm install", shell=True)
    state["dependencies_installed"] = True


def lint():
    """Run linting tools"""
    global state
    run_command("pdm run flake8 .", shell=True)
    run_command("pdm run black --check .", shell=True)
    run_command("pdm run mypy .", shell=True)
    state["lint_passed"] = True


def format_code():
    """Format the code"""
    global state
    run_command("pdm run black .", shell=True)
    run_command("pdm run isort .", shell=True)
    state["code_formatted"] = True


def test():
    """Run tests"""
    global state
    run_command("pdm run pytest", shell=True)
    state["tests_passed"] = True


def bench():
    """Run benchmarks"""
    global state
    run_command("pdm run python src/bench/bench.py", shell=True)
    state["benchmarks_run"] = True


def pre_commit_install():
    """Install pre-commit hooks"""
    global state
    run_command("pdm run pre-commit install", shell=True)
    state["pre_commit_installed"] = True


def introspect():
    """Introspect the current state and print results"""
    logging.info("Introspection results:")
    for key, value in state.items():
        logging.info(f"{key}: {'✅' if value else '❌'}")


def update_shell_environment():
    if platform.system() != "Windows":
        home = os.path.expanduser("~")
        bashrc_path = os.path.join(home, ".bashrc")
        if os.path.exists(bashrc_path):
            subprocess.run(f"source {bashrc_path}", shell=True, executable="/bin/bash")
            logging.info("Updated shell environment from .bashrc")
        else:
            logging.info(".bashrc not found, shell environment might not be up to date")
    else:
        logging.info("On Windows, manual PATH update might be necessary")


def main():
    ensure_pdm()
    update_shell_environment()
    update_path()

    parser = argparse.ArgumentParser(description="Setup and run Abraxus project")
    parser.add_argument(
        "-m",
        "--mode",
        choices=["dev", "non-dev"],
        help="Setup mode: 'dev' or 'non-dev'",
    )
    parser.add_argument(
        "--run-user-main",
        action="store_true",
        help="Run the user-defined main function",
    )
    args = parser.parse_args()
    mode = args.mode
    if not mode:
        choice = prompt_for_mode()
        mode = "dev" if choice == "d" else "non-dev"

    install(mode)

    if mode == "dev":
        lint()
        format_code()
        test()
        bench()
        pre_commit_install()

    if args.run_user_main:
        try:
            import main

            main.usermain()
        except ImportError:
            logging.error(
                "No user-defined main function found. Please add a main.py file and define a usermain() function."
            )
    else:
        logging.info(
            "No additional arguments provided. Skipping user-defined main function."
        )

    introspect()


if __name__ == "__main__":
    main()
    update_path()
