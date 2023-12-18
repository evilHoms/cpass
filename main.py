#!/usr/bin/env python3

from argparser import ArgParser
from cryptor import Cryptor
from storage import Storage
from config import Config
from passgen import gen_pass

# Name of local file as well as file in external storages. json format.
STORAGE_FILE_NAME = "data"

# Name of config file. json format.
CONFIG_FILE_NAME = "config"

# TODO configure, for exteranl services (dropbox?) add encryption to token
# TODO add delete functionality
# TODO add some fake names/values for entities which throw error during decrypting
# TODO use external services to store and verify if version correct
# TODO write tests

args = ArgParser()

if args.mode == "gen":
    print(f"Generated pass: {gen_pass()}")
    exit(0)

if not args.key:
    args.key = input("Enter the key: ")
    
config = Config(CONFIG_FILE_NAME)
dropbox_token = config.get_dropbox_token()
# TODO pass it to storage, add dropbox functionality to compare files and apply latest one if hashes are different
# print(dropbox_token)

cryptor = Cryptor(args.key)
storage = Storage(cryptor, STORAGE_FILE_NAME)

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
elif args.mode == "list":
    storage.list()
elif args.mode == "find":
    if not args.name:
        args.name = input("Enter the name to find or part of a name: ")
    
    found = storage.find(args.name)
    print(found)
elif args.mode == "remove":
    if not args.name:
        args.name = input("Enter the name to remove: ")
    
    storage.delete(args.name)
else:
    print("Wrong mode!")
