import argparse

class ArgParser:
    
    def __init__(self):        
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, prog="cpass", usage="cpass [MODE] [...args]", description="Tool to help you to keep you passwords secure.")
        parser.add_argument("mode", type=str, help="[ls] - show list of all records\n[add] - add new record, login and tip are optional\n[rm] - remove by full name\n[rename] - change record's name\n[find] - find by part of name\n[frm] - find by part of name and remove after confirmation\n[gen] - generate pass without adding to base\n[config] - config external services\n[change] - change key and hash key.")
        parser.add_argument("-k", "--key", type=str, help="Your key key to encode/decode data")
        parser.add_argument("-K", "--hash-key", type=str, help="Your secondary key, additional level of data protection")
        parser.add_argument("-n", "--name", type=str, help="Exact name in case add/rm, or part of a name in case of find/frm")
        parser.add_argument("-r", "--replace", type=str, help="Only for rename mode, new record's name")
        parser.add_argument("-l", "--login", type=str, help="Only for add method, login to save")
        parser.add_argument("-p", "--password", type=str, help="Only for add method, password to save")
        parser.add_argument("-g", "--gen-pass", action="store_true", help="Only for add method, auto generates password as solo string without spaces")
        parser.add_argument("-t", "--tip", type=str, help="Only for add method, add tip to the record.")
        parser.add_argument("-f", "--file-local", action="store_true", help="Runs script in local mode, external storages will be out of sync. Can be synced latter.")
        
        args = parser.parse_args()
        
        self.mode = args.mode
        self.key = args.key
        self.hash_key= args.hash_key
        self.name = args.name
        self.new_name = args.replace
        self.login = args.login
        self.password = args.password
        self.gen_pass = args.gen_pass
        self.tip = args.tip
        self.file_local = args.file_local
        