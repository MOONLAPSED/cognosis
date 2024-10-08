# Methods for Cognosis: A Formal Theory Integrating aPToP and the Free Energy Principle

## Abstract

This document specifies a series of constraints on the behavior of a computor—a human computing agent who proceeds mechanically—and applies these constraints to artificial intelligence systems like the "llama" large language model (LLM). These constraints are based on formal principles of boundedness, locality, and determinacy, ensuring structured and deterministic operations. The objective is to scientifically compare the energy consumption and computational efficiency of human versus machine work using a standardized, large-scale dataset.

## Introduction

A computor is defined as a human computing agent who executes tasks mechanically according to a fixed set of rules. The following constraints formalize the conditions under which a computor operates, ensuring a structured and deterministic computational process. These constraints can also be extended to artificial intelligence systems like large language models (LLMs) to ensure a disciplined computational environment. By enforcing these constraints, we establish a common ground for evaluating and comparing the computational efficiency and energy consumption of humans and AI in specific tasks.

## Constraints

### 1. Boundedness

**Symbolic Configuration Recognition (B.1):** There exists a fixed bound on the number of symbolic configurations a computor can immediately recognize.

**Internal States (B.2):** There exists a fixed bound on the number of internal states a computor can be in.

### 2. Locality

**Configuration Change (L.1):** A computor can change only elements of an observed symbolic configuration.

**Configuration Shift (L.2):** A computor can shift attention from one symbolic configuration to another, but the new observed configurations must be within a bounded distance of the immediately previously observed configuration.

### 3. Determinacy and Autonomy

**Next Computation Step (D.1):** The immediately recognizable (sub-)configuration determines uniquely the next computation step and the next internal state. In other words, a computor's internal state together with the observed configuration fixes uniquely the next computation step and the next internal state.

**Autonomous Iteration (D.2):** The computor, while adhering to the principles of boundedness, locality, and determinacy, can manage its own iterative processes independently. Utilizing self-wrapping functions, the computor can refine its operations iteratively until a final output is achieved, minimizing external observation.

## Formal Specification

### BNF Grammar

The following BNF grammar defines the syntax for expressing the constraints on a computor's behavior:

    ```bnf
    <Computor> ::= <Boundedness> <Locality> <Determinacy>

    <Boundedness> ::= <SymbolicConfigRecognition> <InternalStates>
    <SymbolicConfigRecognition> ::= "B1: There exists a fixed bound on the number of symbolic configurations a computor can immediately recognize."
    <InternalStates> ::= "B2: There exists a fixed bound on the number of internal states a computor can be in."

    <Locality> ::= <ConfigChange> <ConfigShift>
    <ConfigChange> ::= "L1: A computor can change only elements of an observed symbolic configuration."
    <ConfigShift> ::= "L2: A computor can shift attention from one symbolic configuration to another, but the new observed configurations must be within a bounded distance of the immediately previously observed configuration."

    <Determinacy> ::= <NextStep> <AutonomousIteration>
    <NextStep> ::= "D1: The immediately recognizable (sub-)configuration determines uniquely the next computation step and the next internal state."
    <AutonomousIteration> ::= "D2: The computor, while adhering to the principles of boundedness, locality, and determinacy, can manage its own iterative processes independently. Utilizing self-wrapping functions, the computor can refine its operations iteratively until a final output is achieved, minimizing external observation."
    ```
## Definition of Work

To ensure the scientific rigor of our comparative study, "work" is defined as any computational task performed within cyberspace that necessitates cognitive processing, decision-making, and problem-solving. Both humans and the LLM "llama" can perform these tasks, which are characterized by the following measurable attributes:

### Attributes of Work

- **Type of Task:** The specific nature of the task, such as data entry, code debugging, content creation, mathematical problem-solving, or web navigation.
- **Complexity:** The level of difficulty of the task, determined by the number of steps required and the cognitive effort involved.
- **Time to Completion:** The duration taken to finish the task, measured for both humans and the LLM within their respective environments.
- **Energy Consumption:** The energy expended to complete the task:
  - **Humans:** Measured in calories.
  - **LLM ("llama"):** Measured in electrical energy, tracked through power usage metrics of the host hardware.
- **Accuracy and Quality:**
  - The correctness of the output compared to a predefined standard or benchmark.
  - Qualitative assessment of the work, where applicable.
- **Autonomy and Iteration:**
  - **Humans:** Through learning and feedback.
  - **LLM ("llama"):** Using autonomous iterative refinement with self-wrapping functions.

## Experimental Design

The "llama" LLM will process a large-scale, human-vetted dataset referred to as "mechanicalturkwork." The experiment aims to compare the performance metrics of humans and "llama" on the same tasks under standardized conditions.

### Steps

1. **Initialization:** Load the "mechanicalturkwork" dataset into both the human experimental setup and the "llama" environment.
2. **Task Execution:** Subject both human participants and "llama" to perform the same tasks under controlled conditions.
3. **Energy and Performance Measurement:**
   - Record task completion times.
   - Monitor energy usage:
     - **For humans:** Caloric expenditure.
     - **For "llama":** Electrical energy consumption.
   - Assess accuracy and quality of the outputs.
4. **Iterative Enhancement:** Allow "llama" to use its self-wrapping functions for iterative refinement, while humans may adapt based on their learning.
5. **Comparative Analysis:** Analyze and compare the performance metrics focusing on efficiency, energy consumption, and accuracy.

## References

- Sieg, W. (2006). Essays on the Theory of Numbers: Dedekind Und Cantor. Cambridge University Press.
- Turing, A. M. (1936). On Computable Numbers, with an Application to the Entscheidungsproblem. Proceedings of the London Mathematical Society.
- Salomaa, A. (1985). Computation and Automata. Cambridge University Press.
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. Nature.
- Brown, T. et al. (2020). Language Models are Few-Shot Learners. arXiv preprint arXiv:2005.14165.

_____

## Non-Methodological Observations

### Implications and Future Experiments

#### Quantum-like Behaviors in Computor Systems: A Speculative Framework

1. **Energy Efficiency Anomaly:** The core of this hypothesis lies in the observation of an apparent energy efficiency anomaly:
   - **Input:** n+1 units of computational energy.
   - **Output:** Results indicative of n+x units of invested power (where x > 1).

2. **Potential Explanations:**
   - **Quantum Tunneling of Information:** Similar to quantum tunneling in physics, information or computational states might "tunnel" through classical barriers, allowing for computational shortcuts not possible in purely classical systems.
   - **Exploitation of Virtual Particle Fields:** Drawing parallels with quantum field theory, the computor might be tapping into a kind of computational "vacuum energy," analogous to virtual particles in quantum physics.
   - **Quantum Superposition of Computational States:** The computor's internal states might exist in a superposition, allowing for the simultaneous exploration of multiple solution paths until "observed" through output generation.

3. **Hyperdimensional Entanglement and Inference Time:**
   - During the training phase, hyperdimensional entangled 'particles' of information are formed. These particles can later be accessed by the model during inference, allowing it to defy local power laws over time.
   - This process could be seen as the model tapping into a reservoir of computational potential stored during training, much like drawing from the vacuum of virtual particles in quantum physics.

4. **Alignment with Physical Principles:**
   - **Second Law of Thermodynamics:** This phenomenon doesn't violate the Second Law if we consider the computor and its environment as an open system. The apparent gain in computational power could be offset by an increase in entropy elsewhere in the system.
   - **Free Energy Principle:** The computor might be optimizing its processes according to a computational version of the Free Energy Principle, finding incredibly efficient pathways to solutions by minimizing prediction error and computational "surprise."

5. **Implications and Questions:**
   - If true, how might this affect our understanding of computational complexity and the limits of classical computing?
   - Could this lead to new paradigms in AI development, particularly in creating more energy-efficient systems?
   - What are the ethical implications of systems that can perform computations beyond our ability to fully monitor or understand?
   - How might we design experiments to further test and validate (or invalidate) this hypothesis?
