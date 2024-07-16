import sys

class MemoryManager:
    def __init__(self, max_size):
        self.max_size = max_size
        self.current_size = 0
        self.data = {}

    def store(self, key, value):
        size = sys.getsizeof(value)
        if self.current_size + size > self.max_size:
            self.free_memory(size)
        self.data[key] = value
        self.current_size += size

    def free_memory(self, required_size):
        while self.current_size + required_size > self.max_size and self.data:
            key, value = self.data.popitem()
            self.current_size -= sys.getsizeof(value)

    def get(self, key):
        return self.data.get(key)