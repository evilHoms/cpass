from cryptography.fernet import Fernet
from base64 import b64encode
from hashlib import sha256
from hmac import digest

HASH_KEY = '111222'

class Cryptor:
    
    def __init__(self, key: str):
        self.key = key
        encoded_key = b64encode(digest(HASH_KEY.encode(), key.encode(), sha256)).decode()
        self.cryptor = Fernet(encoded_key)
    
    def encrypt(self, string: str):
        return self.cryptor.encrypt(string.encode()).decode()
    
    def decrypt(self, string: str):
        return self.cryptor.decrypt(string.encode()).decode()
    