class CoreException(Exception):
    def __init__(self, message: str, detail: str | None = None):
        super().__init__(message)
        self.detail = detail or message

class NotFoundError(CoreException):
    pass

class ConflictError(CoreException):
    pass

class UnauthorizedError(CoreException):
    pass

class InvalidInputError(CoreException):
    def __init__(self, message: str, errors=None):
        super().__init__(message)
        self.errors = errors or []

class EthicalViolationError(CoreException):
    pass
