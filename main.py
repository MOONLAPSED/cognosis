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


# A globally defined lock (_lock) is used when setting the logging
# configuration to prevent other threads from interfering with this process.
# Once the configuration is set, you should not need to use the lock for
# regular logging operations as the logging module itself handles thread
# safety during message logging. Thus, messages logged from submodules or
# from different threads will still be passed to their parent loggers
# and eventually up to the root logger, and the messages will be safely
# written to the console or file as specified in the configuration.
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
        raise SystemExit(1)
    finally:
        logging.info("Paths initialized.")

def __starter():
    """Platform-agnostic .env initialization"""  # agnostic but only works on windows, lol
    if os.name == 'nt':
        subprocess.run('copy /Y .env.example .env', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run('pip install -r requirements.txt', shell=True, check=True)
    _initialize_paths()
    return True

def main():
    __starter()
    logging.info("Main function started.")

    # A globally defined lock (_lock) is used when setting the logging
    # configuration to prevent other threads from interfering with this process.
    # Once the configuration is set, you should not need to use the lock for
    # regular logging operations as the logging module itself handles thread
    # safety during message logging. Thus, messages logged from submodules or
    # from different threads will still be passed to their parent loggers
    # and eventually up to the root logger, and the messages will be safely
    # written to the console or file as specified in the configuration.
    _lock = threading.Lock()
    with _lock:
        try:
           while True:
              logging.info("main runtime achieved.")
              time.sleep(1)
              text = "main runtime achieved."
              for char in text:
                    logging.info(char)
                    print(char, end="", flush=True)
                    time.sleep(0.05)
        except Exception:
            logging.error("Error setting up logging", exc_info=True)
            raise SystemExit(1)
        finally:
            logging.info("Logging initialized.")

if __name__ == "__main__":
    main()