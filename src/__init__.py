# src/__init__.py

import sys
import os
import importlib
from importlib.util import spec_from_file_location, module_from_spec
import pathlib
import logging
import argparse

# Detect platform
IS_POSIX = os.name == 'posix'

# Setup custom logging format for enhanced error messages and debugging
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;20m"
    reset = "\x1b[0m"

    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.format)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger(name: str, level: int, datefmt: str, handlers: list):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    for handler in handlers:
        if not isinstance(handler, logging.Handler):
            raise ValueError(f"Invalid handler provided: {handler}")
        handler.setLevel(level)
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)

    return logger

def parse_args():
    parser = argparse.ArgumentParser(description="Logger Configuration")
    parser.add_argument('--log-level', type=str, default='DEBUG', choices=logging._nameToLevel.keys(), help='Set logging level')
    parser.add_argument('--log-file', type=str, help='Set log file path')
    parser.add_argument('--log-format', type=str, default='%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)', help='Set log format')
    parser.add_argument('--log-datefmt', type=str, default='%Y-%m-%d %H:%M:%S', help='Set date format')
    parser.add_argument('--log-name', type=str, default=__name__, help='Set logger name')
    return parser.parse_args()

def main():
    args = parse_args()
    log_level = logging._nameToLevel.get(args.log_level.upper(), logging.DEBUG)

    handlers = [logging.FileHandler(args.log_file)] if args.log_file else [logging.StreamHandler()]

    logger = setup_logger(name=args.log_name, level=log_level, datefmt=args.log_datefmt, handlers=handlers)
    logger.info("Logger setup complete.")

if __name__ == "__main__":
    main()

Logger = setup_logger("ApplicationBus", logging.DEBUG, "%Y-%m-%d %H:%M:%S", [logging.StreamHandler()])

# Platform-specific logic
def load_modules():
    try:
        mixins = []
        for path in pathlib.Path(__file__).parent.glob("*.py"):
            if path.name.startswith("_"):
                continue
            module_name = path.stem
            spec = spec_from_file_location(module_name, path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot load module {module_name}")
            module = module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            mixins.append(module)
        return mixins
    except Exception as e:
        Logger.error(f"Error importing internal modules: {e}")
        sys.exit(1)

# Import the internal modules
mixins = load_modules()

if mixins:
    __all__ = [mixin.__name__ for mixin in mixins]
else:
    __all__ = []

# Handle platform-specific dynamic linking logic
if IS_POSIX:
    try:
        from ctypes import cdll
        Logger.info("POSIX system detected.")
    except ImportError:
        Logger.error("Error loading POSIX dynamic linking libraries.")
else:
    try:
        from ctypes import windll
        Logger.info("Windows system detected.")
    except ImportError:
        Logger.error("Error loading Windows dynamic linking libraries.")
