import re
from typing import Union
import dis
import ast

class Token:
    def __init__(self, type_: str, value: Union[str, int, float]):
        self.type = type_  # e.g., "WORD", "NUMBER", "OPERATOR"
        self.value = value  # The token's literal value
    
    def __repr__(self):
        return f"<Token(type={self.type}, value={self.value})>"

def tokenize(text: str):
    token_specification = [
        ("NUMBER", r"\d+(\.\d*)?"),    # Integer or decimal number
        ("WORD",   r"[A-Za-z]+"),      # Words
        ("OPERATOR", r"[-+*/]"),       # Arithmetic operators
        ("PUNCT",  r"[,.]"),           # Punctuation
        ("SKIP",   r"\s+"),            # Skip over spaces
    ]
    
    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    for match in re.finditer(token_regex, text):
        kind = match.lastgroup
        value = match.group()
        if kind == "NUMBER":
            value = float(value) if '.' in value else int(value)
        yield Token(kind, value)


def bytecode_to_tokens(func):
    bytecode = dis.Bytecode(func)
    tokens = []
    for instr in bytecode:
        tokens.append(Token(instr.opname, instr.argval))
    return tokens

def add(a, b):
    return a + b

tokens = bytecode_to_tokens(add)
print(tokens)

class ASTTokenVisitor(ast.NodeVisitor):
    def __init__(self):
        self.tokens = []

    def generic_visit(self, node):
        token = Token(type(node).__name__, getattr(node, 'n', None))
        self.tokens.append(token)
        ast.NodeVisitor.generic_visit(self, node)

def tokenize_ast(source_code: str):
    tree = ast.parse(source_code)
    visitor = ASTTokenVisitor()
    visitor.visit(tree)
    return visitor.tokens

tokens = tokenize_ast("a = 5 + 3")
print(tokens)

# Example usage
text = "5 + 3.14 * 2, test"
tokens = list(tokenize(text))
for t in tokens:
    print(t)
