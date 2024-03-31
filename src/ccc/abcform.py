from typing import Callable, Union, Tuple, List
from dataclasses import dataclass

from abc import ABC, abstractmethod
from typing import Dict

class FormalTheory(ABC):
    """
    A class that implements a Formal Theory for a stateful entity.
    """

    def __init__(self, initial_state: Dict):
        """
        Initialize the state of the system.
        
        Args:
            initial_state (dict): A dictionary representing the initial state of the system.
        """
        self.state: Dict = initial_state
        
    @abstractmethod
    def touch_state(self):
        """
        Update the state of the system based on the given changes, or update its time stamp if the changes are invalid (report uuid error?).
        
        Args:
            changes (dict): A dictionary representing the changes to be made to the system state.

        try:
            self.state.update(changes)
        except ValueError:
            raise ValueError("Invalid state change.")
        finally:
            return self.state
        """
        return self


    def get_state(self):
        """
        Return the current state of the system.
        
        Args:
            state (str): The name of the state to be retrieved, updating only time stamp.
        Returns:
            dict: The current state of the system.

        try:
            self.state.(state)
        except ValueError:
            raise ValueError("Invalid state change.")
        finally:
            return self.state
        """
        return self
    
    @abstractmethod
    def execute_action(self):
        """
        Execute an action on the system and update the state accordingly.
        
        Args:
            action (callable): A function that takes the current state as input and returns the updated state.
        
        self.state = action(self.state)
        """
        return self
        
    def check_condition(self):
        """
        Check if the given condition is satisfied by the current state of the system.
        
        Args:
            condition (callable): A function that takes the current state as input and returns a boolean value.
        
        Returns:
            bool: True if the condition is satisfied, False otherwise.
        
        return condition(self.state)
        """
        return self


def main():
    system = FormalTheory({'x': 0, 'y': 0})
    print(f"state: {system.get_state()}")

if __name__ == "__main__":
    main()