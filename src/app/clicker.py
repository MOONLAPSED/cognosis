import pathlib
import logging
from pydantic import BaseModel, Field, ValidationError
from main import _initialize_paths
from classdef import MetaPoint
from click import Command, option, launch
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class Click(ABC):
    @abstractmethod
    def cli(self):
        pass

    @abstractmethod
    def shells(self):
        pass

    @abstractmethod
    def subshells(self):
        pass

class Clicker(MetaPoint, Click):
    """CLI COMPOSED WITH PYDANTIC BASE MODEL"""

    def __init__(self):
        super().__init__()

    @option('--data-file', type=pathlib.Path, help='Path to the data file')
    def cli(self, data_file):
        self.data_file = data_file
        self.run()

    def shells(self):
        # Define your shell logic here
        pass

    def subshells(self):
        # Define your subshell logic here
        pass

    def run(self):
        try:
            with open(self.data_file, 'r') as f:
                data = f.read()  # Placeholder, you might need different loading logic

            # Create a Pydantic model for the expected data structure
            class DataModel(BaseModel):
                value1: int = Field(..., ge=0)
                value2: str

            validated_data = DataModel.parse_raw(data)
            # Process your validated data here

        except FileNotFoundError:
            logger.error(f"Data file not found: {self.data_file}")
        except ValidationError as e:
            logger.error(f"Data validation failed: {e}")

if __name__ == "__main__":
    _initialize_paths()
    cmd = Command(name="clicker", callback=Clicker().cli)
    launch(cmd)
