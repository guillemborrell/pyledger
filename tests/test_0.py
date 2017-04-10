from pyledger2.db import User, DB
from pyledger2.auth import create_master_user

DB.sync_tables()


def test_0_master_session():
    # Create master session
    create_master_user('password')

    user = User.query().filter(User.name == 'master').one_or_none()
    assert user.is_password('password') == True


