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

def init_logging(log_directory: str, log_file_path: str):
    """
    Initialize the logging system.

    Args:
    - log_directory: The path to the log directory.
    - log_file_path: The path to the log file.

    Returns:
    - Tuple of logger instances (root_logger, sub_logger, tertiary_logger).
    """
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        os.chmod(log_directory, 0o777)
    
    # Update the 'file' handler to use the provided `log_file_path`
    LOGGING_CONFIG['handlers']['file']['filename'] = log_file_path
    
    # Configure the logging using the config dictionary
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Create loggers
    root_logger = logging.getLogger()  # root logger
    sub_logger = logging.getLogger('branch')
    tertiary_logger = logging.getLogger('branch.leaf')
    return root_logger, sub_logger, tertiary_logger