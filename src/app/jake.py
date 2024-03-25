# Chat with an intelligent assistant in your terminal
from openai import OpenAI
from .context import MyThreadSafeContextManager
import json
class client_context_manager(MyThreadSafeContextManager):
    def __init__(self, client):
        self.client = client
    reset_color = "\033[0m"
    gray_color = "\033[90m"

    def __enter__(self):
        return self.client

    def __exit__(self, *args):
        pass
    
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    history = [
        {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
        {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
    ]
    try:
        while True:
            completion = client.chat.completions.create(
                messages=history,
                temperature=0.7,
                stream=True,
                model="open-orca_mistral-7b-openorca"
            )

            new_message = {"role": "assistant", "content": ""}
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="", flush=True)
                    new_message["content"] += chunk.choices[0].delta.content

            history.append(new_message)

            print()
            history.append({"role": "user", "content": input("> ")})
    except KeyboardInterrupt:
        print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
        print(json.dumps(history, indent=2))
        print(f"\n{'-'*55}\n{reset_color}")