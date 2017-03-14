from pyledger.db import DB, Status, Contract
from pyledger.contract import verify_contract
from sqlalchemy import desc


def test_10break_chain():
    contract = DB.session.query(Contract).filter(
        Contract.name == 'NewContract').first()

    status = DB.session.query(
        Status).filter(
        Status.contract == contract).order_by(
        desc(Status.when)).first()

    status.key = b'x'
    DB.session.commit()

    assert verify_contract('NewContract')[:10] == "Chain inco"

