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
        print("Before connecting to firebase, if there is already encrypted data.store, make sure that same KEY and HASH KEY are used.")
        if self.config[FIREBASE_NAME]:
            print(f"Current config:\nCreds: [encrypted]\nBucket: {self.cryptor.decrypt(self.config[FIREBASE_NAME]['bucket'])}")

        path = input("Enter path to the firebase config file: (Full absolute path with file name and extension)\n[Config]: ")
        cred, bucket = None, None
        
        if path:
            try:
                with open(path) as file:
                    cred = self.cryptor.encrypt(file.read())
            except Exception as e:
                print(str(e))
                exit(0)

            bucket = self.cryptor.encrypt(input("Enter firebase bucket name\n[Bucket]: "))
            self.config[FIREBASE_NAME] = { "bucket": bucket, "cred": cred }
            
            with open(self.config_path, 'w') as file:
                json.dump(self.config, file)
            
        return cred, bucket
            
    def recrypt_firebase_config(self, new_key, new_hash_key):
        if self.config[FIREBASE_NAME]:
            new_cryptor = Cryptor(new_key, new_hash_key)
            old_cred = self.cryptor.decrypt(self.config[FIREBASE_NAME]["cred"])
            new_cred = new_cryptor.encrypt(old_cred)
            old_bucket = self.cryptor.decrypt(self.config[FIREBASE_NAME]["bucket"])
            new_bucket = new_cryptor.encrypt(old_bucket)

            self.config[FIREBASE_NAME]["cred"] = new_cred
            self.config[FIREBASE_NAME]["bucket"] = new_bucket
            
            with open(self.config_path, 'w') as file:
                json.dump(self.config, file)
        else:
            print("No Firebase config found.")
        
            
