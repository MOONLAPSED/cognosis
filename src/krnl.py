import json
import logging
import queue
import threading
from typing import Any, Dict, List, Optional, Callable, Type

from app.app import ActionRequest, ActionResponse, Atom, EventBus  # Ensure this import is correct in your context.

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

class Operation(ActionRequest):
    def __init__(self, name: str, action: Callable, args: List[Any] = None, kwargs: Dict[str, Any] = None):
        metadata = {'name': name}
        params = {'args': args or [], 'kwargs': kwargs or {}}
        self_info = {}
        super().__init__(action, params, self_info, metadata)
        self.action = action

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return self.action(*self.params['args'], **self.params['kwargs'])

class Task:
    def __init__(self, task_id: int, operation: Operation):
        self.task_id = task_id
        self.operation = operation
        self.result = None

    def run(self):
        logging.info(f"Running task {self.task_id} with operation {self.operation.action}")
        self.result = self.operation.execute()
        logging.info(f"Task {self.task_id} completed with result: {self.result}")
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
        self.threads = []
        self.running = False
        self.event_bus = EventBus()

    def submit_task(self, operation: Operation):
        task_id = self.task_id_counter
        self.task_id_counter += 1
        task = Task(task_id, operation)
        self.task_queue.put(task)
        logging.info(f"Submitted task {task_id}")
        event = ActionRequest(action="task_submitted", params={"task_id": task_id}, self_info=operation.to_dict())
        self.event_bus.publish("task_submitted", event)
        return task_id

    def run(self):
        self.running = True
        for i in range(len(self.arenas)):
            thread = threading.Thread(target=self._worker, args=(i,))
            thread.start()
            self.threads.append(thread)
        logging.info("Kernel is running")

    def stop(self):
        self.running = False
        for thread in self.threads:
            thread.join()
        logging.info("Kernel has stopped")

    def _worker(self, arena_id: int):
        arena = self.arenas[arena_id]
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)  # Adjust timeout as necessary
                logging.info(f"Worker {arena_id} picked up task {task.task_id}")
                arena.allocate("current_task", task)
                result = task.run()
                arena.deallocate("current_task")
                response = ActionResponse(status="completed", retcode=0, data=result, message=f"Task {task.task_id} completed")
                self.event_bus.publish("task_completed", response)
            except queue.Empty:
                continue

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

# Example event handlers for the EventBus
def handle_task_submitted(event: ActionRequest):
    logging.info(f"Task submitted with details: {event.to_dict()}")

def handle_task_completed(event: ActionResponse):
    logging.info(f"Task completed with details: {event.to_dict()}")

if __name__ == "__main__":
    # Initialize kernel and event bus
    kernel = SpeculativeKernel(num_arenas=4)
    kernel.event_bus.subscribe("task_submitted", handle_task_submitted)
    kernel.event_bus.subscribe("task_completed", handle_task_completed)

    # Example usage
    def example_action(data):
        return sum(data)

    example_operation = Operation(name="example_task", action=example_action, args=[[1, 2, 3]], kwargs={})
    kernel.submit_task(example_operation)
    
    kernel.run()

    import time
    time.sleep(2)  # Allow some time for tasks to be processed

    kernel.stop()

    # Save the state
    kernel.save_state("kernel_state.json")