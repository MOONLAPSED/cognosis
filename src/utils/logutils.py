from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler 
import os
LOGGING_CONFIG = {
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
        },
        'file': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 10485760,
            'backupCount': 10
        }
    },
    'loggers': {
        'branch': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': True
        },
        'branch.leaf': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': True  
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
}

def init_logging(log_file_path: str):
    """
    Initialize the logging system.
    Args:
    - log_file_path: The path to the log file where logs will be stored.

    Returns:
    - Logger instances (root_logger).
    """
    ROOT_LOGGER_NAME = 'root'
    
    # Ensure log directory exists
    log_directory = os.path.dirname(log_file_path)
    if not os.path.exists(log_directory):
        try:
            os.makedirs(log_directory)
            # os.chmod(log_directory, 0o755)  # Reconsidered permissions for security reasons
        except OSError as e:
            print(f"Error creating log directory: {e}")
            raise
    
    LOGGING_CONFIG['handlers']['file']['filename'] = log_file_path
    dictConfig(LOGGING_CONFIG)
    
    root_logger = logging.getLogger(ROOT_LOGGER_NAME)
    
    return root_logger

# Usage:
log_directory = '/path/to/log/directory'
log_file_path = os.path.join(log_directory, 'app.log')
root_logger = init_logging(log_file_path)
# Now any other modules can simply use logging.getLogger() to inherit this setup configuration.