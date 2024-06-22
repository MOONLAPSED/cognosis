# namespace context nspacecntxt.py

import datetime
import sys
import logging
from logging.config import dictConfig
from pathlib import Path
import importlib
import types
from abc import ABC, abstractmethod
import builtins
from types import SimpleNamespace


def setup_logging() -> logging.Logger:
    logs_dir = Path(__file__).resolve().parent / 'logs'
    logs_dir.mkdir(exist_ok=True)

    logging_config = {
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
                'level': logging.DEBUG,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': logging.DEBUG,
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': logs_dir / 'app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 10
            }
        },
        'root': {
            'level': logging.DEBUG,
            'handlers': ['console', 'file']
        }
    }

    dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    logger.info(f'Logging_dir {logs_dir}|'
                f'\nSource_file: {__file__}|'
                f'\nInvocation_dir: {Path(__file__).resolve().parent}|'
                f'\nWorking_dir: {logs_dir.parent}||')
    return logger

logger = setup_logging()

associative_links = {}

class ImportMonitor:
    def __init__(self):
        self.original_import = builtins.__import__
        self.logger = logging.getLogger('import_monitor')

    def __enter__(self):
        builtins.__import__ = self._custom_import
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        builtins.__import__ = self.original_import

    def _custom_import(self, name, globals=None, locals=None, fromlist=(), level=0):
        module = self.original_import(name, globals, locals, fromlist, level)
        self.logger.info(f'Imported module: {name}')
        associative_links[name] = {
            'type': 'ModuleType',
            'import_time': datetime.datetime.now()
        }
        return module

def main():
    with ImportMonitor():
        logger.info(f'||{__file__}_runtime()||')

        # Example usage of imported modules
        import os
        import json

        logger.info(f'os module runtime info: {associative_links.get("os")}')
        logger.info(f'json module runtime info: {associative_links.get("json")}')

if __name__ == '__main__':
    main()
    sys.exit(0)