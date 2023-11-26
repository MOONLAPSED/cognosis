import re
import typer
from base64 import b64encode

app = typer.Typer()

CAMEL_REGEX = r'\{\{([A-Z_]+)\}\}'
# additional regexes can be added here for processing keys that are found by CAMEL_REGEX eg:
# RegexDict = {
    # 'camel': CAMEL_REGEX,
    # 'camel_lower': CAMEL_REGEX.lower(),
    # 'camel_upper': CAMEL_REGEX.upper(),
    # 'camel_capitalize': CAMEL_REGEX.capitalize(),
    # 'camel_title': CAMEL_REGEX.title(),
    # 'camel_swapcase': CAMEL_REGEX.swapcase(),
    # 'camel_casefold': CAMEL_REGEX.casefold(),
    # 'camel_strip': CAMEL_REGEX.strip(),
    # 'camel_lstrip': CAMEL_REGEX.lstrip(),
    # 'camel_rstrip': CAMEL_REGEX.rstrip(),
    # 'camel_replace': CAMEL_REGEX.replace('a', 'b'),
    # 'camel_split': CAMEL_REGEX.split('a'),
    # 'camel_rsplit': CAMEL_REGEX.rsplit('a'),
    # 'camel_startswith': CAMEL_REGEX.startswith('a'),
    # 'camel_endswith': CAMEL_REGEX.endswith('a'),
    # 'camel_find': CAMEL_REGEX.find('a')
# }

class TextChunker:
    def __init__(self, input_text: str, chunk_size: int = 4096, max_chunks: int = 100):
        self.input_text = input_text
        self.chunk_size = chunk_size  
        self.max_chunks = max_chunks

    def get_chunks(self) -> List[str]:
        chunks = []
        for i in range(0, len(self.input_text), self.chunk_size):
            chunk = self.input_text[i:i+self.chunk_size]
            encoded_chunk = b64encode(chunk.encode()).decode()
            chunks.append(encoded_chunk)
        return chunks

    def process_chunks(self):
        chunks = self.get_chunks()
        
        if len(chunks) == 0: 
            return ["<im_start>|im_end>"]

        processed_chunks = []
        max_cont_chunks = self.max_chunks

        for i, chunk in enumerate(chunks):
            if i == 0: 
                processed_chunk = f"<im_start>{chunk}"
            elif i == len(chunks)-1:
                processed_chunk = f"<im_end>{chunk}" 
            elif i < max_cont_chunks:
                processed_chunk = f"<cont>{i}:{chunk}"
            else:
                processed_chunk = f"<cont>{chunk}"

            processed_chunks.append(processed_chunk)

        return processed_chunks

class PostProcessor:
    def __init__(self):
        pass

    def process_chunk(self, chunk: str, chunk_num: int) -> str:
        # Step 1: Find all camel case variables
        camel_matches = re.findall(CAMEL_REGEX, chunk)
        camel_vars = {match.lower(): '' for match in camel_matches}
        
        # Step 2: Replace variables with values from context
        for var, value in camel_vars.items():
            if var in context:
                chunk = chunk.replace('{{' + var + '}}', context[var])
        # Step 3: Additional processing steps...
        return chunk

@app.command()
def main(
    input_text: str,
    chunk_size: int = 4096,
    max_chunks: int = 100
):

    chunker = TextChunker(input_text, chunk_size, max_chunks)
    chunks = chunker.process_chunks()

    processor = PostProcessor()
    processed_chunks = []
    for i, chunk in enumerate(chunks):
        processed = processor.process_chunk(chunk, i) 
        processed_chunks.append(processed)
        
    typer.echo(processed_chunks)

if __name__ == "__main__":
    app()

{"schema": "The provided logic is a description of a custom syntax or markup language that defines how to generate content based on various rules, conditions, and functions. This description outlines the syntax and semantics for defining these rules and conditions."}

"""
// Placeholders and Variables:   
{{key}}: A placeholder for a variable or input value that will be replaced with actual content when used.
${{key}}: A variable or input value that is instantiated or declared and is only required once per variable. It is not replaced with content but serves to declare variables.

// Modifiers:
~{{key}}: Indicates an approximate value or range for the specified key. 
+{{key}}: Appends or concatenates the value of key with another element.
={{key}}: Specifies that the generated content should have an exact match or value equal to key.
!{{key}}: Negates or excludes the value of key from the generated content.  
-{{key}}: Removes or subtracts the value of key from the generated content.
*{{key}}: Specifies that the generated content should repeat the specified property or attribute key times.  
>{{key}}, <{{key}}, <={{key}}, >={{key}}: Define length comparisons for generated content.

// Conditional Expressions:
?{{key1}}:{{key2}}: Used for conditional expressions, where if the condition specified by key1 is met, the generated content will include key2.

// Keywords:   
ANY, ALWAYS, NEVER, WITH, AND, ONLY, NOT, UNIQUE: Keywords that modify or constrain the generated content based on specific conditions.

// Functions:
between({{key1}}, {{key2}}): Specifies a range for a certain attribute or property in the generated content.  
random({{key1}}, {{key2}}, ...): Specifies that the generated content should include one of the provided keys at random.
mixed({{key1}}, {{key2}}, ...): Specifies that the generated content should include a combination of the provided keys.
contains({{key}}): Indicates that the generated content must contain the specified key.
optimize({{key}}): Suggests that the generated content should optimize for a certain aspect represented by the key.
limit({{key}}, {{value}}): Sets a limit on the number of times the specified key can appear in the generated content.

// Function Arguments:
fn(-{{key}}): Represents a function fn that takes the value of key as an input and removes or subtracts it from the generated content. 
fn(*{{key}}): Represents a function fn that takes the value of key as an input and repeats a specific property or attribute key times.
fn(?{{key1}}:{{key2}}): Represents a function fn that takes the values of key1 and key2 as inputs and includes key2 in the generated content if the condition specified by key1 is met.
"""