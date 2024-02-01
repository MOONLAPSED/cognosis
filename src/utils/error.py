import logging
import datetime
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import logging
from logutils import *

"""plugs into: errors.py. See:
    # Update the 'file' handler to use the provided `log_file_path`
    LOGGING_CONFIG['handlers']['file']['filename'] = log_file_path
    
    # Configure the logging using the config dictionary
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Create loggers
    root_logger = logging.getLogger()  # root logger
    sub_logger = logging.getLogger('branch')
    tertiary_logger = logging.getLogger('branch.leaf')
    return root_logger, sub_logger, tertiary_logger
"""

def main():
    r, s = init_logging('logs')
    r.info('')
    s.info('')
    