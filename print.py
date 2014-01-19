import urllib2
import urllib
import os
from pinterest.models.model import *
from PIL import Image
from imageload import *
import imageload
import lob
#GLOBALBOOL = False

def ListOfURLS(b):
    ListOfPins = b.pins()
    attrs= [x.__dict__['attrs'] for x in ListOfPins]
    URLS = [[[str(x[u'image_large_url'])],[x['image_large_size_pixels'].values()], str([x['description']])] for x in attrs]
    return(URLS)

def DownloadPics(URLS):
    if not os.path.exists('C:\Users\Arya\Documents\GitHub\MHacks\pictures'): os.makedirs('C:\Users\Arya\Documents\GitHub\MHacks\pictures')
    x=0
    for pic in URLS:
        urllib.urlretrieve(pic, "C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".jpg")
        x+=1

def SingleDownload(url):
    #print(url)
    if not os.path.exists(r'C:\Users\Arya\Documents\GitHub\MHacks\pictures'): os.makedirs(r'C:\Users\Arya\Documents\GitHub\MHacks\pictures')
    urllib.urlretrieve(url, r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\temporary.jpg")

lob.api_key = 'test_73af1296c5d22b8fb07b68f7f0c56b05cd5'
   	
CLIENT_ID = "1435561"
CLIENT_SECRET = "fad954f90dd2e4fbbd344d84cad7828e38383e40"
Pinterest.configure_client(CLIENT_ID, CLIENT_SECRET)

username = str(raw_input("What is your username: "))
board = str(raw_input("What board would you like to print: "))
b = Board(username+"/"+board)
URLDIMS = ListOfURLS(b)
blank = raw_input("Type 'skip' to skip previewing the  "+str(len(URLDIMS))+" postcards ($1 each): ")
if blank=="skip":
    DownloadPics([i[0][0] for i in URLDIMS])
    GoodDims=URLDIMS
#DownloadPics([i[0][0] for i in URLDIMS])

else:     
    GoodDims=[]
    number = 0
    for x in URLDIMS:
        SingleDownload(x[0][0])
        imageshow(x[2])
        global GLOBALBOOL
       # print(GLOBALBOOL)
      #  print(imageload.GLOBALBOOL)
        if (imageload.GLOBALBOOL):
            os.rename(r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\temporary.jpg",r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(number)+".jpg")
            #raw_input("RENAMED!!")
            GoodDims+=[x]
            number+=1
        else:
            os.remove(r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\temporary.jpg")

for x in range(len(GoodDims)):
    #print GoodDims[x]
    #width,height =  GoodDims[x][1][0][0],GoodDims[x][1][0][1]
    rotat = Image.open(r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".jpg")
    #print(GoodDims[x][1][0][0],GoodDims[x][1][0][1])
    width,height = rotat.size
    print(width,height)
    if width>height:
        rotat = (rotat.rotate(90,0,1))#.save(r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".jpg")
        print("It rotated")
        width,height = rotat.size
        print(width,height)

    ##The whitespace format
    bg = Image.open("4in6in.jpg")
    bgw,bgh = bg.size
    if (round(float(height)/width,1)==(6.0/4)):
        rotat = rotat.resize((bgw,bgh))
    elif (float(height)/width)>(6.0/4):    
        print("thin")
        rotat = rotat.resize(width*int(float(bgh)/height),bgh)
        box = ((bgw-width)/2,0,width+((bgw-width)/2),height)
        big.paste(rotat, box)
    else:
        print("too square")
        rotat = rotat.resize((bgw,height*int(float(bgw)/width)))
        box = ((0,(bgh-height)/2, bgw, height+((bgh-height)/2)))

#        print(big.size)
       # print(int((width*(6.0/4)-height)/2))
       # print(width)
        #print(height+(int((width*(6.0/4)-height)/2)))
        bg.paste(rotat, box)
    #iw = (int(width)+(int(width)%2))
    #big = big.resize((iw,int(1.5*iw)))
    bg.save(r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".pdf", "PDF", resolution = 100)
    #big.save(r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".jpg")#, "PDF", resolution = 100)
raw_input("You are about to order "+str(len(GoodDims))+" postcards at $1 each. Press enter to continue")

name = str(raw_input("What is your name?"))
address = str(raw_input("What is your address?"))
city = str(raw_input("What is your city?"))
state = str(raw_input("What is your state?"))
zipcode = str(raw_input("What is your zip?"))
country = "US"
verified_address = lob.AddressVerify.verify(name=name, address_line1=address,
                             address_city=city, address_state=state, address_country=country,
                             address_zip=zipcode)

print verified_address.to_dict()
created_address = lob.Address.create(name='New Address', address_line1=verified_address.address.address_line1,	
address_city=verified_address.address.address_city, address_state=verified_address.address.address_state, address_country=verified_address.address.address_country,
                             address_zip=verified_address.address.address_zip)

print created_address.to_dict()
#go through all files in folder and create postcard of each file

for x in range(len(GoodDims)):
    lob.Postcard.create(name=name,to=created_address.id,message="hi",front=open(r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".pdf",'rb'),from_address=created_address.id).to_dict 
    print("Printed: "+str(x))

print("Your post cards have been created and will be processed in 2-3 days! :)")
