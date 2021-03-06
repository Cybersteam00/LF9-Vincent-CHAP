#!/usr/bin/env python3

import hashlib
from xmlrpc.client import ServerProxy

username = 'Vincent'
password = 'Passwort'

s = ServerProxy('http://localhost:1337')

salt = s.getSalt(username)
print("salt: ", salt)

hashed_password = hashlib.sha512((password + str(salt)).encode('utf-8')).hexdigest()
token = s.login(username, hashed_password) #save login-token for further usage
print("token: ", token)

print("Userliste:")
print(s.listUsers(username, token))
