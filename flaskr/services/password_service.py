from cryptography.fernet import Fernet
from flask import current_app

def get_chiper_suite():
    with current_app.app_context():
        fernet_key = current_app.config.get('FERNET_KEY')
        return Fernet(fernet_key)

def encrypt_pass(password: str)->str:
    return get_chiper_suite().encrypt(str.encode(password))

def decrypt_pass(password: str)->str:
    return get_chiper_suite().decrypt(bytes(password)).decode()