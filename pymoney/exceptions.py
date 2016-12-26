"""Exceptions for pymoney"""


class MoneyError(Exception):
    """Generic Money error"""


class InvalidAmount(MoneyError, ValueError):
    """Raised when the amount of money is invalid"""
