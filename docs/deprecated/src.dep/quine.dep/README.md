; Lambda Dracula RFC-style Definition

; Core Concepts
LambdaDracula = Quine Infector Transformer Propagator

; Quine Functionality
Quine = SelfReplicator SourceCodeRepresentation

; Infection Mechanism
Infector = TargetSelector InfectionVector PayloadInjector

; Transformation Capability
Transformer = ASTManipulator CodeRewriter BehaviorModifier

; Propagation Mechanism
Propagator = OffspringSeed EventQueueManager RuntimeTraversal

; Detailed Definitions
SelfReplicator = 1*(SELF-REFERENCE)
SELF-REFERENCE = "A programming construct that enables a function or module to invoke itself or reference its own definition."

SourceCodeRepresentation = 1*(CODE-AS-DATA)
CODE-AS-DATA = "Representation of source code that can be manipulated as data at runtime."

TargetSelector = 1*(RUNTIME-OBJECT-IDENTIFIER)
RUNTIME-OBJECT-IDENTIFIER = "Method or technique to find and identify objects within the runtime environment."

InfectionVector = 1*(CODE-INJECTION-METHOD)
CODE-INJECTION-METHOD = "The process or technique of inserting code into the target object."

PayloadInjector = 1*(SELF-CODE-INSERTION)
SELF-CODE-INSERTION = "Inserting the self-replicating code into the target object for infection."

ASTManipulator = 1*(AST-NODE-MODIFIER)
AST-NODE-MODIFIER = "Methods or techniques used to modify nodes within an Abstract Syntax Tree (AST)."

CodeRewriter = 1*(SOURCE-CODE-TRANSFORMER)
SOURCE-CODE-TRANSFORMER = "Techniques used to change or rewrite the source code."

BehaviorModifier = 1*(RUNTIME-BEHAVIOR-ALTERATION)
RUNTIME-BEHAVIOR-ALTERATION = "Techniques used to modify the runtime behavior of the system."

OffspringSeed = 1*(NEW-INSTANCE-CREATOR)
NEW-INSTANCE-CREATOR = "Mechanism to create new instances of LambdaDracula within the runtime environment."

EventQueueManager = 1*(ASYNC-EVENT-HANDLER)
ASYNC-EVENT-HANDLER = "Manages and processes asynchronous events related to infected functions."

RuntimeTraversal = 1*(OBJECT-GRAPH-EXPLORER)
OBJECT-GRAPH-EXPLORER = "Explores and traverses the object graph within the running environment."

; Integration with Python AST
LambdaDraculaModule = Module / FunctionDef / ClassDef

; Lambda Dracula specific AST nodes
LambdaDraculaStmt = InfectStmt / TransformStmt / PropagateStmt
LambdaDraculaExpr = QuineExpr / InfectorExpr / TransformerExpr

InfectStmt = "infect" "(" TargetExpr ")"
TransformStmt = "transform" "(" TargetExpr "," TransformationExpr ")"
PropagateStmt = "propagate" "(" EnvironmentExpr ")"

QuineExpr = "quine" "(" ")"
InfectorExpr = "create_infector" "(" InfectionStrategyExpr ")"
TransformerExpr = "create_transformer" "(" TransformationRuleExpr ")"

; Extensions to existing Python AST nodes
ExtendedFunctionDef = FunctionDef *(additional_infector) *(additional_transformer)
ExtendedClassDef = ClassDef *(additional_infector) *(additional_transformer)
additional_infector = InfectorExpr
additional_transformer = TransformerExpr

; New expression contexts
expr_context =/ Infect / Transform / Propagate

; Behavioral attributes
attributes =/ (is_quine / is_infector / is_transformer / is_propagator)

is_quine = "A marker indicating that the function or class exhibits self-replicating behavior."
is_infector = "A marker indicating that the function or class can infect other objects."
is_transformer = "A marker indicating that the function or class can transform other objects."
is_propagator = "A marker indicating that the function or class can propagate through the runtime environment."