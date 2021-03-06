# -*- coding: utf-8 -*-
import decimal
from decimal import Decimal as D

from .exceptions import (
    InvalidAmount,
    CurrencyMismatch,
    UnsupportedOperatorType,
)


class Money(object):
    """Representation of a monetary value. Money consists of an decimal amount
    and an currency.

    The :attr:`amount` of :class:`Money` is rounded using
    :attr:`rounding_method` with :attr:`cent_factor`. Which default to
    :attr:`rounding_method` = decimal.ROUND_HALF_EVEN and
    :attr:`cent_factor` = '.01'

    :param amount: The value of the instance. The given `amount` will be
    converted into an :class:`decimal.Decimal` and rounded.
    :type amount: numeric
    :param str currency: string representation of the currency country
    code.
    """

    cent_factor = '.01'
    rounding_method = decimal.ROUND_HALF_EVEN

    def __init__(self, amount, currency):
        """Create a :class:`Money` instance with given `amount` and `currency`.

        :param amount: The value of the instance. The given `amount` will be
        converted into an :class:`decimal.Decimal` and rounded.
        :param str currency: string representation of the currency country
        code.
        """
        try:
            amount = D(amount)
        except decimal.InvalidOperation:
            raise InvalidAmount(
                'Not possible to create {} with amount {}'.format(
                    self.__class__.__name__, amount))

        self.amount = D(amount.quantize(D(self.cent_factor),
                                        rounding=self.rounding_method))
        self.currency = currency

    def __repr__(self):
        return '{}(amount={!r}, currency={!r})'.format(
            self.__class__.__name__,
            self.amount, self.currency)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.amount == other.amount and self.currency == other.currency

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.amount, self.currency))

    def __gt__(self, other):
        self._raise_for_unsupported_type(other, '>')
        self._raise_for_different_currency(other)
        return self.amount > other.amount

    def __ge__(self, other):
        self._raise_for_unsupported_type(other, '>=')
        self._raise_for_different_currency(other)
        return self.amount >= other.amount

    def __lt__(self, other):
        self._raise_for_unsupported_type(other, '<')
        self._raise_for_different_currency(other)
        return self.amount < other.amount

    def __le__(self, other):
        self._raise_for_unsupported_type(other, '<=')
        self._raise_for_different_currency(other)
        return self.amount <= other.amount

    def __add__(self, other):
        self._raise_for_unsupported_type(other, '+')
        self._raise_for_different_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other):
        self._raise_for_unsupported_type(other, '-')
        self._raise_for_different_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, other):
        if not isinstance(other, D):
            raise UnsupportedOperatorType(other, '*')
        return Money(self.amount * other, self.currency)

    def __rmul__(self, other):
        if not isinstance(other, D):
            raise UnsupportedOperatorType(other, '*')
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Money):
            self._raise_for_different_currency(other)
            if other.amount == D('0'):
                raise ZeroDivisionError()
            return self.amount / other.amount
        elif other == D('0'):
            raise ZeroDivisionError()
        return Money(self.amount / other, self.currency)

    __div__ = __truediv__

    def _raise_for_different_currency(self, other):
        if self.currency != other.currency:
            raise CurrencyMismatch(
                'Not possible to perform operation with different currencies')

    def _raise_for_unsupported_type(self, other, operator):
        if not isinstance(other, type(self)):
            raise UnsupportedOperatorType(
                'Operator {} is not supported for {} and {}'.format(
                    operator, type(self), type(other))
                )
