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

	url = "https://www.zillow.com/webservice/GetDeepSearchResults.htm"
	payload = {
		"zws-id": key,
		"address": address,
		"citystatezip": citystatezip,
		"rentzestimate": True
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
	comparables = links["comparables"]["$"]
	
	### for_sale may only exist in GetSearchResults and not GetDeepSearchResults
	#for_sale = results["localRealEstate"]["region"]["links"]["forSale"]["$"]
	num_baths = results["bathrooms"]["$"]
	num_beds = results["bedrooms"]["$"]
	sq_ft = results["finishedSqFt"]["$"]
	last_sold_date = results["lastSoldDate"]["$"]
	last_sold_price = results["lastSoldPrice"]["$"]
	year_built = results["yearBuilt"]["$"]
	rent_zestimate = results["rentzestimate"]["amount"]["$"]

	return {
			"zestimate": zestimate,
			"home_details_link": home_details,
			#"for_sale_link": for_sale,
			"comparables_link": comparables,
			"lat": latitude,
			"lng": longitude,
			"num_baths": num_baths,
			"num_beds": num_beds, 
			"sq_ft": sq_ft,
			"last_sold_date": last_sold_date,
			"last_sold_price": last_sold_price,
			"year_built": year_built,
			"rent_zestimate": rent_zestimate
			}


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
					  "latitude": home.latitude,
					  "longitude": home.longitude,
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
		

