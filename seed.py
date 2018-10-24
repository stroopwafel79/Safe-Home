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

            # get a list of street_adrs objects
            adrs_lst = db.session.query(Address.street_adrs).all()

            # get the value of the street address from the file
            s_adrs = crime_lst[5].title()

            # Turn type_lst into a set to avoid duplication
            # Then turn that into a list of tuples
            # Then turn that into a list of strings
            # Check if c_type is in the list and only add if it isn't
            if s_adrs not in ([adrs[0] for adrs in list(set(adrs_lst))]):
                address = Address(street_adrs=s_adrs,
                                  lat_long=lat_long)
                db.session.add(address)

            


            # get a list of crime_type objects
            type_lst = db.session.query(CrimeType.crime_type).all()

            # get the value of the crime type from the file
            c_type = crime_lst[0].title()

            # Turn type_lst into a set to avoid duplication
            # Then turn that into a list of tuples
            # Then turn that into a list of strings
            # Check if c_type is in the list and only add if it isn't
            if c_type not in ([crm_type[0] for crm_type in  list(set(type_lst))]):
                crime_type = CrimeType(c_type)
                db.session.add(crime_type)

            # get the crime_type_id associated with crime_type from crimetypes table
            # for adding to crime object below
            type_id = CrimeType.query.filter_by(crime_type=c_type).first()
            c_type_id = type_id.crime_type_id
            
           


                
                


            # address = Address(street_adrs=crime_lst[5].title(),
            #                   lat_long=lat_long,)

            crime = Crime(crime_type_id=c_type_id,
                          date_time=date_time, 
                          case_num=crime_lst[2],
                          description=crime_lst[3].title(),
                          beat=crime_lst[4])

            # crime.address = address
            # crime.crime_type = type_id.

            # add each object to the session
            db.session.add(crime)
            # db.session.add(crime_type)
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


    
