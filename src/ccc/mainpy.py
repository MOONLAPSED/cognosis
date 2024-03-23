# orchestration coroutine (tests, verifications, etc)
import app.context as context
from app.context import MyThreadSafeContextManager, worker
import uuid
import threading
import queue
import logging
from typing import Optional

logger = context.MyThreadSafeContextManager._root()

def app(filepath: str, logger: Optional[logging.Logger]) -> None:
    # create a thread-safe queue
    q = queue.Queue()

    # create a context manager
    manager = MyThreadSafeContextManager()

    # create a new thread
    t = threading.Thread(target=worker, args=(q, filepath, manager))

    # start the thread
    t.start()

    # wait for the thread to finish
    t.join()

    if logger:
        logger.info(f"File {filepath} processed with UUID: {manager.uuid}")

    return None