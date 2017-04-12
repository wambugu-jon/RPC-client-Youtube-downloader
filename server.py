#import sockets and shit
from __future__ import unicode_literals
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os
import re
import youtube_dl
import socket

#Initialize meta variables
filename_concantenated = ""
meta_uploader = ""
meta_title=""
meta_id=""
meta_likes= ""
meta_dislikes=""
meta_duration=""
meta_description=""
meta_upload_date=""
meta_views=""

#my hook function for youtube_dl
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

#Initialise the ydl options to naught because it won't do shit without them.
ydl_opts = {}

#Process link to give out meta datafunction
def processLink(ytlink):

	#Receive youtube url as a parameter and extract its data
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		meta = ydl.extract_info(ytlink, download=False)

		#Store the meta data in global variables
		global meta_upload_date
		global meta_uploader
		global meta_title
		global meta_id
		global meta_likes
		global meta_dislikes
		global meta_duration
		global meta_description
		global meta_upload_date
		global meta_views
		meta_upload_date=(meta['upload_date'])
		meta_uploader=(meta['uploader'])
		meta_views=(str(meta['view_count']))
		meta_likes=(str(meta['like_count']))
		meta_dislikes=(str(meta['dislike_count']))
		meta_id=(str(meta['id']))
		meta_format=(str(meta['format']))
		meta_duration=(str(meta['duration']))
		meta_title=(str(meta['title']))
		meta_description=(str(meta['description']))

		#Concantenate the details and return them to the client
		total = ('Title: ' + meta_title + '\n' + 'Uploader: ' + meta_uploader + '\n'+ 'Description: ' + meta_description
		 + '\n' + 'Duration ' + meta_duration + '\n' + 'Upload date: '
		  + meta_upload_date + '\n' + 'ID: ' + meta_id + '\n' + 'Format: ' + meta_format + '\n' 'Likes: '
		   + meta_likes + '\n' + 'Dislikes: ' + meta_dislikes + '\n')
		return total

#Download video from the passed URL
def download_video(video_link):
	try:
		ydl_opts = {}
		with youtube_dl.YoutubeDL(ydl_opts) as downloadVideo:
			#Get new file name
			filename = (meta_title + '-' + meta_id + '.mp4')
			
			#Download video
			downloadVideo.download([video_link])
			global filename_concantenated

			#Remove all whitespace from the name
			filename_concantenated = filename.replace(" ", "")
			
			#Rename the file on thee server in  prep for upload
			os.rename(filename, filename_concantenated)
	except:
		error = ('Error experienced processing link. Make sure you:\n1. Have an active internet connection\n Enter a valid YouTube Link\n')
		return error
	else:
		#Retun the file name as saved to be used to create another such file on the client side
		return filename_concantenated

#Function download  link with the  URL passed to it.
def download_audio(audio_link):
	
	#define parameters to be used while downloading the video; 
	#in our case we want to download an audio file only and save it as [meta_id]
	ydl_opts = {
		    'format': 'bestaudio/best',       
    		'outtmpl': '%(id)s',        
    		'noplaylist' : True,        
    		'progress_hooks': [my_hook],
    }
	try:
		#Download audio
		with youtube_dl.YoutubeDL(ydl_opts) as downloadaudio:
			downloadaudio.download([audio_link])

			#Create a new file name
			filename = (meta_title + '-' + meta_id + '.m4a')

			#Remove all whitespace in prep for transferring
			filename_concantenated = filename.replace(" ", "")

			#Rename the actual audio file on the server
			os.rename(meta_id, filename_concantenated)
	except:
		#return errors of any
		error = ('Error experienced processing link. Make sure you:\n1. Have an active internet connection\n Enter a valid YouTube Link\n')
		return error
	else:
		#return the name of the file
		return filename_concantenated

#Upload function with no parameters passed
def upload_audio():
	with youtube_dl.YoutubeDL(ydl_opts) as downloadVideo:

		#Create file name
		filename_concantenated2 = (meta_title + '-' + meta_id + '.m4a')

		#Remove whitespace
		filename_concantenated2 = filename_concantenated2.replace(" ", "")
		
		#read file as a binary and start uploading it
		with open(filename_concantenated2, "rb") as handle:

			#Upload the binary file via a TCP RCP connection because Sockets ain't shit
			return xmlrpc.client.Binary(handle.read())
		
#Open video for reading and upload it to the client
def upload_video():
	with open(filename_concantenated, "rb") as handle:

		#Upload the binary file via a TCP RCP connection because Sockets ain't shit
		return xmlrpc.client.Binary(handle.read())

#Get and return server name
def getServerName(my_clients_name):

	#Create a socket object
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()     
	name = ("Hello " + my_clients_name + ". You are connected to " + host + ". Enjoy!\n")
	return name

    

#Function gets a file name as a parameter
def clear_cache(filename_to_delete):

	#Use the file name to delete the file on the server after a successful transfer
	os.remove(filename_to_delete)
	return "Cache cleared.\n"


#def get_title(title_link):
	#with youtube_dl.YoutubeDL(ydl_opts) as ydl2:
		#return meta_title
#server = SimpleXMLRPCServer(("41.89.64.44", 8000), allow_none=False)

#Start RPC client and shit
#server = SimpleXMLRPCServer(("41.89.64.44", 8000), allow_none=False)

#Make sure to connect to the correct IP
server = SimpleXMLRPCServer(("localhost", 8000), allow_none=False)

#Alert user thet the server is active
print("Listening on port 8000...lewis")

#Register all functions that we need to be recognized by the RPC Server
server.register_function(getServerName, "getServerName")
server.register_function(processLink, "processLink")
#server.register_function(get_title, "get_title")
server.register_function(download_audio, "download_audio")
server.register_function(upload_audio, "upload_audio")
server.register_function(clear_cache, "clear_cache")
server.register_function(download_video, "download_video")
server.register_function(upload_video, "upload_video")
server.register_function(my_hook, 'my_hook')

#Keep server active
server.serve_forever()
