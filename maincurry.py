import concurrent.futures
import logging
import sys
from pathlib import Path
from main import main, _init_basic_logging


def run_main_parallel(args):
    """
    Run the main function in parallel for each argument.

    Args:
        args (list): A list of arguments to pass to the main function.
    """
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Run main() for each argument in parallel
        futures = [executor.submit(main, arg) for arg in args[1:]]

        # Wait for all the tasks to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.exception(f"Error in parallel execution: {e}")


if __name__ == "__main__":
    # Initialize basic logging
    _init_basic_logging()
    logger = logging.getLogger(__name__)

    if len(sys.argv) > 1:
        run_main_parallel(sys.argv)
    else:
        # No arguments provided, call main() without arguments
        main()
