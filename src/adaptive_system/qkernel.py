import asyncio
#from .knowledge_base import Graph
#from .file_manager import FileSystemManager
#from .memory_manager import MemoryManager
#from .cpu_scheduler import CPUScheduler
from .llama_interface import LlamaInterface

class SymbolicKernel:
    def __init__(self, kb_dir, output_dir, max_memory):
        #self.knowledge_base = Graph()
        #self.file_manager = FileSystemManager(kb_dir, output_dir)
        #self.memory_manager = MemoryManager(max_memory)
        #self.cpu_scheduler = CPUScheduler()
        self.llama = None
        self.running = False

    async def __aenter__(self):
        self.llama = await LlamaInterface().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.llama:
            await self.llama.__aexit__(exc_type, exc, tb)

    async def initialize(self):
        files = self.file_manager.list_kb_files()
        for file in files:
            content = self.file_manager.read_file(file)
            await self.process_file(content)

    async def process_file(self, content):
        concepts = await self.llama.extract_concepts(content)
        for concept in concepts:
            self.knowledge_base.add_node(concept)

    async def run(self):
        self.running = True
        while self.running:
            task = await self.cpu_scheduler.get_next_task()
            result = await self.process_task(task)
            self.memory_manager.store(task, result)

    async def process_task(self, task):
        return await self.llama.process(task)

    async def stop(self):
        self.running = False
        await self.save_state()

    async def save_state(self):
        state = self.knowledge_base.serialize()
        self.file_manager.write_file('knowledge_state.json', state)

    def get_status(self):
        return {
            'kb_size': len(self.knowledge_base.nodes),
            'memory_usage': self.memory_manager.current_size,
            'tasks_queued': self.cpu_scheduler.queue_size()
        }

    async def query(self, query):
        return await self.llama.query(self.knowledge_base, query)
