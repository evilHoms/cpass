import firebase_admin
from firebase_admin import credentials, storage
from cryptor import Cryptor
from datetime import datetime
import json

class FirebaseStore:
    
    def __init__(self, enc_cred: str, bucket: str, files_dir: str, store_name: str, cryptor: Cryptor):
        self.cryptor = cryptor
        conf = json.loads(self.cryptor.decrypt(enc_cred))
        cred = credentials.Certificate(conf)
        
        firebase_admin.initialize_app(cred, { "storageBucket": self.cryptor.decrypt(bucket).replace("gs://", "") })
        
        self.files_dir = files_dir
        self.store_name = store_name
        self.bucket = storage.bucket()
        
        blob = self.bucket.get_blob(self.store_name)
        if not blob or not blob.exists():
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
        rawdata = blob.download_as_text()
        if not rawdata:
            data = {}
        else:
            data = json.loads(self.cryptor.decrypt(blob.download_as_text()))
        date = datetime.utcfromtimestamp(round(blob.updated.timestamp()))
        return date, data
