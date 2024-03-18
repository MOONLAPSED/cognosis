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
logger = logging.getLogger(__name__)
SimpleFileRecord = namedtuple("SimpleFileRecord", ["filepath", "metadata", "tags"])
class FileModel(BaseModel):
        # enables using fields with non-Python built-in types and custom classes in the FileValidationBase class.
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            type: lambda v: v.__name__
        }

    filepath: Path
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    extracted_text: Optional[str] = None
    summary: Optional[str] = None

    def process_text_file(self):
        with open(self.filepath, 'r') as file:
            # Sample NLP - Very basic for illustration
            self.extracted_text = file.read()
            self.tags.extend(self.filepath.suffixes)

    def create_file_model(filepath: Path):
        file_model = FileModel(filepath=filepath)

        if filepath.suffix in ['.md', '.txt']:
            file_model.process_text_file()
        # ... Other processing logic based on file type, tags, metadata, etc.
        """  "check for 'error'" example for subclasses to extend
        simple_analysis = self.extracted_text.lower().count('error')
        if simple_analysis > 0:
            self.tags.append('error')
        else:
            self.tags.append('ok')
        """
        return file_model
    

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        abspath=str(self.file_must_exist(self.filepath))
        self.valid = self.validate()
        if not self.valid:
            raise ValueError(f"Validation failed for {self.filepath}")

    @classmethod
    def handle_kwargs(cls, **kwargs):
        # Pop the first file path from kwargs and queue the rest
        first_filepath = kwargs.pop('filepath', None)
        queued_filepaths = [Path(fp) for fp in kwargs.values()]

        # Return a dataclass containing the first file path and the queued file paths
        @dataclass
        class FilePathsData:
            first_filepath: Path
            queued_filepaths: List[Path]

        return FilePathsData(first_filepath=first_filepath, queued_filepaths=queued_filepaths)

    @classmethod
    def validate(cls):
        return cls.valid or False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"

    @validator('filepath')
    def file_must_exist(cls, v):
        if not v.exists():
            logging.Logger.info(f"Validating file {v} failed: File not found")
            raise ValueError(f"File not found: {v}")
        return v.absolute()

class TextFileValidation(FileValidationBase):
    @validator('filepath')
    def is_text_file(cls, v):
        if v.suffix not in ['.md', '.txt']:
            raise ValueError(f"Unsupported file type: {v}")
        return v

    def validate(self):
        super().validate()
        with open(self.filepath, 'r') as file:
            content = file.read().strip()
            if not content:
                raise ValueError(f"File {self.filepath} appears to be empty")

class MultimediaFileValidation(FileValidationBase):
    @validator('filepath')
    def is_multimedia_file(cls, v):
        if v.suffix not in ['.jpg', '.png', '.mp4', '.mp3']:
            raise ValueError(f"Unsupported multimedia file type: {v}")
        return v

    def validate(self):
        super().validate()
        # Tagging as multimedia, skipping content validation
        logger.info(f"File {self.filepath} is tagged as multimedia and skipped from content validation")


def create_file_model(filepath: Path):
    file_model = FileModel(filepath=filepath)

    if filepath.suffix in ['.md', '.txt']:
        file_model.process_text_file()
    # ... Other processing logic based on file type

    return file_model
