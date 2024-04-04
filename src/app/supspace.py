from abc import ABC, abstractmethod
from typing import Any, Optional, Type


class Resource(ABC):
    """
    Abstract base class for managing a single type of system or application resource.
    """

    @abstractmethod
    def acquire(self):
        """
        Acquire the resource.
        """
        pass

    @abstractmethod
    def release(self):
        """
        Release the resource.
        """
        pass


class Executable(ABC):
    """
    Abstract base class representing a unit of work that can be executed.
    """

    @abstractmethod
    def prepare(self, **params):
        """
        Prepare the executable with necessary parameters.
        """
        pass

    @abstractmethod
    def run(self):
        """
        Run the executable.
        """
        pass


class Authenticator(ABC):
    """
    Abstract base class for authentication mechanisms.
    """

    @abstractmethod
    def authenticate(self, credentials):
        """
        Authenticate a user or process based on credentials.
        """
        pass

    @abstractmethod
    def deauthenticate(self):
        """
        Deauthenticate the current user or process.
        """
        pass


class Permission(ABC):
    """
    Abstract base class for managing access permissions.
    """

    @abstractmethod
    def check(self, permission):
        """
        Check if a certain permission is granted.
        """
        pass

    @abstractmethod
    def assign(self, permission):
        """
        Assign a new permission.
        """
        pass


class Logger(ABC):
    """
    Abstract base class for logging system messages.
    """

    @abstractmethod
    def log(self, message, level):
        """
        Log a message with a specified severity level.
        """
        pass