import logging
import logging.config
import logging.handlers
import os
import sys
import subprocess
import threading
from dataclasses import dataclass, field

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
        format='[%(levelname)s] %(asctime)s || %(name)s: %(message)s',
        datefmt='%Y-%m-%d~%H:%M:%S%z',
    )

# Initialize basic logging immediately to capture any issues during module import.
_init_basic_logging()

class CustomLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

    def error(self, msg, *args, exc_info=True, **kwargs):
        super().error(msg, *args, exc_info=exc_info, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        super().exception(msg, *args, exc_info=exc_info, **kwargs)
    

# Override the class used when instantiating a logger
logging.setLoggerClass(CustomLogger)

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
        with _lock:
            logging.config.dictConfig(LoggingDataClass.get_config())
            logging.getLogger(__name__).info("Paths and logging initialized.")


@dataclass(frozen=True)
class LoggingDataClass:
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = field(default_factory=lambda: {
        'default': {
            'format': '[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
            'datefmt': '%Y-%m-%d~%H:%M:%S%z'
        }
    })
    handlers: dict = field(default_factory=lambda: {
        'console': {
            'level': logging.INFO,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': logging.INFO,
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.abspath(
                os.path.join(os.path.dirname(__file__), 'logs', 'app.log')),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10
        }
    })
    root: dict = field(default_factory=lambda: {
        'level': logging.INFO,
        'handlers': ['console', 'file']
    })

    @staticmethod
    def get_config():  
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': LoggingDataClass.formatters,
            'handlers': LoggingDataClass.handlers,
            'root': LoggingDataClass.root
        }


def __starter():
    """Platform-agnostic .env initialization"""  # agnostic but only works on windows, lol
    if os.name == 'nt':
        subprocess.run('copy /Y .env.example .env', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run('pip install -r requirements.txt', shell=True, check=True)
    
def __pipenv() -> tuple:
    """Wrapper for __starter(), handles potential errors"""
    try:
        __starter()
        mp = _initialize_paths()
        return mp
    except Exception as e:
        logging.error(f"Error installing dependencies: {e}", exc_info=True)
        raise SystemExit(1)
    
class MetaPoint:  # a spacetime diagram for the morphisim between a (locked/causal) root-logger and a runtime ephemeral and unlocked/causal branch-logger
    def __init__(self, content, logger_name=None):
       self.morphism = content
       if logger_name:
           self.logger = logging.getLogger(logger_name)
       else:
           self.logger = logging.getLogger(f"metapoint_{id(self)}")  # Unique fallback 

    def log_event(self, event_type, message):
        self.logger.info(f"{event_type}: {message}")
    # Systemic vs. Individual Temporality The contrast between the kernel agent's 'internal' clock and arbitrarily injected "ticks" from the Python runtime creates the dynamic tension and temporal duality

def main():
    mp = __pipenv()
    logging.getLogger(__name__).info("Cognosis initialized.")
    # ... runtime
    return 0

if __name__ == "__main__":
    sys.exit(main())