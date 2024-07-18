import random
import math
import cmath
from typing import List, Tuple

class QuantumInfoDynamics:
    def __init__(self, dimensions=3):
        self.dimensions = dimensions
        self.state = [random.random() for _ in range(dimensions)]
        self._normalize()

    @property
    def state(self):
        return self._state.copy()

    @state.setter
    def state(self, value):
        self._state = value
        self._normalize()

    def _normalize(self):
        norm = math.sqrt(sum(x ** 2 for x in self._state))
        self._state = [x / norm for x in self._state]

    def rotate(self, axis: Tuple[float, float, float], angle: float):
        axis = self._normalize_vector(axis)
        cos_angle = math.cos(angle / 2)
        sin_angle = math.sin(angle / 2)
        x, y, z = axis

        rotation_matrix = [
            [cos_angle + x * x * (1 - cos_angle), x * y * (1 - cos_angle) - z * sin_angle, x * z * (1 - cos_angle) + y * sin_angle],
            [y * x * (1 - cos_angle) + z * sin_angle, cos_angle + y * y * (1 - cos_angle), y * z * (1 - cos_angle) - x * sin_angle],
            [z * x * (1 - cos_angle) - y * sin_angle, z * y * (1 - cos_angle) + x * sin_angle, cos_angle + z * z * (1 - cos_angle)]
        ]

        self.state = [
            sum(rotation_matrix[i][j] * self._state[j] for j in range(3))
            for i in range(3)
        ]
        self._normalize()

    def interact(self, other: 'QuantumInfoDynamics'):
        interaction = self._cross_product(self.state, other.state)
        self.state = [s + i for s, i in zip(self.state, interaction)]
        other.state = [s + i for s, i in zip(other.state, interaction)]
        self._normalize()
        other._normalize()

    def measure(self) -> float:
        return sum(x ** 2 for x in self.state)

    @staticmethod
    def _normalize_vector(vector: Tuple[float, float, float]) -> Tuple[float, float, float]:
        norm = math.sqrt(sum(x ** 2 for x in vector))
        return tuple(x / norm for x in vector)

    @staticmethod
    def _cross_product(v1: List[float], v2: List[float]) -> List[float]:
        return [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ]

class TripartiteState:
    def __init__(self, *args: complex):
        if len(args) != 4:
            raise ValueError("TripartiteState must be initialized with exactly 4 arguments")
        self.q = list(args)

    @property
    def q(self):
        return self._q.copy()

    @q.setter
    def q(self, value):
        self._q = value

    def __mul__(self, other: 'TripartiteState') -> 'TripartiteState':
        a1, b1, c1, d1 = self.q
        a2, b2, c2, d2 = other.q
        return TripartiteState(
            a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
            a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
            a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
        )

    def conjugate(self) -> 'TripartiteState':
        return TripartiteState(*[x.conjugate() for x in self.q])

    @property
    def norm(self) -> float:
        return math.sqrt(sum(abs(x) ** 2 for x in self.q))

def rotate(state: TripartiteState, axis: Tuple[int, int, int], angle: float) -> TripartiteState:
    if len(axis) != 3:
        raise ValueError("Axis must be a 3-tuple")
    
    half_angle = angle / 2
    sin_half = cmath.sin(half_angle)
    cos_half = cmath.cos(half_angle)
    
    # Create a quaternion representation of the rotation
    x, y, z = axis
    r = cos_half
    i = x * sin_half
    j = y * sin_half
    k = z * sin_half
    
    rotated_state_q = []
    for q in state.q:
        q_r = r * q.real - i * q.imag
        q_i = r * q.imag + i * q.real
        q_j = j * q.imag
        q_k = k * q.imag
        rotated_state_q.append(complex(q_r - q_j, q_i + q_k))
    
    return TripartiteState(*rotated_state_q)

def main():
    # Example usage
    initial_state = TripartiteState(1, 0, 0, 0)  # Pure information state
    rotated_state = rotate(initial_state, (0, 1, 0), math.pi / 4)  # Rotate towards matter

    # Example usage
    qid1 = QuantumInfoDynamics()
    qid2 = QuantumInfoDynamics()

    print("Initial states:")
    print(qid1.state, qid2.state)

    qid1.rotate((0, 1, 0), math.pi / 4)
    qid2.rotate((1, 0, 0), math.pi / 3)

    print("After rotation:")
    print(qid1.state, qid2.state)

    qid1.interact(qid2)

    print("After interaction:")
    print(qid1.state, qid2.state)

    print("Measurements:")
    print(qid1.measure(), qid2.measure())

if __name__ == "__main__":
    main()
