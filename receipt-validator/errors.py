class ValidationError(Exception):
    """ Base class """

    pass


class AppStoreValidationError(ValidationError):
    message = None

    def __init__(
        self,
        message: str
    ):
        self.message = message

        super().__init__(message)

    def __str__(self) -> str:
        return self.message
