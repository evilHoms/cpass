from cryptor import Cryptor
from config import Config
from filestore import FileStore
from pathlib import Path
from firebasestore import FirebaseStore

class Storage:
    
    def __init__(self, cryptor: Cryptor, config: Config, file_dir: Path, store_name: str):
        # Get data from local file
        self.file_store = FileStore(Path(f"{file_dir}/{store_name}"), cryptor)
        local_mod_time, local_data = self.file_store.read_file_data()
        
        # Get data from firebase
        fb_path, fb_bucket, fb_key = config.get_firebase_config()
        if fb_path and fb_bucket and fb_key:
            self.fb = FirebaseStore(fb_path, fb_bucket, file_dir, store_name, cryptor.decrypt(fb_key))
            fb_mod_time, fb_data = self.fb.download_data()

        # Check data from local file and from firebase, if data not synced ask which one to apply
        data_to_use = local_data
        if fb_path and fb_bucket and fb_key and local_data != fb_data:
            print("Local data not synced with external data: ")
            print(f"[Firebase]: last modified: {fb_mod_time} UTC,   number of records: {len(fb_data)}")
            print(f"[Local]:    last modified: {local_mod_time} UTC, number of records: {len(local_data)}")
            ans = None
            while ans != "local" and ans != "firebase":
                ans = input(f"Which one to apply? (local/firebase): ").lower()
            if ans == "firebase":
                data_to_use = fb_data
                self.file_store.save_old(local_data)
                self.file_store.update_file(data_to_use)
            else:
                self.file_store.save_old(fb_data)
                self.fb.upload_data()

        self.store = data_to_use
    
    def add(self, name: str, value: str):
        self.store[name] = value
        # Update local and external storages
        self.file_store.update_file(self.store)
        self.fb.upload_data()
        
    def remove(self, name: str):
        keys_to_del = []
        for key in self.store:
            if key == name:
                keys_to_del.append(key)
                
        for key in keys_to_del:
            del self.store[key]
        
        if len(keys_to_del) > 0:
            # Update local and external storages
            self.file_store.update_file(self.store)
            self.fb.upload_data()
            return len(keys_to_del)
        
        return 0
            
    def remove_by_substring(self, name: str):
        keys_to_del = []
        for key in self.store:
            if key.find(name) != -1:
                keys_to_del.append(key)
                
        for key in keys_to_del:
            del self.store[key]
                
        if len(keys_to_del) > 0:
            # Update local and external storages
            self.file_store.update_file(self.store)
            self.fb.upload_data()
            return len(keys_to_del)
        
        return 0
        
    def find(self, name: str):
        result = ""
        for key in  self.store:
            if key.find(name) != -1:
                result += f"{key}: {self.store[key]}\n"
                
        return result
    
    def list(self):
        key_list = []
        for key in self.store:
            key_list.append(key)
        if len(key_list) == 0:
            print("No records")
        key_list.sort()
        for key in key_list:
            print(f"{key}: {self.store[key]}")
            
    def check_name(self, name: str):
        index = 0
        pname = name
        while pname in self.store:
            index += 1
            pname = name + f" ({index})"
        return pname
            
    