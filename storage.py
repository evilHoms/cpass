from cryptor import Cryptor
from config import Config
from filestore import FileStore

class Storage:
    
    def __init__(self, cryptor: Cryptor, config: Config, file_name: str):
        self.file_store = FileStore(file_name)
        local_data = self.file_store.read_file_data()
        
        # Get data from file and from external storages
        self.cryptor = cryptor
        
        # TODO check date of local file and external data, apply latest one (check for the key before it?)
        dropbox_token = config.get_dropbox_token()
        self.store = local_data
    
    def add(self, name: str, value: str):
        self.store[self.cryptor.encrypt(name)] = self.cryptor.encrypt(value)
        # TODO sync with external services
        self.file_store.update_file(self.store)
        
    def remove(self, name: str):
        keys_to_del = []
        for key in self.store:
            store_name = self.cryptor.decrypt(key)
            if store_name == name:
                keys_to_del.append(key)
                
        for key in keys_to_del:
            del self.store[key]
        
        if len(keys_to_del) > 0:
            # TODO sync with external services
            self.file_store.update_file(self.store)
            return len(keys_to_del)
        
        return 0
            
    def remove_by_substring(self, name: str):
        keys_to_del = []
        for key in  self.store:
            if self.cryptor.decrypt(key).find(name) != -1:
                keys_to_del.append(key)
                
        for key in keys_to_del:
            del self.store[key]
                
        if len(keys_to_del) > 0:
            # TODO sync with external services
            self.file_store.update_file(self.store)
            return len(keys_to_del)
        
        return 0
        
    def find(self, name: str):
        result = ""
        for key in  self.store:
            if self.cryptor.decrypt(key).find(name) != -1:
                result += f"{self.cryptor.decrypt(key)}: {self.cryptor.decrypt(self.store[key])}\n"
                
        return result
    
    def list(self):
        decrypted_map = {}
        key_list = []
        for key in self.store:
            decrypted_key = self.cryptor.decrypt(key)
            decrypted_map[decrypted_key] = self.cryptor.decrypt(self.store[key])
            key_list.append(decrypted_key)
        key_list.sort()
        for key in key_list:
            print(f"{key}: {decrypted_map[key]}")
            
    def check_name(self, name: str):
        decrypted_map = {}
        for key in self.store:
            decrypted_key = self.cryptor.decrypt(key)
            decrypted_map[decrypted_key] = self.cryptor.decrypt(self.store[key])
        index = 0
        pname = name
        while pname in decrypted_map:
            index += 1
            pname = name + f" ({index})"
        return pname
            
    