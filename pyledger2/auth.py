from .db import User, DB
from .config import password_backend, SECRET
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import datetime


def create_master_user(password):
    master_user = User()
    master_user.name = 'master'
    master_user.when = datetime.datetime.now()

    kpdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SECRET,
        iterations=1000000,
        backend=password_backend
    )
    master_user.set_password(kpdf.derive(password.encode('utf-8')))

    DB.session.add(master_user)
    DB.session.commit()
