import asyncio


class CPUScheduler:
    def __init__(self):
        self.task_queue = asyncio.Queue()

    async def add_task(self, task):
        await self.task_queue.put(task)

    async def get_next_task(self):
        return await self.task_queue.get()

    def queue_size(self):
        return self.task_queue.qsize()
