# cognitive coherence coroutines

 -/hyde/ - is the home of all ruby gems and jekyll files
 -/src/ - is the home of all python application files
 -/api/ - api-def and README.md

The repo is beginning to sprawl, allow ccc to converge the dispirate parts into a coherent whole. ccc will orchestrate the static 'runtime' mutable files 'testing' against the immutable 'knowledge graph' which, at this stage, will always take the form of an unsorted directory full of files with contents and at its most-basic; amounts to a directory tree of dirs and files which are visible at runtime.

## init
 -we use some method to acquire pip, we then install pipx and PDM.

 -we use PDM to install dependencies from Pipfile and setup virtual env.
 
 -we init python logging for the build-out as-fast as possible in main.py
 
 -we init ruby gems and jekyll build environment using bundler
 
 -we init (not yet implemented) python api
 
 -we init (not yet implemented) GO server

\# -we init rust via rustup for future Rust needs

\# -we init node via NPM and JDK vía SDKMAN! for future JavaScript and Java needs

\# -we init docker and kubernetes routines and coroutines including iteration etc. (not yet implemented)

 -we utilize python to populate our static runtime files (jekyll, markdown etc) using jinja templates and markdown filters - creating a 'traversable' artifact (for ai agents) as we go

 -we utilize python to instantiate agent behavior, file-system (jekyll) and api (not yet implemented) interaction and evolution - when we create good artifacts with coherent thought patterns and utilize git versioning for genetic failures.


## rationale
Okay, we have a bunch of programming languages and compilers and things? Well, yes, the project does have a wide-base because the goals of the program are for the program to expand its own goals. We establish the core data structure, the main repository, and then allow various languages and tools to build upon that core while utilizing continous integration practices to keep everything coherent and with git as the panopticon are able to re-cohere or re-wind, permutate, iterate, perhaps even curry or serialize. Indeed, I may as-well trot out some neologisim or another because I need to start to **define** what any of that entails. For now, the core data structure is a directory tree - a knowledge graph in name only. But it gives me something to refer-to, a knowledge graph is an evolving data structure at runtime not just in the development-sense. All changes to the graph can and will be abstracted to-changes-to files, file contents, metadata, and directory (permissions, shell environment and ENV variables) structure + state; implemented as abstract dataclasses, modules, Named Tuples, or SimpleNamespaces at runtime. A diversity of methods are provided but they are **all** the core methods; they are not meant to evolve independently of one-another. The core data structure itself and its (for lack of a better descriptor: instance) methods must evolve together to remain coherent. That is to say that the class and class methods (init, __enter__ (context managers), __call__, etc.) must evolve together in lock-step to remain coherent, while instance methods are able to preform runtime action and evolve based-on what they encounter. The overall goal is to define and evolve the core datastructure and its methods in a way that allows for the coherent and continuous integration of diverse solutions to evolving problems without those solutions fragmenting the whole or each-other.

## okay, but why really?
For AI agents. For humans. For both - the latent AI coroutines are improved-by and-always-positioned-for the user. Every user has its own kb and goals. The kb grows more coherent over time as the user and AI work together. AI helps user, user helps AI helps user better. Win-win. The first system is 'obsidian flash cards' which involves no AI or evolving instance methods, instead it is a collection of (python) submodules that build a flashcard app for spaced repetition learning using Obsidian (or whatever godforsaken mess the user may call an obsidian vault) as the kb. The point is that either user OR ai can do flash cards, or they can do them together as a team. The ai is always learning from the user and improving its pedagogic and semantic coherence in the long-term via its own evolving instance methods and the users (or agent's 'forked') evolving kb.

Flash cards should massage the user's kb into a more coherent semantic graph over time. They should point out gaps, inconsistencies, related ideas that could be connected via backlinking, [[entities]] to-be disambiguated or expanded upon. In summary - spaced repetition is the initial vehicle for evolving a kb coherently but it is not the end goal. The end goal is an AI-augmented, mutually-evolving semantic network that benefits both user and AI over the long run.