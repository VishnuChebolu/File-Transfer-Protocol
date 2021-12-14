import json
import hashlib

uname = input("Enter username : ")
password = input("Enter password : ")
password = hashlib.md5(password.encode()).hexdigest()
access = input("Enter access of the user ('r','w','rw') : ")
a = open("credentials.json", 'r')
credentials = json.load(a)
credentials[uname] = [password, access]

a = open("credentials.json", 'w')
json.dump(credentials, a, indent=4)