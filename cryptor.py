from cryptography.fernet import Fernet
from base64 import b64encode
from hashlib import sha256
from hmac import digest

class Cryptor:
    
    def __init__(self, key: str, hash_key: str):
        self.key = key
        self.hash_key = hash_key
        encoded_key = b64encode(digest(hash_key.encode(), key.encode(), sha256)).decode()
        self.cryptor = Fernet(encoded_key)
    
    def encrypt(self, string: str):
        return self.cryptor.encrypt(string.encode()).decode()
    
    def decrypt(self, string: str):
        return self.cryptor.decrypt(string.encode()).decode()
    