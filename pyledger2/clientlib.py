from pyledger2.pyledger_message_pb2 import PyledgerResponse, PyledgerRequest
import pickle


def auth_info(kwargs):
    user = ''
    password = ''

    if 'user' in kwargs:
        user = kwargs['user']

    if 'password' in kwargs:
        password = kwargs['password']

    return user, password


def session_info(kwargs):
    session = ''

    if 'session' in kwargs:
        session = kwargs['session']

    return session


def call_request(**kwargs):
    request = PyledgerRequest()

    request.user, request.password = auth_info(kwargs)
    request.session_key = session_info(kwargs)
    request.request = 'call'

    if 'contract' not in kwargs:
        raise ValueError('Contract should be a keyword argument')
    request.contract = kwargs['contract']

    if 'call' not in kwargs:
        raise ValueError('Call should be a keyword argument')
    request.call = kwargs['call']

    if 'data' not in kwargs:
        raise ValueError('Data should be a keyword argument')
    request.data = pickle.dumps(kwargs['data'])

    return request.SerializeToString()


def contracts_request(**kwargs):
    # This is simple, doesn't require authentication.
    request = PyledgerRequest()
    request.request = 'contracts'
    return request.SerializeToString()


def handle_response(bin_response, callback=None):
    response = PyledgerResponse()
    response.ParseFromString(bin_response)

    if response.successful:
        if callback:
            response_data = pickle.loads(response.data)
            print('Executing callback...')
            callback(response_data)
            return True, response_data
        else:
            return True, pickle.loads(response.data)

    else:
        return False, response.data.decode('utf-8')