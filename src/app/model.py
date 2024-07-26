import json
import logging
import struct
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Generic, TypeVar
import threading
import queue
import time
import asyncio
# Define typing variables
T = TypeVar('T')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_atom(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> T:
        if not self.validate():
            raise ValueError(f"Invalid {self.__class__.__name__} object")
        return func(self, *args, **kwargs)
    return wrapper

def log_execution(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        logging.info(f"Executing {func.__name__} with args: {args} and kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"{func.__name__} executed successfully")
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

class Atom(ABC): # core base class for all possible elements of a formal system
    def __init__(self, metadata: Optional[Dict[str, Any]] = None):
        self.metadata = metadata or {}

    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value
        
    def get_metadata(self, key: str) -> Optional[Any]:
        return self.metadata.get(key)

    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def encode(self) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes) -> None:
        pass

    @abstractmethod
    @wraps
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Atom':
        return cls(metadata=data.get("metadata", {}))

@dataclass
class Token(Atom):
    def __init__(self, value: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(metadata)
        self.value = value

    def validate(self) -> bool:
        return isinstance(self.value, str) and isinstance(self.metadata, dict)

    @validate_atom
    def encode(self) -> bytes:
        data = {
            'type': 'token',
            'value': self.value,
            'metadata': self.metadata
        }
        json_data = json.dumps(data)
        return struct.pack('>I', len(json_data)) + json_data.encode()

    @validate_atom
    def decode(self, data: bytes) -> None:
        size = struct.unpack('>I', data[:4])[0]
        json_data = data[4:4+size].decode()
        parsed_data = json.loads(json_data)
        self.value = parsed_data.get('value', '')
        self.metadata = parsed_data.get('metadata', {})

    @validate_atom
    @log_execution
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return self.value

@dataclass
class Event(Atom):
    id: str
    type: str
    detail_type: str
    message: List[Dict[str, Any]]

    def __init__(self, id: str, type: str, detail_type: str, message: List[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None):
        super().__init__(metadata)
        self.id = id
        self.type = type
        self.detail_type = detail_type
        self.message = message

    def validate(self) -> bool:
        return all([
            isinstance(self.id, str),
            isinstance(self.type, str),
            isinstance(self.detail_type, str),
            isinstance(self.message, list)
        ])

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "id": self.id,
            "type": self.type,
            "detail_type": self.detail_type,
            "message": self.message
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        return cls(
            id=data["id"],
            type=data["type"],
            detail_type=data["detail_type"],
            message=data["message"],
            metadata=data.get("metadata", {})
        )

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    def decode(self, data: bytes) -> None:
        obj = json.loads(data.decode())
        self.id = obj['id']
        self.type = obj['type']
        self.detail_type = obj['detail_type']
        self.message = obj['message']
        self.metadata = obj.get('metadata', {})

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        logging.info(f"Executing event: {self.id}")
        # Implement necessary functionality here
        # possible modified-quine behavior, epigenetic behavior, etc.

@dataclass
class ActionRequest(Atom):
    action: str
    params: Dict[str, Any]
    self_info: Dict[str, Any]

    def __init__(self, action: str, params: Dict[str, Any], self_info: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None):
        super().__init__(metadata)
        self.action = action
        self.params = params
        self.self_info = self_info

    def validate(self) -> bool:
        return all([
            isinstance(self.action, str),
            isinstance(self.params, dict),
            isinstance(self.self_info, dict)
        ])

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "action": self.action,
            "params": self.params,
            "self_info": self.self_info
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionRequest':
        return cls(
            action=data["action"],
            params=data["params"],
            self_info=data["self_info"],
            metadata=data.get("metadata", {})
        )

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    def decode(self, data: bytes) -> None:
        obj = json.loads(data.decode())
        self.action = obj['action']
        self.params = obj['params']
        self.self_info = obj['self_info']
        self.metadata = obj.get('metadata', {})

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        logging.info(f"Executing action: {self.action}")
        # EXTEND from here; possibly into state encapsulation via quine ast source code

@dataclass
class ActionResponse(Atom):
    status: str
    retcode: int
    data: Dict[str, Any]
    message: str = ""

    def __init__(self, status: str, retcode: int, data: Dict[str, Any], message: str = "", metadata: Optional[Dict[str, Any]] = None):
        super().__init__(metadata)
        self.status = status
        self.retcode = retcode
        self.data = data
        self.message = message

    def validate(self) -> bool:
        return all([
            isinstance(self.status, str),
            isinstance(self.retcode, int),
            isinstance(self.data, dict),
            isinstance(self.message, str)
        ])

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "status": self.status,
            "retcode": self.retcode,
            "data": self.data,
            "message": self.message
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionResponse':
        return cls(
            status=data["status"],
            retcode=data["retcode"],
            data=data["data"],
            message=data.get("message", ""),
            metadata=data.get("metadata", {})
        )

    def encode(self) -> bytes:
        return json.dumps(self.to_dict()).encode()

    def decode(self, data: bytes) -> None:
        obj = json.loads(data.decode())
        self.status = obj['status']
        self.retcode = obj['retcode']
        self.data = obj['data']
        self.message = obj['message']
        self.metadata = obj.get('metadata', {})

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        logging.info(f"Executing response with status: {self.status}")
        if self.status == "success":
            return self.data
        else:
            raise Exception(self.message)

@dataclass
class FormalTheory(Generic[T], Atom):
    top_atom: Optional[Atom] = None
    bottom_atom: Optional[Atom] = None
    reflexivity: Callable[[T], bool] = lambda x: x == x
    symmetry: Callable[[T, T], bool] = lambda x, y: x == y
    transitivity: Callable[[T, T, T], bool] = lambda x, y, z: (x == y and y == z)
    transparency: Callable[[Callable[..., T], T, T], T] = lambda f, x, y: f(True, x, y) if x == y else None
    operators: Dict[str, Callable[..., Any]] = field(default_factory=lambda: {
        '⊤': lambda x: True,
        '⊥': lambda x: False,
        '¬': lambda a: not a,
        '∧': lambda a, b: a and b,
        '∨': lambda a, b: a or b,
        '→': lambda a, b: (not a) or b,
        '↔': lambda a, b: (a and b) or (not a and not b)
    })

    def validate(self) -> bool:
        return (self.top_atom is None or isinstance(self.top_atom, Atom)) and \
               (self.bottom_atom is None or isinstance(self.bottom_atom, Atom))

    @validate_atom
    def encode(self) -> bytes:
        top_encoded = self.top_atom.encode() if self.top_atom else b''
        bottom_encoded = self.bottom_atom.encode() if self.bottom_atom else b''
        return struct.pack('>II', len(top_encoded), len(bottom_encoded)) + top_encoded + bottom_encoded

    @validate_atom
    def decode(self, data: bytes) -> None:
        top_length, bottom_length = struct.unpack('>II', data[:8])
        if top_length > 0:
            self.top_atom = Token()  # Replace with dynamic instantiation
            self.top_atom.decode(data[8:8+top_length])
        if bottom_length > 0:
            self.bottom_atom = Token()  # Replace with dynamic instantiation
            self.bottom_atom.decode(data[8+top_length:8+top_length+bottom_length])

    @validate_atom
    @log_execution
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return {
            "top_value": self.top_atom.execute(*args, **kwargs) if self.top_atom else None,
            "bottom_value": self.bottom_atom.execute(*args, **kwargs) if self.bottom_atom else None
        }

class EventBus: # Define Event Bus (pub/sub pattern)
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Atom], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Atom], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable[[Atom], None]):
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(handler)

    def publish(self, event_type: str, event: Atom):
        if not isinstance(event, Atom):
            raise TypeError(f"Published event must be an Atom, got {type(event)}")
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                handler(event)
event_bus = EventBus()

class Operation(ActionRequest):
    def __init__(self, name: str, action: Callable, args: List[Any] = None, kwargs: Dict[str, Any] = None):
        metadata = {'name': name}
        params = {'args': args or [], 'kwargs': kwargs or {}}
        self_info = {}
        super().__init__(action, params, self_info, metadata)
        self.action = action

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return self.action(*self.params['args'], **self.params['kwargs'])

# -------------------below are runtime.py scoped classes and methods---------
# these are runtime.py scoped classes and methods but are here because 
# this is a monolithic file for purposes of collaboration etc.

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
                task = self.task_queue.get(timeout=1)
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



@dataclass
class MultiDimensionalAtom(Atom):
    dimensions: List[Atom] = field(default_factory=list)

    def add_dimension(self, atom: Atom):
        self.dimensions.append(atom)
    
    def validate(self) -> bool:
        if not all(isinstance(atom, Atom) for atom in self.dimensions):
            logging.error("Invalid Atom in dimensions")
            return False
        return True

    @validate_atom
    def encode(self) -> bytes:
        encoded_dims = [atom.encode() for atom in self.dimensions]
        lengths = struct.pack(f'>{len(encoded_dims)}I', *map(len, encoded_dims))
        return struct.pack('>I', len(encoded_dims)) + lengths + b''.join(encoded_dims)

    @validate_atom
    def decode(self, data: bytes) -> None:
        num_dims = struct.unpack('>I', data[:4])[0]
        lengths = struct.unpack(f'>{num_dims}I', data[4:4 + 4 * num_dims])
        offset = 4 + 4 * num_dims
        self.dimensions = []
        for length in lengths:
            atom_data = data[offset:offset + length]
            atom = Token()  # Initialize as Token by default, can be replaced dynamically
            atom.decode(atom_data)
            self.dimensions.append(atom)
            offset += length

    @validate_atom
    @log_execution
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return [atom.execute(*args, **kwargs) for atom in self.dimensions]
# ---------------------------------------------------------------
# TODO: refactor from here down
@dataclass
class ExperimentResult:
    input_data: Any
    output_data: Any
    success: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return (
            f"ExperimentResult(\n"
            f"  input_data={self.input_data},\n"
            f"  output_data={self.output_data},\n"
            f"  success={self.success},\n"
            f"  metadata={self.metadata}\n"
            f")"
        )


@dataclass
class ExperimentAgent(Atom):
    theory_name: str
    ttl: int
    experiment: Callable[[Any], ExperimentResult]
    termination_condition: Callable[[ExperimentResult], bool]
    initial_input: Any
    experiment_log: List[ExperimentResult] = field(default_factory=list)
    retries: int = 3
    retry_delay: float = 1.0
    max_parallel: int = 1

    async def run(self) -> Optional[ExperimentResult]:
        current_input = self.initial_input
        for iteration in range(self.ttl):
            try:
                tasks = [asyncio.create_task(self._run_experiment(current_input))
                         for _ in range(min(self.retries, self.max_parallel))]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                success_result = next((r for r in results if isinstance(r, ExperimentResult) and r.success), None)

                if success_result:
                    if self.termination_condition(success_result):
                        return success_result
                    current_input = success_result.output_data
            except Exception as e:
                logging.error(f"{self.theory_name} - Unexpected error in run method: {e}")

        return None

    async def _run_experiment(self, input_data: Any) -> Optional[ExperimentResult]:
        for attempt in range(self.retries):
            try:
                result = self.experiment(input_data)
                self.experiment_log.append(result)
                return result
            except Exception as e:
                logging.error(f"Experiment failed on attempt {attempt + 1} with error: {e}")
                if attempt < self.retries - 1:
                    await asyncio.sleep(self.retry_delay)
        return None

    def get_experiment_log(self) -> List[ExperimentResult]:
        return self.experiment_log

    def encode(self) -> bytes:
        raise NotImplementedError("ExperimentAgent cannot be directly encoded")

    def decode(self, data: bytes) -> None:
        raise NotImplementedError("ExperimentAgent cannot be directly decoded")

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        return asyncio.run(self.run())

    def __repr__(self) -> str:
        total_experiments = len(self.experiment_log)
        success_experiments = len([r for r in self.experiment_log if r.success])
        failed_experiments = total_experiments - success_experiments
        success_rate = (success_experiments / total_experiments) * 100 if total_experiments > 0 else 0

        detailed_results = "\n".join([repr(result) for result in self.experiment_log])
        return (
            f"ExperimentAgent(\n"
            f"  theory_name={self.theory_name},\n"
            f"  ttl={self.ttl},\n"
            f"  retries={self.retries},\n"
            f"  retry_delay={self.retry_delay},\n"
            f"  max_parallel={self.max_parallel},\n"
            f"  total_experiments={total_experiments},\n"
            f"  successful_experiments={success_experiments},\n"
            f"  failed_experiments={failed_experiments},\n"
            f"  success_rate={success_rate:.2f}%,\n"
            f"  detailed_results=[\n{detailed_results}\n"
            f"  ]\n"
            f")"
        )
    def validate(self) -> bool:
        return super().validate()

@dataclass
class Theory:
    name: str
    hypothesis: Callable[[Any], bool]
    experiment: Callable[[Any], ExperimentResult]

    def test(self, input_data: Any) -> ExperimentResult:
        result = self.experiment(input_data)
        result.metadata['hypothesis_result'] = self.hypothesis(result.output_data)
        return result

@dataclass
class AntiTheory:
    theory: Theory

    def test(self, input_data: Any) -> ExperimentResult:
        result = self.theory.test(input_data)
        result.success = not result.success
        result.metadata['anti_hypothesis_result'] = not result.metadata['hypothesis_result']
        return result


class AtomicBotApplication:
    def __init__(self):
        self.event_bus = EventBus()
        self.theories: List[Theory] = []
        self.experiment_agents: List[ExperimentAgent] = []

    def register_theory(self, theory: Theory):
        self.theories.append(theory)

    def create_experiment_agent(self, theory: Theory, initial_input: Any, ttl: int, termination_condition: Callable[[ExperimentResult], bool]):
        agent = ExperimentAgent(
            theory_name=theory.name,
            ttl=ttl,
            experiment=theory.test,
            termination_condition=termination_condition,  # User must provide
            initial_input=initial_input
        )
        self.experiment_agents.append(agent)

    async def run_experiments(self):
        tasks = [agent.run() for agent in self.experiment_agents]
        results = await asyncio.gather(*tasks)
        return results

    def process_event(self, event: Event):
        event.execute()

    def handle_action_request_async(self, request: ActionRequest) -> ActionResponse:
        return request.execute()

    def __repr__(self) -> str:
        total_agents = len(self.experiment_agents)
        agents_results = "\n".join([repr(agent) for agent in self.experiment_agents])
        return (
            f"AtomicBotApplication(\n"
            f"  total_agents={total_agents},\n"
            f"  agents_results=[\n{agents_results}\n"
            f"  ]\n"
            f")"
        )

# -------------------------------------------------------
# end of library code




# Library users are expected to implement their own logic using the provided data structures and classes.
# Below is an example:

def sample_experiment(input_data: Any) -> ExperimentResult:
    """
    Example implementation of an experiment function.
    This function doubles the input data and returns an ExperimentResult.
    """
    try:
        output_data = input_data * 2  # Simple operation for demonstration
        success = True
        metadata = {'extra_info': 'This is a doubling operation'}
    except Exception as e:
        output_data = None
        success = False
        metadata = {'error': str(e)}
    return ExperimentResult(
        input_data=input_data,
        output_data=output_data,
        success=success,
        metadata=metadata
    )

def sample_hypothesis(output_data: Any) -> bool:
    """
    Example hypothesis function.
    This function checks if the output data is a positive integer.
    """
    return isinstance(output_data, int) and output_data > 0

def sample_termination_condition(result: ExperimentResult) -> bool:
    """
    Example termination condition function.
    This function stops the experiment if the output data is greater than 20.
    """
    return result.success and result.output_data > 20

async def main():
    """
    The main function demonstrating usage of the library.
    """
    # Track the start time
    start_time = time.time()

    # Create the application instance
    application = AtomicBotApplication()

    # Step 1: Create and register a theory
    theory_name = "SampleTheory"
    theory = Theory(name=theory_name, hypothesis=sample_hypothesis, experiment=sample_experiment)
    application.register_theory(theory)

    # Step 2: Create an experiment agent for the theory
    initial_input = 10  # Example initial input
    ttl = 5  # Time to live (number of iterations) for experiments
    application.create_experiment_agent(
        theory=theory,
        initial_input=initial_input,
        ttl=ttl,
        termination_condition=sample_termination_condition
    )

    results = await application.run_experiments()
    end_time = time.time()
    total_duration = end_time - start_time

    # Step 4: Compile detailed report
    total_experiments = len(results)
    successful_experiments = len([r for r in results if r and r.success])
    failed_experiments = total_experiments - successful_experiments
    success_rate = (successful_experiments / total_experiments) * 100 if total_experiments > 0 else 0

    print(f"\nExperiment Report for {theory_name}:")
    print(f"===================================")
    print(f"Total Experiments Run: {total_experiments}")
    print(f"Successful Experiments: {successful_experiments} ({success_rate:.2f}%)")
    print(f"Failed Experiments: {failed_experiments}")
    print(f"Total Duration: {total_duration:.2f} seconds\n")

    print("Detailed Results:")
    print("=================")
    for idx, result in enumerate(results, start=1):
        if not result:
            print(f"Experiment {idx}: Failed")
        else:
            print(f"Experiment {idx}:")
            print(f"  Input Data: {result.input_data}")
            print(f"  Output Data: {result.output_data}")
            print(f"  Success: {result.success}")
            print(f"  Hypothesis Result: {result.metadata.get('hypothesis_result', 'N/A')}")
            print(f"  Metadata: {result.metadata}")

if __name__ == "__main__":
    asyncio.run(main())
    # Create a Token
    token = Token("example")
    result = token.execute()
    logging.info(f"Token result: {result}")

    # Create a MultiDimensionalAtom
    multi_dim_atom = MultiDimensionalAtom()
    multi_dim_atom.add_dimension(Token("dim1"))
    multi_dim_atom.add_dimension(Token("dim2"))
    result = multi_dim_atom.execute()
    logging.info(f"MultiDimensionalAtom result: {result}")

    # Create a FormalTheory
    formal_theory = FormalTheory()
    formal_theory.top_atom = Token("top")
    formal_theory.bottom_atom = Token("bottom")
    result = formal_theory.execute()
    logging.info(f"FormalTheory result: {result}")

    # Publish and Subscribe with the EventBus
    event_bus.subscribe("example_event", lambda e: logging.info(f"Received event: {e.to_dict()}"))

    event = Event(id="1", type="example_event", detail_type="test", message=[{"key": "value"}])
    event_bus.publish("example_event", event)
