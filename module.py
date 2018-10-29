"""Module containing functions to assist in getting
   crime and zillow data"""

from model import CrimeType, Crime, Address
from os import environ # to access environ.get("zillow_key")
import requests
from xmljson import BadgerFish
from xml.etree.ElementTree import fromstring
bf = BadgerFish(dict_type=dict)


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
	
	links = results["links"]
	home_details = links["homedetails"]["$"]
	map_home = links["mapthishome"]["$"]

	return (zestimate, home_details, map_home)
