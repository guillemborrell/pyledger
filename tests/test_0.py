from pyledger2.db import User, DB
from pyledger2.auth import create_master_user
from pyledger2.config import password_backend, SECRET
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DB.sync_tables()


def test_0_master_session():
    # Create master session
    create_master_user('password')

    user = User.query().filter(User.name == 'master').one_or_none()

    kpdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SECRET,
        iterations=1000000,
        backend=password_backend
    )

    kpdf.verify('password'.encode('utf-8'), user.get_password())
