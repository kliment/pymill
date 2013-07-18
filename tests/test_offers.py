import pytest
from mock import MockPymill

def test_offer_requirements():
    """
    Tests that all requirement checks work creation of offers.
    Following parameters have to be passed in order to create an offer:

    * amount
    * interval
    * currency
    * name
    """
    pm = MockPymill('key')
    pm.new_offer(interval="1 month", amount=123, currency='EUR', name="NAME")
    assert pm.api_called
    assert pm.call_args['params'].get('interval') == '1 month'
    assert pm.call_args['params'].get('amount') == '123'
    assert pm.call_args['params'].get('currency') == "EUR"


def test_offer_amount():
    """
    Tests that amount raises ValueErrors on false parameters.
    """
    params = {'interval': "1 month", 'currency': 'EUR', 'name': "NAME"}

    pm = MockPymill('key')
    with pytest.raises(ValueError):
        pm.new_offer(amount='X', **params)
    with pytest.raises(ValueError):
        pm.new_offer(amount='10.1', **params)

    # FIXME: should raise an exception, too?
    pm.new_offer(amount=0, **params)
    assert pm.api_called == False

    # with correct value
    pm.new_offer(amount="100", **params)
    assert pm.api_called
    assert pm.call_args['params'].get('amount') == '100'


def test_offer_intervals():
    """
    Tests for correct intervals.

    From API documentation:
    ``Format: number DAY|WEEK|MONTH|YEAR Example: 2 DAY``
    """
    params = {'amount': 100, 'currency': 'EUR', 'name': "NAME"}

    pm = MockPymill('key')
    for value in ('month', '1 year', '10 day', '2 week'):
        pm.new_offer(interval=value, **params)
        assert pm.api_called
        assert pm.call_args['params'].get('interval') == value
