# -*- coding: utf-8 -*-

from mock import MockPymill

def test_umlaut_new_client_description():
    """
    Tests umlaut on description string.
    """
    pm = MockPymill('key')
    pm.new_client(email="foo@example.com", description='Ümläüt')
    assert pm.api_called
    assert pm.call_args['params'].get('description') == 'Ümläüt'


def test_umlaut_update_client_description():
    """
    Tests umlaut on description string.
    """
    pm = MockPymill('key')
    clientid = "client_12345"
    pm.update_client(client_id = clientid, email="foo@example.com", description='Ümläüt')
    assert pm.api_called
    assert pm.call_args['params'].get('description') == 'Ümläüt'
