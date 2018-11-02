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

def get_crimedata_by_latlong_range(input_lat, input_lng):
	"""Based on input lat and long, get a range of lat/longs to populate crimes
	only on viewable google maps window""" 

	# Based on lat/lng of input address, calculate the min and max
	# lat/lng for gmap view window
	max_lat = input_lat + 0.004
	min_lat = input_lat - 0.004
	max_lng = input_lng + 0.012
	min_lng = input_lng - 0.012

	# list of ohjects Address objects with lat/lng within specified range
	# latlng_range = Address.query.filter(Address.latitude.between(min_lat, max_lat), 
	# 										   Address.longitude.between(min_lng, max_lng)).all()
	
	# crime data at addresses within range specified by input address
	# # 
	# crime_data_range_query = db.session.query(Crime.address.latitude, 
	# 									Crime.address.longitude,
	# 									CrimeType.crime_type, 
	# 								    Crime.date_time, 
	# 							        Crime.case_num).join(Crime).filter(Crime.address.latitude.between(min_lat, max_lat), 
	# 								  	 Crime.address.longitude.between(min_lng, max_lng)).all()

	# 	SELECT crimetypes.crime_type, crimes.date_time, crimes.case_num, crimes.description
	# 	FROM crimetypes
	# 	JOIN crimes ON crimetypes.crime_type_id = crimes.crime_type_id 
	# 	JOIN addresses ON crimes.address_id = addresses.address_id
	# 	WHERE addresses.latitude = loc['lat'] AND addresses.longitude = loc['lng']







	# cromes = Address.query.options(db.joinedload('crimes')).filter(Address.latitude.between(min_lat, max_lat), Address.longitude.between(min_lng, max_lng)).all()



	# crime_data_range_query = db.session.query(Address.latitude, 
	# 									Address.longitude,
	# 									CrimeType.crime_type, 
	# 								    Crime.date_time, 
	# 							        Crime.case_num).join(Crime).join(Address)
	# 									.filter(Address.latitude.between(min_lat, max_lat), 
	# 									Address.longitude.between(min_lng, max_lng)).all()

	# crime_data_range_query = db.session.query(CrimeType.crime_type, 
	# 								    Crime.date_time, 
	# 							        Crime.case_num).join(Crime).join(Address)
	# 									.filter(Address.latitude.between(min_lat, max_lat), 
	# 									Address.longitude.between(min_lng, max_lng)).all()

	crime_addresses = Address.query.options(db.joinedload('crimes').joinedload('crime_type')).filter(Address.latitude.between(min_lat, max_lat), Address.longitude.between(min_lng, max_lng)).all()
	# test cases
	# max_lat = 37.83918 + 0.004
	# min_lat = 37.83918 - 0.004

	# max_lng = -122.267245 - 0.006
	# min_lng = -122.267245 + 0.006

	#crime = Crime.query.options(db.joinedload('address')).filter(Crime.address.latitude.between(min_lat, max_lat), Crime.address.longitude.between(min_lng, max_lng)).all()
	# # will be a list of dictionaries that google maps wants
	crimedata_in_range = []

	for address in crime_addresses:
		for crime in address.crimes:
			lat = crime.address.latitude
			lng = crime.address.longitude
			ctype = crime.crime_type.crime_type
			case_num = crime.case_num
			desc = crime.description
			date_time = crime.date_time.isoformat()
			beat = crime.beat

			crime_dict = {
						  "lat": lat, 
				    	  "lng": lng,
				    	  "crime_type": ctype,
				    	  "case_num": case_num,
				    	  "description": desc,
				    	  "date_time": date_time,
				    	  "police_beat": beat
						}

			crimedata_in_range.append(crime_dict)

	return crimedata_in_range


	# max_lat = 37.839535 + 0.004	
	# min_lat = 37.839535 - 0.004
	# max_lng = -122.2684415 + 0.006
	# min_lng = -122.2684415 - 0.006

	# get crime data per location within the range
	# loop over locations list and query db for crime data
	# for loc in locations:
	# 	# query db for crime_type, datetime, case_num where
	# # 	# lat/lng == location
	# crime_data = db.session.query(CrimeType.crime_type, Crime.date_time, Crime.case_num)
	# .join(Crime).join(Address).filter(Address.latitude == 37.83918, Address.longitude == -122.267245).all()
		
	#[('Assault', datetime.datetime(2018, 8, 17, 7, 30), '18-041355'), ('Motor Vehicle Theft', datetime.datetime(2018, 9, 19, 5, 30), '18-048754')]# # SQL version of above query
		# SELECT crimetypes.crime_type, crimes.date_time, crimes.case_num, crimes.description
		# FROM crimetypes
		# JOIN crimes ON crimetypes.crime_type_id = crimes.crime_type_id 
		# JOIN addresses ON crimes.address_id = addresses.address_id
		# WHERE addresses.latitude = loc['lat'] AND addresses.longitude = loc['lng']


