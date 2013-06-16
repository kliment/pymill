import pymill


class MockPymill(pymill.Pymill):
    """
    This is a simple mocker for Pymill's _api_call handling which exposes
    the call parameters after being called.
    """
    call_params = None
    call_kwargs = None
    api_called = False

    def _api_call(self, url, params={}, method="GET", headers=None,
                  parse_json=True, return_type=None):
        self.api_called = True
        self.call_args = {
            'url': url,
            'params': params,
            'method': method,
            'headers': headers,
            'parse_json': parse_json,
            'return_type': return_type,
        }


def test_transact_requirements_with_token():
    """
    Tests that all requirement checks work for calls using a token. In this
    case following parameters have to be passed in order to create a
    transaction:

    * token
    * amount
    * currency
    """
    pm = MockPymill('key')
    pm.transact(token="token", amount=123, currency='EUR')
    assert pm.api_called
    assert pm.call_args['params'].get('token') == 'token'


def test_transact_requirements_with_preauth():
    """
    Required parameters:

    * preauth
    * amount
    * currency
    """
    pm = MockPymill('key')
    pm.transact(preauth="preauth", amount=123, currency='EUR')
    assert pm.api_called
    assert pm.call_args['params'].get('preauthorization') == 'preauth'


def test_trasact_requirements_with_payment():
    """
    Required parameters:

    * payment (or account, code, holder, client)
    * amount
    * currency
    """
    pm = MockPymill('key')
    pm.transact(payment='payment', amount=123, currency='EUR')
    assert pm.api_called

    pm = MockPymill('key')
    pm.transact(code='code', account='account', client='client',
                holder='holder', amount=123, currency='EUR')
    assert pm.api_called
