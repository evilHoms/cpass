#!/usr/bin/env python3

from argparser import ArgParser
from cryptor import Cryptor
from storage import Storage
from config import Config
from passgen import gen_pass
from pathlib import Path
from getpass import getpass
import os

# Path to dir with local files and make sure that it is exist
LOCAL_FILES_DIR = f"{Path(__file__).parent.resolve()}/local"
if not os.path.exists(LOCAL_FILES_DIR):
    os.mkdir(LOCAL_FILES_DIR)

# File name for local and external storages
DATA_FILE_NAME = "data.store"

# Path to config file. json format
CONFIG_FILE_PATH = Path(f"{LOCAL_FILES_DIR}/config.json")

args = ArgParser()

if args.mode == "gen":
    print(f"Generated pass: {gen_pass()}")
    exit(0)

if not args.key:
    args.key = getpass("[KEY]: ")
    
if not args.hash_key:
    args.hash_key = getpass("[HASH_KEY]: ")

cryptor = Cryptor(args.key, args.hash_key)
config = Config(cryptor, CONFIG_FILE_PATH)

if args.mode == "config":
    print("Config will be encrypted with the key you entered. Make sure you use same key as for local storage.")
    cred, bucket = config.set_firebase_config()
    if not cred or not bucket:
        print("Firebase creds and bucket are required.")
        exit(0)
    print("Config encrypted and cached.")
try:
    storage = Storage(cryptor, config, LOCAL_FILES_DIR, DATA_FILE_NAME, args.file_local)
except:
    print("[Error]: storage can't be initialized, check your key/config/internet connection.")
    print("If you want to run script in local mode, add `-fl` flag. If data in this mode will be changed, external storage will be out of sync, but it can be synced latter.")
    exit(0)

if args.mode == "change":
    print("Keys for both local and external storeage will be changed.")
    new_key = getpass("[KEY] Enter new key (Leave empty to keep same key): ")
    if new_key:
        new_key_rep = getpass("[KEY] Repeat the key: ")
        if new_key != new_key_rep:
            print("Entered keys are not the same!")
            exit(0)
    else:
        new_key = cryptor.key
        
    new_hash_key = getpass("[HASH KEY] Enter new key (Leave empty to keep same key): ")
    if new_hash_key:
        new_hash_key_rep = getpass("[HASH KEY] Repeat the key: ")
        if new_hash_key != new_hash_key_rep:
            print("Entered keys are not the same!")
            exit(0)
    else:
        new_hash_key = cryptor.hash_key
        
    storage.recrypt(new_key, new_hash_key)
    print("Keys are applied, the data is recrypted.")
    print("If you use the script with saved via install.sh key, you will need to reinstall it.")

if args.mode == "add" or args.mode == "update":
    if not args.name:
        args.name = input("Enter the name: ")
    
    checked_name = storage.check_name(args.name)
    
    if args.mode == "update" and checked_name == args.name:
        print(f"Record with name {args.name} doesn't exist")
        exit(0)
        
    if args.mode == "add":
        args.name = checked_name
    
    if args.gen_pass:
        args.password = gen_pass()
        
    add_tip_prompt = False
    if not args.password and not args.tip:
        add_tip_prompt = True
        
    if not args.login and not args.password:
        args.login = input(f"Enter the login to save for {args.name} (Empty by default): ")

    if not args.password:
        args.password = input(f"Enter the password to save for {args.name}: ")
        
    if add_tip_prompt:
        args.tip = input(f"Any tips for the record {args.name}? (Empty by default): ")
        
    value = f"{args.login + ' ' if args.login else ''}{args.password}{' : ' + args.tip if args.tip else ''}"
    storage.add(args.name, value)
    
    print(f"{args.name}: {value}")

elif args.mode == "ls":
    storage.list()

elif args.mode == "find":
    if not args.name:
        args.name = input("Enter the name to find or part of a name: ")
    found = storage.find(args.name)
    print(found)

elif args.mode == "frm":
    if not args.name:
        args.name = input("Enter the name to find or part of a name: ")
    found = storage.find(args.name)
    if not found:
        print(f"No items found by '{args.name}' string")
    else:
        print(found)
        should_remove = input("Are you sure to remove all listed above records? (y/n): ").lower() == "y"
        if should_remove:
            num_removed = storage.remove_by_substring(args.name)
            print(f"Removed records: {num_removed}")

elif args.mode == "rm":
    if not args.name:
        args.name = input("Enter the name to remove: ")
    num_removed = storage.remove(args.name)
    if not num_removed:
        print(f"No items found by '{args.name}' name")
    else:
        print(f"Removed records: {num_removed}")
        
elif args.mode == "rename":
    if not args.name:
        args.name = input("Enter the name to remove: ")
    if not args.new_name:
        args.new_name = input("Enter new name: ")
    is_renamed = storage.rename(args.name, args.new_name)
    if is_renamed:
        print(f"Renamed {args.name} -> {args.new_name}")
    else:
        print(f"No record with name: {args.name}")

elif args.mode != "config" and args.mode != "change":
    print("Wrong mode!")
