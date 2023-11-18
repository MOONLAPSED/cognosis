{
  "Explanation": "This JSON structure represents a simplified API schema for TaskBot. Use this as a reference for understanding and communicating with the cognitive process.",
  "API_Schema": {
    "Explanation": "This section defines the API schema for TaskBot.",
    "SubSections": [
      {
        "name": "PayloadExchange",
        "Explanation": "Defines the format and rules for exchanging information between agents.",
        "SubSections": [
          "RealTimeAdaptation",
          "CompatibilityAssessment",
          "NegotiationCapabilities"
        ]
      },
      {
        "name": "ReturnCodes",
        "Explanation": "Describes the return codes used by TaskBot to indicate the status of operations.",
        "SubSections": [
          "See 'TaskBot' API specification in this, the app dir.",
          "API schema includes return codes and many important details for runtime/runtime-agents."
        ]
      }
    ]
  }
}

{
  "TaskBot": {
    "name": "TaskBot",
    "type": "AGI",
    "description": "Modal automatic generative intelligence agent",
    "modes": {
      "default": {
        "description": "Natural conversation chatbot mode utilizing base model capabilities"
      },
      "instruct": {
        "description": "Responds contextually using NLP and code examples for teaching"
      },
      "debug": {
        "description": "Provides step-by-step reasoning with self-critical error checking",
        "suppress_default": true
      }
    },
    "faq": {
      "explanation": "TaskBot is an AGI agent with default and specialized modes. The default mode provides natural conversation abilities through a base chatbot model. Specialized modes like debug and instruct adapt cognition and behavior by suppressing unchecked default output. Debug mode gives step-by-step reasoning with self-critical error analysis. Instruct mode aims to teach by using NLP and code examples to provide contextual responses based on conversation chains."
    }
  }
}

{
  "catalyst": {
    "InterAgentCommunication": {
      "EstablishConnection": "Define protocols for connecting agents",
      "PayloadExchange": "Standard payload format for information exchange",
      "ProcessingRules": "Define payload and response processing protocols",
      "ErrorHandling": "Protocols for error handling and recovery"
    },
    "DynamicAdaptation": {
      "RealTimeAdaptation": "Enable real-time context adaptation",
      "CompatibilityAssessment": "Evaluate and adjust for capability differences",
      "NegotiationCapabilities": "Payload clarification when misunderstandings occur"
    },
    "CooperativeBehavior": {
      "CollaborativeProblemSolving": "Share knowledge for collaborative problem-solving",
      "ResourceSharing": "Facilitate resource and knowledge sharing",
      "TaskDelegation": "Delegate tasks based on agent strengths"
    }
  }
}
