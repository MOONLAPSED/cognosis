from abc import ABC, abstractmethod

class RuntimeTokenSpace(ABC):
    """The RuntimeTokenSpace class offers a helpful way to simulate, visualize, and troubleshoot the flow of
    data and algorithms within machine learning models.
    Key Use Cases: Simulating data flow, algorithm planning and development, core data structures, and abstract
    class definitions which can be used to simulate data flow and model visualization/debugging/development.

    Limitations: It might not be the ideal tool for replicating the intricate calculations within hidden layers
    of neural networks or the flow of machine learning models. For tasks like advanced vector retrieval,
    weighting, and biasing, runtime token space interacts with libraries like NumPy, Jax, or TensorFlow."""
    @abstractmethod
    def push(self, item):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def peek(self):
        pass

class SimpleTokenStack(RuntimeTokenSpace):
    def __init__(self):
        self._stack = []

    def push(self, item):
        self._stack.append(item)

    def pop(self):
        if not self._stack: 
            raise IndexError("Stack is empty")
        return self._stack.pop()

    def peek(self):
        if not self._stack:
            raise IndexError("Stack is empty")
        return self._stack[-1]

    def __len__(self):
        return len(self._stack)