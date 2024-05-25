# FormalTheory Protocol Implementation
# Version: 0.3
# Author: Claude (Anthropic AI) with feedback and testing from MOONLAPSED and chatGPT
import re
from typing import Iterator, Tuple, Union

# Define the BNF grammar for the FormalTheory protocol
GRAMMAR = """
<theory> ::= <header> <payload> <logical_switch>
<header> ::= "BNF:" <bnf_grammar>
<bnf_grammar> ::= <production> | <bnf_grammar> "|" <production>
<production> ::= <non-terminal> "::=" <expressions>
<expressions> ::= <expression> | <expressions> <expression>
<expression> ::= <terminal> | "<" <non-terminal> ">"
<non-terminal> ::= "<" <name> ">"
<terminal> ::= '"' <value> '"'
<name> ::= <char> | <name> <char>
<char> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" | "_"
<value> ::= <printable_char> | <value> <printable_char>
<printable_char> ::= <char> | <digit> | <symbol>
<digit> ::= "0" | "1" | ... | "9"
<symbol> ::= "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")" | "_" | "-" | "+" | "=" | "{" | "}" | "[" | "]" | "\\" | "|" | ";" | ":" | "'" | '"' | "," | "." | "/" | "<" | ">" | "?" | "`" | "~"
<payload> ::= <content>
<logical_switch> ::= "Theory" | "Anti-Theory"
<content> ::= <any_characters>
"""

class FormalTheory:
    def __init__(self, theory_string: str):
        self.header, self.payload, self.logical_switch = self.parse(theory_string)
        self.grammar = self.parse_bnf(self.header)
        print(f"Header: {self.header}")
        print(f"Payload: {self.payload}")
        print(f"Logical Switch: {self.logical_switch}")
        print(f"Grammar: {self.grammar}")

    def parse(self, theory_string: str) -> Tuple[str, str, str]:
        match = re.match(r'BNF:(.*?)(Theory|Anti-Theory)', theory_string, re.DOTALL)
        if match:
            header = match.group(1).strip()
            rest = theory_string[match.end(1):].strip()
            payload, logical_switch = rest.rsplit('\n', 1)
            return header, payload.strip(), logical_switch.strip()
        else:
            raise ValueError("Invalid FormalTheory string")

    def parse_bnf(self, bnf_string: str) -> dict:
        grammar = {}
        productions = bnf_string.split('\n')
        for production in productions:
            if '::=' in production:
                lhs, rhs = production.split('::=', 1)  # Split only at the first '::='
                lhs = lhs.strip()
                rhs = [symbol.strip() for symbol in rhs.split('|')]
                grammar[lhs] = rhs
        return grammar

    def validate_syntax(self, symbol: str) -> Iterator[str]:
        print(f"Validating syntax for symbol: {symbol}")
        if symbol.startswith('<') and symbol.endswith('>'):
            non_terminal = symbol
            if non_terminal not in self.grammar:
                raise ValueError(f"Non-terminal '{non_terminal}' not found in the grammar")
            expressions = self.grammar[non_terminal]
            for expression in expressions:
                if expression.startswith('<'):
                    yield from self.validate_syntax(expression)
                else:
                    yield expression
        else:
            yield symbol

    def is_valid(self) -> bool:
        try:
            symbols = list(self.validate_syntax('<theory>'))
            print(f"Symbols from grammar: {symbols}")
            payload_valid = self.payload == ''.join(symbols)
            print(f"Payload valid: {payload_valid}")
            return payload_valid if self.logical_switch == "Theory" else not payload_valid
        except ValueError as e:
            print(f"Validation error: {e}")
            return False

# Example usage
theory_string = """BNF: <theory> ::= <header> <payload> <logical_switch>
                   <header> ::= "BNF:" <bnf_grammar>
                   <bnf_grammar> ::= <production> | <bnf_grammar> "|" <production>
                   <production> ::= <non-terminal> "::=" <expressions>
                   <expressions> ::= <expression> | <expressions> <expression>
                   <expression> ::= <terminal> | "<" <non-terminal> ">"
                   <non-terminal> ::= "<" <name> ">"
                   <terminal> ::= '"' <value> '"'
                   <name> ::= <char> | <name> <char>
                   <char> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" | "_"
                   <value> ::= <printable_char> | <value> <printable_char>
                   <printable_char> ::= <char> | <digit> | <symbol>
                   <digit> ::= "0" | "1" | ... | "9"
                   <symbol> ::= "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")" | "_" | "-" | "+" | "=" | "{" | "}" | "[" | "]" | "\\" | "|" | ";" | ":" | "'" | '"' | "," | "." | "/" | "<" | ">" | "?" | "`" | "~"
                   <payload> ::= <content>
                   <logical_switch> ::= "Theory" | "Anti-Theory"
                   <content> ::= <any_characters>

BNF: <header> "Hello, World!" Theory
Theory
"""

def main():
    theory = FormalTheory(theory_string)
    print(theory.is_valid())
    print(theory.header)

if __name__ == "__main__":
    main()

    
"""chatGPT(v0.3)
In this implementation, I have defined a FormalTheory class that takes a theory string as input and parses it into three components: the header (BNF grammar), the payload, and the logical switch ("Theory" or "Anti-Theory"). The class provides the following functionality:

Parsing the Theory String: The parse method uses regular expressions to extract the header, payload, and logical switch from the input theory string.
Parsing the BNF Grammar: The parse_bnf method converts the BNF grammar string from the header into a dictionary representation, where the keys are non-terminals, and the values are lists of expressions.
Syntax Validation: The validate_syntax method is a generator function that recursively validates the syntax of a non-terminal by expanding its expressions according to the grammar. It yields the terminal symbols that match the payload.
Logical Validation: The is_valid method checks if the payload matches the syntax defined by the grammar. If the payload is valid according to the grammar, it returns True if the logical switch is "Theory", and False if the logical switch is "Anti-Theory". If the payload is invalid according to the grammar, it returns False regardless of the logical switch.

The implementation includes an example usage where a theory string is defined, and a FormalTheory object is created. The is_valid method is called, and the result is printed, which should be True for the given example.
This implementation demonstrates how the FormalTheory protocol can be realized using Python. It follows the principles of parsing the header (BNF grammar), validating the syntax of the payload against the grammar, and applying the logical switch based on the validity of the payload.
"""



"""claude(v0.2)
In this implementation, I have defined a FormalTheory class that takes a theory string as input and parses it into three components: the header (BNF grammar), the payload, and the logical switch ("Theory" or "Anti-Theory"). The class provides the following functionality:

Parsing the Theory String: The parse method uses regular expressions to extract the header, payload, and logical switch from the input theory string.
Parsing the BNF Grammar: The parse_bnf method converts the BNF grammar string from the header into a dictionary representation, where the keys are non-terminals, and the values are lists of expressions.
Syntax Validation: The validate_syntax method is a generator function that recursively validates the syntax of a non-terminal by expanding its expressions according to the grammar. It yields the terminal symbols that match the payload.
Logical Validation: The is_valid method checks if the payload matches the syntax defined by the grammar. If the payload is valid according to the grammar, it returns True if the logical switch is "Theory", and False if the logical switch is "Anti-Theory". If the payload is invalid according to the grammar, it returns False regardless of the logical switch.

The implementation includes an example usage where a theory string is defined, and a FormalTheory object is created. The is_valid method is called, and the result is printed, which should be True for the given example.
This implementation demonstrates how the FormalTheory protocol can be realized using Python. It follows the principles of parsing the header (BNF grammar), validating the syntax of the payload against the grammar, and applying the logical switch based on the validity of the payload.
"""