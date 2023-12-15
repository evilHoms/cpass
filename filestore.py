from pathlib import Path
from dropbox import Dropbox
import json

class FileStore:
    
    def __init__(self, file_name):
        self.dir_path = Path(__file__).parent.resolve()
        self.store_path = Path(f"{self.dir_path}/{file_name}.json")
        
        if not self.store_path.exists():
            file = open(self.store_path, "w")
            file.write("{}")
            file.close()
            
    def read_file_data(self):
        with open(self.store_path) as file:
            data = json.load(file)
            
        return data
    
    def update_file(self, data):
        with open(self.store_path, "w") as file:
            json.dump(data, file)
            