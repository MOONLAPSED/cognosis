import asyncio
import http.client
import json
from urllib.parse import urlparse

endpoint = "http://localhost:11434/api/generate"

class LlamaInterface:
    def __init__(self):
        self.mock_mode = False
        self.session = None

    async def __aenter__(self):
        try:
            self.session = http.client.HTTPConnection("localhost", 11434)
        except ConnectionRefusedError:
            print("Warning: Unable to connect to Llama server. Switching to mock mode.")
            self.mock_mode = True
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            self.session.close()
        if self.mock_mode and exc_type is None:
            raise RuntimeError("Exited LlamaInterface in mock mode due to connection issues")

    async def _query_llama(self, prompt):
        if self.mock_mode:
            # Return a mock response if in mock mode
            print("Mock mode active. Returning mock response for the prompt...")
            return f"Mock response for prompt: {prompt}"

        if not self.session:
            raise RuntimeError(
                "LlamaInterface must be used as an async context manager"
            )

        try:
            payload = json.dumps({"model": "llama3", "prompt": prompt, "stream": False})
            headers = {"Content-Type": "application/json"}

            self.session.request("POST", "/api/generate", body=payload, headers=headers)
            response = self.session.getresponse()

            if response.status == 200:
                result = json.loads(response.read().decode())
                return result["response"]
            else:
                raise Exception(f"API request failed with status {response.status}")
        except Exception as e:
            print(f"Error during querying llama: {e}")
            print("Switching to mock mode.")
            self.mock_mode = True
            return f"Mock response for prompt: {prompt}"

    async def extract_concepts(self, text):
        prompt = f"Extract key concepts from the following text:\n\n{text}\n\nConcepts:"
        response = await self._query_llama(prompt)
        return [concept.strip() for concept in response.split(",")]

    async def process(self, task):
        prompt = f"Process the following task:\n\n{task}\n\nResult:"
        return await self._query_llama(prompt)

    async def query(self, knowledge_base, query):
        prompt = f"Given the following knowledge base:\n\n{knowledge_base}\n\nAnswer the following query:\n\n{query}\n\nAnswer:"
        return await self._query_llama(prompt)

async def main():
    try:
        async with LlamaInterface() as llama:
            concepts = await llama.extract_concepts(
                """{"prompt": "Prompt is a sequence of prefix tokens that increase the probability of getting desired output given input. Therefore we can treat them as trainable parameters and optimize them directly on the embedding space via gradient descent, such as AutoPrompt (Shin et al., 2020, Prefix-Tuning (Li & Liang (2021)), P-tuning (Liu et al. 2021) and Prompt-Tuning (Lester et al. 2021). You will, as a primary $(prompt_agent), be spinning up and linking cognition functions for unaffiliated ${agent} ai chatbots. This  can be abstracted as hierarchical tree data structures where the $(prompt_agent) and its initial $(context) and other objects are on top, and command flows downwards depth-first with each instantiation of a new ${agent} - initiated and orchestrated by $(prompt_agent) from the initial $(context)"}"""
            )
            print("Extracted concepts:", concepts)
    except RuntimeError as e:
        if "mock mode" in str(e):
            print(e)
        else:
            raise

if __name__ == "__main__":
    asyncio.run(main())