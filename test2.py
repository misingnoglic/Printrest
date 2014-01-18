from pinterest.models.model import *

def ListOfURLS(b):
    ListOfPins = b.pins()

    URLS = [str(x.__dict__['attrs'][u'image_large_url']) for x in ListOfPins]
    return(URLS)

	
CLIENT_ID = "1435561"
CLIENT_SECRET = "fad954f90dd2e4fbbd344d84cad7828e38383e40"
Pinterest.configure_client(CLIENT_ID, CLIENT_SECRET)

username = str(raw_input("What is your username: "))
board = str(raw_input("What board would you like to print: "))
b = Board(username+"/"+board)
URLS = ListOfURLS(b)
blank = raw_input("Press enter if you are you sure you want to print "+str(len(URLS))+" postcards ($1 each)")
print(URLS)
