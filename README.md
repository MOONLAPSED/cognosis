# cognosis - Cognitive Coherence Coroutines
NLP + LLM + KB for lifelong learning and development
## MIT license - MOONLAPSED@gmail.com + MOONLAPSED@github


\!#include: @`/docs/README.md`, @`src/app/README.md`, @`src/api/README.md`, @`src/ccc/README.md`

\!#currently: @`/README.md`

### ::Key Concepts::

cognosis is an experimental framework that explores the dynamic evolution of software architectures during runtime. It aims to combine the fluidity of live interactions with the stability of traditional code.  At its core lies the concept of "Morphological Source Code," where code adapts and changes in response to user interactions, particularly those leveraging natural language processing (NLP).

    Knowledge Base (KB): A repository for storing diverse cognitive insights, forming a foundation for continuous learning.

    Cognitive Systems: Modular units that encapsulate knowledge and reasoning capabilities. Cognitive systems can be dynamically created or reoriented within larger cognitive structures. They communicate using namespaces, syntaxes, and by passing other cognitive systems as parameters.

    Morphological Source Code: A paradigm shift where source code is not static but actively adapts in response to interactions with users and the environment.

There is an assumption inherint in the project that a neural network is a cognitive system. The assumption is that there IS some THING for this cognitive system to DO in any-given situation, and that it is the cognitive system's job to figure out what that THING is. Upon location of its head/parent it either orients itself within a cognitive system, or it creates a new cognitive system. Cognitive systems pass as parameters namespaces, syntaxes, and cognitive systems. Namespaces and syntaxes are in the form of key-value pairs. Cognitive systems are also in the form of key-value pairs, but the values are cognitive systems. **kwargs are used to pass these parameters.

Imagine a software architecture that dynamically evolves during runtime, encapsulating the fluidity of live interactions while ensuring persistence and the rigidity of conventional code. This system, let's call it the "Morphological Source Code" framework, is an innovative take on the traditional lifecycle of software development and deployment. It merges the concepts of static source code with a dynamic runtime environment that not only serves content but also adapts and changes based on user interaction, particularly with sophisticated features like NLP (Natural Language Processing).

In a nutshell, "Morphological Source Code" is a paradigm in which the source code adapts and morphs in response to real-world interactions, governed by the principles of dynamic runtime configuration and contextual locking mechanisms. The-described is an architecture, only. The kernel agents themselves are sophisticated LLM trained-on ELFs, LLVM compiler code, systemd and unix, python, and C. It will utilize natural language along with the abstraction of time to process cognosis frames and USDs.

The challenge (of this architecture) lies in the 'cognitive lambda calculus' needed to bring these runtimes into existence and evolve them, not the computation itself. Cognosis is designed for consumer hardware and extreme scalability via self-distribution of cognitive systems (amongst constituent [[subscribers|asynchronous, stake-holders]]) peer-to-peer.

"""Cognitive systems are defined by actions, orientations within structures, and communicative parameters, all of which align with the goal of creating a coherent and organized cognitive framework. The idea of modular cognitive units communicating via namespaces and syntaxes resonates with the framework of prioritizing and organizing cognitive tasks."""

A core component of cognosis, cognOS establishes a hyper-interface designed to manage the evolution of cognitive algorithms. It focuses on:

    Meta-versioning: Tracking and managing the evolution of code over time.

    Pre-commit Hooks and Validation: Ensuring code quality and integrity. Meta CICD.

    Hardware Provisioning: Allocation of computational resources.

    Time Abstraction: Modeling cognition beyond the constraint of a fixed present (t=0).

### ::video instructions::
[youtube video link](https://www.youtube.com/watch?v=-rGRMM7jZhA)

### Setup Instructions

#### Docker Client Setup
Start by initializing the Docker environment, which hosts the client components.


FROM ghcr.io/ai-dock/comfyui:latest

For more detailed documentation and configuration options, visit AI Dock + ComfyUI + PyTorch Documentation. <https://github.com/ai-dock/base-image/wiki>

The Caddy web server acts as a reverse proxy, allowing services within the Docker container to listen for connections at 0.0.0.0, granting flexibility for interacting with your instance.

Client Components:

AI Dock: A robust environment including Caddy, PyTorch, Stable Diffusion, etc., for running AI models.
ComfyUI: A user interface layer for model interaction, visualization, and orchestration.

Server Setup:

Establish a secure and isolated server environment using a hypervisor:Windows Sandbox (cfg.wsb) or WSL2 with an Ubuntu 22.04 image (docker-compose.yml).

Integration and Orchestration:

Utilize ComfyUI for orchestrating your cognitive system from the moment of initialization (t=0) and beyond.

AI Dock + PyTorch + ComfyUI collectively form the agent 'runtime' or 'server' environment.

The hypervisor functions as an isolated 'brain' for the agent.

Please follow the respective setup procedures for Docker and your chosen hypervisor to ensure proper environment initialization.

<!-- More Setup Instructions -->

### windows sandbox version
+ micromamba - via environment.yaml (any hypervisor/os):
    ```
    - `cd {{app_dir}}`
    - conda activate {{env_name}}
    - conda env create -f environment.yml
    - `python -m {{app_name}}`
    ```
+ pipx, pdm - via pyproject.toml (wsl preferred):
    ```
    * clone to your local machine, set local $PATH manually in cfg.wsb and scoop.ps1.
    * run cfg.wsb to open container
    * inside container; try `boxy.bat` to init the container installation 
        - if it fails try again and if nothing you need to exit and restart the whole container
    * run `miniforge Prompt.lnk` to open a conda environment 
        - 'windows-key' + type 'terminal', select windows terminal
        - cd Desktop
        - .\"Miniforge Prompt.lnk"
        - conda create -n 3ten python=3.10
        - conda init
        - exit
        - cmd.exe (from inside windows terminal)
        - cd Desktop
        - .\"Miniforge Prompt.lnk"
        - conda activate 3ten
        - python3 -m pip install --upgrade pip
        - python3 -m pip install --user pipx
        - python -m pipx install virtualenv
        - python -m venv test_env
        - .\test_env\Scripts\activate  # unix->'source test_env/bin/activate'
        - pip install -e -r requirements.txt
    ```



    ### WSL Python_App install:
    ```
    wsl # this is the ubuntu-22.04 vers.
    python3 -m pip install --user pipx  # source it in .bashrc to add path
    python3 -m pipx ensurepath
    source .bashrc

    ```

    see: @`docs/wsl_install.md` for a quick and dirty 0-69 wsl guide.




    ### Advanced - potential runtime configuration or **kwargs:

    ```
    [[loopback|local host]]::Ollama binds 127.0.0.1 port 11434 by default. Change the bind address with the OLLAMA_HOST environment variable.

    ```


references to 'Hehner' are to Dr. Hehner and/or APTOP: http://www.cs.toronto.edu/~hehner/aPToP/

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