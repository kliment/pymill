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

