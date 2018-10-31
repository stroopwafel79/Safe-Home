"""Module containing functions to assist in getting
   crime and zillow data"""

from model import CrimeType, Crime, Address
from os import environ # to access environ.get("zillow_key")
import requests
from pprint import pprint
from xmljson import BadgerFish
from xml.etree.ElementTree import fromstring
bf = BadgerFish(dict_type=dict)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy() 


def show_crimes(address):
	"""Show a list of crimes at that address"""

	# get the value of the input address from the form
	
	# query db, get Address object
	adrs_object = Address.query.filter_by(street_adrs=address).first()
	# access address_id
	adrs_id = adrs_object.address_id
	# query db to get list of Crime objects with address_id
	# loop over this crimes_lst in jinja
	crimes_lst = Crime.query.filter_by(address_id=adrs_id).all()
	return crimes_lst


def call_zillow(address, zipcode):
	"""Call zillow's api"""

	# get secret key for zillow api
	key = environ.get("KEY")

	# since only dealing with Oakland crime data, hardcode city and state
	# need to join it all to meet zillow api call requirements
	citystatezip = " ".join(["Oakland,", "CA", zipcode])

	url = "https://www.zillow.com/webservice/GetSearchResults.htm"
	payload = {
		"zws-id": key,
		"address": address,
		"citystatezip": citystatezip
	}

	# make a request to the api with the payload as parameters. Returns XML.
	response = requests.get(url, params=payload) # <class requests.models.Response>
	return response


def xml_to_dict(data):
	"""Turns an api response from XML to a dictionary"""
	data_dict = bf.data(fromstring(data.text)) # <class dict>
	return data_dict


def get_zillow_details(zillow_dict):
	"""Access detail zillow info from api call dictionary result"""
	key1 = "{http://www.zillow.com/static/xsd/SearchResults.xsd}searchresults"
	results = zillow_dict[key1]["response"]["results"]["result"][0]
	zestimate = results["zestimate"]["amount"]["$"]
	latitude = results["address"]["latitude"]["$"]
	longitude = results["address"]["longitude"]["$"]

	
	links = results["links"]
	home_details = links["homedetails"]["$"]
	map_home = links["mapthishome"]["$"]

	return (zestimate, home_details, map_home, latitude, longitude)

def get_gkey():
	"""Get the Google Maps API secret key"""

	gkey = environ.get("GKEY")
	return gkey

# def get_crimes():
# 	"""Query database for all crimes. Result is a list of Crime objects"""
# 	return Crime.query.all()

# def get_crime_latlong():
# 	"""Get the latitude and longitude coordinates of all reported crimes"""

# 	# will be a list of dictionaries that google maps wants
# 	locations = []
# 	# get a list of Crime objects
# 	crimes_lst = get_crimes()
# 	for crime in crimes_lst:
# 		lat = crime.address.latitude
# 		lng = crime.address.longitude
# 		# crime_type = crime.crime_type.crime_type
# 		# case_num = crime.case_num

# 		# create list of dictionaries
# 		loc_dict = {
# 					"lat": lat, 
# 				    "lng": lng 
# 				    # "crime_type": crime_type,  
# 				    # "case_num": case_num 
# 				    }

# 		locations.append(loc_dict)

# 	return locations

def get_latlong_range(input_lat, input_lng):
	"""Based on input lat and long, get a range of lat/longs to populate crimes
	only on viewable google maps window""" 

	# Based on lat/lng of input address, calculate the min and max
	# lat/lng for gmap view window
	max_lat = input_lat + 0.004
	min_lat = input_lat - 0.004
	max_lng = input_lng + 0.012
	min_lng = input_lng - 0.012

	# list of ohjects Address objects with lat/lng within specified range
	latlng_range = Address.query.filter(Address.latitude.between(min_lat, max_lat), 
											   Address.longitude.between(min_lng, max_lng)).all()

	# will be a list of dictionaries that google maps wants
	locations = []

	for item in latlng_range:
		lat = item.latitude
		lng = item.longitude

		# create list of dictionaries
		loc_dict = {
					"lat": lat, 
				    "lng": lng 
				    }

		locations.append(loc_dict)

	return locations


	# max_lat = 37.839535 + 0.004	
	# min_lat = 37.839535 - 0.004
	# max_lng = -122.2684415 + 0.006
	# min_lng = -122.2684415 - 0.006


