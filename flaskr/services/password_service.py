from cryptography.fernet import Fernet

chiper_suite = Fernet('tqRu_aP1o9zOvDMD4dBoZhyUb92nTcT4U4nM2ml_p90=')

def encrypt_pass(password: str)->str:
    return chiper_suite.encrypt(str.encode(password))

def decrypt_pass(password: str)->str:
    return chiper_suite.decrypt(bytes(password)).decode()