import logging

class ErrorHandler(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def handle_error(self):
        logging.error(self.message)

class FallbackError(ErrorHandler):
    def __init__(self):
        super().__init__("An unspecified error has occurred.")

    def handle_error(self):
        logging.error("FallbackError: " + self.message)

class BadRequestError(ErrorHandler):
    def __init__(self):
        super().__init__("Bad Request: Malformed request")

    def handle_error(self):
        logging.error("BadRequestError: " + self.message)

class UnsupportedActionError(ErrorHandler):
    def __init__(self):
        super().__init__("Unsupported Action: Unimplemented action")

    def handle_error(self):
        logging.error("UnsupportedActionError: " + self.message)

class BadParamError(ErrorHandler):
    def __init__(self):
        super().__init__("Bad Param: Invalid parameter")

    def handle_error(self):
        logging.error("BadParamError: " + self.message)

class BadHandlerError(ErrorHandler):
    def __init__(self):
        super().__init__("Bad Handler: Implementation error")

    def handle_error(self):
        logging.error("BadHandlerError: " + self.message)

class InternalHandlerError(ErrorHandler):
    def __init__(self):
        super().__init__("Internal Handler Error: Uncaught exception")

    def handle_error(self):
        logging.error("InternalHandlerError: " + self.message)
