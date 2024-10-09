import math

"""
Establishing a Bijective Mapping with Natural Logarithms

Let's say you want to define a bijective mapping between a set of integers {1,2,3,…,n}{1,2,3,…,n} and their logarithmic transformations.

    Mapping Definition:
        Define a function f:N→Rf:N→R such that:
    f(n)=ln⁡(n)
    f(n)=ln(n)

    This function is a bijection for n>0n>0 since the natural logarithm is defined for positive integers and is both injective (one-to-one) and surjective (onto) over its range.

    Inverse Mapping:
        The inverse function f−1(y)=eyf−1(y)=ey allows you to retrieve the original integer from its logarithmic representation.

Proof Structure

    Injectivity: Prove that if f(a)=f(b)f(a)=f(b), then a=ba=b.
    Surjectivity: Show that for every y∈Ry∈R, there exists an n∈Nn∈N such that f(n)=yf(n)=y.
"""

def f(n: int) -> float:
    """Bijective mapping from natural numbers to their natural logarithm."""
    if n <= 0:
        raise ValueError("Input must be a positive integer.")
    return math.log(n)

def f_inverse(y: float) -> int:
    """Inverse mapping from logarithm to natural number."""
    return round(math.exp(y))  # rounding to get the closest natural number

def validate_bijection(max_n: int) -> None:
    """Validate the bijective mapping and its inverse."""
    for n in range(1, max_n + 1):
        ln_value = f(n)
        recovered_n = f_inverse(ln_value)
        assert n == recovered_n, f"Error: For n={n}, recovered {recovered_n} != original {n}"

if __name__ == "__main__":
    # Validate the bijection for the first 100 natural numbers
    validate_bijection(10000000)
    print("All tests passed!")
