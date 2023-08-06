import json
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os.path
class Database:
    def __init__(self, key, filename="troll.trolldb"):
        if len(key) < 0:
            raise Exception("""Key not defined, Usage: Database("key here")""")
        try:
            self.key = bytes(key, 'utf-8')
        except:
            raise Exception("Invalid, generate a key with trolldb.genkey()")
        self.filename = filename
        if not os.path.isfile(filename):
            open(filename, 'wb').write(Fernet(self.key).encrypt(b"{}"))
        # testing key if its valid
        try:
            key = Fernet(self.key)
            str(key.decrypt(open(self.filename, 'rb').read()), 'utf-8')
        except InvalidToken:
            raise Exception("Wrong key defined.")
    def getkey(self):
        return self.key
    def getfilename(self):
        return self.filename
    def setvariable(self, name, value):
        key = Fernet(self.key)
        d = json.loads(key.decrypt(open(self.filename, 'rb').read()))
        d[name] = value
        with open(self.filename, 'wb') as a:
            a.write(Fernet(self.key).encrypt(bytes(json.dumps(d), 'utf-8')))
    def getvariable(self, name):
        if len(name) < 0:
            raise Exception("Name of the variable not defined")
        key = Fernet(self.key)
        d = json.loads(key.decrypt(open(self.filename, 'rb').read()))
        return d[name]
    def getplainjson(self):
        key = Fernet(self.key)
        return str(key.decrypt(open(self.filename, 'rb').read()), 'utf-8')
class Table:
    def new(self, db):
        key = db.getkey()
def genkey():
    gk = Fernet.generate_key()
    print(f"your generated key = {gk}, written to key.trolldb")
    open("key.trolldb", 'wb').write(gk)
    exit()
def key_by_filename(filename):
    return open(filename,'r').read()