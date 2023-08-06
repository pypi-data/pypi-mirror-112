# TrollDB
Just a simple json database project made by Walter.

### Example code

    import trolldb


    database = trolldb.Database(trolldb.key_by_filename('key.trolldb')) # new database
    print('Doing database on {0}'.format(database.getfilename())) 

    v = str(1)
    database.setvariable(v, '{0}'.format(v)) # sets variable in the database
    print(database.getvariable(v)) # get variable 
    print(database.getplainjson()) # prints the whole json
