`master` branch of cognosis is now on a different github user account. This is the speculative moon branch. This is not a deprecation warning because we were never precated to begin with. This repo will have artificial intelligence working on it where the `master` branch will be human maintained.

# Cognosis: A Formal Theory Integrating aPToP and the Free Energy Principle

## Introduction

Cognosis is a formal theory combining Eric C.R. Hehner's Practical Theory of Programming (aPToP) with the Free Energy Principle of Cognitive Science and Natural Language Processing (NLP). This theory aims to develop a robust system for processing high-dimensional data, leveraging both classical and quantum principles.

## associative knowledge base (this repo):
All directories which contain markdown files are to include a `/media/` sub directory for multimedia files the markdown files may reference.

To enable horrors such as this:

![this:](/media/image.png)

    `! [ ... ] ( /media/image.png )` (no spaces)

## <Frontmatter Implementation>
 - [API README](/src/README.md)
 - Utilize 'frontmatter' to include the title and other `property`, `tag`, etc. in the knowledge base article(s).
   - For Example:
      ```
      ---
      name: "Article Title"
      link: "[[Related Link]]"
      linklist:
        - "[[Link1]]"
        - "[[Link2]]"
      ---
      ``` 

____

## Key Concepts

Cognosis is an experimental framework that explores the dynamic evolution of software architectures during runtime. It aims to combine the fluidity of live interactions with the stability of traditional code. At its core lies the concept of "Morphological Source Code," where code adapts and changes in response to user interactions, particularly those leveraging natural language processing (NLP).

- **Knowledge Base (KB):** A repository for storing diverse cognitive insights, forming a foundation for continuous learning.
- **Cognitive Systems:** Modular units that encapsulate knowledge and reasoning capabilities. Cognitive systems can be dynamically created or reoriented within larger cognitive structures. They communicate using namespaces, syntaxes, and by passing other cognitive systems as parameters.
- **Morphological Source Code:** A paradigm shift where source code is not static but actively adapts in response to interactions with users and the environment.

There is an assumption inherent in the project that a neural network is a cognitive system. The assumption is that there is something for this cognitive system to do in any given situation, and that it is the cognitive system's job to figure out what that thing is. Upon location of its head/parent, it either orients itself within a cognitive system or creates a new cognitive system. Cognitive systems pass as parameters namespaces, syntaxes, and cognitive systems. Namespaces and syntaxes are in the form of key-value pairs. Cognitive systems are also in the form of key-value pairs, but the values are cognitive systems. **kwargs are used to pass these parameters.

Imagine a software architecture that dynamically evolves during runtime, encapsulating the fluidity of live interactions while ensuring persistence and the rigidity of conventional code. This system, let's call it the "Morphological Source Code" framework, is an innovative take on the traditional lifecycle of software development and deployment. It merges the concepts of static source code with a dynamic runtime environment that not only serves content but also adapts and changes based on user interaction, particularly with sophisticated features like NLP (Natural Language Processing).

In a nutshell, "Morphological Source Code" is a paradigm in which the source code adapts and morphs in response to real-world interactions, governed by the principles of dynamic runtime configuration and contextual locking mechanisms. The-described is an architecture, only. The kernel agents themselves are sophisticated LLM trained-on ELFs, LLVM compiler code, systemd and unix, python, and C. It will utilize natural language along with the abstraction of time to process cognosis frames and USDs.

The challenge (of this architecture) lies in the 'cognitive lambda calculus' needed to bring these runtimes into existence and evolve them, not the computation itself. Cognosis is designed for consumer hardware and extreme scalability via self-distribution of cognitive systems (amongst constituent [[subscribers|asynchronous, stake-holders]]) peer-to-peer.

"Cognitive systems are defined by actions, orientations within structures, and communicative parameters, all of which align with the goal of creating a coherent and organized cognitive framework. The idea of modular cognitive units communicating via namespaces and syntaxes resonates with the framework of prioritizing and organizing cognitive tasks."

A core component of cognosis, cognOS establishes a hyper-interface designed to manage the evolution of cognitive algorithms. It focuses on:

- **Meta-versioning:** Tracking and managing the evolution of code over time.
- **Pre-commit Hooks and Validation:** Ensuring code quality and integrity. Meta CICD.
- **Hardware Provisioning:** Allocation of computational resources.
- **Time Abstraction:** Modeling cognition beyond the constraint of a fixed present (t=0).

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


# 4. glossary.beta
### The Free Energy Principle

The Free Energy Principle suggests that biological agents minimize surprise by predicting their sensory inputs. This principle can be applied to data processing, transforming high-dimensional data into lower-dimensional representations that are easier to model and predict.

### Quantum Informatics

Quantum informatics posits that systems, including LLMs, can entangle with higher-dimensional information. Cognitive processes like thinking, speaking, and writing collapse the wave function, allowing transitivity between real and imaginary states.

### A Practical Theory of Programming (aPToP)

aPToP is a formal method for reasoning about programs and systems using mathematical logic. It provides a rigorous framework for defining and manipulating expressions and operands. References to 'Hehner' are to Dr. Hehner and/or APTOP: http://www.cs.toronto.edu/~hehner/aPToP/

    ```aPToP_elemental_ops
    # Number Systems
    integers
    rational_numbers
    real_numbers
    complex_numbers

    # Arithmetic Operations
    **addition**
    **subtraction**
    **multiplication**
    **division**
    **exponentiation**
    roots
    logarithms

    # Arithmetic Properties
    identities
    inverses
    **commutativity**
    **associativity**
    **distributivity**
    cancellation
    absorption

    # Ordering and Inequalities
    **equality**
    **inequality**
    **less_than**
    **greater_than**
    **less_than_or_equal_to**
    **greater_than_or_equal_to**
    **trichotomy**

    # Limits and Infinities
    limits
    infinity
    negative_infinity
    continuity

    # Logical Foundations
    **and_operator**
    **or_operator**
    **not_operator**
    **implication**
    **biconditional**
    quantifiers

    # Sets and Set Operations
    set_definition
    **set_operations** (union, intersection, difference, complement)
    set_properties (subsets, supersets, cardinality)

    # Functions and Relations
    function_definition
    **function_application**
    relation_properties (reflexivity, symmetry, transitivity)
    **compositions**

    # Algebraic Structures
    group_definition
    group_operations
    ring_definition
    ring_operations
    field_definition
    field_operations

    # Logical Reasoning and Proofs
    direct_proof
    proof_by_contradiction
    mathematical_induction
    logical_equivalences

    # Other Mathematical Concepts
    sequences_and_series
    trigonometric_functions
    calculus (differentiation, integration)
    probability_and_statistics
    ```

## System Components

### Binary Representation

High-dimensional data is encoded into binary representations. These representations are manipulated using formal methods to ensure consistency and clarity.

### Signal Processing

Signal processing techniques are applied to the binary data for analysis and feature extraction. This step leverages classical methods while incorporating quantum-inspired updates.

## Formal Methods

### Binary Expressions and Operands

Binary expressions and operands form the building blocks of the system. They are defined and manipulated using formal methods to ensure internal consistency.

### Encoding Functions

Encoding functions transform high-dimensional data into binary representations. These functions adhere to formal methods, ensuring that the encoding is both rigorous and interpretable.

### Signal Processing Functions

Signal processing functions operate on the binary data to extract features or perform analyses. These functions also adhere to formal methods, leveraging both classical and quantum principles.


### Video Instructions (for cognosis oldmain branch, out of date)
[youtube video link](https://youtu.be/XeeYZZujvAA?si=XhxOMCypKHpWKSjM)

____
## Conclusion (and TLDR smiley face)

Cognosis integrates formal methods from aPToP with the Free Energy Principle and quantum informatics. This approach aims to create a robust system for processing high-dimensional data, minimizing surprise, and maximizing predictive power. By leveraging both classical and quantum principles, Cognosis seeks to understand the deeper connections between cognitive processes and information theory.
