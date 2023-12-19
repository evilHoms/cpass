from cryptor import Cryptor
from config import Config
from filestore import FileStore
from dropboxstore import DropboxStore
from pathlib import Path
import dropbox

class Storage:
    
    def __init__(self, cryptor: Cryptor, config: Config, file_path: Path):
        # self.cryptor = cryptor
        
        # Get data from local file
        self.file_store = FileStore(file_path, cryptor)
        local_mod_time, local_data = self.file_store.read_file_data()
        print(len(local_data))
        
        # Get data from dropbox
        dpx_token = config.get_dropbox_token()
        dpx_path = f"/{file_path.name}"
        self.dpx = DropboxStore(dpx_token, dpx_path, cryptor)
        
        try:
            dpx_mod_time, dpx_data = self.dpx.download()
        except dropbox.exceptions.ApiError as e:
            if e.error.is_path():
                print(e.error.get_path())
            exit()

        # Check data from local file and from dropbox, if data not synced ask which one to apply
        data_to_use = local_data
        if local_data != dpx_data:
            print("Local data not synced with external data: ")
            print(f"Dropbox last modified: {dpx_mod_time} UTC,   number of records: {len(dpx_data)}")
            if len(local_data) == 0:
                print("Local   no records")
            else:
                print(f"Local   last modified: {local_mod_time} UTC, number of records: {len(local_data)}")
            ans = None
            while ans != "local" and ans != "dropbox":
                ans = input(f"Which one to apply? (local/dropbox): ").lower()
            if ans == "dropbox":
                data_to_use = dpx_data
                self.file_store.update_file(data_to_use)
            else:
                self.dpx.upload(data_to_use)

        self.store = data_to_use
    
    def add(self, name: str, value: str):
        self.store[name] = value
        # self.store[self.cryptor.encrypt(name)] = self.cryptor.encrypt(value)
        # Update local and external storages
        self.file_store.update_file(self.store)
        self.dpx.upload(self.store)
        
    def remove(self, name: str):
        keys_to_del = []
        for key in self.store:
            if key == name:
                keys_to_del.append(key)
            # store_name = self.cryptor.decrypt(key)
            # if store_name == name:
            #     keys_to_del.append(key)
                
        for key in keys_to_del:
            del self.store[key]
        
        if len(keys_to_del) > 0:
            # Update local and external storages
            self.file_store.update_file(self.store)
            self.dpx.upload(self.store)
            return len(keys_to_del)
        
        return 0
            
    def remove_by_substring(self, name: str):
        keys_to_del = []
        for key in self.store:
            if key.find(name) != -1:
                keys_to_del.append(key)
            # if self.cryptor.decrypt(key).find(name) != -1:
            #     keys_to_del.append(key)
                
        for key in keys_to_del:
            del self.store[key]
                
        if len(keys_to_del) > 0:
            # Update local and external storages
            self.file_store.update_file(self.store)
            self.dpx.upload(self.store)
            return len(keys_to_del)
        
        return 0
        
    def find(self, name: str):
        result = ""
        for key in  self.store:
            if key.find(name) != -1:
                result += f"{key}: {self.store[key]}\n"
            # if self.cryptor.decrypt(key).find(name) != -1:
            #     result += f"{self.cryptor.decrypt(key)}: {self.cryptor.decrypt(self.store[key])}\n"
                
        return result
    
    def list(self):
        # decrypted_map = {}
        key_list = []
        for key in self.store:
            key_list.append(key)
            # decrypted_key = self.cryptor.decrypt(key)
            # decrypted_map[decrypted_key] = self.cryptor.decrypt(self.store[key])
            # key_list.append(decrypted_key)
        if len(key_list) == 0:
            print("No records")
        key_list.sort()
        for key in key_list:
            print(f"{key}: {self.store[key]}")
            # print(f"{key}: {decrypted_map[key]}")
            
    def check_name(self, name: str):
        # decrypted_map = {}
        # for key in self.store:
        #     decrypted_key = self.cryptor.decrypt(key)
        #     decrypted_map[decrypted_key] = self.cryptor.decrypt(self.store[key])
        index = 0
        pname = name
        while pname in self.store:
            index += 1
            pname = name + f" ({index})"
        # while pname in decrypted_map:
        #     index += 1
        #     pname = name + f" ({index})"
        return pname
            
    