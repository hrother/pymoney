"""Exceptions for pymoney"""


class MoneyError(Exception):
    """Generic Money error"""


class InvalidAmount(MoneyError, ValueError):
    """Raised when the amount of money is invalid"""


class CurrencyMismatch(MoneyError, ValueError):
    """Raised when a operation is performed on money with different
    currencies."""


class UnsupportedOperatorType(MoneyError, TypeError):
    """Raised when a operation is performed with an unsupported type."""
