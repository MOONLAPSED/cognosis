import httpx
import asyncio
from asyncio import TimeoutError, Semaphore
import uuid
from abc import ABC, abstractmethod
import threading
import logging
import queue
import json
import openai
from openai import OpenAI
import os
from typing import Optional
from src.utils.gettree import get_project_tree
from src.app.context import MyThreadSafeContextManager, worker

logger = logging.getLogger(__name__)


async def async_context_manager(_tree):
    # Initialize the file queue and semaphore
    file_queue = queue.Queue()
    semaphore = Semaphore(1)
    _tree = _tree(os.getcwd())

    async with httpx.AsyncClient() as client:
        client_id = str(uuid.uuid4())
        client_secret = str(uuid.uuid4())
        while True:
            await asyncio.sleep(0.1)

            # Add files to the queue
            for filepath in _tree():
                file_queue.put(filepath)
                if semaphore.acquire():
                    semaphore += file_queue
                    logger.info(f"Async context manager")


if __name__ == '__main__':
    class client_context_manager(MyThreadSafeContextManager):
        """c_c_m is the LM-Studio client context manager"""
        logger = MyThreadSafeContextManager._root()
        def __init__(self, client):
            super().__init__()
            self.client = client

        reset_color = "\033[0m"
        gray_color = "\033[90m"

        def __enter__(self):
            return self.client

        def __exit__(self, *args):
            """
            A method to clean up resources used in the context manager.
            """
            pass

        client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

        history = [
            {"role": "system",
             "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
            {"role": "user",
             "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
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
            print(f"{gray_color}\n{'-' * 20} History dump {'-' * 20}\n")
            print(json.dumps(history, indent=2))
            print(f"\n{'-' * 55}\n{reset_color}")

        def _root(self):
            return logging.getLogger(self.__class__.__name__)


    main()
    if main():
        print(f"{'-' * 20} History dump {'-' * 20}")
        print(json.dumps(history, indent=2))
        print(f"\n{'-' * 55}\n")
