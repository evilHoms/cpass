from dropbox import Dropbox, files
import json

class DropboxStore(Dropbox):
    
    def __init__(self, token: str, file_path: str):
        super().__init__(token)
        self.file_path = file_path
            
    def upload(self, data):
        self.files_upload(json.dumps(data).encode(), self.file_path, mode=files.WriteMode.overwrite)
        
    def meta(self):
        return self.files_get_metadata(self.file_path).server_modified
        
    def download(self):
        meta, res = self.files_download(self.file_path)
        return json.loads(res.content)