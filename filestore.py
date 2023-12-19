from pathlib import Path
import json

class FileStore:
    
    def __init__(self, store_path: Path):
        self.store_path = store_path
        
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
            