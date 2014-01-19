import lob
import urllib2
import os

lob.api_key = 'test_73af1296c5d22b8fb07b68f7f0c56b05cd5'

# yo arya how do I make global variables? these should be it


name = str(raw_input("What is your name?"))
address = str(raw_input("What is your address?"))
city = str(raw_input("What is your city?"))
state = str(raw_input("What is your state?"))
country = str(raw_input("What is your country?"))
zip = str(raw_input("What is your zip?"))
addy = lob.Address.create(name=name, address_line1=address,
                             address_city=city, address_state=state, address_country=country,
                             address_zip=zip)




#address = lob.Address.create(name,address,city,state,country,zip)
	
verify = lob.AddressVerify.verify(addy)
addy = verify


#go through all files in folder and create postcard of each file
lob.Postcard.create(name=name,to_address=addy,message="hi",front=open('/Users/peternagel/Downloads/pytest/test.pdf','rb'),from_address=addy).to_dict #change message and fix the file the thing opens

=print("Your post cards have been created and will be processed in 2-3 days! :)")
