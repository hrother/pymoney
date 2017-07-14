# -*- coding: utf-8 -*-

"""
pymoney library
~~~~~~~~~~~~~~~

pymoney is library for working with monetary values, written in python.

Basic usage:

    >>> from pymoney import Money
    >>> m = Money('42', 'EUR')
    >>> m
    Money(amount=Decimal('42.00'), currency='EUR')

... numeric operations

    >>> from decimal import Decimal as D
    >>> m * D('2.124')
    Money(amount=Decimal('89.21'), currency='EUR')
    >>> sum([Money('20.5', 'EUR'), Money('21.5', 'EUR')])
    Money(amount='42.00', currency='EUR')

... comparison

    >>> m > Money('21', 'EUR')
    True

:copyright: (c) 2017 by Holger Rother.
:license: MIT, see LICENCE for more details

"""

__title__ = 'pymoney'
__version__ = '0.1.0'
__author__ = 'Holger Rother'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Holger Rother'
__email__ = 'hrother@hrother.org'

from .pymoney import Money
from .exceptions import (
    MoneyError, InvalidAmount, CurrencyMismatch,
    UnsupportedOperatorType
)
