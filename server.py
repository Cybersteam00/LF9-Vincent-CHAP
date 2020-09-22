#!/usr/bin/env python3

import random
import hashlib
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("0.0.0.0", 1337), requestHandler=RequestHandler)
server.register_introspection_functions()

class User:

	username = ''
	password = ''
	loggedIn = False
	salt = 0
	token = 0
	
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def gen_salt(self):
		self.salt = random.randrange(100000,999999)
		return self.salt
	
	def login(self, hash):
		if self.salt == 0:
			return False
		hashed_password = hashlib.sha512((self.password + str(self.salt)).encode('utf-8')).hexdigest()
		if hash == hashed_password:
			self.loggedIn = True
			self.token = hashlib.sha512((str(random.randrange(100000,999999)) + str(self.salt)).encode('utf-8')).hexdigest()
		else:
			self.loggedIn = False
			self.token = 0
		return self.token

	def auth(self, token):
		if token == self.token:
			return True
		else:
			return False

userList_mock = dict({"Vincent": User("Vincent", "Passwort"), "Andreas": User("Andreas", "qwertz"), "Marius": User("Marius", "asdfgh")})

def getSalt(username):
	if username in userList_mock:
		return userList_mock[username].gen_salt()
	return "User not found"

def login(username, hash):
	if username in userList_mock:
		return userList_mock[username].login(hash)
	return "login failed"

def listUsers(username, token):
	if validateUser(username, token):
		userlist = []
		for userkey in userList_mock:
			userlist.append(userkey)
		return userlist
	return "unautherized"
	
def validateUser(username, token):
	if token == 0:
		return False
	return username in userList_mock and userList_mock[username].auth(token)

server.register_function(getSalt)
server.register_function(login)
server.register_function(listUsers)

server.serve_forever()
