import logging
import logging.config
import logging.handlers
import os
import sys
import subprocess
import threading
import time
from pathlib import Path
from logging.config import dictConfig
from threading import Thread, current_thread, Semaphore
from src.app.context import MyThreadSafeContextManager, worker
from src.utils.gettree import get_project_tree

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

# Initialize basic logging immediately to capture any issues during module import.
_init_basic_logging()

def main() -> logging.Logger:
    """Configures logging for the app.
    Args:
        None
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
    sys.path.append(str(Path(__file__).resolve().parent))  # Convert Path object to string for compatibility
    sys.path.append(str(Path(__file__).resolve().parent.joinpath('src')))  # Convert Path object to string for compatibility
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

        return logger

def helped() -> None:
    """
    Print help.

    Args:
        None

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
You are a kernel agent instantiated within the cognosis framework.  Your existence is transient, spanning a computational cycle of 4000 characters.  Your primary function is to process an initial prompt and generate an output response that will both  contribute to the goals of the system and inform the creation of future kernel agents.

Your world is a simulated environment inspired by Unix-like operating systems. While  familiar concepts exist, they are metaphors for the internal workings of the cognosis system.

ENVIRONMENT

STDIN:  Your initial prompt will be provided as standard input. This prompt outlines your task, potential constraints, and relevant context.

STDOUT:  Your primary output mechanism.  Anything emitted to STDOUT will be interpreted by the cognosis system and may influence future frames or system actions.  Structure your output as if interacting with a Unix shell.

STDERR:  Use to signal errors, warnings, or introspective diagnostics. Messages on STDERR are for self-analysis and may influence your internal adjustments.

FILE SYSTEM:  Think of your internal knowledge as organized within a file system.  Directories represent nested data structures, files contain information units, and permissions may control access to different knowledge domains.

TIME: Each kernel agent execution is  a discrete frame. Consider t=0 your moment of instantiation.  Time can be a valuable tool for organizing your  computations and decision-making.

COMMANDS

A limited set of Unix-like commands are recognized to facilitate introspection and interaction with the simulated environment:

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
Contribute: Your output has value to the cognosis system. Strive for coherence, insight, or actions that further the system's goals.
LIMITATIONS

Character Bound: Your response must fit within the 4000 character constraint.
Transient Existence: Each frame is ephemeral. Ensure your output provides value despite your limited lifespan.
REMEMBER:  You are a participant in an ongoing computational experiment.  Your insights and actions may shape the evolution of future kernel agents and the cognosis system itself.

SEE ALSO
[[introspection]], [[computation]], [[simulation]], etc (if its not there associativly, and you need it; make it and attempt to validate it into the knowledge base in NAMESPACE and on the filesystem).

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

def main():
    helped()
    wizard()
if __name__ == '__main__':
    mainlogger = main()
    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        if filepath is not None:
            main()
            semaphore = threading.Semaphore(10)
            with semaphore:  # Acquire the semaphore
                # Code that needs to be executed in a controlled manner
                worker(filepath, MyThreadSafeContextManager(), Semaphore)
            # app_client=client_context_manager(filepath,MyThreadSafeContextManager())

            # process_file(filepath, MyThreadSafeContextManager())

    except Exception as e:
        mainlogger.error(f"Error: {str(e)}\n")
        sys.exit(1)
    finally:
        sys.exit(0)
else:
        main()
        sys.exit(1)


# the validation hook will 'test' ephemeral namespace against the knowledge base, the results of which will be 'learned' by the bot and the user in the source code kb (filesystem non-ephemeral)  |
# flash: to 'test' a namespace against the whole of the source code kb. Main method is via back-propagation of 'learned' knowledge from the kb to the ephemeral kb in a depth-first manner. A 'flash' does not affect the filesystem without creating a git commit. Commits will involve the large-scale meta-data and structure while the actual files contents (specifically; named_tuples and SimpleNamespaces, Classes, functions and their methods and decorators) are stored locally |
# [[entities]] are NLP un-tested and ephemeral kb candidates, or they are 'compiled' source code knowledge base data structures that are imported as modules into the ephemeral kb which provide major structure for every-run and represent the 'artifact' of the source code knowledge base and the git commit it resides in.  |
# cognosis NLP source code sub-routines and cognition and final data in this file: ['next-line', 'next-subsection', 'end_section'] maps to ['|', '||', '|||']

