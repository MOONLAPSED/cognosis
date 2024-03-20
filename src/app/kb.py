import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

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
