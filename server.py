"""BLHA"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
				   session, url_for, jsonify)

from model import CrimeType, Crime, Address, connect_to_db, connect_to_db
from flask_debugtoolbar import DebugToolbarExtension
from os import environ # to access environ.get("zillow_key")
import requests
import zillow
from xmljson import BadgerFish
from xml.etree.ElementTree import fromstring
import json
from pprint import pprint

bf = BadgerFish(dict_type=dict)

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "12345"

# Normally, if you use an indefined variable in Jinja2, it fails
# silently. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_form():
	"""Show form on homepage for entering search criteria"""
	return render_template("homepage.html")



# @app.route('/results')
# def combine_results():
# 	"""Combine crimes and zillow data"""

# 	return show_crimes()

@app.route("/results")
def show_crimes():
	"""Show a list of crimes at that address"""

	# get the value of the input address from the form
	address = request.args.get("address")

	# query db, get Address object
	adrs_object = Address.query.filter_by(street_adrs=address.title()).first()
	# access address_id
	adrs_id = adrs_object.address_id
	# query db to get list of Crime objects with address_id
	# loop over this crimes_lst in jinja
	crimes_lst = Crime.query.filter_by(address_id=adrs_id).all()

	return render_template("address.html", 
						   address=address,
						   crimes_lst=crimes_lst)



# @app.route('/results')
# def get_zillow_data():
# 	"""Get info from zillow via api request"""

# 	# get secret key for zillow api
# 	key = environ.get("KEY")
	
# 	street_adrs = request.args.get("address").title()
	
# 	zipcode = request.args.get("zip")
# 	citystatezip = " ".join(["Oakland,", "CA", zipcode])

# 	url = "https://www.zillow.com/webservice/GetSearchResults.htm"
# 	payload = {
# 		"zws-id": key,
# 		"address": street_adrs,
# 		"citystatezip": citystatezip
# 	}

# 	# make a request to the api with the payload as parameters. Returns XML.
# 	data = requests.get(url, params=payload) # <class requests.models.Response>
	

# 	# turn the XML recieved into a dictionary
# 	data_dict = bf.data(fromstring(data.text)) # <class dict>
	
# 	# first key of data_dict
# 	key1 = "{http://www.zillow.com/static/xsd/SearchResults.xsd}searchresults"
# 	results = data_dict[key1]["response"]["results"]["result"][0]
# 	zestimate = results["zestimate"]["amount"]["$"]
	
# 	links = results["links"]
# 	home_details = links["homedetails"]["$"]
# 	map_home = links["mapthishome"]["$"]
	

# 	return render_template("zillow_data.html", 
# 						   zestimate=zestimate,
# 						   home_details=home_details,
# 						   map_home=map_home,
# 						   links=links)



######################################################################
if __name__ == '__main__':
	# We have to set debug=True here, since it has to be True at the
	# point that we invoke the DebugToolbarExtension
	app.debug = True
	# make sure templates, etc. are not cached in debug mode
	app.jinja_env.auto_reload = app.debug

	connect_to_db(app)

	# Use the DebugToolbar
	DebugToolbarExtension(app)

	app.run(port=5000, host='0.0.0.0')
