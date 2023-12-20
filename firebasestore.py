import firebase_admin
from firebase_admin import credentials, storage
from cryptor import Cryptor
from datetime import datetime
import json

class FirebaseStore:
    
    def __init__(self, config_path: str, bucket: str, files_dir: str, store_name: str, cryptor: Cryptor):
        cred = credentials.Certificate(config_path)
        firebase_admin.initialize_app(cred, { "storageBucket": bucket.replace("gs://", "") })
        
        self.cryptor = cryptor
        self.files_dir = files_dir
        self.store_name = store_name
        self.bucket = storage.bucket()
        
        blob = self.bucket.get_blob(self.store_name)
        if not blob.exists():
            print(f"Firebase: no file with name {self.store_name}. Uploading local file to firebase storage.")
            self.upload_data()
    
    # Uploads local data file to firebase
    def upload_data(self):
        local_data_path = f"{self.files_dir}/{self.store_name}"
        blob = self.bucket.blob(self.store_name)
        blob.upload_from_filename(local_data_path)
    
    # Downloads data from firebase by probided during init store_name
    def download_data(self):
        blob = self.bucket.get_blob(self.store_name)
        data = json.loads(self.cryptor.decrypt(blob.download_as_text()))
        date = datetime.utcfromtimestamp(round(blob.updated.timestamp()))
        return date, data 
