# src\utils\scale.py - Wrapper for infinite loops to manage resource usage
import math
from typing import Callable, Union
from dataclasses import dataclass
from collections import Counter

@dataclass
class StringEntropy:
    """Class to calculate entropy of strings."""

    @staticmethod
    def calculate_entropy(text: str) -> float:
        """
        Calculate the entropy of a string based on character frequency.
        
        Args:
            text (str): The input string.
        
        Returns:
            float: The calculated entropy.
        """
        n = len(text)
        if n == 0:
            return 0
        
        freq = Counter(text)
        entropy = -sum((count / n) * math.log2(count / n) for count in freq.values())
        return entropy

@dataclass
class QuantifiedValue:
    """Class to handle and evaluate different types of values."""

    value: Union[int, float, str]

    def evaluate(self) -> float:
        """
        Evaluate the value and convert it to a float.
        
        Returns:
            float: The evaluated value.
        
        Raises:
            ValueError: If the value type is unsupported.
        """
        if isinstance(self.value, int):
            return float(self.value)
        elif isinstance(self.value, float):
            return self.value
        elif isinstance(self.value, str):
            # Use string entropy if the value is a string
            return StringEntropy.calculate_entropy(self.value)
        else:
            raise ValueError("Unsupported type for QuantifiedValue")

@dataclass
class AdaptiveIntegerLimit:
    """Class to calculate adaptive integer limits based on entropy."""

    max_entropy: float
    resource_function: Callable[[float], float]
    base_limit: int = 2**32 - 1
    max_possible_limit: int = 2**64 - 1

    def calculate_limit(self, current_entropy: float) -> int:
        """
        Calculate the adaptive limit based on current entropy.
        
        Args:
            current_entropy (float): The current entropy value.
        
        Returns:
            int: The calculated adaptive limit.
        """
        normalized_entropy = current_entropy / self.max_entropy
        available_resources = self.resource_function(normalized_entropy)
        k = 10
        limit_factor = 1 / (1 + math.exp(-k * (available_resources - 0.5)))
        adaptive_limit = int(self.base_limit + (self.max_possible_limit - self.base_limit) * limit_factor)
        return adaptive_limit

    def get_max_int(self, value: QuantifiedValue) -> int:
        """
        Get the maximum integer limit for the given quantified value.
        
        Args:
            value (QuantifiedValue): The quantified value to evaluate.
        
        Returns:
            int: The maximum integer limit.
        """
        current_entropy = value.evaluate()
        return min(self.calculate_limit(current_entropy), self.max_possible_limit)

# Example resource function
def example_resource_function(normalized_entropy: float) -> float:
    """Example resource function that returns the inverse of normalized entropy."""
    return 1 - normalized_entropy

def main():
    """Main function to demonstrate the usage of AdaptiveIntegerLimit."""
    max_system_entropy = 1e6
    adaptive_limit = AdaptiveIntegerLimit(max_system_entropy, example_resource_function)

    values = [
        QuantifiedValue(0),
        QuantifiedValue(1e5),
        QuantifiedValue(5e5),
        QuantifiedValue(9e5),
        QuantifiedValue(1e6),
        QuantifiedValue("Hello World"),
    ]

    for value in values:
        max_int = adaptive_limit.get_max_int(value)
        print(f"Value: {value.value}, Max Integer: {max_int}")

if __name__ == "__main__":
    main()
