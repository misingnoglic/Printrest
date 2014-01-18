import Tkinter as tk
from PIL import Image, ImageTk
import os
GLOBALBOOL = False

def accepted():
    global GLOBALBOOL
    GLOBALBOOL = True
def yesno(str):
    if str in ['y','yes','1']: return True
    if str in ['n','no','0']: return False
    else: return False
    
def imageshow(x):
    global GLOBALBOOL
    GLOBALBOOL= False
    root = tk.Tk()
    root.title('Postcard')

    # pick an image file you have .bmp  .jpg  .gif.  .png
    # load the file and covert it to a Tkinter image object
    imageFile = "C:\Users\Arya\Documents\GitHub\MHacks\pictures\postcard"+str(x)+".jpg"
    image1 = ImageTk.PhotoImage(Image.open(imageFile))

    # get the image size
    w = image1.width()
    h = image1.height()

    # position coordinates of root 'upper left corner'
    x = 0
    y = 0

    # make the root window the size of the image
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))

    # root has no image argument, so use a label as a panel
    panel1 = tk.Label(root, image=image1)
    panel1.pack(side='top', fill='both', expand='yes')

    # put a button on the image panel to test it
    button2 = tk.Button(panel1, text='Press To Keep, then close image',command=accepted)
    button2.pack(side='top')

    # save the panel's image from 'garbage collection'
    panel1.image = image1
    # start the event loop
    root.mainloop()
    global GLOBALBOOL
    print GLOBALBOOL
    #return yesno(raw_input("Keep this Picture?: "))
    
    
    
