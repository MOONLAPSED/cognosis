#!/usr/bin/env python3
# /src/external/umain.py - usermain.py wrapper for loading the UserMain module located
# in /src/user/usermain.py to enable the UserMain to include external libraries.

import importlib.util
import os
import subprocess
import sys
import logging
import argparse
import asyncio

class ExternalMain:
    def __init__(self, external_dir: str = 'src/external', packages=None):
        self.external_dir = os.path.abspath(external_dir)
        self.packages = packages or []

    def _create_init_files(self):
        """Create empty __init__.py files in /src/external/ and its subdirectories if they don't exist."""
        if not os.path.exists(os.path.join(self.external_dir, '__init__.py')):
            open(os.path.join(self.external_dir, '__init__.py'), 'w').close()
        
        for subdir in os.listdir(self.external_dir):
            subdir_path = os.path.join(self.external_dir, subdir)
            if os.path.isdir(subdir_path):
                init_file = os.path.join(subdir_path, '__init__.py')
                if not os.path.exists(init_file):
                    open(init_file, 'w').close()

    def _install_dependencies(self, packages):
        """Install dependencies using pdm."""
        for package in packages:
            logging.info(f"Installing {package} with pdm...")
            result = subprocess.run(['pdm', 'add', package], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"Successfully installed {package}.")
            else:
                logging.error(f"Failed to install {package}. Error: {result.stderr}")

    def _initialize_external_modules(self):
        """Initialize external modules by creating init files."""
        self._create_init_files()

    def run(self):
        """Run the external setup and initialization."""
        self._install_dependencies(self.packages)
        self._initialize_external_modules()

def main():
    parser = argparse.ArgumentParser(description="Setup and run Cognosis project")
    parser.add_argument("-m", "--mode", choices=["dev", "non-dev", "pip"], help="Setup mode: 'dev', 'non-dev' or 'pip'")
    parser.add_argument("-u", "--skip-user-main", action="store_true", help="Skip running the user-defined main function")
    args = parser.parse_args()

    if args.mode == "dev":
        # Example: external libraries to be installed in dev mode can be passed through configuration
        external_main = ExternalMain(packages=['transformers', 'lib1', 'lib2'])
        external_main.run()

    if not args.skip_user_main:
        # Dynamically import usermain from /src/external/umain.py
        user_main_path = os.path.join('src', 'external', 'umain.py')
        if os.path.exists(user_main_path):
            spec = importlib.util.spec_from_file_location("UserMain", user_main_path)
            user_main_module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(user_main_module)
                if hasattr(user_main_module, 'usermain'):
                    asyncio.run(user_main_module.usermain())
                else:
                    logging.error("No user-defined main function 'usermain' found in umain.py")
            except Exception as e:
                logging.error(f"An error occurred while running usermain: {e}", exc_info=True)
        else:
            logging.error("The file umain.py does not exist in src/external")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()