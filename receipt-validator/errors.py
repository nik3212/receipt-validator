class ValidationError(Exception):
    """ Base class """


class AppStoreValidationError(ValidationError):
    """  """

    def __init__(
        self,
        message: str
    ):
        """  """
