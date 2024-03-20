import logging
import abc
import typing
import dataclasses
from abc import ABC, abstractmethod
from click import command, option, argument
from dataclasses import dataclass, field
from pathlib import Path
from pydantic import BaseModel, ValidationError, validator
from typing import List, Dict, Any, Optional, Union
from collections import namedtuple  # For SimpleNamespace alternative
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
SimpleFileRecord = namedtuple("SimpleFileRecord", ["filepath", "metadata", "tags"])


class ObsidianFile(BaseModel):
    title: str
    content: str
    date: datetime = datetime.now()
    
    @validator('date', pre=True)
    def validate_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, '%Y%m%d%H%M%S')
        elif isinstance(value, datetime):
            return value
        raise ValueError('Invalid date format')

    @validator('title', 'content')
    def not_empty(cls, v):
        if not v:
            raise ValueError('must not be empty')
        return v

    class Config:
        arbitrary_types_allowed = True  # Allows any type to be used; use with caution

    def write_to_vault(self, vault_path: Path) -> None:
        obsidian_file_path = vault_path / f'{self.title}_{self.date:%Y%m%d%H%M%S}.md'
        obsidian_file_path.write_text(
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

for file_data in files_data:
    try:
        obsidian_file = ObsidianFile(**file_data)
        obsidian_file.write_to_vault(obsidian_vault)
    except ValidationError as e:
        print(f'Error validating file data: {e}')