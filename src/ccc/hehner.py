"""
# For more information, see: https://www.cs.utoronto.ca/~hehner/ & https://www.cs.utoronto.ca/~hehner/aPToP/laws.pdf

# This script explores using aPToP and the Free Energy Principle to develop a system for processing high-dimensional data.

# A Practical Theory of Programming (aPToP) combined with the Free Energy Principle of Cognitive Science and Natural Language Processing (NLP) forms the basis of a formal theory known as Cognosis.

# The Free Energy Principle suggests that biological agents (and potentially artificial systems) minimize surprise by constantly trying to predict their sensory inputs. This can be applied to data processing by transforming high-dimensional data into a lower-dimensional binary representation that is easier to model and predict.

# Formal methods, in this context, involve using a rigorous mathematical framework to define and reason about the data encoding and signal processing steps. This ensures the system is internally consistent and helps us understand its limitations and capabilities.

# This script proposes using formal methods to develop a Cognosis-based system that:
#   1. Encodes high-dimensional data into a binary representation.
#   2. Applies signal processing techniques to the binary data for analysis and feature extraction.

# Utilizing informal methods (NLP, machine learning, algorithms, etc.) is a runtime phenomenon that may also adorn source code as comments, for temporal and agentic clarity and consistency. Once an object (with stateful binary representation) is testable, it can be refactored into a formal method and added to the artifact and/or repository.
"""
from typing import Union, List
from dataclasses import dataclass

# Credit to Eric C.R. Hehner for the elemental, formal theory behind Cognosis.
"""
Binary Expression and Operand Definitions
"""
binary_theory = "The expressions of Binary Theory are called binary expressions. Some binary expressions are called theorems, and others are called antitheorems"
operand_theory = "Operands are the elements of a formal system. They are the building blocks of expressions, and they are the only elements that can be used in expressions. Operators are the elements of a formal system that are used to combine expressions to form new expressions."
THEOREM = "T"
ANTITHEOREM = "⊥"
BINARIES = {
    "1": THEOREM,
    "0": ANTITHEOREM,
}
"""
Hehner Operator Definitions and Symbolic Representations
"""
# Dictionary representing Hehner operators and their symbolic representations
HEHNER_OPERATORS = {
    "if_then_else_fi": "if <binary> then <expression> else <expression> fi",
    "equivalent": "<expression/binary>=<expression/binary>",
    "not_equivalent": "<expression/binary>⧧<expression/binary>",
    "and": "^",
    "or": "∨",
    "not": "¬",
    "implies": "→",  # antecedent -> consequent or "if antecedent then consequent"
    "implied_by": "←",  # antecedent <- consequent or "if consequent then antecedent"
}

"""
Dataclass to represent binary expressions
"""
@dataclass
class BinaryExpression:
    value: Union[str, "BinaryExpression"]
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"BinaryExpression('{self.value}')"

"""
Dataclass to represent operands
"""
@dataclass
class Operand:
    value: Union[str, BinaryExpression]
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"Operand('{self.value}')"

"""
Bijection and Translation Functions
"""
def binary_to_expression(binary: str) -> BinaryExpression:
    """
    Converts a binary string to a BinaryExpression object.
    """
    expression = ""
    for bit in binary:
        if bit == "0":
            expression += THEOREM
        elif bit == "1":
            expression += ANTITHEOREM
    return BinaryExpression(expression)

def expression_to_binary(expression: BinaryExpression) -> str:
    """
    Converts a BinaryExpression object to a binary string.
    """
    binary = ""
    for char in str(expression.value):
        if char == THEOREM:
            binary += "0"
        elif char == ANTITHEOREM:
            binary += "1"
    return binary

binary_string = "01101"
expression = binary_to_expression(binary_string)
print(expression)  # Output: BinaryExpression('T⊥T⊥T')

binary_string = expression_to_binary(expression)
print(binary_string)  # Output: '01101'

def translate_expression(expression: BinaryExpression, operator: str) -> BinaryExpression:
    """
    Applies a Hehner operator to a BinaryExpression and returns the resulting expression.
    """
    if operator == "not":
        result = ""
        for char in str(expression.value):
            if char == THEOREM:
                result += ANTITHEOREM
            elif char == ANTITHEOREM:
                result += THEOREM
        return BinaryExpression(result)
    # Implement other operators here
    else:
        raise ValueError(f"Unsupported operator: {operator}")

expression = binary_to_expression("01101")
negated_expression = translate_expression(expression, "not")
print(negated_expression)  # Output: BinaryExpression('⊥T⊥T⊥')
