import logging
import logging.config
import logging.handlers
import os
import sys
import subprocess
import threading
import time

# flow: 
# 1) This notes section, _lock function
# 2) _init_basic_logging
# 3)    invoke _init_basic_logging
# 4)    _initialize_paths # no invoked
# 5)        __starter # invokes _initialize_paths # returns True
# 6)


# configuration to prevent other threads from interfering with this process, especially during setup and teardown.
# A globally defined lock (_lock) is used when setting the logging:
_lock = threading.Lock()

def _init_basic_logging():
    basic_log_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'logs', 'setup.log'))
    logging.basicConfig(
        filename=basic_log_file_path,
        level=logging.INFO,
        format='[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
        datefmt='%Y-%m-%d~%H:%M:%S%z',
    )

# Initialize basic logging immediately to capture any issues during module import.
_init_basic_logging()

def _initialize_paths():
    try:
        project_root = os.path.abspath(os.path.dirname(__file__))
        os.environ['PROJECT_ROOT'] = project_root
        sys.path.extend([
            os.path.abspath(os.path.join(project_root, 'src')),
            project_root,
        ])
    except Exception as e:
        logging.error("Error setting up paths", exc_info=True)
        return False
    finally:
        logging.info("Paths initialized.")
    if __name__ == '__main__':
        logging.info(f"{__name__} running as main.")
    else:
        logging.info(f"{__name__} running as submodule.")

def __starter():
    with _lock:
        logging.info("Ensuring Rust and GCC are correctly installed and configured.")
    """Platform-agnostic .env initialization, dependency setup, and ensuring Rust and GCC are available for builds"""
    success = False  # Initialize success flag
    try:
        subprocess.run('curl --proto \'=https\' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y', shell=True, check=True)
        env_example_path = os.path.join(os.path.dirname(__file__), '.env.example')
        bashrc = os.path.join(os.path.dirname(__file__), 'docs', '.bashrc')
        if os.path.exists(env_example_path):
            if os.name == 'nt':
                subprocess.run(f'copy /Y {env_example_path} .env', shell=True, check=True)
                subprocess.run(f'copy /Y {bashrc} %USERPROFILE%\\.bashrc', shell=True, check=True)
                subprocess.run('source %USERPROFILE%\\.bashrc', shell=True, check=True)
            elif os.name == 'posix':
                subprocess.run(f'cp -f {env_example_path} .env', shell=True, check=True)
                subprocess.run(f'cp -f {bashrc} ~/.bashrc && source ~/.bashrc', shell=True, check=True)
        else:
            logging.error("Error: .env.example file does not exist.")
            return False  # Exit the function early if .env.example file is missing
        subprocess.run('pip install --upgrade pip', shell=True, check=True)
        subprocess.run('pip install pdm', shell=True, check=True)

        _initialize_paths()  # Set up paths

        # Attempt to install dependencies with PDM
        try:
            subprocess.run('pdm install', shell=True, check=True)
            success = True  # Set success flag if PDM install succeeds
        except subprocess.CalledProcessError as e:
            logging.error("PDM installation failed with error: {}".format(e), exc_info=True)
            success = False  # Explicitly set success to False to indicate failure

        # If PDM install fails, fall back to pip
        if not success:
            logging.warning("PDM setup failed, falling back to pip")
            subprocess.run('pip install -r requirements.txt', shell=True, check=True)
    except Exception as e:
        logging.critical("Critical error during setup: {}".format(e), exc_info=True)
        success = False  # Ensure success is False after a critical error
    finally:
        if success:
            logging.info("Dependencies installed successfully with PDM.")
        else:
            logging.error("Failed to install dependencies with PDM, attempted to utilize pip instead. This may have unknown consequences.")

__starter()


def main():
    __starter()
    logging.info("Main function started.")
    _lock = threading.Lock()
    with _lock:
        try:
          while True:
              logging.info("Main runtime achieved.")
              time.sleep(1)
              text = "Main runtime achieved.\n"
              for i in range(10):
                  for char in text:
                      logging.info(char)
                      print(char, end="", flush=True)
                      time.sleep(0.05)
              break
        except Exception as e:
            logging.error("Error during main function execution: {}".format(e), exc_info=True)
            raise SystemExit(1)
        finally:
            logging.info("Main function execution completed successfully.")
if __name__ == "__main__":
    main()