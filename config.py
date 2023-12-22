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
            print("Firebase config is not found. only local storage will be used.")
            print("Run script in config mode to apply config: `cpass config -k[key]`")
            return None, None, None
        return self.config[FIREBASE_NAME]["cred"], self.config[FIREBASE_NAME]["bucket"], self.config[FIREBASE_NAME]["key"]
    
    def set_firebase_config(self):
        if self.config[FIREBASE_NAME]:
            print(f"Current config:\nCreds: [encrypted]\nBucket: {self.config[FIREBASE_NAME]['bucket']}")

        path = input("Enter path to the firebase config file: (Full absolute path with file name and extension)\n[Config]: ")
        cred, bucket = None, None
        
        if path:
            try:
                with open(path) as file:
                    cred = self.cryptor.encrypt(file.read())
            except Exception as e:
                print(str(e))
                exit(0)

            bucket = input("Enter firebase bucket name\n[Bucket]: ")
            fb_key = input("If there is any encrypted data in the bucket and there was used another key to encrypt it, enter it here (Or leave empty if key is the same or bucket store is empty)\n[Key]: ")
            key = fb_key if fb_key else self.cryptor.key
            self.config[FIREBASE_NAME] = { "bucket": bucket, "cred": cred, "key": self.cryptor.encrypt(key) }
            
            with open(self.config_path, 'w') as file:
                json.dump(self.config, file)
            
        return cred, bucket
            
    def recrypt_firebase_config(self, new_key):
        if self.config[FIREBASE_NAME]:
            new_cryptor = Cryptor(new_key)
            new_key = new_cryptor.encrypt(new_key)
            old_cred = self.cryptor.decrypt(self.config[FIREBASE_NAME]["cred"])
            new_cred = new_cryptor.encrypt(old_cred)

            self.config[FIREBASE_NAME]["key"] = new_key
            self.config[FIREBASE_NAME]["cred"] = new_cred
            
            with open(self.config_path, 'w') as file:
                json.dump(self.config, file)
        else:
            print("No Firebase config found.")
        
            
