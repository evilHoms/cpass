import argparse

class ArgParser:
    
    def __init__(self):        
        parser = argparse.ArgumentParser("Crypto Pass", "Tool to help you to keep you passwords secure.", "Some text")
        parser.add_argument("mode", type=str, help="add - add new record/rm - remove by full name/ls - show list/find - find by part of name/gen - generate pass without adding to base/frm - find by part of name and remove after confirm/config - config external services/change - change key.")
        parser.add_argument("-k", "--key", type=str, help="Your master key to encode/decode data")
        parser.add_argument("-n", "--name", type=str, help="Exact name in case add/remove, or part of a name in case of find, ignored in case of list")
        parser.add_argument("-l", "--login", type=str, help="Only for add method, login to save")
        parser.add_argument("-p", "--password", type=str, help="Only for add method, password to save")
        parser.add_argument("-gp", "--gen-pass", action="store_true", help="Only for add method, auto generates password as solo string without spaces")
        parser.add_argument("-t", "--tip", type=str, help="Only for add method, add tip to the record.")
        parser.add_argument("-fl", "--file-local", action="store_true", help="Runs script in local mode, external storages will be out of sync. Can be synced latter.")
        
        args = parser.parse_args()
        
        self.mode = args.mode
        self.key = args.key
        self.name = args.name
        self.login = args.login
        self.password = args.password
        self.gen_pass = args.gen_pass
        self.tip = args.tip
        self.file_local = args.file_local
        