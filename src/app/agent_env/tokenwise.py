import tokenize
"""The tokenize module can be executed as a script from the command line. It is as simple as:
$python -m tokenize [-e] [filename.py]
The tokenize.py module produces a sequence of tuples, where each tuple contains the token type, the token value, the starting line number, the starting column number, and the ending line number."""
prompt = []

tokenize.detect_encoding(prompt)
tokenize.open(prompt)



source_code = """
def hello_world():
  print("Hello, World!")

if __name__ == "__main__":
  hello_world()
"""

tokens = tokenize.generate_tokens(source_code)

for token in tokens:
  print(token)
"""
(1, 'def', 1, 0)
(2, 'hello_world', 1, 4)
(3, '(', 1, 13)
(4, ')', 1, 14)
(5, ':', 1, 15)
(6, 'print', 2, 0)
(7, '(', 2, 5)
(8, '"', 2, 6)
(9, 'Hello, World!', 2, 7)
(10, '"', 2, 21)
(11, ')', 2, 22)
(12, '\n', 2, 22)
(13, 'if', 3, 0)
(14, '__name__', 3, 3)
(15, '==', 3, 11)
(16, '"__main__', 3, 13)
(17, '"', 3, 22)
(18, ':', 3, 23)
(19, 'hello_world', 4, 0)
(20, '(', 4, 11)
(21, ')', 4, 12)
(22, '\n', 4, 12)
(0, 'EOF', 5, 0)
"""