
## About The Project
Python command line app for managing passwords. It allow to save pairs [resource-name]: [resource-password] and optionaly add [resource-login], [resource-tip].

All information is encrypted with key, which you enter after adding first record. By default all data is saved locally, but there is opportynity to sync it with firebase storage, for this you'll need a firebase account with config file and bucket.

### Prerequisites
Was tested on Mint/Ubuntu with Python -V 3.10.12
Installed python3-pip is required

### Installation
#### Local version:
Put the script where you want it to be, cd to the script's dir.
run `./install.sh` script, it will generate `cpass` script, put it to your PATH dirrectory for easy use.
If you will run `cpass -k[key] ls` and see `No records` in the console - everething is good.

There are few options for data protection:
* Most secured but not very convenient: `./install.sh` without arguments and enter 2 keys all the time you use cpass, `cpass ls` and then enter in hidden prompt 2 passwords. Or you can pass key and hash key as parameters `cpass -k[key] -K[hash_key] ls`, but it a bit less secured as people can see you keys.
Use this method if other people have access to the computer where you use it. If you are not going to use computer anymore, remove `./local` dir.
* Optimal way: `./install.sh [hash_key]` installation with one of the keys, so you will need to enter only one to run cpass. Run `cpass ls` without key arguments and enter one key in the secret prompt or pass the key via arguments `cpass -k[key] ls`. Optimal for home, where strangers don't have access to your computer. Don't use this install method on public computers as your hash key will be exposed.
* Less secured (not recommended): only if you know what you are doing, `./install.sh [hash_key] [key]` use install script with both keys, so you won't be asked to enter keys when you run cpass. Data still will be encrypted, but anybody will be able to see all records without entering any passwords.

#### With firebase:
After installing dependencies, you will need https://firebase.google.com/ account, config and bucket.
1. To get config, go to account console -> Project settings -> Click `Generate new private key`
Use same config between different computers/users if you want to share same store.
2. To get bucket, go to Build -> Storage -> New bucket -> Copy folder path
3. Then run script in config mode with the key you will use `cpass -k[key] config`.
4. When it'll be asked to enter path to the config file, enter path to the json file which you get after clicking on `Generate new private key` button in firebase console.
5. When it'll be asked to enter bucket, just past path you copied on the 2nd step

If you have an account with existed already data.store, make sure that key and hash key are the same. If not, change keys before configuring.

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

Write tests