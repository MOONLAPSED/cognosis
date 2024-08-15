import tokenize
import io

def tokenize_source_code(source_code):
    """
    Tokenize the given source code string and return a list of tokens.

    Args:
        source_code (str): The Python source code to tokenize.

    Returns:
        list of tokenize.TokenInfo: A list of token information tuples.
    """
    tokens = []
    source_io = io.StringIO(source_code)
    for token in tokenize.generate_tokens(source_io.readline):
        tokens.append(token)
    return tokens

# Source code to be tokenized
source_code = """
def hello_world():
  print("Hello, World!")

if __name__ == "__main__":
  hello_world()
"""

# Tokenize the source code
tokens = tokenize_source_code(source_code)

# Print the tokens with additional context
for token in tokens:
    token_type = tokenize.tok_name[token.type]
    print(f"Type: {token_type:<10} | String: {token.string:<20} | Start: {token.start} | End: {token.end} | Line: {token.line.strip()}")
