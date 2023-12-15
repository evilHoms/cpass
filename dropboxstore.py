from dropbox import Dropbox
import json

class DropboxStore(Dropbox):
    
    def __init__(self, token, file_name):
        super().__init__(token)
        self.file_name = file_name
            
    def upload(self, data):
        self.files_upload(json.dumps(data).encode(), f"{self.file_name}.json")
        
    def meta(self):
        return self.files_get_metadata(f"{self.file_name}.json").server_modified
        
    def download(self):
        self.files_download(f"{self.file_name}.json")