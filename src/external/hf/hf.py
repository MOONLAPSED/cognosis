# /src/external/hf/hf.py - huggingface transformers dep code
from dataclasses import dataclass, field
from typing import List, Callable
from transformers import BertTokenizer

def nominative(cls):
    """Decorator to add a __nominative__ attribute to the class for metadata."""
    cls.__nominative__ = True
    return cls

@dataclass
@nominative
class TokenModel:
    """
    A data model for tokenizing raw text using a BERT tokenizer.

    Attributes:
        raw_text (str): The input text to be tokenized.
        tokens (List[str]): The list of tokens extracted from raw_text.
        tokenizer (Callable[[str], List[str]]): A function that tokenizes the input text.
    """

    raw_text: str
    tokens: List[str] = field(init=False)
    tokenizer: Callable[[str], List[str]] = field(default_factory=lambda: BertTokenizer.from_pretrained('bert-base-uncased').tokenize, init=False)

    def __post_init__(self):
        """
        Post-initialization process to tokenize the raw_text and validate the resulting tokens.
        
        The tokenizer is applied to raw_text, and the results are stored in the tokens attribute.
        After tokenization, _validate() is called to ensure that the tokens list is not empty.
        """
        self.tokens = self.tokenizer(self.raw_text)
        self._validate()

    def _validate(self):
        """
        Validate the tokenization process.

        Ensures that the tokens list is not empty. Raises a ValueError if tokenization fails.
        """
        if not self.tokens:
            raise ValueError("Tokenization failed. Input text is invalid.")

    def __call__(self) -> List[str]:
        """
        Return the list of tokens.

        Allows the instance to be called as a function to access the tokens directly.
        
        Returns:
            List[str]: The list of tokens generated from raw_text.
        """
        return self.tokens

# Example usage
if __name__ == "__main__":
    try:
        data_instance = TokenModel(raw_text="Hello world!")
        print(data_instance())  # Output the tokens
    except ValueError as e:
        print(f"Error: {e}")
