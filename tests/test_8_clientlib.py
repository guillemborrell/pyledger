from pyledger2.clientlib import call_request, call_response
from pyledger2.handlers import handle_request


def test_clientlib_call_request():
    request = call_request(call='add_account', user='master',
                           password='password', contract='AuthDigitalCurrency',
                           data={'key': 'another_account'})

    succesful, response = call_response(handle_request(request))

    assert succesful == True
    assert response == 'another_account'


def test_clientlib_call_request_fail():
    request = call_request(call='add_account', contract='AuthDigitalCurrency',
                           data={'key': 'yet_another_account'})

    successful, response = call_response(handle_request(request))

    assert successful == False
    assert response == 'Not enough permissions'
