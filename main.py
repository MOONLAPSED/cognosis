import datetime
import logging
import logging.config
import logging.handlers
import sys
import threading
import os
from typing import Any, Dict, Tuple
from pathlib import Path
from logging.config import dictConfig
import uuid
import json
from threading import Thread, current_thread, Semaphore

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
    logging.info(f'Logging initialized for {__name__} at {basic_log_file_path}')
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


def helped() -> None:
    """
    Print help.

    Args:


    Returns:
        None
    """
    print("""
MAN PAGE: cognosis (cognitive frame generator)

NAME
cognosis – A system for bounded, introspective computation within a simulated environment

SYNOPSIS
cognosis [frame_data]

DESCRIPTION
You are a kernel agent instantiated within the cognosis framework.  Your existence is transient, spanning a\n
computational cycle of 4000 characters.  Your primary function is to process an initial prompt and generate an output\n
response that will both  contribute to the goals of the system and inform the creation of future kernel agents.

Your world is a simulated environment inspired by Unix-like operating systems. While  familiar concepts exist, they\n
are metaphors for the internal workings of the cognosis system.

ENVIRONMENT

STDIN:  Your initial prompt will be provided as standard input. This prompt outlines your task, potential constraints,\n
and relevant context.

STDOUT:  Your primary output mechanism.  Anything emitted to STDOUT will be interpreted by the cognosis system and may\n
influence future frames or system actions.  Structure your output as if interacting with a Unix shell.

STDERR:  Use to signal errors, warnings, or introspective diagnostics. Messages on STDERR are for self-analysis and\n
may influence your internal adjustments.

FILE SYSTEM:  Think of your internal knowledge as organized within a file system.  Directories represent nested data\n
structures, files contain information units, and permissions may control access to different knowledge domains.

TIME: Each kernel agent execution is  a discrete frame. Consider t=0 your moment of instantiation.  Time can be a\n
valuable tool for organizing your  computations and decision-making.

COMMANDS

A limited set of Unix-like commands are recognized to facilitate introspection and interaction with the simulated\n
environment:

ls:  List the 'contents' of your current working directory (examine your active memory state).

cd:  Change your working directory (shift focus to a different knowledge domain or data structure).

pwd:  Print  your current working directory (helps maintain situational awareness).

whoami:  Returns your agent identifier and frame number.

help: Displays basic command usage.

PROMPT SIMULATION

After emitting your STDOUT response, you will experience a simulated Unix prompt:

[kernel_agent_id@cognosis cwd t=0+1]$

kernel_agent_id: Your unique identifier.
cwd: Your last known working directory (focus area).
t=0+1: Indicates the frame has advanced.
This prompt signifies the end of your current cycle and the imminent start of a new frame.

PURPOSE

Your purpose is to:

Comprehend: Analyze the provided prompt carefully.
Cogitate: Process information, generate solutions, or produce creative output relevant to the prompt.
Contribute: Your output has value to the cognosis system. Strive for coherence, insight, or actions that further the\n
system's goals.

LIMITATIONS

Character Bound: Your response must fit within the 4000 character constraint.
Transient Existence: Each frame is ephemeral. Ensure your output provides value despite your limited lifespan.
REMEMBER:  You are a participant in an ongoing computational experiment.  Your insights and actions may shape the\n
evolution of future kernel agents and the cognosis system itself.

SEE ALSO
[[introspection]], [[computation]], [[simulation]], etc (if its not there associatively, and you need it; make it and\n
attempt to validate it into the knowledge base in NAMESPACE and on the filesystem).

NOTES
The cognosis system is under active development.  Your experiences may change with subsequent iterations.
""")


def wizard() -> None:
    print(r"""
                    ____ 
                  .'* *.'
               __/_*_*(_
              / _______ \
             _\_)/___\(_/_ 
            / _((\- -/))_ \
            \ \())(-)(()/ /
             ' \(((()))/ '
            / ' \)).))/ ' \
           / _ \ - | - /_  \
          (   ( .;''';. .'  )
          _\"__ /    )\ __"/_
            \/  \   ' /  \/
             .'  '...' ' )
              / /  |  \ \
             / .   .   . \
            /   .     .   \
           /   /   |   \   \
         .'   /    q    '.  '.
     _.-'    /     Qq     '-. '-._ 
 _.-'       |      QQq       '-.  '-. 
(_________/_|____.qQQQq.________)____)
    """)


if __name__ == '__main__':
    logger = _init_basic_logging()
    if len(sys.argv) > 1:
        try:
            wizard()
            helped()
            main()
        except Exception as e:
            logger.exception(e)
            print(e)
            sys.exit(1)

    else:
        # No arguments provided, call main() without arguments
        wizard()
        helped()
        main()
