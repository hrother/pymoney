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
from pymoney.exceptions import (
        InvalidAmount,
        CurrencyMismatch,
        UnsupportedOperatorType,
)


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


def test_money_equal_operator():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('42'), 'EUR')
    assert m1 == m2


def test_money_equal_operator_with_different_amount():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('21'), 'EUR')
    assert not m1 == m2


def test_money_equal_operator_with_different_currencies():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('42'), 'USD')
    assert not m1 == m2


def test_money_not_equal_operator_with_other_objects():
    m1 = pymoney.Money(D('42'), 'EUR')
    assert m1 != 42
    assert m1 != D('42')
    assert m1 != (D('42'), 'EUR')


def test_money_not_equal_operator_with_different_amount():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('21'), 'EUR')
    assert m1 != m2


def test_money_not_equal_operator_with_different_currencies():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('42'), 'USD')
    assert m1 != m2


def test_money_not_equal_operator_with_equal_money():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('42'), 'EUR')
    assert not m1 != m2


def test_money_which_is_equal_has_same_hash():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('42'), 'EUR')
    assert hash(m1) == hash(m2)


def test_money_which_is_unequal_has_different_hash():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('21'), 'EUR')
    assert hash(m1) != hash(m2)


def test_money_greater_than():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('21'), 'EUR')
    assert m1 > m2


def test_money_not_greater_than():
    m1 = pymoney.Money(D('21'), 'EUR')
    m2 = pymoney.Money(D('42'), 'EUR')
    assert not m1 > m2


def test_money_not_greater_than_equal():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('42'), 'EUR')
    assert not m1 > m2


def test_money_greater_or_equal_than():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('42'), 'EUR')
    assert m1 >= m2


def test_money_not_greater_or_equal_than():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('21'), 'EUR')
    assert not m2 >= m1


def test_money_less_than():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('21'), 'EUR')
    assert m2 < m1


def test_money_not_less_than():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('21'), 'EUR')
    assert not m1 < m2


def test_money_not_less_than_equal():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('42'), 'EUR')
    assert not m1 < m2


def test_money_less_than_or_equal_with_equal():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('42'), 'EUR')
    assert m1 <= m2


def test_money_less_than_or_equal_with_less():
    m1 = pymoney.Money(D('21'), 'EUR')
    m2 = pymoney.Money(D('42'), 'EUR')
    assert m1 <= m2


def test_money_not_less_than_or_equal():
    m1 = pymoney.Money(D('42'), 'EUR')
    m2 = pymoney.Money(D('21'), 'EUR')
    assert not m1 <= m2


def test_comparing_money_with_different_currencies_raises():
    with pytest.raises(CurrencyMismatch):
        pymoney.Money(D('42'), 'EUR') > pymoney.Money(D('84'), 'USD')
    with pytest.raises(CurrencyMismatch):
        pymoney.Money(D('42'), 'USD') >= pymoney.Money(D('84'), 'EUR')
    with pytest.raises(CurrencyMismatch):
        pymoney.Money(D('42'), 'USD') < pymoney.Money(D('21'), 'EUR')
    with pytest.raises(CurrencyMismatch):
        pymoney.Money(D('42'), 'USD') <= pymoney.Money(D('21'), 'EUR')


def test_comparing_money_with_different_type_raises():
    with pytest.raises(UnsupportedOperatorType):
        pymoney.Money(D('42'), 'EUR') > 21
    with pytest.raises(UnsupportedOperatorType):
        pymoney.Money(D('42'), 'EUR') >= D('42')
    with pytest.raises(UnsupportedOperatorType):
        pymoney.Money(D('42'), 'EUR') < 21
    with pytest.raises(UnsupportedOperatorType):
        pymoney.Money(D('42'), 'EUR') <= 42

