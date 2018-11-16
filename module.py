"""Module containing functions to assist in getting
   crime and zillow data"""

from model import CrimeType, Crime, Address, HomesForSale
from os import environ # to access environ.get("zillow_key")
import requests
from pprint import pprint
from xmljson import BadgerFish
from xml.etree.ElementTree import fromstring
bf = BadgerFish(dict_type=dict)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy() 


def get_gkey():
    """Get the Google Maps API secret key"""

    gkey = environ.get("GKEY")
    return gkey

def get_latlong_range(input_lat, input_lng):
    """ Get a range of latitudes and longitudes based on the lat and long of the 
        address entered in the homepage.
    """
    return {
            "max_lat": input_lat + 0.004,
            "min_lat": input_lat - 0.004,
            "max_lng": input_lng + 0.012,
            "min_lng": input_lng - 0.012
           }

def get_crimedata_by_latlong_range(input_lat, input_lng):
    """Based on input lat and long, get a range of lat/longs to populate crimes
    only on viewable google maps window""" 

    latlong_range = get_latlong_range(input_lat, input_lng) # returns a dictionary

    # get list of address objects within the range and associate with crimes
    crime_addresses = Address.query.options(
                                 db.joinedload('crimes').joinedload('crime_type')
                                 ).filter(Address.latitude.between(latlong_range["min_lat"], 
                                                                   latlong_range["max_lat"]), 
                                          Address.longitude.between(latlong_range["min_lng"], 
                                                                    latlong_range["max_lng"])).all()
    
    crimedata_in_range = []

    for address in crime_addresses:
        for crime in address.crimes:

            crime_dict = {
                          "lat": crime.address.latitude, 
                          "lng": crime.address.longitude,
                          "crime_type": crime.crime_type.crime_type,
                          "case_num": crime.case_num,
                          "description": crime.description,
                          "date_time": crime.date_time.isoformat(),
                          "police_beat": crime.beat
                         }

            crimedata_in_range.append(crime_dict)

    return crimedata_in_range


def get_homedata_by_latlong_range(input_lat, input_lng):
    """Based on input lat and long, get a range of lat/longs to populate 
    homes for sale in Google map""" 

    latlong_range = get_latlong_range(input_lat, input_lng) # returns a dictionary

    # query db for all home for sale details that are in the latitude longitude range
    home_for_sale_data = HomesForSale.query.filter(HomesForSale.latitude.between(latlong_range["min_lat"], 
                                                                                 latlong_range["max_lat"]), 
                                                   HomesForSale.longitude.between(latlong_range["min_lng"], 
                                                                                  latlong_range["max_lng"])).all()
    homedata_in_range = [] # list of dictionaries for each home

    for home in home_for_sale_data:
        home_dict = { 
                      "lat": home.latitude,
                      "lng": home.longitude,
                      "mls_num": home.mls_num,
                      "street_adrs": home.street_adrs,
                      "city": home.city,
                      "state": home.state,
                      "zipcode": home.zipcode,
                      "price": home.price,
                      "property_type": home.property_type,
                      "neighborhood": home.neighborhood,
                      "year_built": home.year_built,
                      "sq_ft": home.sq_ft,
                      "price_per_sqft": home.price_per_sqft,
                      "lot_size": home.lot_size,
                      "num_bed": home.num_bed,
                      "num_bath": home.num_bath,
                      "days_on_market": home.days_on_market,
                      "hoa_per_month": home.hoa_per_month 
                    }

        homedata_in_range.append(home_dict)
    
    return homedata_in_range

def get_crimetype_chart_data(data):
    """Get data to display on chart on website"""
  # for each iteration, item =  {
     #  "lat": crime.address.latitude, 
     #  "lng": crime.address.longitude,
     #  "crime_type": Vandalism
     #  "case_num": crime.case_num,
     #  "description": crime.description,
     #  "date_time": crime.date_time.isoformat(),
     #  "police_beat": crime.beat
     # }

    crimetype_dict = {}

    # item is a dictionary b/c data is a list of dictionaries
    for item in data: 
        if item["crime_type"] in crimetype_dict:
            crimetype_dict[item["crime_type"]] += 1
        else:
            crimetype_dict[item["crime_type"]] = 1
            
    return crimetype_dict   

        

