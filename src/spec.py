import json
import logging
import queue
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import contextmanager
from typing import Any, Callable, Dict, List, Tuple

# Logger configuration
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Task:
    def __init__(self, task_id: int, func: Callable, args=(), kwargs=None):
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kwargs = kwargs if kwargs else {}
        self.result = None

    def run(self):
        logging.info(f"Running task {self.task_id}")
        try:
            self.result = self.func(*self.args, **self.kwargs)
            logging.info(f"Task {self.task_id} completed with result: {self.result}")
        except Exception as e:
            logging.error(f"Task {self.task_id} failed with error: {e}")
        return self.result


class Arena:
    def __init__(self, name: str):
        self.name = name
        self.lock = threading.Lock()
        self.local_data = {}

    def allocate(self, key: str, value: Any):
        with self.lock:
            self.local_data[key] = value
            logging.info(f"Arena {self.name}: Allocated {key} = {value}")

    def deallocate(self, key: str):
        with self.lock:
            value = self.local_data.pop(key, None)
            logging.info(f"Arena {self.name}: Deallocated {key}, value was {value}")

    def get(self, key: str):
        with self.lock:
            return self.local_data.get(key)


class SpeculativeKernel:
    def __init__(self, num_arenas: int):
        self.arenas = {i: Arena(f"Arena_{i}") for i in range(num_arenas)}
        self.task_queue = queue.Queue()
        self.task_id_counter = 0
        self.executor = ThreadPoolExecutor(max_workers=num_arenas)
        self.running = False

    def submit_task(self, func: Callable, args=(), kwargs=None) -> int:
        task_id = self.task_id_counter
        self.task_id_counter += 1
        task = Task(task_id, func, args, kwargs)
        self.task_queue.put(task)
        logging.info(f"Submitted task {task_id}")
        return task_id

    def run(self):
        self.running = True
        for i in range(len(self.arenas)):
            self.executor.submit(self._worker, i)
        logging.info("Kernel is running")

    def stop(self):
        self.running = False
        self.executor.shutdown(wait=True)
        logging.info("Kernel has stopped")

    def _worker(self, arena_id: int):
        arena = self.arenas[arena_id]
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
                logging.info(f"Worker {arena_id} picked up task {task.task_id}")
                with self._arena_context(arena, "current_task", task):
                    task.run()
            except queue.Empty:
                continue

    @contextmanager
    def _arena_context(self, arena: Arena, key: str, value: Any):
        arena.allocate(key, value)
        try:
            yield
        finally:
            arena.deallocate(key)

    def handle_fail_state(self, arena_id: int):
        arena = self.arenas[arena_id]
        with arena.lock:
            logging.error(f"Handling fail state in {arena.name}")
            arena.local_data.clear()

    def allocate_in_arena(self, arena_id: int, key: str, value: Any):
        arena = self.arenas[arena_id]
        arena.allocate(key, value)

    def deallocate_in_arena(self, arena_id: int, key: str):
        arena = self.arenas[arena_id]
        arena.deallocate(key)

    def get_from_arena(self, arena_id: int, key: str) -> Any:
        arena = self.arenas[arena_id]
        return arena.get(key)

    def save_state(self, filename: str):
        state = {arena.name: arena.local_data for arena in self.arenas.values()}
        with open(filename, "w") as f:
            json.dump(state, f)
        logging.info(f"State saved to {filename}")

    def load_state(self, filename: str):
        with open(filename, "r") as f:
            state = json.load(f)
        for arena_name, local_data in state.items():
            arena_id = int(arena_name.split("_")[1])
            self.arenas[arena_id].local_data = local_data
        logging.info(f"State loaded from {filename}")


def main():
    kernel = SpeculativeKernel(3)
    kernel.run()
    kernel.submit_task(lambda x: x**2, (2,))
    kernel.submit_task(lambda x: x**2, (3,))
    kernel.submit_task(lambda x: x**2, (4,))
    kernel.submit_task(lambda x: x**2, (5,))
    kernel.submit_task(lambda x: x**2, (6,))
    kernel.submit_task(lambda x: x**2, (7,))
    kernel.submit_task(lambda x: x**2, (8,))
    kernel.submit_task(lambda x: x**2, (9,))
    kernel.submit_task(lambda x: x**2, (10,))
    kernel.stop()
    kernel.save_state("state.json")


if __name__ == "__main__":
    main()
