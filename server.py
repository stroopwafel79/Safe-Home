"""BLHA"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
				   session, url_for)

from model import CrimeType, Crime, Address, connect_to_db, connect_to_db
from flask_debugtoolbar import DebugToolbarExtension
from os import environ # to access environ.get("zillow_key")
import requests
import zillow

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

@app.route('/results')
def show_crimes():
	"""Show a list of crimes at that address"""

	# get the value of the input address from the form
	# address = request.args.get("address")

	# # query db, get Address object
	# adrs_object = Address.query.filter_by(street_adrs=address.title()).first()
	# # access address_id
	# adrs_id = adrs_object.address_id
	# # query db to get list of Crime objects with address_id
	# # loop over this crimes_lst in jinja
	# crimes_lst = Crime.query.filter_by(address_id=adrs_id).all()

	# return render_template("address.html", 
	# 					   address=address,
	# 					   crimes_lst=crimes_lst)


@app.route("/results")
def show_zillow():
	"""Show data from zillow based on input address"""

	# get secret key for zillow api
	key = environ.get("zillow_key") 

	api = zillow.ValuationApi()

	street_adrs = request.args.get("address")
	address = " ".join([street_adrs, "Oakland,", "CA"])
	zipcode = request.args.get("zip")

	data = api.GetSearchResults(key, address, zipcode)
	payload = {
		"key": key,
		"address": address,
		"zipcode": zipcode
	}

	return render_template("results.html", data=data)



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
