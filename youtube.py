#
#ydl3.py
from __future__ import unicode_literals
import youtube_dl

ydl_opts = {}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    meta = ydl.extract_info(
        'https://www.youtube.com/watch?v=9bZkp7q19f0', download=False) 

print ('upload date : %s' %(meta['upload_date']))
print ('uploader    : %s' %(meta['uploader']))
