import uuid
from abc import ABC, abstractmethod  
import threading
import logging
import queue
import os
from typing import Optional

class MyBaseContextManager(ABC):
    """
    Abstract base class for custom context managers.
    """
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @abstractmethod
    def _root(self):
        pass  # accesses the __main__/__file__ 'root' logger

class MyThreadSafeContextManager(MyBaseContextManager):
    """
    Custom thread-safe context manager with lock and UUID.
    """
    def __init__(self):
        self.lock = threading.Lock()
        self.uuid = uuid.uuid4()

    def __enter__(self):
        self.lock.acquire()
        print(f"Entering context with UUID: {self.uuid}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is not None:
                print(f"Exception caught in UUID {self.uuid}: {exc_value}")
            # Any other resource cleanup can be done here.
        finally:
            self.lock.release()
            print(f"Exiting context with UUID: {self.uuid}")
            # Optionally, return True to suppress the exception if handled

    def _root(self):
        return logging.getLogger(self.__class__.__name__)

def process_file(filepath: str, manager: MyThreadSafeContextManager):
    """
    Example of how to use context manager with UUID inside the processing function.
    """
    with manager:
        print(f"Processing file {filepath} with UUID: {manager.uuid}")
        # Load and process the file
        # Make API calls
        # Update the file or create new output

def worker(q: queue.Queue, filepath: str, semaphore: threading.Semaphore):
    """
    Worker function to process files from the queue.
    Args:
      q: queue.Queue - a queue to track task completion
      filepath: str - the file path to process
      semaphore: threading.Semaphore - a semaphore to limit concurrent processes
    """
    semaphore = threading.Semaphore(10)  # Create a semaphore instance

    with semaphore:  # Acquire the semaphore
        # Code that needs to be executed in a controlled manner
        process_file(filepath, MyThreadSafeContextManager()) 

# Initialize the file queue and semaphore
file_queue = queue.Queue()
semaphore = threading.Semaphore(10)
