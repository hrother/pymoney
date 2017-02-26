#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pymoney
----------------------------------

Tests for `pymoney` module.
"""

import pytest
from decimal import Decimal as D

from pymoney import Money
from pymoney import (
    InvalidAmount,
    CurrencyMismatch,
    UnsupportedOperatorType,
)


def test_money_init_decimal_amount():
    m = Money(D('10'), 'EUR')
    assert m.amount == D('10')
    assert m.currency == 'EUR'


def test_money_init_string_amount():
    m = Money('10', 'EUR')
    assert m.amount == D('10')
    assert m.currency == 'EUR'


def test_money_init_integer_amount():
    m = Money(10, 'EUR')
    assert m.amount == D('10')
    assert m.currency == 'EUR'


def test_money_init_float_amount():
    m = Money(10.0, 'EUR')
    assert m.amount == D('10')
    assert m.currency == 'EUR'


def test_money_init_invalid_amount():
    with pytest.raises(InvalidAmount):
        _ = Money('9,231', 'EUR')


def test_money_init_with_changed_cent_factor():
    old_precision = Money.cent_factor
    Money.cent_factor = '.001'
    m = Money(D('10.00123231'), 'EUR')
    assert m.amount == D('10.001')
    assert m.currency == 'EUR'
    Money.cent_factor = old_precision


def test_money_init_rounds_amount_to_cent_factor():
    m = Money(D('10.00123231'), 'EUR')
    assert m.amount == D('10.00')
    assert m.currency == 'EUR'


def test_money_repr():
    m = Money(D('42'), 'EUR')
    assert "Money(amount=Decimal('42.00'), currency='EUR')" == repr(m)


def test_money_equal_operator():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('42'), 'EUR')
    assert m1 == m2


def test_money_equal_operator_with_different_amount():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('21'), 'EUR')
    assert not m1 == m2


def test_money_equal_operator_with_different_currencies():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('42'), 'USD')
    assert not m1 == m2


def test_money_not_equal_operator_with_other_objects():
    m1 = Money(D('42'), 'EUR')
    assert m1 != 42
    assert m1 != D('42')
    assert m1 != (D('42'), 'EUR')


def test_money_not_equal_operator_with_different_amount():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('21'), 'EUR')
    assert m1 != m2


def test_money_not_equal_operator_with_different_currencies():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('42'), 'USD')
    assert m1 != m2


def test_money_not_equal_operator_with_equal_money():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('42'), 'EUR')
    assert not m1 != m2


def test_money_which_is_equal_has_same_hash():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('42'), 'EUR')
    assert hash(m1) == hash(m2)


def test_money_which_is_unequal_has_different_hash():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('21'), 'EUR')
    assert hash(m1) != hash(m2)


def test_money_greater_than():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('21'), 'EUR')
    assert m1 > m2


def test_money_not_greater_than():
    m1 = Money(D('21'), 'EUR')
    m2 = Money(D('42'), 'EUR')
    assert not m1 > m2


def test_money_not_greater_than_equal():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('42'), 'EUR')
    assert not m1 > m2


def test_money_greater_or_equal_than():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('42'), 'EUR')
    assert m1 >= m2


def test_money_not_greater_or_equal_than():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('21'), 'EUR')
    assert not m2 >= m1


def test_money_less_than():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('21'), 'EUR')
    assert m2 < m1


def test_money_not_less_than():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('21'), 'EUR')
    assert not m1 < m2


def test_money_not_less_than_equal():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('42'), 'EUR')
    assert not m1 < m2


def test_money_less_than_or_equal_with_equal():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('42'), 'EUR')
    assert m1 <= m2


def test_money_less_than_or_equal_with_less():
    m1 = Money(D('21'), 'EUR')
    m2 = Money(D('42'), 'EUR')
    assert m1 <= m2


def test_money_not_less_than_or_equal():
    m1 = Money(D('42'), 'EUR')
    m2 = Money(D('21'), 'EUR')
    assert not m1 <= m2


def test_comparing_money_with_different_currencies_raises():
    with pytest.raises(CurrencyMismatch):
        Money(D('42'), 'EUR') > Money(D('84'), 'USD')
    with pytest.raises(CurrencyMismatch):
        Money(D('42'), 'USD') >= Money(D('84'), 'EUR')
    with pytest.raises(CurrencyMismatch):
        Money(D('42'), 'USD') < Money(D('21'), 'EUR')
    with pytest.raises(CurrencyMismatch):
        Money(D('42'), 'USD') <= Money(D('21'), 'EUR')


def test_comparing_money_with_different_type_raises():
    with pytest.raises(UnsupportedOperatorType):
        Money(D('42'), 'EUR') > 21
    with pytest.raises(UnsupportedOperatorType):
        Money(D('42'), 'EUR') >= D('42')
    with pytest.raises(UnsupportedOperatorType):
        Money(D('42'), 'EUR') < 21
    with pytest.raises(UnsupportedOperatorType):
        Money(D('42'), 'EUR') <= 42


def test_addition_of_money():
    m1 = Money(D('21'), 'EUR')
    m2 = Money(D('21'), 'EUR')
    expected = Money(D('42'), 'EUR')
    assert m1 + m2 == expected


def test_addition_of_money_with_different_currencie_raises():
    m1 = Money(D('21'), 'EUR')
    m2 = Money(D('21'), 'USD')
    with pytest.raises(CurrencyMismatch):
        m1 + m2


def test_addition_of_money_with_other_types_raises():
    with pytest.raises(UnsupportedOperatorType):
        Money(D('21'), 'EUR') + D('21')


def test_using_sum_on_money():
    m1 = Money(D('21'), 'EUR')
    m2 = Money(D('21'), 'EUR')
    assert Money(D('42'), 'EUR') == sum([m1, m2])


def test_subtraction_of_money():
    assert Money(D('21'), 'EUR') == (
            Money(D('42'), 'EUR') - Money(D('21'), 'EUR'))


def test_subtraction_of_money_with_different_currencies_raises():
    with pytest.raises(CurrencyMismatch):
        Money(D('42'), 'EUR') - Money(D('42'), 'USD')


def test_subtraction_of_money_with_other_types_raises():
    with pytest.raises(UnsupportedOperatorType):
        Money(D('42'), 'EUR') - D('42')


def test_multiplication_of_money_with_money_raises():
    with pytest.raises(UnsupportedOperatorType):
        Money(D('21'), 'EUR') * Money(D('2'), 'EUR')


def test_multiplication_of_money_with_decimal():
    assert Money(D('42'), 'EUR') == Money(D('21'), 'EUR') * D('2')
    assert Money(D('42'), 'EUR') == D('2') * Money(D('21'), 'EUR')


def test_multiplication_with_non_decimal_raises():
    with pytest.raises(UnsupportedOperatorType):
        Money(D('21'), 'EUR') * 2


def test_division_of_money_with_money():
    assert D('2') == Money(D('42'), 'EUR') / Money(D('21'), 'EUR')


def test_division_by_zero_raises_exception():
    with pytest.raises(ZeroDivisionError):
        Money(D('42'), 'EUR') / Money(D('0'), 'EUR')


def test_division_by_one_returns_money():
    assert Money(D('42'), 'EUR') == Money(D('42'), 'EUR') / D('1')


def test_division_by_decimal_returns_money():
    assert Money(D('8.4'), 'EUR') == Money(D('42'), 'EUR') / D('5')


def test_division_with_different_currency_raises():
    with pytest.raises(CurrencyMismatch):
        Money(D('42'), 'EUR') / Money(D('21'), 'USD')
