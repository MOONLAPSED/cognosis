# jekyll + jinja2 templating for 'static-site' generation - all sites are in a .md obsidian file strucutes, but can also be HTML, static javascript, etc. for 'actual' sites
# Jekyll Site Generation from Obsidian-style Knowledge Base

"""Note that this script assumes that your Markdown files have a title field in the front matter and that your Wiki links are in the format [[Note Name]]. You may need to adjust the regular expressions or other parts of the code based on your specific Markdown formatting conventions."""

import re
from pathlib import Path
from datetime import datetime
import os
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from kb import KnowledgeBase
from context import MyBaseContextManager, MyThreadSafeContextManager

# Setup
vault_path = Path(__file__).parent / "my_vault"  # Your knowledge base directory
templates_path = Path(__file__).parent / "templates" 
output_path = Path(__file__).parent / "output"  

def process_file(file_path: Path):
    """Processes a single file, extracts metadata, and applies template."""
    with file_path.open() as f:
        lines = f.readlines()

    metadata = {}
    content = []
    in_frontmatter = True

    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
        elif in_frontmatter:
            # Extract metadata (assume key: value format)
            key, value = line.strip().split(":")
            metadata[key.strip()] = value.strip()
        else:
            content.append(line)

    # Apply template
    env = Environment(loader=FileSystemLoader(templates_path))
    template = env.get_template("post.html")  # Assuming a post.html template
    output = template.render(metadata=metadata, content="".join(content))

    # Write output
    output_file = output_path / (metadata["title"].replace(" ", "_") + ".html")
    output_file.write_text(output)

# Main logic
if __name__ == "__main__":
    for file_path in vault_path.glob("*.md"):
        process_file(file_path)