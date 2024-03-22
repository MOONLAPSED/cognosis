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


def obsidian_to_jekyll(obsidian_vault_path, jekyll_site_path):
   """
   Converts an Obsidian-style knowledge base (individual Markdown files) to a Jekyll site.

   Args:
       obsidian_vault_path (Path): The path to the Obsidian vault (directory containing Markdown files).
       jekyll_site_path (Path): The path to the Jekyll site directory.

   Returns:
       None
   """
   # Create the _posts directory if it doesn't exist
   jekyll_posts_dir = jekyll_site_path / '_posts'
   jekyll_posts_dir.mkdir(parents=True, exist_ok=True)

   # Iterate over Markdown files in the Obsidian vault
   for md_path in obsidian_vault_path.glob('*.md'):
       markdown_content = md_path.read_text()

       # Extract the title from the front matter
       title_search = re.search(r'^title: (.+)$', markdown_content, re.MULTILINE)
       if title_search:
           title = title_search.group(1).strip()
           jekyll_post_name = title.replace(' ', '-') + '.md'
       else:
           raise ValueError('Title not found in markdown front matter')

       # Find all related notes (Wiki links)
       related_notes = re.findall(r'\[\[(.+?)\]\]', markdown_content)
       jekyll_post_imports = '\n'.join(f'  - {note}' for note in related_notes)

       # Create the Jekyll post content
       jekyll_post_content = f"""---
layout: post
title: "{title}"
references:
{jekyll_post_imports}
---

{markdown_content}
"""

       # Write the Jekyll post to the _posts directory
       jekyll_post_path = jekyll_posts_dir / jekyll_post_name
       jekyll_post_path.write_text(jekyll_post_content)
       print(f'Jekyll post created: {jekyll_post_path}')

# Example usage
obsidian_vault_path = Path('/path/to/your/obsidian/vault')
jekyll_site_path = Path('/path/to/your/jekyll/site')

obsidian_to_jekyll(obsidian_vault_path, jekyll_site_path)