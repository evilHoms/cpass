from pathlib import Path
from cryptor import Cryptor
import json

FIREBASE_NAME = "firebase"

class Config:
    
    def __init__(self, cryptor: Cryptor, config_path: Path):
        self.cryptor = cryptor
        self.config_path = config_path

        if not self.config_path.exists():
            with open(self.config_path, 'w') as file:
                json.dump({FIREBASE_NAME: None}, file)
                
        with open(self.config_path) as file:
            self.config = json.load(file)
            
    def get_firebase_config(self):
        if not self.config[FIREBASE_NAME]:
            path = input("Firebase config is not found. Without it data can't be sync.\nEnter path to the config file: (Full absolute path with file name and extension)\n")
            if not path:
                return None
            bucket = input("Enter firebase bucket name:\n")
            self.set_firebase_config(path, bucket)
            return path, bucket
        return self.config[FIREBASE_NAME]["path"], self.config[FIREBASE_NAME]["bucket"]
    
    def set_firebase_config(self, path: str, bucket: str):
        self.config[FIREBASE_NAME] = { "path": path, "bucket": bucket }
        with open(self.config_path, 'w') as file:
            json.dump(self.config, file)
