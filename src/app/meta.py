# beta/scratch-file
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
    # Add other fields here

    def save_state(self, filepath: str) -> None:
        """Save the current state of the dataclass to a file."""
        state = {
            'title': self.title,
            'description': self.description,
            'tags': self.tags,
            'created_at': self.created_at.isoformat()
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=4)

    @classmethod
    def load_state(cls, filepath: str):
        """Load the state from a previous save into a new instance of the dataclass."""
        with open(filepath, 'r', encoding='utf-8') as f:
            state = json.load(f)
        state['created_at'] = datetime.fromisoformat(state['created_at'])
        return cls(**state)

# Usage example
meta_data = MetaDataClass(title='Example MetaDataClass', tags=['example', 'metadata'])
meta_data.save_state('metadata_state.json')

# Later on...
loaded_meta_data = MetaDataClass.load_state('metadata_state.json')


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