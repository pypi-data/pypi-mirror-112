import re

from cryptography.fernet import Fernet


def decrypt_string(string, key):
    f = Fernet(key)
    decrypt_single_secret = lambda s: f.decrypt(str.encode(s.group(1))).decode()
    return re.sub(r'%MASKED{(.+?)}', decrypt_single_secret, string)


def encrypt_string(string, key):
    f = Fernet(key)
    encrypt_single_secret = lambda s: "%MASKED{" + f.encrypt(str.encode(s.group(1))).decode() + "}"
    return re.sub(r'%MASK{(.+?)}', encrypt_single_secret, string)


def generate_key():
    return Fernet.generate_key()
