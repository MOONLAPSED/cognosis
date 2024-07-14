"""This implementation covers the creation of a qubit, measurement, and an
iterative update using Newton's method while maintaining normalization. The
newton_iteration function iteratively updates the qubit state based on the
provided function and its derivative, ensuring that the qubit remains
normalized throughout the iterations."""
# see https://en.wikipedia.org/wiki/Newton%27s_method
# see /src/calc/README.md
import math
import random
import cmath

class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __truediv__(self, scalar):
        return ComplexNumber(self.real / scalar, self.imag / scalar)

    def __abs__(self):
        return math.sqrt(self.real**2 + self.imag**2)

    def conjugate(self):
        return ComplexNumber(self.real, -self.imag)

    def __repr__(self):
        return f"{self.real:.2f} + {self.imag:.2f}i"

    def to_complex(self):
        return complex(self.real, self.imag)

    @staticmethod
    def from_complex(c):
        return ComplexNumber(c.real, c.imag)

class ComplexQubit:
    def __init__(self, alpha_real, alpha_imag):
        self.alpha = ComplexNumber(alpha_real, alpha_imag)
        self._normalize()

    def _normalize(self):
        norm = abs(self.alpha)
        if norm > 1:
            self.alpha = self.alpha / norm

    @property
    def beta(self):
        beta_real = math.sqrt(1 - (self.alpha.real**2 + self.alpha.imag**2))
        return ComplexNumber(beta_real, 0)

    def measure(self):
        prob_zero = abs(self.alpha)**2
        return 0 if random.random() < prob_zero else 1

    def apply_hadamard(self):
        new_alpha = (self.alpha + self.beta) / math.sqrt(2)
        return ComplexQubit(new_alpha.real, new_alpha.imag)

    def bloch_coordinates(self):
        theta = 2 * math.acos(abs(self.alpha))
        phi = math.atan2(self.beta.imag, self.beta.real) - math.atan2(self.alpha.imag, self.alpha.real)
        return (math.sin(theta) * math.cos(phi),
                math.sin(theta) * math.sin(phi),
                math.cos(theta))

def newton_iteration(F, F_prime, x0, tol=1e-7, max_iter=1000):
    x = x0
    for _ in range(max_iter):
        Fx = F(x)
        if abs(Fx) < tol:
            break
        x = x - Fx / F_prime(x)
    return x

def F(alpha, beta):
    return alpha.to_complex() * beta.to_complex().conjugate() - 1

def F_prime(alpha, beta):
    return beta.to_complex().conjugate()

def update_qubit(qubit):
    alpha, beta = qubit.alpha, qubit.beta
    alpha_new = newton_iteration(lambda a: F(a, beta), lambda a: F_prime(a, beta), alpha.to_complex())
    return ComplexQubit(alpha_new.real, alpha_new.imag)

# Example usage
initial_alpha_real, initial_alpha_imag = random.uniform(0, 1), random.uniform(0, 1)
qubit = ComplexQubit(initial_alpha_real, initial_alpha_imag)

# Apply Newton's method update
updated_qubit = update_qubit(qubit)
print(f"Updated Qubit: α={updated_qubit.alpha}, β={updated_qubit.beta}")

# Measure the updated qubit
measurements = [updated_qubit.measure() for _ in range(1000)]
print(f"Measurement results: {sum(measurements)/len(measurements):.2f} ones")
