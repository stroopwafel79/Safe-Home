"""Utility file to seed crime data from Oakland
   Open Source data in seed_data/"""

from sqlalchemy import func
from datetime import datetime
from csv import reader

from model import Crime, Address, CrimeType
from model import connect_to_db, connect_to_db
from server import app
from csv import reader

def load_crimes():
	"Load crimes from Oakland Open Data into the database from a CSV file"

	print("Crimes:")

	# Delete all rows in a table, so if we need to run this a second time,
	# we won't be trying to add duplicate users.

	Crime.query.delete()

	# Read crime file and import data
	
	with open("CrimeWatch_TEST.csv") as f:
    	next(f)  # ignore header row
    	# reader function from csv module knows where end of row is despite
    	# one row taking up 3 lines in the file.
    	crimereader = reader(f, delimiter=',')  
    
    	for row in crimereader: 
        	crime = ', '.join(row).split(', ')


	
