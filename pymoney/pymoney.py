# -*- coding: utf-8 -*-
import decimal
from decimal import Decimal as D

from .exceptions import InvalidAmount


class Money(object):
    """Representation of a monetary value. Money consists of an decimal amount
    and an currency.

    The :attr:`amount` of :class:`Money` is rounded using
    :attr:`rounding_method` with :attr:`cent_factor`. Which default to
    :attr:`rounding_method` = decimal.ROUND_HALF_EVEN and
    :attr:`cent_factor` = '.01'

    :param amount: of money
    :type amount: numeric
    :param str currency: In which the given `amount` is denoted.

    """

    cent_factor = '.01'
    rounding_method = decimal.ROUND_HALF_EVEN

    def __init__(self, amount, currency):
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
