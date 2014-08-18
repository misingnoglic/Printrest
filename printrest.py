import urllib2
import urllib
import os
from pinterest.models.model import * #pinterest API
from PIL import Image
import lob #Lob API
import shutil
import imageload
from imageload import * #Local file for loading images

def ListOfURLS(b):
    #Takes in a pinterest board and returns a (very convolted) list of URLS and data associate with them
    ListOfPins = b.pins()
    attrs= [x.__dict__['attrs'] for x in ListOfPins]
    URLS = [[[str(x[u'image_large_url'])],[x['image_large_size_pixels'].values()], ([x['description']])] for x in attrs]
    return(URLS)

def DownloadPics(URLS):
    #downloads all pictures in the URL list coming from ListOfURLS
    current_directory = os.getcwd()
    if not os.path.exists(current_directory+'\pictures'):
        os.makedirs(current_directory+'\pictures')
    x=0
    for pic in URLS:
        urllib.urlretrieve(pic, current_directory+"\postcard"+str(x)+".jpg")
        x+=1

def SingleDownload(url):
    #downloads single URL
    current_directory = os.getcwd()
    if not os.path.exists(current_directory+r'\pictures'):
        os.makedirs(current_directory+r'\pictures')
    urllib.urlretrieve(url, current_directory+r"\pictures\temporary.jpg")

picture_directory = os.getcwd()+r'\pictures'

lob.api_key = None #Key for Lob development - Taken out for privacy
   	
CLIENT_ID = None #ID for pinterest - Taken out for privacy
CLIENT_SECRET = None #secret key for pinterest - Taken out for privacy

Pinterest.configure_client(CLIENT_ID, CLIENT_SECRET)

username = str(raw_input("What is your username: ")) #or username with board on it
board = str(raw_input("What board would you like to print: "))
b = Board(username+"/"+board) #creates board object
URLDIMS = ListOfURLS(b) #Url dimmensions
blank = raw_input("Type 'skip' to skip previewing the  "+str(len(URLDIMS))+" postcards ($1 each): ") #if you do this you print all
if blank=="skip":
    DownloadPics([i[0][0] for i in URLDIMS]) #downloads all pics
    GoodDims=URLDIMS #all pics are good pics

else:     #if not skipping
    GoodDims=[]
    number = 0
    for x in URLDIMS:
        SingleDownload(x[0][0]) #downloads pic
        imageshow(x[2][0]) #shows the pic
        global GLOBALBOOL
       # print(GLOBALBOOL)
      #  print(imageload.GLOBALBOOL)
        if (imageload.GLOBALBOOL): #if pic wants to be kept, it's made permanant
            os.rename(picture_directory+r"\temporary.jpg",picture_directory+r"\postcard"+str(number)+".jpg")
            GoodDims+=[x] #added to good list
            number+=1 #next good item
        else: #if not needed file will be deleted
            os.remove(picture_directory+r"\temporary.jpg")

for x in range(len(GoodDims)): #for every good picture
    rotat = Image.open(picture_directory+r"\postcard"+str(x)+".jpg") #opens pic
    width,height = rotat.size 
    if width>height: #if width is greater than height it will be rotated
        rotat = (rotat.rotate(90,0,1))
        width,height = rotat.size #Must adjust width and height

    ##The whitespace format
    bg = Image.open("white4b6.jpg") #white background (images must be 4 by 6 inches)
    if (round(float(height)/width,1)==(6.0/4)): #if image is this size picture has no bg
        big = rotat
    elif (float(height)/width)>=(6.0/4):    #If it is skinnier white background will fill extra width
        big = bg.resize(((int(height*(4.0/6))),height))
        box = ((int(height*(4.0/6)- width)/2), 0, width+int((height*(4.0/6) - width)/2), height)
        big.paste(rotat, box)
        
    else: #if it's too square white will fill up extra height
        big = bg.resize((width,int(width*(6.0/4))))
        box = (0,int(((width*(6.0/4)-height)/2)),width, height+int(((width*(6.0/4)-height)/2)))
        big.paste(rotat, box)
    iw = (int(width)+(int(width)%2)) #to have an even width
    big = big.resize((iw,int(1.5*iw))) #this will have 4 by 6 ratio
    bigw,bigh = big.size
        big.save(picture_directory+r"\postcard"+str(x)+".pdf", "PDF", resolution = float(bigh)/6)
    ##^^IMPORTANT CODE: THIS SAVED MY LIFE
    
raw_input("You are about to order "+str(len(GoodDims))+" postcards at $1 each. Press enter to continue")

name = str(raw_input("What is your name? "))
address = str(raw_input("What is your address? "))
city = str(raw_input("What is your city? "))
state = str(raw_input("What is your state? "))
zipcode = str(raw_input("What is your zip? "))
country = "US"
verified_address = lob.AddressVerify.verify(name=name, address_line1=address,
                             address_city=city, address_state=state, address_country=country,
                             address_zip=zipcode)

created_address = lob.Address.create(name='Printrest', address_line1=verified_address.address.address_line1,	
                    address_city=verified_address.address.address_city, address_state=verified_address.address.address_state,
                    address_country=verified_address.address.address_country,
                    address_zip=verified_address.address.address_zip)

#go through all files in folder and create postcard of each file

for x in range(len(GoodDims)):
    lob.Postcard.create(name=name,to=created_address.id,message=GoodDims[x][2][0],
                        front=open(r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".pdf",'rb'),
                        from_address=created_address.id).to_dict
    print("Printed: "+str(x))

shutil.rmtree('/pictures')
print("Your post cards have been created and will be processed in 2-3 days! :)")
raw_input()
