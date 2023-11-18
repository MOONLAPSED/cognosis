from random import choice

def process_custom_syntax(text, context):
    output = ""

    for token in text.split():
        if token.startswith("{{"):
            key = token[2:-2]
            if key in context:
                output += context[key] 
            elif key.startswith("~"):
                output += choice(context[key[1:]]) 
            elif key.startswith("+"):
                output += context[key[1:]] + " "
            elif key.startswith("="):
                output += context[key[1:]]
            elif key.startswith("!"):
                if key[1:] not in context:
                    output += key[1:] + " "
            elif key.startswith("-"):
                output += "NOT " + context[key[1:]] + " "
            elif key.startswith("*"):
                output += context[key[1:]] * 2 + " "
            else:
                output += token
        else:
            output += token + " "
    
    return output.strip()


text = "This is an {{example}} with some {{~placeholders}} and {{+concatenation}}."

context = {
    "example": "custom text",
    "placeholders": ["placeholder1", "placeholder2", "placeholder3"],
    "concatenation": "text"
}

print(process_custom_syntax(text, context))