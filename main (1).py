#!/usr/bin/python
from sys import exit
import json
import os
from urllib.parse import urlencode, quote_plus
import json
from urllib.request import urlopen

import urllib
import httplib2 # pip3 install httplib2
from googleapiclient.discovery import build # pip3 install google-api-python-client
from googleapiclient.http import MediaFileUpload
from oauth2client.client import AccessTokenCredentials # pip3 install oauth2client
details_ = {}

# AREA YOU NEED TO EDIT
#######################################################################################################################################
details_['client_id'] = "<< CLIENT ID >>"
details_['client_secret'] = "<< CLIENT SECRET >>"
details_['refresh_token'] = "<< REFRESH TOKEN >>"
details_['video_title'] = "Video title goes here"
details_['video_desc'] = "Video description goes here"

 # Must be number, Visit link to check defined numbers for categories: https://gist.github.com/dgp/1b24bf2961521bd75d6c
details_['category'] = "1"
details_['privacy'] = "public" # private, public, unlisted
details_['tags'] = ['hello', 'how']

# Please use `\\` double backslash for path seperator
path = details_['file_path'] = r'C:\\Users\\BILAL AHMAD\\Videos\\spinner.mp4'
#######################################################################################################################################


if not os.path.exists(path):
    print ("File '%s' doesn't exists" % str(path))
    exit(0)




if 'refresh_token' not in details_ or 'client_secret'  not in details_ or 'client_id' not in details_ or\
   "file_path" not in details_ or 'video_title' not in details_ or 'video_desc' not in details_ or 'tags' not in details_ or\
   'category' not in details_ or 'privacy' not in details_:
    print ("""\n\nERROR::\n\nPlease put content in config file like this:
    {

	"client_id" : "<<>>" ,
	"client_secret" : "<<>>",
	"refresh_token" : "<<>>",
	"file_path" : "<<>>",
	"video_title" : "<<>>",
	"video_desc" : "<<>>",
	"tags" : "<<>> (each tag seperated by comma)",
	"category" : "<<>> number only",
	"privacy" : "private, unlisted or public"
}

""")
    exit(0)

if not os.path.exists(details_['file_path']):
    print ("Video File '%s' doesn't exists" % str(path))
    exit(0)

print ("\n\nUploading video with following details:")
for key in details_.keys():
    if key == "client_id" or key == "refresh_token" or key == "client_secret":
        continue
    print ("\t" , key, ":", details_[key])



if type(details_['tags']) is not list:
    print ("\n\nERROR:: Please enclose tags in square brackets (inverted commas \" on both side) and each tag must be closed in inverted commas \' and should be seperated by comma \n\n")
    exit(0)
try:
    int(details_['category'])
except:
    print ("\n\nERROR:: Please entry category only in number\n\n")
    

POST = "https://www.googleapis.com/oauth2/v4/token"
# preparing form data for getting access token
data = dict(refresh_token=details_[u'refresh_token'],
            client_secret=details_[u'client_secret'],
            grant_type='refresh_token',
            client_id=details_[u'client_id'])

# Getting ACCESS TOKEN:
data = urllib.parse.urlencode(data, doseq=False, quote_via=quote_plus)
data = data.encode('utf-8') # data should be bytes
req = urllib.request.Request(POST, data)

try:
    resp = urllib.request.urlopen(req)
    details = json.load(resp)
except Exception as e:
    print ("ERROR", e, "Quiting Application")
    exit(0)
if 'access_token' not in details:
    print ('Can\'t get access token. Something bad happened, please contact developer')
    exit(0)
    

scopes = ["https://www.googleapis.com/auth/youtube.upload"]


def upload():
    print ("\nStarting uploading...")
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
    api_service_name = "youtube"
    api_version = "v3"
    credentials = AccessTokenCredentials(details['access_token'], "")
    http = httplib2.Http()
    http = credentials.authorize(http)
    youtube = build(api_service_name, api_version, http=http)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": details_[u'category'],
                "description": details_[u'video_desc'],
                "title": details_[u'video_title'],
                "tag" : details_[u'tags']
            },
            "status": {
                "privacyStatus": details_[u'privacy']
            }
        },

        media_body=MediaFileUpload(details_[u'file_path'])
    )
    print ("Uploading completed with following response message:")
    print(request.execute())


if __name__ == "__main__":
    try:
        upload()
    except Exception as e:
        print ("ERROR", e, "Quiting Application")
