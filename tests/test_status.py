from pyledger2.status import Status, SimpleStatus


def test_1():
    status = SimpleStatus(key='value')
    assert isinstance(status, Status) == True
    assert ('key' in status) == True


def test_2():
    status = SimpleStatus(accounts={})
    status.accounts['My_account'] = 100
    assert status.accounts['My_account'] == 100


def test_serialization():
    status = SimpleStatus(accounts={})
    status.accounts['My_account'] = 100

    data = status.dump()
    del status

    status = SimpleStatus()
    status.load(data)

    assert status.accounts['My_account'] == 100
