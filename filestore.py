from pathlib import Path
from cryptor import Cryptor
import os
import json
import datetime

class FileStore:
    
    def __init__(self, store_path: Path, cryptor: Cryptor):
        self.store_path = store_path
        self.cryptor = cryptor
        
        if not self.store_path.exists():
            file = open(self.store_path, "x")
            file.close()
            
    def read_file_data(self):
        with open(self.store_path) as file:
            cdata = file.read()
            data = None
            if len(cdata) == 0:
                data = {}
            else:
                data = json.loads(self.cryptor.decrypt(cdata))
           
        mtime = os.path.getmtime(self.store_path)
        return datetime.datetime.utcfromtimestamp(round(mtime)), data
    
    def update_file(self, data):
        with open(self.store_path, "w") as file:
            file.write(self.cryptor.encrypt(json.dumps(data)))
            
    def save_old(self, data):
        old_path = self.store_path.with_name("old.store")
        with open(old_path, "w") as file:
            file.write(self.cryptor.encrypt(json.dumps(data)))