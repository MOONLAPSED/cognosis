import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

def KnowledgeBase(vault_path):
    kb = {}

    for file_path in vault_path.glob('*.md'):
        with file_path.open() as f:
            metadata = json.loads(f.readline())
            kb[metadata['title']] = {
    'path': str(file_path),
    'metadata': metadata
}

@dataclass
class MetaDataClass:
    title: str
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default=datetime.now(timezone.utc))
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

# Example usage:
obsidian_vault = Path(__file__).parent / '.obsidian'
obsidian_vault.mkdir(exist_ok=True)

# Let's say you have a list of dicts representing your files
files_data = [
    {'title': 'Article 1', 'content': 'Content of article 1', 'date': '20230408103025'},
    {'title': 'Article 2', 'content': 'Content of article 2'}
    # If 'date' is omitted, the current date and time will be used
]
# Generate a Python module based on a markdown file
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

# Example usage
markdown_files = list(vault_path.glob('*.md'))
for md_path in markdown_files:
    create_python_module_from_markdown(md_path)