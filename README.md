
## About The Project
Python command line app for managing passwords. It allow to save pairs [resource-name]: [resource-password] and optionaly add [resource-login], [resource-tip].

All information is encrypted with key, which you enter after adding first record. By default all data is saved locally, but there is opportynity to sync it with firebase storage, for this you'll need a firebase account with config file and bucket.

### Prerequisites
Was tested on Mint/Ubuntu with Python -V 3.10.12

### Installation
#### Local version:
Put the script where you want it to be, cd to the script's dir.
run `./install.sh` script, it will generate `cpass` script, put it to your PATH dirrectory for easy use.
If you will run `cpass -k[key] ls` and see `No records` in the console - everething is good.

#### With firebase:
After installing dependencies, you will need https://firebase.google.com/ account, config and bucket.
1. To get config, go to account console -> Project settings -> Click `Generate new private key`
2. To get bucket, go to Build -> Storage -> New bucket -> Copy folder path
3. Then run script in config mode with the key you will use `cpass -k[key] config`.
4. When it'll be asked to enter path to the config file, enter path to the json file which you get after clicking on `Generate new private key` button in firebase console.
5. When it'll be asked to enter bucket, just past path you copied on the 2nd step
6. If you didn't use this bucket from other pc with different key, leave 3st prompt empty

## Usage
To show all records `cpass -k[key] ls`

To add new record `cpass -k[key] add` or `cpass -k[key] add -n[resource-name] -l[resource-login] -p[resource-password] -t[resource-tip]` to avoid questions

To find records by part of name [resource-name] `cpass -k[key] find` or `cpass -k[key] find -n[resource-name]`

To remove record `cpass -k[key] rm` or `cpass -k[key] rm -n[resource-name]`

To get full list of commands `cpass --help`

  

## Notes

* If wrong store applied after sync error, old one will be stored in local/old.store file. If you want to replace data back, replace data.store file with old.store.

* Key param is required for each mode except pass gen. If you don't have yet any local stored data, any key will work. If you already have some data, key must be the same until you change it via key change mode `cpass -k[key] change`.

  

## TODO

Add bash script to automate instalation and adding to PATH.
Write tests