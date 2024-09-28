# Guidelines for Creating Informative and Self-contained `{Prompt}` Objects for Runtime Instantiated Agents

> See also: [Prompt Objects](/docs/prompt.json)  
> See also: [Meta Prompting](/docs/meta_prompt.yaml)

## Introduction

The purpose of this document is to provide comprehensive guidelines for creating informative and self-contained `{prompt}` objects for use with runtime instantiated agents. These agents operate using pre-trained large language models (LLMs) and are dynamically configured during their ephemeral runtime states. The focus is on producing `{prompt}` objects tailored to specific tasks or domains, facilitating effective AI chatbot responses with instructions and constraints.

## Key Considerations for Prompt Engineering

When creating `{prompt}` objects for runtime instantiated agents, several key considerations should be taken into account:

1. **Understand the Specific Purpose and Requirements**: Clearly define the purpose of the `{prompt}` and identify the target domain(s) it will serve, such as Prompt Engineering, Prompt Generation, NLP tasks, or AI assistance. This understanding is crucial for tailoring the `{prompt}` effectively.
2. **Clarity, Specificity, and Context**: Ensure that the `{prompt}` is well-defined, specific, and contextually rich to provide sufficient information for generating desired responses. Avoid ambiguity and vagueness in the `{prompt}`.
3. **Incorporate Necessary Data and Context**: Include all relevant data and context within the `{prompt}` object, which may involve using variables and placeholders to represent dynamic elements.
4. **Address Potential Biases and Variations**: Be mindful of potential biases or variations in the `{prompt}` that may influence the generated responses. Provide guidelines on how to handle these biases and variations appropriately.
5. **Explicit Instructions and Guidelines**: Clearly specify the instructions and constraints for generating responses based on the `{prompt}`. Ensure that the AI model knows the boundaries and limitations.
6. **Structured Data Formats**: Utilize structured data formats like JSON to represent the `{prompt}` object. Consistent naming conventions, nesting, and comments can enhance readability and understanding.

## How to Ensure Inclusion of Necessary Data and Context

To ensure that a `{prompt}` object includes all the necessary data and context, follow these steps:

1. **Define Variables and Placeholders**: Identify the dynamic elements in the `{prompt}` that require specific values during generation. Represent these elements as variables or placeholders.
2. **Provide Examples and Data Sources**: If applicable, offer examples of data or entities that can fill the variables or placeholders. You can also reference external data sources to populate these elements.
3. **Contextual References**: Refer to relevant information from previous questions or interactions within the `{prompt}` object to maintain context and coherence.
4. **Use Structured Data Formats**: Use JSON or other structured formats to organize and represent the data and context effectively.

## Guidelines for Addressing Potential Biases and Variations

To address potential biases and variations in `{prompt}` objects, follow these guidelines:

1. **Controlled Language**: Employ controlled language and instructions in the `{prompt}` to steer the AI model away from generating biased or inappropriate responses.
2. **Contextual Sensitivity**: Make the `{prompt}` sensitive to context, so the generated responses align with the intent and appropriateness for different scenarios.
3. **Bias Testing and Validation**: Regularly test and validate the responses from the `{prompt}` to identify and rectify any unintended biases.

## Strategies for Providing Explicit Instructions and Guidelines

To provide explicit instructions and guidelines within a `{prompt}` object, follow these strategies:

1. **Precise Language**: Use clear and concise language to express the instructions and constraints. Avoid ambiguity or vagueness that could lead to misinterpretation.
2. **Step-by-Step Instructions**: Break down complex tasks or requirements into step-by-step instructions to guide the AI model's responses effectively.
3. **Boundary Definitions**: Clearly define the boundaries and limitations within which the AI model should operate. Specify what is allowed and what is not allowed in the generated responses.
4. **Example Usage**: Provide examples of correct usage and expected responses to demonstrate the desired behavior.
5. **Error Handling**: Include instructions on how to handle potential errors or unexpected situations. Define fallback options or alternative instructions.
6. **Documentation and References**: Include relevant documentation, guidelines, or references within the `{prompt}` object to assist users in understanding and following the instructions effectively.

## Examples of Existing High-quality `{Prompt}` Objects

Here are a few examples of existing high-quality `{prompt}` objects for runtime instantiated agents that can serve as references:

### Customer Support `{Prompt}` Object

```json
{
  "data": {
    "purpose": "Generating customer support responses",
    "target_domain": "Customer service",
    "instructions": "Provide step-by-step troubleshooting guidance for common issues faced by customers."
  },
  "context": "The purpose of this `{prompt}` object is to assist AI models in generating accurate and helpful responses to customer support queries.",
  "variables": {
    "issue_type": ["connectivity", "billing", "product"],
    "troubleshooting_steps": ["Check connections", "Restart the device", "Update software"]
  }
}
```

### Code Refactoring `{Prompt}` Object

```json
{
  "data": {
    "purpose": "Generating refactoring suggestions for code",
    "target_domain": "Software development",
    "instructions": "Identify and suggest code refactorings to improve performance and maintainability."
  },
  "context": "This `{prompt}` object aims to guide AI models in generating actionable code refactoring recommendations.",
  "variables": {
    "code_snippet": "<INSERT CODE SNIPPET HERE>"
  }
}
```

### Legal Document Analysis `{Prompt}` Object

```json
{
  "data": {
    "purpose": "Generating insights from legal documents",
    "target_domain": "Legal industry",
    "instructions": "Analyze legal contracts for potential risks and highlight critical clauses."
  },
  "context": "This `{prompt}` object facilitates AI models in extracting valuable information from legal documents.",
  "variables": {
    "document_text": "<INSERT LEGAL DOCUMENT TEXT HERE>"
  }
}
```

Please note that the above examples are just illustrative and may require further customization to suit specific needs.

## References

To further enhance your understanding and implementation of {prompt} objects, consider referring to the following:

- Published research papers on prompt engineering
- Documentation and guidelines from OpenAI
- Existing high-quality {prompt} objects, such as those used by OpenAI and Antrhopic

By following these guidelines and leveraging structured data formats, you can create informative and self-contained {prompt} objects that effectively guide runtime instantiated agents in generating responses with instructions and constraints, ensuring clarity, context, and relevance to the desired purpose and domain.