"""Utility file to seed crime data from Oakland
   Open Source data in seed_data/"""

from sqlalchemy import func
from datetime import datetime
from csv import reader

from model import Crime, Address, CrimeType, HomesForSale
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
    with open("CrimeWatch_Maps_Past_90-Days_12-30-18") as f:
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

            # TODO testing if datetime can be string instead
            # Turn date and time in string form to a datetime object
            date_time = datetime.strptime(crime_lst[1], "%m/%d/%Y %I:%M:%S %p")
            #date_time = crime_lst[1]
        
            # check if lat/long included. Get the lat/long via
            # searching for the above pattern
            if pattern.search(crime_lst[-1]):
                lat_long = pattern.search(crime_lst[-1]).group(0)
                ll_split = lat_long.split(",")
                latitude = float(ll_split[0])
                longitude = float(ll_split[1])
            else:
                continue
                
        

            # get a list of street_adrs objects
            adrs_lst = db.session.query(Address.street_adrs).all()

            # get the value of the street address from the file
            s_adrs = crime_lst[5].title()

            # Turn type_lst into a set to avoid duplication
            # Then turn that into a list of tuples
            # Then turn that into a list of strings
            # Check if c_type is in the list and only add if it isn't
            if s_adrs not in ([adrs[0] for adrs in list(set(adrs_lst))]) and lat_long:
                address = Address(street_adrs=s_adrs,
                                  latitude=latitude,
                                  longitude=longitude)
                db.session.add(address)

            # get the address_id associated with street_adrs from addresses table
            # for adding to crime object below
            adrs_id = Address.query.filter_by(street_adrs=s_adrs).first()
            # import pdb
            # pdb.set_trace()

            s_adrs_id = adrs_id.address_id


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
            
            crime = Crime(address_id=s_adrs_id,
                          crime_type_id=c_type_id,
                          date_time=date_time, 
                          case_num=crime_lst[2],
                          description=crime_lst[3].title(),
                          beat=crime_lst[4])

            db.session.add(crime)
        db.session.commit()


def load_homes():
    """Load homes for sale in Oakland"""

    # Read crime file and import data
    with open("seed_data/redfin_11-6-18.csv") as f:
        # ignore header row
        next(f)

        homereader = reader(f, delimiter=',') 
        for row in homereader: 
            home_lst = ', '.join(row).split(', ') # each row is a list of strings

            if home_lst[16] == '':
                hoa = None
            else:
                hoa = home_lst[16]

            # if home_lst[8] == '':
            #     bed = None
            # else:
            #     bed = int(home_lst[8]) 

            homes = HomesForSale(mls_num=home_lst[-5],
                                 street_adrs=home_lst[3],
                                 city=home_lst[4],
                                 state=home_lst[5],
                                 zipcode=home_lst[6],
                                 price=int(home_lst[7]),
                                 property_type=home_lst[2],
                                 neighborhood=home_lst[10],
                                 year_built=home_lst[13],
                                 sq_ft=home_lst[11],
                                 price_per_sqft=home_lst[15],
                                 lot_size=home_lst[12],
                                 num_bed=home_lst[8],
                                 num_bath=home_lst[9],
                                 days_on_market=home_lst[14],
                                 hoa_per_month=hoa,
                                 latitude=float(home_lst[-2]),
                                 longitude=float(home_lst[-1]))

            db.session.add(homes)
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

    # Import data from the crimes tsv
    load_crimes()
    # Import data from the homes for sale csv
    load_homes()


    
