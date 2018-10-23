"""Utility file to seed crime data from Oakland
   Open Source data in seed_data/"""

from sqlalchemy import func
from datetime import datetime
from csv import reader

from model import Crime, Address, CrimeType
from model import connect_to_db, connect_to_db
from server import app
from csv import reader
import re

def load_crimes():
	"Load crimes from Oakland Open Data into the database from a CSV file"

	print("Crimes:")

	# Delete all rows in a table, so if we need to run this a second time,
	# we won't be trying to add duplicate users.

	Crime.query.delete()

	# Read crime file and import data
	
	with open("CrimeWatch_TEST.csv") as f:
    	# ignore header row
    	next(f)

    	# reader function from csv module knows where end of row is despite
    	# one row taking up 3 lines in the file.
    	crimereader = reader(f, delimiter=',')  

    	# Creates a pattern for latitude and longitude so dirty data can
    	# be searched more reliably.
    	pattern = re.compile("-?\d+.\d+") 

    	for row in crimereader: 
        	crime_lst = ', '.join(row).split(', ')

        	# Turn date and time in string form to a datetime object
        	date_time = datetime.strptime(crime_lst[1], "%m/%d/%Y %I:%M:%S %p")

        
        	# check if lat/long included. If not call function to look
        	# it up based on the address
        	if pattern.search(crime_lst[-1]):
        		latitude=pattern.search(crime_lst[9]).group(0),
        		longitude=pattern.search(crime_lst[10]).group(0)
        		# call other function ####################
        	else:
        		pass



        	crime = Crime(date_time=date_time, 
        				  case_num=crime_lst[2],
        				  description=crime_lst[3].title(),
        				  beat=crime_type[4]
        				   )

        	crime_type = CrimeType(crime_lst[0].title())

        	address = Address(street_adrs=crime_lst[5].title(),
        					  latitude=,
        					  longitude=




	
