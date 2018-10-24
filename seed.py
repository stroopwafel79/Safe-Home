"""Utility file to seed crime data from Oakland
   Open Source data in seed_data/"""

from sqlalchemy import func
from datetime import datetime
from csv import reader

from model import Crime, Address, CrimeType
from model import connect_to_db, db
from server import app
from csv import reader
import re

def load_crimes():
    """Load crimes from Oakland Open Data into the database from a CSV file"""

    print("Crimes, Addresses, and Crimetypes tables have been seeded.")

    # Delete all rows in a table, so if we need to run this a second time,
    # we won't be trying to add duplicate users.

    Crime.query.delete()

    ##############################
    ### REFACTOR IF TIME: slicing depends on columns in this order (index in parens):
    ###       crime_type(0), date_time(1), case_num(2), description(3),
    ###       beat(4), street_adrs(4), latitude(-2), longitude(-1)
    ################################ 
    
    # Read crime file and import data
    with open("seed_data/CrimeWatch_TEST(20_crimes_tab).tsv") as f:
        # ignore header row
        next(f)

        # reader function from csv module knows where end of row is despite
        # one row taking up 3 lines in the file.
        crimereader = reader(f, delimiter='\t')  

        # Creates a pattern for latitude and longitude so dirty data can
        # be searched more reliably.
        pattern = re.compile("-?\d+.\d+, -?\d+.\d+") 

        for row in crimereader: 
            crime_lst = '\t '.join(row).split('\t ')

            # Turn date and time in string form to a datetime object
            date_time = datetime.strptime(crime_lst[1], "%m/%d/%Y %I:%M:%S %p")

        
            # check if lat/long included. If not call function to look
            # it up based on the address
            if pattern.search(crime_lst[-1]):
                lat_long = pattern.search(crime_lst[-1]).group(0)
                
            else:
                # call other function ###################
                lat_long = "NOOOOOOO"

            type_lst = db.session.query(CrimeType.crime_type).all()

            # import pdb

            # pdb.set_trace()

            c_type = crime_lst[0].title()

            if c_type not in ([crm_type[0] for crm_type in  list(set(type_lst))]):
                crime_type = CrimeType(c_type)
                


            # address = Address(street_adrs=crime_lst[5].title(),
            #                   lat_long=lat_long,)

            # crime = Crime(date_time=date_time, 
                          # case_num=crime_lst[2],
                          # description=crime_lst[3].title(),
                          # beat=crime_lst[4])

            # crime.address = address
            # crime.crime_type = crime_type

            # add each object to the session
            # db.session.add(crime)
            db.session.add(crime_type)
            # db.session.add(address)

        db.session.commit()

############################################################################
if __name__ == '__main__':
    import os

    # Upon running the file every time:
    # First, delete the test table(start with a new slate)
    # Second, create the test database anew
    os.system("dropdb test")
    os.system("createdb test")  

    connect_to_db(app)

    # create tables in case they haven't been created
    db.create_all()

    # Import data from the crimes csv
    load_crimes()


    
