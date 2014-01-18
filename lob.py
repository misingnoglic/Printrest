import lob
import urllib2
import os

lob.api_key = 'test_73af1296c5d22b8fb07b68f7f0c56b05cd5'

# yo arya how do I make global variables? these should be it
name
address

def makeAddress():
	name = str(raw_input("What is your name?"))
	address = str(raw_input("What is your address?"))
	city = str(raw_input("What is your city?"))
	state = str(raw_input("What is your state?"))
	country = str(raw_input("What is your country?"))
	zip = str(raw_input("What is your zip?"))
	address = lob.Address.create(name,address,city,state,country,zip)
	
	verify = lob.AddressVerify.verify(newAddress)
	address = verify

def createPostCards():
	#go through all files in folder and create postcard of each file
	lob.Postcard.create(name=name,to_address=address,message="hi",front=open('/Users/peternagel/Downloads/pytest/test.pdf','rb'),from_address=to_address).to_dict #change message and fix the file the thing opens

createPostCards()
makeAddress()
print("Your post cards have been created and will be processed in 2-3 days! :)")