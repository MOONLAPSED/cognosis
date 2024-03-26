# jekyll + jinja2 templating for 'static-site' generation - all sites are in a .md obsidian file strucutes, but can also be HTML, static javascript, etc. for 'actual' sites
# Jekyll Site Generation from Obsidian-style Knowledge Base

"""Note that this script assumes that your Markdown files have a title field in the front matter and that your Wiki links are in the format [[Note Name]]. 
You may need to adjust the regular expressions or other parts of the code based on your specific Markdown formatting conventions."""
import re
from pathlib import Path
from datetime import datetime
import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from jinja2 import Environment, FileSystemLoader
from typing import Optional, List

"""# This jina translation-layer and static jekyll site generator integrates with the KnowledgeBase and ContextManager classes to enable thread-safe processing of proxy files and metadata extraction from a centralized knowledge graph store which is immutable.
from kb import KnowledgeBase
from context import MyBaseContextManager, MyThreadSafeContextManager
""" # we will seperate these concerns into distinct submodules.

# Setup paths
vault_path = Path(__file__).parent / "my_vault"  # Your knowledge base directory
templates_path = Path(__file__).parent / "templates"
output_path = Path(__file__).parent / "output"
output_path.mkdir(parents=True, exist_ok=True)

@dataclass
class KnowledgeItem:
    title: str
    content: str
    tags: list[str]
    created: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    references: list[str] = None

    def write_to_vault(self, vault_path: Path):
        front_matter = f"""---
title: {self.title}
tags: {', '.join(self.tags)}
created: {self.created.isoformat()}
---

"""

        body = '\n\n'.join([self.content] + [f'[[{ref}]]' for ref in self.references or []])

        file_path = vault_path / (self.title.replace(' ', '_') + '.md')
        file_path.write_text(front_matter + body)

@dataclass
class MetaDataClass:
    title: str
    content: str
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now())
    references: list[str] = None

    def __init__(self, vault_path):
        obsidian_file_path = vault_path / f'{self.title}_{self.date:%Y%m%d%H%M%S}.md'

        body = '\n\n'.join([self.content] + [f'[[{ref}]]' for ref in self.references or []])

        file_path = vault_path / (self.title.replace(' ', '_') + '.md')

    def write_to_vault(self):
        self.file_path.write_text(self.front_matter + self.body)
        front_matter = f"""---
    title: {self.title}
    tags: {', '.join(self.tags)}
    created: {self.created.isoformat()}
    ---

    """
        self.obsidian_file_path.write_text(
            '---\n'
            f'date: {self.date:%Y%m%d%H%M%S}\n'
            f'title: {self.title}\n'
            '---\n\n'
            f'{self.content}'
        )

    def to_html(self, template_path: Path, output_path: Path):
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template("post.html")  # Assuming a post.html template
        metadata = {
            'title': self.title,
            'description': self.description,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
        }
        html_content = template.render(metadata=metadata, content=self.content)
        
        filename = f"{self.created_at.strftime('%Y-%m-%d')}-{self.title.replace(' ', '-')}.html"
        output_file = output_path / filename
        output_file.write_text(html_content)

def process_file(file_path: Path):
    with file_path.open() as f:
        content = f.read()

    # Parse the markdown file content
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    metadata_content = frontmatter_match.group(1) if frontmatter_match else ''
    
    # Extract metadata
    metadata = dict(re.findall(r"(\w+):\s*(.+)", metadata_content))
    content_body = content.split('---', 2)[-1].strip()
    metadata['content'] = content_body

    # Convert Date
    if 'date' in metadata:
        metadata['created_at'] = datetime.strptime(metadata['date'], '%Y-%m-%d %H:%M:%S')
        del metadata['date']
    
    # Convert tags from string to list
    if 'tags' in metadata:
        metadata['tags'] = [tag.strip() for tag in metadata['tags'].split(',')]

    post = MetaDataClass(**metadata)
    return post

def create_python_module_from_markdown(markdown_path: Path):
    markdown_content = markdown_path.read_text()
    title_search = re.search(r'^title: (.+)$', markdown_content, re.MULTILINE)
    if title_search:
        title = title_search.group(1).strip()
        python_module_name = title.replace(' ', '_') + '.py'
    else:
        raise ValueError('Title not found in markdown front matter')

    related_notes = re.findall(r'\[\[(.+?)\]\]', markdown_content)
    python_imports = '\n'.join(f'import {note.replace(" ", "_")}' for note in related_notes)

    python_module_path = vault_path / python_module_name
    python_module_content = f'""" Generated module for: {title} """\n\n{python_imports}\n\n# Your code here...'
    python_module_path.write_text(python_module_content)
    print(f'Module {python_module_name} created.')

# Main logic
if __name__ == "__main__":
    for file_path in vault_path.glob("*.md"):
        post = process_file(file_path)
        post.to_html(templates_path, output_path)

    print("Site generation completed.")