#!/usr/bin/env python3

import hashlib
from xmlrpc.client import ServerProxy

username = 'Felix'
password = 'asdfgh'

s = ServerProxy('http://localhost:1337')

salt = s.getSalt(username) #error, user not found
print(salt)

hashed_password = hashlib.sha512((password + str(salt)).encode('utf-8')).hexdigest()
token = s.login(username, hashed_password)
print(token)

print(s.listUsers(username, token))
