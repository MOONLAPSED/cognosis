import uuid
from typing import Any, Dict, Set, List, Callable
from dataclasses import dataclass, field

class Atom:
    def __init__(self, value: Any = None):
        self.id = str(uuid.uuid4())
        self.value = value
        self.attributes: Dict[str, Any] = {}
        self.subscribers: Set['Atom'] = set()

    def __getattr__(self, name):
        if name in self.attributes:
            return self.attributes[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name in ('id', 'value', 'attributes', 'subscribers'):
            super().__setattr__(name, value)
        else:
            self.attributes[name] = value

    def spawn(self, value: Any = None) -> 'Atom':
        new_atom = Atom(value)
        new_atom.attributes = self.attributes.copy()
        return new_atom

    def subscribe(self, atom: 'Atom'):
        self.subscribers.add(atom)

    def unsubscribe(self, atom: 'Atom'):
        self.subscribers.discard(atom)

    def notify(self, message: Any):
        for subscriber in self.subscribers:
            subscriber.receive(message)

    def receive(self, message: Any):
        print(f"Atom {self.id} received: {message}")

    def __repr__(self):
        return f"Atom(id={self.id}, value={self.value}, attributes={self.attributes})"

class Runtime:
    def __init__(self):
        self.root_atom = Atom("Runtime")
        self.atoms: Dict[str, Atom] = {self.root_atom.id: self.root_atom}

    def create_atom(self, value: Any = None) -> Atom:
        atom = self.root_atom.spawn(value)
        self.atoms[atom.id] = atom
        return atom

    def get_atom(self, atom_id: str) -> Atom:
        return self.atoms.get(atom_id)

    def create_model(self, name: str, **attributes) -> Atom:
        model_atom = self.create_atom(name)
        for key, value in attributes.items():
            setattr(model_atom, key, value)
        return model_atom

    def create_theory(self, name: str, elements: List[Atom]) -> 'AtomicTheory':
        theory_atom = self.create_atom(name)
        theory = AtomicTheory(theory_atom, elements)
        theory_atom.theory = theory
        return theory

class AtomicTheory:
    def __init__(self, atom: Atom, elements: List[Atom]):
        self.atom = atom
        self.elements = elements
        self.operations: Dict[str, Callable[..., Any]] = {
            '∧': lambda a, b: a and b,
            '∨': lambda a, b: a or b,
            '¬': lambda a: not a,
            '→': lambda a, b: (not a) or b,
            '↔': lambda a, b: (a and b) or (not a and not b)
        }

    def add_operation(self, symbol: str, operation: Callable[..., Any]):
        self.operations[symbol] = operation

    def execute(self, operation: str, *args):
        if operation in self.operations:
            return self.operations[operation](*args)
        raise ValueError(f"Unknown operation: {operation}")

    def __repr__(self):
        return f"AtomicTheory(atom={self.atom}, elements={self.elements})"

# Usage example
runtime = Runtime()

# Create BaseModel as an Atom
base_model = runtime.create_model("BaseModel", 
                                  create=lambda **kwargs: runtime.create_model(**kwargs),
                                  dict=lambda self: self.attributes)

# Create Atom as an extension of BaseModel
atom_model = runtime.create_model("Atom", 
                                  __init__=Atom.__init__,
                                  spawn=Atom.spawn,
                                  subscribe=Atom.subscribe,
                                  unsubscribe=Atom.unsubscribe,
                                  notify=Atom.notify,
                                  receive=Atom.receive)
setattr(atom_model, '__base__', base_model)

# Create AtomicTheory
theory_a = runtime.create_atom(True)
theory_b = runtime.create_atom(False)
atomic_theory = runtime.create_theory("BasicLogic", [theory_a, theory_b])

# Execute theory operations
result_and = atomic_theory.execute('∧', theory_a.value, theory_b.value)
result_or = atomic_theory.execute('∨', theory_a.value, theory_b.value)

print(f"A ∧ B = {result_and}")
print(f"A ∨ B = {result_or}")

# Demonstrate self-referential nature
meta_theory = runtime.create_theory("MetaTheory", [atomic_theory.atom])
meta_theory.add_operation('execute_sub_theory', 
                          lambda theory, op, *args: theory.theory.execute(op, *args))

meta_result = meta_theory.execute('execute_sub_theory', atomic_theory.atom, '∧', theory_a.value, theory_b.value)
print(f"Meta-execution of A ∧ B = {meta_result}")