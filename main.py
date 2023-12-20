#!/usr/bin/env python3

from argparser import ArgParser
from cryptor import Cryptor
from storage import Storage
from config import Config
from passgen import gen_pass
from pathlib import Path
import os

# Path to dir with local files and make sure that it is exist
LOCAL_FILES_DIR = f"{Path(__file__).parent.resolve()}/local"
if not os.path.exists(LOCAL_FILES_DIR):
    os.mkdir(LOCAL_FILES_DIR)

# File name for local and external storages
DATA_FILE_NAME = "data.store"

# Path to config file. json format
CONFIG_FILE_PATH = Path(f"{LOCAL_FILES_DIR}/config.json")

# TODO copy fb config to file with encryption. Print message that original config can be deleted
# TODO add posibility to keep copy of file, when out of sync and replace one file with another
# TODO remove encryption from inmemory store, encrypt only when writing to file or external service
# TODO resend firebase requests in case of error up to 3 times with 3 sec intervals
# TODO configure, for exteranl services (firebase)
# TODO add some fake names/values for entities which throw error during decrypting
# TODO use external services to store and verify if version correct
# TODO write tests

args = ArgParser()

if args.mode == "gen":
    print(f"Generated pass: {gen_pass()}")
    exit(0)

if not args.key:
    args.key = input("Enter the key: ")

cryptor = Cryptor(args.key)
config = Config(cryptor, CONFIG_FILE_PATH)
storage = Storage(cryptor, config, LOCAL_FILES_DIR, DATA_FILE_NAME)

if args.mode == "add":
    add_tip_prompt = False
    if (not args.name or not args.login or not args.password) and not args.tip:
        add_tip_prompt = True
    
    if not args.name:
        args.name = input("Enter the name: ")
        
    args.name = storage.check_name(args.name)
        
    if not args.login:
        args.login = input(f"Enter the login to save for {args.name} (Empty by default): ")

    if args.gen_pass:
        args.password = gen_pass()
    elif not args.password:
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

else:
    print("Wrong mode!")
