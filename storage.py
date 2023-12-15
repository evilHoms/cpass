from cryptor import Cryptor
from filestore import FileStore

class Storage:
    
    def __init__(self, cryptor: Cryptor, file_name: str):
        self.file_store = FileStore(file_name)
        local_data = self.file_store.read_file_data()
        
        # Get data from file and from external storages
        self.cryptor = cryptor
        
        # TODO check date of local file and external data, apply latest one (check for the key before it?)
        self.store = local_data
    
    def add(self, name: str, value: str):
        # TODO if name already exist show prompt to ask rewrite or rename
        self.store[self.cryptor.encrypt(name)] = self.cryptor.encrypt(value)
        self.file_store.update_file(self.store)
        
    def remove(self, name: str):
        del self.store[self.cryptor.encrypt(name)]
        
    def find(self, name: str):
        result = ""
        for key in  self.store:
            if self.cryptor.decrypt(key).find(name) != -1:
                result += f"{self.cryptor.decrypt(key)}: {self.cryptor.decrypt(self.store[key])}\n"
                
        return result
    
    def list(self):
        for key in self.store:
            print(f"{self.cryptor.decrypt(key)}: {self.cryptor.decrypt(self.store[key])}")
    