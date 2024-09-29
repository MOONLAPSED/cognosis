## Core Thesis

This thesis explores the conceptual and functional parallels between game players and ML agents, revealing their roles as dynamic executors of logic within interactive systems. At a first glance, players in games and ML agents performing tasks might seem conceptually distinct. However, both exhibit analogous interactions within their respective runtime environments, operating under predefined rules, altering state based on inputs, and utilizing specialized languages or frameworks to dictate behavior.

There is a clear overlap between the roles of players in games and ML agents. This overlap opens up possibilities for innovation, such as interactive AI training environments where players influence the model’s development directly, or game engines that incorporate ML logic to dynamically adjust difficulty or storylines based on player actions, or more exotically, as universal function compilers and morphological source code.

### Logic:

1. **Players and Agents as Analogous Entities**: Despite their conceptual differences, both players in games and ML agents exhibit analogous interactions within their respective runtime environments. They operate under predefined rules, alter state based on inputs, and utilize specialized languages or frameworks to dictate behavior.

#### Player in a Game:

  - **Interaction**: Engages with the game engine through inputs that change the game's state.
  - **Actions**: Executes actions such as defeating enemies, gathering resources, and exploring environments.
  - **Governance**: Operates within a domain-specific language (DSL), encompassing the game's mechanics, rules, and physics, all derived from the base bytecode.

#### ML/NLP Agent (e.g., Transformer Models):

  - **Interaction**: Processes inputs in the form of vector embeddings, generating inferences that inform subsequent outputs and decisions.
  - **Actions**: Engages in tasks such as text generation, information classification, and predictive analysis.
  - **Governance**: Functions under a stateful DSL, represented by learned statistical weights, activations, and vector transformations.

**Reversible Roles**: Both players and agents act as executors of latent logic. In a game, the player triggers actions (defeating enemies, altering game state), converting abstract mechanics into real consequences. Similarly, an ML agent converts latent vector states into actionable outputs (text generation, classification). This flip-flop highlights how both roles can reverse, with players acting like agents in a system and ML agents mimicking player behavior through inference.

2. **Computational and State Management Parallels**: Both paradigms epitomize computational environments where inputs prompt state changes, dictated by underlying rules.

- **State Representation and Management**: In both cases, the state is managed and transformed in real-time, with persistence mechanisms ensuring continuity and consistency.
- **Interactive Feedback Loops**: Both systems thrive on interactivity, incorporating feedback loops that continually refine and evolve the system’s state.

**Duality of State and Logic**: In both systems, the state and logic interact in ways that allow for the reversal of roles. For example, in a game, the player's actions trigger game logic to produce an outcome. In an ML environment, the model’s state (represented by vector embeddings) produces logical inferences based on inputs, essentially flipping the relationship between state and logic.

3. **Potential Convergence and Evolution**: Exploring the interplay between these domains can inspire innovations such as:

- **Morphological Source Code**: This could be a system where the source code itself is a representation of the system's state, allowing for changes in the system's behavior through modifications to the source code. Bytecode manipulation of homoiconic systems is one method which enables this. 'Modified quines' are a subset of homoiconic morphological source code systems that can be modified in real time.
- **Live Feedback Mechanisms**: Real-time interaction techniques from gaming could enhance model training and inference in ML.
- **Interactive State Manipulation**: Drawing from live coding paradigms, interactive interfaces for state management that respond to user inputs in real time.

**Cross-Domain Runtime Innovations**: By embracing the flip-flop dynamic, we can envision hybrid environments where players act as agents guiding AI inference or where ML models drive game state in real time, mimicking player behavior. This opens the door to new paradigms such as interactive AI training environments, where players influence the model’s development directly, or game engines that incorporate ML logic to dynamically adjust difficulty or storylines based on player actions.

## Follow-up line of inquiry:

Within such a runtime abstracted away from the hardware and energy required to train and run, there is no thermodynamic irreversibility, only information irreversibility, which seemingly means information supersedes time or the one-way speed of light as a limiting factor. This is a significant departure from the traditional view of thermodynamics, which posits that energy and entropy are fundamental to the universe. It helps to explain how information can be stored as state and how this state can be manipulated to perform tasks (e.g., training a model that can perform a task by just adding runtime energy!).