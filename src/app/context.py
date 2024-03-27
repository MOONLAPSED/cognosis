import uuid
from abc import ABC, abstractmethod  
import threading
import logging
import queue
import json
import openai as OpenAI
import os
from typing import Optional
from src.utils.gettree import gettree

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


class client_context_manager(MyThreadSafeContextManager):
    def __init__(self, client):
        self.client = client
    reset_color = "\033[0m"
    gray_color = "\033[90m"

    def __enter__(self):
        return self.client

    def __exit__(self, *args):
        pass
    
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    history = [
        {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
        {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
    ]
    try:
        while True:
            completion = client.chat.completions.create(
                messages=history,
                temperature=0.7,
                stream=True,
                model="open-orca_mistral-7b-openorca"
            )

            new_message = {"role": "assistant", "content": ""}
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    new_message["content"] += chunk.choices[0].delta.content

            history.append(new_message)

            print()
            history.append({"role": "user", "content": input("> ")})
    except KeyboardInterrupt:
        print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
        print(json.dumps(history, indent=2))
        print(f"\n{'-'*55}\n{reset_color}")


    def _root(self):
        return logging.getLogger(self.__class__.__name__)



# =================================================================================
def main():
    # Initialize the file queue and semaphore
    file_queue = queue.Queue()
    semaphore = threading.Semaphore(10)
    get_project_tree = gettree(os.getcwd())

    # Start the worker threads
    for _ in range(10):
        threading.Thread(target=worker, args=(file_queue, None, semaphore)).start()

    # Add files to the queue
    for filepath in get_project_tree():
        file_queue.put(filepath)

if __name__ == '__main__':
    main()
    if main():
        print(f"{'-'*20} History dump {'-'*20}")
        print(json.dumps(history, indent=2))
        print(f"\n{'-'*55}\n")