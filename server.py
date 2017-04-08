#P15/36076/2015
#Lewis Munyi
#Assignment 1
from __future__ import unicode_literals
from xmlrpc.server import SimpleXMLRPCServer
#from xmlrpc.server import SimpleXMLRPCRequestHandler

import youtube_dl
serverName = 'RPC@127.0.0.1'

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'format': 'bestaudio/best',       
    'outtmpl': '%(id)s',        
    'noplaylist' : True,        
    'progress_hooks': [my_hook],  
}

def processLink(ytlink):
	print (ytlink)
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([ytlink])
	print("Complete")
def getServerName():
    return serverName

#def greeting(greet):
#	if greet == 'Hello':
#		return 'Hi'
#	elif greet == 'How do you do?':
#		return 'How do you do too.'

server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
print("Listening on port 8000...")
server.register_function(getServerName, "getServerName")
#server.register_function(greeting, "greeting")
server.register_function(processLink, "processLink")
server.register_function(my_hook, 'my_hook')
server.serve_forever()