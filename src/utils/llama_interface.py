import asyncio
import json
import http.client
from urllib.parse import urlparse

endpoint = 'http://localhost:11434/api/generate'


class LlamaInterface:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = http.client.HTTPConnection('localhost', 11434)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.session.close()

    async def _query_llama(self, prompt):
        if not self.session:
            raise RuntimeError("LlamaInterface must be used as an async context manager")

        payload = json.dumps({
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        })
        headers = {
            'Content-Type': 'application/json'
        }

        self.session.request('POST', '/api/generate', body=payload, headers=headers)
        response = self.session.getresponse()

        if response.status == 200:
            result = json.loads(response.read().decode())
            return result['response']
        else:
            raise Exception(f"API request failed with status {response.status}")

    async def extract_concepts(self, text):
        prompt = f"Extract key concepts from the following text:\n\n{text}\n\nConcepts:"
        response = await self._query_llama(prompt)
        return [concept.strip() for concept in response.split(',')]

    async def process(self, task):
        prompt = f"Process the following task:\n\n{task}\n\nResult:"
        return await self._query_llama(prompt)

    async def query(self, knowledge_base, query):
        prompt = f"Given the following knowledge base:\n\n{knowledge_base}\n\nAnswer the following query:\n\n{query}\n\nAnswer:"
        return await self._query_llama(prompt)


async def main():
    async with LlamaInterface() as llama:
        concepts = await llama.extract_concepts("The quick brown fox jumps over the lazy dog.")
        print("Extracted concepts:", concepts)

        result = await llama.process("Summarize the benefits of exercise.")
        print("Processed task:", result)

        kb = "Exercise is beneficial for health. It improves cardiovascular fitness and strengthens muscles."
        query_result = await llama.query(kb, "What are the benefits of exercise?")
        print("Query result:", query_result)


if __name__ == "__main__":
    asyncio.run(main())
