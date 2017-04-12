from pyledger2.pyledger_message_pb2 import PyledgerRequest, PyledgerResponse
from pyledger2.handlers import handle_request
from pyledger2.db import Session


def test_master_session():
    """
    Get a master session key
    """
    request = PyledgerRequest()
    request.request = 'session'
    request.user = 'master'
    request.password = 'password'

    response = PyledgerResponse()
    response.ParseFromString(handle_request(request.SerializeToString()))

    assert response.successful == True

    session_key = response.data.decode('utf-8')
    session = Session.from_key(session_key)

    assert session.key == session_key
