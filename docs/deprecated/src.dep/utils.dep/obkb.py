# obsidian knowledge base
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import logging
import sys
import os
from src.app.abstract import BaseContextManager, BaseRuntime, BaseProtocol, TokenSpace

# Setup paths
vault_path = Path(__file__).parent / "my_vault"  # Your knowledge base directory
templates_path = Path(__file__).parent / "templates"
output_path = Path(__file__).parent / "output"
output_path.mkdir(parents=True, exist_ok=True)
Logger = logging.getLogger(__name__)


# Custom ContextManager for file operations
class FileContextManager(BaseContextManager):
    def __init__(self, file_path: Path, mode: str):
        self.file_path = file_path
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.file_path, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()


@dataclass
class KnowledgeItem:
    def __init__(self):
        self.name: str
        self.description: str
        self.category: str
        self.author: str
        self.date: datetime
        self.url_symlink: str
    title: str
    content: str
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now())

    def write_to_vault(self, vault_url_symlink: Path):
        filename = f"{self.created_at.strftime('%Y-%m-%d')}-{self.title.replace(' ', '-')}.md"
        file_path = vault_url_symlink / filename
        front_matter = f"""---
title: {self.title}
description: {self.description}
tags: {', '.join(self.tags)}
created_at: {self.created_at.isoformat()}
---
"""
        body = '\n\n'.join([front_matter, self.content])
        with FileContextManager(file_path, 'w') as file:
            file.write(body)
        Logger.info(f"Wrote {filename} to {vault_url_symlink}")

# Entry point for the script
if __name__ == '__main__':
    # Add the project root to the Python path
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.append(PROJECT_ROOT)