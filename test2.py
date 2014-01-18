import urllib2
import urllib
import os
from pinterest.models.model import *
def ListOfURLS(b):
    ListOfPins = b.pins()
    attrs= [x.__dict__['attrs'] for x in ListOfPins]
    URLS = [[[str(x[u'image_large_url'])],[x['image_large_size_pixels'].values()], [x['description']]] for x in attrs]
    return(URLS)

def DownloadPics(URLS):
    if not os.path.exists('C:\Users\Arya\Documents\GitHub\MHacks\pictures'): os.makedirs('C:\Users\Arya\Documents\GitHub\MHacks\pictures')
    x=0
    for pic in URLS:
        urllib.urlretrieve(pic, "C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".jpg")
        x+=1
	
CLIENT_ID = "1435561"
CLIENT_SECRET = "fad954f90dd2e4fbbd344d84cad7828e38383e40"
Pinterest.configure_client(CLIENT_ID, CLIENT_SECRET)

username = str(raw_input("What is your username: "))
board = str(raw_input("What board would you like to print: "))
b = Board(username+"/"+board)
URLDIMS = ListOfURLS(b)
blank = raw_input("Press enter if you are you sure you want to print "+str(len(URLDIMS))+" postcards ($1 each)")
DownloadPics([i[0][0] for i in URLDIMS])
