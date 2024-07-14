# Qubit Probability Amplitudes

A qubit state ∣ψ⟩∣ψ⟩ can be written as:
∣ψ⟩=α∣0⟩+β∣1⟩
∣ψ⟩=α∣0⟩+β∣1⟩

where αα and ββ are complex numbers and ∣α∣2+∣β∣2=1∣α∣2+∣β∣2=1.
Step 2: Measurement Probabilities

The probability of measuring the state ∣0⟩∣0⟩ is ∣α∣2∣α∣2, and the probability of measuring the state ∣1⟩∣1⟩ is ∣β∣2∣β∣2.
Step 3: Iterative Methods and Normalization

Define the iterative update rule using Newton's Method in lambda calculus:
xn+1=xn−F(xn)F′(xn)
xn+1​=xn​−F′(xn​)F(xn​)​

Ensure that each iteration maintains the normalization condition:
∣αn+1∣2+∣βn+1∣2=1
∣αn+1​∣2+∣βn+1​∣2=1
Step 4: Probabilistic Modeling

Use probability distributions to describe the initial state and the evolution of the qubit state. For example, if αα and ββ are initially uniformly distributed, show how they evolve under the update rules.
Step 5: Mathematical Proofs
Normalization Proof

Assume:
∣αn∣2+∣βn∣2=1
∣αn​∣2+∣βn​∣2=1

Prove:
∣αn+1∣2+∣βn+1∣2=1
∣αn+1​∣2+∣βn+1​∣2=1

given the update rules for αn+1αn+1​ and βn+1βn+1​.
Convergence Proof

Show that the iterative method converges to a solution that satisfies F(x)=0F(x)=0 within the normalized qubit space.

## The Challenge:

Represent a qubit state as compactly as possible in a quantity-conserving, invariant way while still being able to represent the full state.

### Key Concepts

**Invariant**: The state of the qubit should remain unchanged by the application of the update rule. This implies that the state must be a normalized vector.

### Normalization Condition

To ensure invariance, the state must be a normalized vector. This means that the sum of the probabilities of measuring the state in any of its possible outcomes must equal 1.

For a qubit state \(|\psi\rangle\) represented as:
\[
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle
\]

The normalization condition is:
\[
|\alpha|^2 + |\beta|^2 = 1
\]

### Measurement Probabilities

The probability of measuring the state \(|0\rangle\) is \(|\alpha|^2\), and the probability of measuring the state \(|1\rangle\) is \(|\beta|^2\). These probabilities must sum to 1 to ensure the state is normalized.

### Update Rule

When applying an update rule, such as Newton's Method in lambda calculus, the state must remain normalized. This means that the update rule must preserve the normalization condition.

For example, if the update rule is:
\[
x_{n+1} = x_n - \frac{F(x_n)}{F'(x_n)}
\]

we need to ensure that after applying this rule, the new state \(|\psi_{n+1}\rangle\) still satisfies:
\[
|\alpha_{n+1}|^2 + |\beta_{n+1}|^2 = 1
\]

This ensures that the representation is invariant and quantity-conserving.
