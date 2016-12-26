#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pymoney
----------------------------------

Tests for `pymoney` module.
"""

import pytest
from decimal import Decimal as D

from pymoney import pymoney
from pymoney.exceptions import InvalidAmount


def test_money_init_decimal_amount():
    m = pymoney.Money(D('10'), 'EUR')
    assert m.amount == D('10')
    assert m.currency == 'EUR'


def test_money_init_string_amount():
    m = pymoney.Money('10', 'EUR')
    assert m.amount == D('10')
    assert m.currency == 'EUR'


def test_money_init_integer_amount():
    m = pymoney.Money(10, 'EUR')
    assert m.amount == D('10')
    assert m.currency == 'EUR'


def test_money_init_float_amount():
    m = pymoney.Money(10.0, 'EUR')
    assert m.amount == D('10')
    assert m.currency == 'EUR'


def test_money_init_invalid_amount():
    with pytest.raises(InvalidAmount):
        _ = pymoney.Money('9,231', 'EUR')


def test_money_init_with_changed_cent_factor():
    old_precision = pymoney.Money.cent_factor
    pymoney.Money.cent_factor = '.001'
    m = pymoney.Money(D('10.00123231'), 'EUR')
    assert m.amount == D('10.001')
    assert m.currency == 'EUR'
    pymoney.Money.cent_factor = old_precision


def test_money_init_rounds_amount_to_cent_factor():
    m = pymoney.Money(D('10.00123231'), 'EUR')
    assert m.amount == D('10.00')
    assert m.currency == 'EUR'


def test_money_repr():
    m = pymoney.Money(D('42'), 'EUR')
    assert "Money(amount=Decimal('42.00'), currency='EUR')" == repr(m)
