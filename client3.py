#!/usr/bin/env python3

import hashlib
from xmlrpc.client import ServerProxy

username = 'Marius'
password = 'asdfgh'

s = ServerProxy('http://localhost:1337')

print("Userliste:")
print(s.listUsers(username, 0)) #unautherized call

salt = s.getSalt(username)
print("salt: ", salt)

hashed_password = hashlib.sha512((password + str(salt)).encode('utf-8')).hexdigest()
token = s.login(username, hashed_password)
print("token: ", token)

print("Userliste:")
print(s.listUsers(username, token)) #autherized
