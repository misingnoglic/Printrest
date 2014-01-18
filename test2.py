import urllib2
import urllib
import os
from pinterest.models.model import *
from PIL import Image
from imageload import *
import imageload
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
        print("It rotated")
        (height, width)= (width,height)
        print(width,height)
        rotat = (rotat.rotate(90,0,1))#.save(r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".jpg")

    ##The whitespace format
    bg = Image.open("white4b6.jpg")
    if (round(float(height)/width,1)==(6.0/4)):
        big = rotat
    elif (float(height)/width)>=(6.0/4):    
        print("thin")
        big = bg.resize(((int(height*(4.0/6))),height))
        print(big.size)
        print(int(height*(4.0/6)- width)/2)
        print(width+int((height*(4.0/6) - width)/2))
        print(height)

        box = ((int(height*(4.0/6)- width)/2), 0, width+int((height*(4.0/6) - width)/2), height)
        big.paste(rotat, box)
        
    else:
        print("too square")
        big = bg.resize((width,int(width*(6.0/4))))
        box = (0,(int((width*(6.0/4)-height)/2)),width, height+(int((width*(6.0/4)-height)/2)))
        big.paste(rotat, box)
    big.save(r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".pdf", "PDF", resolution = 100)
    #big.save(r"C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".jpg")#, "PDF", resolution = 100)

        
        
