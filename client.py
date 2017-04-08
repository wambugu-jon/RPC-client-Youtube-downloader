import xmlrpc.client

with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
	print('Hello '+proxy.getServerName())
	#print('Say hi ')
	url = "https://www.youtube.com/watch?v=JZncdTFNcg0"
	print(proxy.processLink(url))
	#x = input('Say hi ')
	#print(proxy.greeting(x))
	#print('Say hi again')
	#x = input('Say hi again')
	#print(proxy.greeting(x))
