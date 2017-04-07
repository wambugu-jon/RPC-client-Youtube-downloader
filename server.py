#P15/36076/2015
#Lewis Munyi
#Assignment 1

from xmlrpc.server import SimpleXMLRPCServer

serverName = 'RPC@127.0.0.1'

def getServerName():
    return serverName

def greeting(greet):
	if greet == 'Hello':
		return 'Hi'
	elif greet == 'How do you do?':
		return 'How do you do too.'

server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_function(getServerName, "getServerName")
server.register_function(greeting, "greeting")
server.serve_forever()