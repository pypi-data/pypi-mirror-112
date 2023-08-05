"""Module to hold RocketTokens custome exceptions"""


class BadlyFormattedTokenException(Exception):
    """Exception to be raised for tokens which do not pass validation."""


class InvalidTokenException(Exception):
    """Exception to be raised for tokens which do not pass validation."""


class PathMismatchException(InvalidTokenException):
    """Exception to be raised for tokens which do not pass validation."""


class MethodMismatchException(InvalidTokenException):
    """Exception to be raised for tokens which do not pass validation."""


class TokenExpiredException(InvalidTokenException):
    """Exception to be raised for tokens which do not pass validation."""


class NoPrivateKeyException(Exception):
    """
    Exception to be raised when an attempt is made to decode
    an encrypted token without access to a private key.
    """
