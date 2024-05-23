from dataclasses import dataclass, field
from typing import Callable, Dict, List, Generic, TypeVar, Any
from math import sqrt, cos, pi

T = TypeVar('T')

@dataclass
class FormalTheory(Generic[T]):
    reflexivity: Callable[[T], bool] = lambda x: x == x
    symmetry: Callable[[T, T], bool] = lambda x, y: x == y
    transitivity: Callable[[T, T, T], bool] = lambda x, y, z: (x == y) and (y == z) and (x == z)
    transparency: Callable[[Callable[..., T], T, T], T] = lambda f, x, y: f(True, x, y) if x == y else None
    case_base: Dict[str, Callable[[T, T], T]] = field(default_factory=dict)
    states: List[List[float]] = field(default_factory=list)

    def __post_init__(self):
        self.case_base = {
            '⊤': lambda x, _: x,
            '⊥': lambda _, y: y,
            'a': self.if_else_a
        }

    def if_else(self, a: bool, x: T, y: T) -> T:
        """Conditionally return x if a is True, otherwise return y."""
        return x if a else y

    def if_else_a(self, x: T, y: T) -> T:
        """Always return x due to True condition."""
        return self.if_else(True, x, y)

    def compare(self, atoms: List[Any]) -> bool:
        """Ensure symmetry comparison for a list of atoms."""
        if not atoms:
            return False
        comparison = [self.symmetry(atoms[0], atoms[i]) for i in range(1, len(atoms))]
        return all(comparison)

    def encode(self) -> bytes:
        """Encode the formal theory properties into bytes."""
        return str(self.case_base).encode()

    def decode(self, data: bytes) -> None:
        """Decode the formal theory properties from bytes."""
        pass

    def execute(self, *args, **kwargs) -> Any:
        """Placeholder for execution logic."""
        pass

    def __repr__(self):
        case_base_repr = {
            key: (value.__name__ if callable(value) else value)
            for key, value in self.case_base.items()
        }
        return (f"FormalTheory(\n"
                f"  reflexivity={self.reflexivity.__name__},\n"
                f"  symmetry={self.symmetry.__name__},\n"
                f"  transitivity={self.transitivity.__name__},\n"
                f"  transparency={self.transparency.__name__},\n"
                f"  case_base={case_base_repr}\n"
                f")")

    def initialize_soliton(self, N: int, width: int) -> (List[float], List[float]):
        """Initialize a soliton-shaped initial condition."""
        u = [0.0] * N
        du = [0.0] * N
        mid = N // 2
        for i in range(mid - width // 2, mid + width // 2):
            u[i] = 0.5 * (1 - cos(2 * pi * (i - (mid - width // 2)) / (width - 1)))
        self.states.append(u.copy())
        return u, du

    def update_soliton(self, u: List[float], du: List[float], c: float = 1.0, non_linear_factor: float = 0.0) -> List[float]:
        """Update the soliton state based on a non-linear wave equation."""
        N = len(u)
        u_new = [0.0] * N
        for i in range(N):
            non_linear_term = non_linear_factor * u[i]**2 if i < N else 0
            u_new[i] = 2 * u[i] - du[i] + c * (u[(i-1) % N] - 2 * u[i] + u[(i+1) % N]) + non_linear_term
        return u_new

    def run_simulation(self, steps: int, N: int, width: int, c: float = 1.0, non_linear_factor: float = 0.0):
        """Run soliton propagation simulation for a number of steps."""
        u, du = self.initialize_soliton(N, width)
        for _ in range(steps):
            u_new = self.update_soliton(u, du, c, non_linear_factor)
            du = u
            u = u_new
            self.states.append(u.copy())

    def plot_soliton(self):
        """Visualize the soliton propagation over time."""
        for step, state in enumerate(self.states):
            state_str = ' '.join(f'{amplitude:.2f}' for amplitude in state)
            print(f'Step {step}: {state_str}')

# Example usage
theory = FormalTheory()
theory.run_simulation(steps=10, N=20, width=5, c=1.0, non_linear_factor=0.1)
theory.plot_soliton()