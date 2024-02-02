import os
import queue
import logging
from logging.config import dictConfig
from logging.handlers import QueueHandler, QueueListener

class LoggerManager:
    def __init__(self, log_file_path: str, branch_name: str = 'branch', leaf_name: str = None):
        self.log_file_path = log_file_path
        self.branch_name = branch_name
        self.leaf_name = leaf_name
        self.LOGGING_CONFIG = {
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
                    'filename': self.log_file_path,
                    'maxBytes': 10485760,
                    'backupCount': 10
                },
                'queue': {
                    'class': 'logging.handlers.QueueHandler',
                    'queue': queue.Queue(-1),
                }
            },
            'loggers': {
                '': {
                    'level': 'DEBUG',
                    'handlers': ['queue'],
                    'propagate': True
                },
                self.branch_name: {
                    'level': 'DEBUG',
                    'handlers': [],
                    'propagate': True
                },
                f'{self.branch_name}.{self.leaf_name}': {
                    'level': 'DEBUG',
                    'handlers': [],
                    'propagate': True  
                }
            },
            'root': {
                'level': 'INFO',
                'handlers': ['console', 'file']
            }
        }

    def init_logging(self):
        # Ensure log directory exists
        log_directory = os.path.dirname(self.log_file_path)
        if not os.path.exists(log_directory):
            try:
                os.makedirs(log_directory)
            except OSError as e:
                print(f"Error creating log directory: {e}")
                raise

        # Apply the logging configuration
        dictConfig(self.LOGGING_CONFIG)

        # Create a listener for the queue
        queue_listener = QueueListener(
            self.LOGGING_CONFIG['handlers']['queue']['queue'], 
            self.LOGGING_CONFIG['handlers']['console'], 
            self.LOGGING_CONFIG['handlers']['file'],
            respect_handler_level=True
        )

        # Start the listener
        queue_listener.start()

        # Return the loggers
        root_logger = logging.getLogger()
        branch_logger = logging.getLogger(self.branch_name)
        leaf_logger = logging.getLogger(f"{self.branch_name}.{self.leaf_name}")

        return root_logger, branch_logger, leaf_logger
