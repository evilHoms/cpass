import firebase_admin
from firebase_admin import credentials
import json
from cryptor import Cryptor

class FirebaseStore:
    
    def __init__(self, token: str, file_path: str, cryptor: Cryptor):
        cred = credentials.Certificate("path/to/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        
        self.file_path = file_path
        self.cryptor = cryptor
        # try:
        #     self.files_upload(self.cryptor.encrypt(json.dumps({})).encode(), self.file_path)
        # except:
        #     pass
            
    def upload(self, data):
        self.files_upload(self.cryptor.encrypt(json.dumps(data)).encode(), self.file_path, mode=files.WriteMode.overwrite)
        
    def meta(self):
        return self.files_get_metadata(self.file_path).server_modified
        
    def download(self):
        meta, res = self.files_download(self.file_path)
        content = res.content.decode()
        return meta.client_modified, json.loads(self.cryptor.decrypt(content))
