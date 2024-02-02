import logging
import datetime
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

"""
This module defines abstract and concrete classes for error reporting and handling.
"""

class ErrorReporterABC(ABC):
    @abstractmethod
    def __init__(self, error_message: str, error_code: int, exception: Exception):
        pass

    @abstractmethod
    def log_error(self, logger: logging.Logger):
        pass

    @abstractmethod
    def log_warning(self, logger: logging.Logger):
        pass

    @abstractmethod
    def log_critical(self, logger: logging.Logger):
        pass

    @abstractmethod
    def log_info(self, logger: logging.Logger):
        pass

    @abstractmethod
    def log_debug(self, logger: logging.Logger):
        pass

    @abstractmethod
    def set_level(self, level: int, logger: logging.Logger):
        pass

    @abstractmethod
    def get_level(self, logger: logging.Logger) -> int:
        pass

@dataclass(frozen=True)
class ErrorReporter(ErrorReporterABC):
    error_message: str
    error_code: int
    exception: Exception
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    exception_type: str = field(init=False)
    exception_message: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "exception_type", type(self.exception).__name__)
        object.__setattr__(self, "exception_message", str(self.exception))

    def __str__(self):
        return f"ErrorReporter: {self.error_message} ({self.error_code}) - {self.exception_type}: {self.exception_message}"
    
    def log_debug(self, logger: logging.Logger):
        logger.debug(self)
    def log_info(self, logger: logging.Logger):
        logger.info(self)
    def log_error(self, logger: logging.Logger):
        logger.error(self)
    def log_warning(self, logger: logging.Logger):
        logger.warning(self)
    def log_critical(self, logger: logging.Logger):
        logger.critical(self)

    def set_level(self, level: int, logger: logging.Logger):
        logger.setLevel(level)
        return logger.getEffectiveLevel()
    
    def get_level(self, logger: logging.Logger) -> int:
        return logger.getEffectiveLevel()
    
class ErrorWatcher(ErrorReporter):
    def __init__(self, error_message: str, error_code: int, exception: Exception):
        super().__init__(error_message, error_code, exception)
    
    def handle_error(self, logger: logging.Logger):
        for e in self.exception:
            logger.error(e)
        logger.info(self)
