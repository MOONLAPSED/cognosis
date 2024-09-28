import asyncio
from src.app.llama import LlamaInterface

class SymbolicKernel:
    def __init__(self, kb_dir, output_dir, max_memory):
        self.kb_dir = kb_dir
        self.output_dir = output_dir
        self.max_memory = max_memory
        self.llama = None
        self.running = False
        self.knowledge_base = set()  # set of concepts as simplified kb

    async def __aenter__(self):
        self.llama = await LlamaInterface().__aenter__()
        self.running = True
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.llama:
            await self.llama.__aexit__(exc_type, exc, tb)
        self.running = False

    async def process_task(self, task):
        if not self.running:
            raise RuntimeError("Kernel is not initialized or has been stopped")

        result = await self.llama.process(task)
        concepts = await self.llama.extract_concepts(result)
        self.knowledge_base.update(concepts)

        return result

    async def stop(self):
        if self.running:
            self.running = False
            if self.llama:
                await self.llama.__aexit__(None, None, None)  # Use __aexit__ for cleanup

    def get_status(self):
        return {"kb_size": len(self.knowledge_base), "running": self.running}

    async def query(self, query):
        if not self.running:
            raise RuntimeError("Kernel is not initialized or has been stopped")
        return await self.llama._query_llama(query)  # Assuming _query_llama is an async method

    async def generate_knowledge_base(self):
        if not self.running:
            raise RuntimeError("Kernel is not initialized or has been stopped")
        await self.llama.generate_knowledge_base(self.kb_dir, self.knowledge_base, self.max_memory)
