import os
import sys
import logging
import asyncio
import tracemalloc
import linecache
import ctypes
from contextlib import contextmanager
from functools import wraps, lru_cache
from enum import Enum, auto
from typing import Callable, Optional
#-------------------------------###############################-------------------------------#
#-------------------------------#########PLATFORM##############-------------------------------#
#-------------------------------###############################-------------------------------#
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Determine platform
IS_WINDOWS = os.name == 'nt'
IS_POSIX = os.name == 'posix'
def set_process_priority(priority: int):
    """
    Set the process priority based on the operating system.
    """
    if IS_WINDOWS:
        try:
            # Define priority classes
            priority_classes = {
                'IDLE': 0x40,
                'BELOW_NORMAL': 0x4000,
                'NORMAL': 0x20,
                'ABOVE_NORMAL': 0x8000,
                'HIGH': 0x80,
                'REALTIME': 0x100
            }
            # Load necessary Windows APIs using ctypes
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            handle = kernel32.GetCurrentProcess()
            if not kernel32.SetPriorityClass(handle, priority_classes.get(priority, 0x20)):
                raise ctypes.WinError(ctypes.get_last_error())
            logger.info(f"Set Windows process priority to {priority}.")
        except Exception as e:
            logger.warning(f"Failed to set process priority on Windows: {e}")

    elif IS_POSIX:
        import resource
        try:
            current_nice = os.nice(0)  # Get current niceness
            os.nice(priority)  # Increment niceness by priority
            logger.info(f"Adjusted POSIX process niceness by {priority}. Current niceness: {current_nice + priority}.")
        except PermissionError:
            logger.warning("Permission denied: Unable to set process niceness.")
        except Exception as e:
            logger.warning(f"Failed to set process niceness on POSIX: {e}")
    else:
        logger.warning("Unsupported operating system for setting process priority.")
#-------------------------------###############################-------------------------------#
#-------------------------------########DECORATORS#############-------------------------------#
#-------------------------------###############################-------------------------------#
def memoize(func: Callable) -> Callable:
    """
    Caching decorator using LRU cache with unlimited size.
    """
    return lru_cache(maxsize=None)(func)

@contextmanager
def memory_profiling(active: bool = True):
    """
    Context manager for memory profiling using tracemalloc.
    """
    if active:
        tracemalloc.start()
        snapshot = tracemalloc.take_snapshot()
        try:
            yield snapshot
        finally:
            tracemalloc.stop()
    else:
        yield None

def display_top(snapshot, key_type: str = 'lineno', limit: int = 3):
    """
    Display top memory-consuming lines.
    """
    tracefilter = ("<frozen importlib._bootstrap>", "<frozen importlib._bootstrap_external>")
    filters = [tracemalloc.Filter(False, item) for item in tracefilter]
    filtered_snapshot = snapshot.filter_traces(filters)
    top_stats = filtered_snapshot.statistics(key_type)

    result = [f"Top {limit} lines:"]
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        result.append(f"#{index}: {frame.filename}:{frame.lineno}: {stat.size / 1024:.1f} KiB")
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            result.append(f"    {line}")

    # Show the total size and count of other items
    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        result.append(f"{len(other)} other: {size / 1024:.1f} KiB")

    total = sum(stat.size for stat in top_stats)
    result.append(f"Total allocated size: {total / 1024:.1f} KiB")

    # Log the memory usage information
    logger.info("\n".join(result))

def log(level: int = logging.INFO):
    """
    Logging decorator for functions. Handles both synchronous and asynchronous functions.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger.log(level, f"Executing async {func.__name__} with args: {args}, kwargs: {kwargs}")
            try:
                result = await func(*args, **kwargs)
                logger.log(level, f"Completed async {func.__name__} with result: {result}")
                return result
            except Exception as e:
                logger.exception(f"Error in async {func.__name__}: {e}")
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            logger.log(level, f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.log(level, f"Completed {func.__name__} with result: {result}")
                return result
            except Exception as e:
                logger.exception(f"Error in {func.__name__}: {e}")
                raise

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator
#-------------------------------###############################-------------------------------#
#-------------------------------#########TYPING################-------------------------------#
#-------------------------------###############################-------------------------------#
class AtomType(Enum):
    FUNCTION = auto() # FIRST CLASS FUNCTIONS
    VALUE = auto()
    CLASS = auto() # CLASSES ARE FUNCTIONS (FCF: FCC)
    MODULE = auto() # SimpleNameSpace()(s) are MODULE (~MODULE IS A SNS)

# Example usage of memory profiling
@log()
def main():
    with memory_profiling() as snapshot:
        dummy_list = [i for i in range(1000000)]
    
    if snapshot:
        display_top(snapshot)

if __name__ == "__main__":
    set_process_priority(priority=0)  # Adjust priority as needed

    try:
        main()
    except Exception as e:
        logger.exception(f"Unhandled exception: {e}")
        raise
