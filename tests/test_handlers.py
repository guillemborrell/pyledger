from pyledger2.handlers import Handler, handler_methods, handle_request, \
    serialize_for_testing
from pyledger2.pyledger_message_pb2 import PyledgerResponse, PyledgerRequest


def test_handler_methods():
    assert set(handler_methods(Handler())) == {
        '__init__', 'activation', 'authentication', 'api', 'key', 'echo',
        'contracts', 'verify', 'call', 'status'
    }


def test_failed_message():
    response = PyledgerResponse()
    response.ParseFromString(serialize_for_testing(handle_request(b'xxxyyy')))
    assert response.successful == False
    assert response.data == b'Message not properly formatted'


def test_wrong_request():
    request = PyledgerRequest()
    response = PyledgerResponse()
    request.request = 'blahblah'
    response.ParseFromString(
        serialize_for_testing(
            handle_request(
                request.SerializeToString()
            )
        )
    )
    assert response.successful == False
    assert response.data == b'Request type not available'
