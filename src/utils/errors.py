import logging
import datetime
from dataclasses import dataclass, field, InitVar
from abc import ABC, abstractmethod
import logging

"""plugs into: errors.py. See:
    # Update the 'file' handler to use the provided `log_file_path`
    LOGGING_CONFIG['handlers']['file']['filename'] = log_file_path
    
    # Configure the logging using the config dictionary
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Create loggers
    root_logger = logging.getLogger()  # root logger
    sub_logger = logging.getLogger('branch')
    tertiary_logger = logging.getLogger('branch.leaf')
    return root_logger, sub_logger, tertiary_logger
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
    exception_type: InitVar[str] = field(init=False)
    exception_message: InitVar[str] = field(init=False)

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

        pass

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

    

class FallbackError(ErrorWatcher):
    def __init__(self):
        super().__init__("An unspecified error has occurred.")

    def handle_error(self, logger):
        logger.error("FallbackError: " + self.message)


class BadRequestError(ErrorWatcher):
    def __init__(self):
        super().__init__("Bad Request: Malformed request")

    def handle_error(self, logger):
        logger.error("BadRequestError: " + self.message)

class UnsupportedActionError(ErrorWatcher):
    def __init__(self):
        super().__init__("Unsupported Action: Unimplemented action")

    def handle_error(self, logger):
        logger.error("UnsupportedActionError: " + self.message)

class BadParamError(ErrorWatcher):
    def __init__(self):
        super().__init__("Bad Param: Invalid parameter")

    def handle_error(self, logger):
        logger.error("BadParamError: " + self.message)

class BadHandlerError(ErrorWatcher):
    def __init__(self):
        super().__init__("Bad Handler: Implementation error")

    def handle_error(self, logger):
        logger.error("BadHandlerError: " + self.message)

class InternalHandlerError(ErrorWatcher):
    def __init__(self):
        super().__init__("Internal Handler Error: Uncaught exception")

    def handle_error(self, logger):
        logger.error("InternalHandlerError: " + self.message)
