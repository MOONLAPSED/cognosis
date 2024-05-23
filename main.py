import datetime
import json
import logging
import logging.config
import logging.handlers
import operator
import os
import sys
import threading
import uuid
from pathlib import Path
from functools import reduce
from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging.config import dictConfig
from typing import Callable, TypeVar, List, Optional, Union, Any, Tuple, Dict, NamedTuple, Set
from threading import Thread, current_thread, Semaphore
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser

from src.utils.kb import KnowledgeItem, FileContextManager
from src.utils.helpr import helped, wizard


# Setup paths
vault_path = Path(__file__).parent / "my_vault"  # Your knowledge base directory
templates_path = Path(__file__).parent / "templates"
output_path = Path(__file__).parent / "output"
output_path.mkdir(parents=True, exist_ok=True)
_lock = threading.Lock()

def _init_basic_logging():
    basic_log_file_path = Path(__file__).resolve().parent.joinpath('logs', 'setup.log')
    basic_log_file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the logs directory exists
    logging.basicConfig(
        filename=str(basic_log_file_path),  # Convert Path object to string for compatibility
        level=logging.INFO,
        format='[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
        datefmt='%Y-%m-%d~%H:%M:%S%z',
    )
    logging.info(f'Logging initialized for {__name__}')
    return logging.getLogger(__name__)

# Initialize basic logging immediately to capture any issues during module import.
_init_basic_logging()

def main(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> logging.Logger:
    """Configures logging for the app.

    Args:
        *args: Positional arguments to be passed to the function.
        **kwargs: Keyword arguments to be passed to the function.

    Returns:
        logging.Logger: The logger for the module.
    """
    for arg in args:
        print(arg)
        pass
    for arg in kwargs:
        print(arg)
        pass
    # Find the current directory for logging
    current_dir = Path(__file__).resolve().parent
    while not (current_dir / 'logs').exists():
        current_dir = current_dir.parent
        if current_dir == Path('/'):
            break
    # Ensure the logs directory exists
    logs_dir = Path(__file__).resolve().parent.joinpath('logs')
    logs_dir.mkdir(exist_ok=True)
    # Add paths for importing modules
    sys.path.append(str(Path(__file__).resolve().parent))
    sys.path.append(str(Path(__file__).resolve().parent.joinpath('src')))
    run_id = os.getenv("GITHUB_RUN_ID")
    if run_id:
        print(f"Workflow run ID: {run_id}")
    with _lock:
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
                    'level': 'INFO',  # Explicitly set level to 'INFO'
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                    'stream': 'ext://sys.stdout'
                },
                'file': {
                    'level': 'INFO',  # Explicitly set level to 'INFO'
                    'formatter': 'default',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': str(logs_dir / 'app.log'),  # Convert Path object to string for compatibility
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 10
                }
            },
            'root': {
                'level': logging.INFO,
                'handlers': ['console', 'file']
            }
        }

        dictConfig(logging_config)

        logger = logging.getLogger(__name__)
        logger.info(f'Logging_dir {logs_dir}|'
                    f'\nSource_file: {__file__}|'
                    f'\nInvocation_dir: {Path(__file__).resolve().parent}|'
                    f'\nWorking_dir: {current_dir}||')

        arguments = [_ for _ in str(sys.argv).lower().strip().split(' ') if len(_) > 0]
        if len(arguments) > 1:
            logger.debug(f'Arguments: {arguments}')
            runtime_arguments = {}
            for arg in arguments:
                if arg == '-h':
                    helped()
                    sys.exit()
                elif str(arg).startswith('-'):
                    print(f'Unrecognized argument: {arg}')
                elif len(str(arg).strip()) >= 5_000:
                    print(f'Argument is too long: {arg}')
                # '--h' for args and flags of invocations of cognosis
                elif arg.startswith('~'):
                    print(f'Argument starts with tilde: {arg}')
                # '--v' verbose debugging for invocations of cognosis, their args, flags, and curried/runtime args
                elif arg.startswith('!'):
                    print(f'Argument starts with exclamation point: {arg}')
                else:
                    # Generate a timestamp as the key
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    timestamp += f'_{str(uuid.uuid4())}'
                    timestamp = timestamp.replace('-', '')
                    timestamp = timestamp.replace(':', '')
                    timestamp = timestamp.replace('.', '')
                    hash_key = f'{timestamp}_{arg}'
                    runtime_arguments[hash_key] = arg
                    logger.debug(f'Argument: {arg}|{hash_key}')
                rtjson_path = os.path.join(output_path, 'runtime_arguments.json')
                with open(str(rtjson_path), 'w') as f:
                    json.dump(runtime_arguments, f, indent=4)
        else:
            logger.debug(f'No arguments provided.')

        return logger


if __name__ == '__main__':
    logger = _init_basic_logging()
    try:
        if len(sys.argv) > 1:
            try:
                wizard()
                helped()
                pmain = sys.argv[1+len(sys.argv)//2]
                main(pmain)
                sys.argv.pop(1)
                pass
            except Exception as e:
                logger.exception(e)
                print(e)
                sys.exit(1)
        else:
            # No arguments provided, call main() without arguments
            wizard()
            helped()
            main()
    except:
        ArgumentParser(description='Run the main function in parallel for each argument.')
