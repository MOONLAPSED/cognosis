from __future__ import annotations
import datetime
import json
import logging
import logging.config
import logging.handlers
import operator
import os
import shutil
import subprocess
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


def __timestamp__() -> str:
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    timestamp += f'_{str(uuid.uuid4())}'
    timestamp = timestamp.replace('-', '')
    timestamp = timestamp.replace(':', '')
    timestamp = timestamp.replace('.', '')
    return timestamp


def main(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> logging.Logger:
    """Configures logging & paths for the app. Handles currying and MPI
    Args:
        *args: Positional arguments to be passed to the function.
        **kwargs: Keyword arguments to be passed to the function.
    Returns:
        logging.Logger: The logger for the module.
        runtime_arguments: The runtime arguments for the module, are 
            also saved in .json format in the logs dir.
        curried_arguments: The curried arguments for the module.
    """
    # Setup paths
    global _lock, output_path, media_path, logs_dir, current_dir
    _lock = threading.Lock()
    current_dir = Path(__file__).resolve().parent
    logs_dir = current_dir / "logs"

    # Find project root
    while not (current_dir / 'src').exists():
        current_dir = current_dir.parent
        if current_dir == Path('/'):
            raise Exception("Unable to find project root")

    logs_dir.mkdir(exist_ok=True)

    try:
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
                        'level': 'INFO',
                        'class': 'logging.StreamHandler',
                        'formatter': 'default',
                        'stream': 'ext://sys.stdout'
                    },
                    'file': {
                        'level': 'INFO',
                        'formatter': 'default',
                        'class': 'logging.handlers.RotatingFileHandler',
                        'filename': str(logs_dir / 'app.log'),
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

            arguments = [_ for _ in str(sys.argv).lower().strip().split(' ') if len(_) > 0]
            if len(arguments) > 1:
                logger.debug(f'Arguments: {arguments}')
                runtime_arguments = {}
                for arg in arguments:
                    if '-h' in arg:
                        print(f'Help: {__name__.__doc__}')
                        print(f"'-v' verbose debugging for invocations of cognosis, their args, flags, and curried/runtime args")
                        sys.exit()
                    elif len(str(arg).strip()) >= 5000:
                        print(f'Argument is too long: {arg}')
                    else:
                        # Generate a timestamp as the key
                        timestamp = __timestamp__()
                        hash_key = f'{timestamp}_{arg}'
                        runtime_arguments[hash_key] = arg
                        logger.debug(f'Argument: {arg}|{hash_key}')
                    rtjson_path = os.path.join(logs_dir, 'runtime_arguments.json')
                    with open(str(rtjson_path), 'a') as f:
                        json.dump(runtime_arguments, f, indent=4)
                        f.write('\n')
            else:
                logger.debug(f'No arguments provided.')
            try:
                # Create output and media directories
                output_path = current_dir / "output"
                output_path.mkdir(parents=True, exist_ok=True)
                media_path = current_dir / "media"
                media_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.error(f"Error creating directories: {e}")
                raise e

            logger.info(f"Timestamp: {__timestamp__()}")
            logger.info(f"Threading hash: {hash(threading)}")
            logger.info(f"Invocation dir: {current_dir}")
            logger.info(f"Src dir: {current_dir}")
            logger.info(f"Media dir size: {media_path.__sizeof__()} bytes, Output dir size: {output_path.__sizeof__()} bytes")
            return logger

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(f'Error in main(): {e}')
        raise e
    finally:
        if _lock.locked():
            _lock.release()


if __name__ == '__main__':
    main()
