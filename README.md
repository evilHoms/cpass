For firebase: account is needed. Create json config file, and bucket.
If after sync error applyed wrong store, old one will be stored in local/old.store file. If you want to replace data back, replace data.store file with old.store.
Key param is required for each mode except pass gen. If you don't have yet any local stored data, any key will work. If you already have some data, key must be the same until you change it via key change mode.