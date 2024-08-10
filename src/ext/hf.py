# /src/ext/hf.py - huggingface transformers dep code
from dataclasses import dataclass, field
from typing import List, Callable, Any
from transformers import BertTokenizer

# Custom decorator to enforce nominative reflection
def nominative(cls):
    cls.__nominative__ = True
    return cls

@dataclass
@nominative
class MyDataModel:
    raw_text: str
    tokens: List[str] = field(init=False)
    tokenizer: Callable[[str], List[str]] = field(default=BertTokenizer.from_pretrained('bert-base-uncased').tokenize, init=False)

    def __post_init__(self):
        self.tokens = self.tokenizer(self.raw_text)
        self._validate()

    def _validate(self):
        # Implement validation logic here
        if not self.tokens:
            raise ValueError("Tokenization failed. Input text is invalid.")

    def __call__(self) -> List[str]:
        # Callable method to return tokens
        return self.tokens

try:
    data_instance = MyDataModel(raw_text="This is a test.")
    print(data_instance())  # Output the tokens
except ValueError as e:
    print(f"Error: {e}")
