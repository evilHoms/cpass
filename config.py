from pathlib import Path
from cryptor import Cryptor
import os
import json

DROPBOX_NAME = "dropbox"

class Config:
    
    def __init__(self, cryptor: Cryptor, config_path: Path):
        self.cryptor = cryptor
        self.config_path = config_path

        if not self.config_path.exists():
            with open(self.config_path, 'w') as file:
                json.dump({DROPBOX_NAME: None}, file)
                
        with open(self.config_path) as file:
            self.config = json.load(file)
    
    def get_dropbox_token(self):
        if not self.config[DROPBOX_NAME]:
            token = input("Dropbox access token is not specified. Without it data can't be sync with dropbox.\nEnter the token or leave empty to ignore")
            if not token:
                return None
            self.set_dropbox_token(token)
            return token
            
        return self.cryptor.decrypt(self.config[DROPBOX_NAME])
            
    def set_dropbox_token(self, token):
        self.config[DROPBOX_NAME] = self.cryptor.encrypt(token)
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file)
