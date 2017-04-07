import xmlrpc.client

with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
	print('Hello '+proxy.getServerName())
	#print('Say hi ')
	x = input('Say hi ')
	print(proxy.greeting(x))
	#print('Say hi again')
	x = input('Say hi again')
	print(proxy.greeting(x))
