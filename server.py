"""Flask server to run my app on"""
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
				   session, url_for, jsonify)
from model import connect_to_db
from flask_debugtoolbar import DebugToolbarExtension
from module import (get_gkey, get_crimedata_by_latlong_range,
					get_homedata_by_latlong_range)
from pprint import pprint
import geocoder

from flask_sqlalchemy import SQLAlchemy 

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can find
# the "session" object, where we do most of our interactions (committing, etc.)

db = SQLAlchemy()


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "12345"

# Normally, if you use an indefined variable in Jinja2, it fails
# silently. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_homepage():
	""" Show the homepage"""

	return render_template("homepage.html")

@app.route("/map")
def get_gmap():
	""" 
		Get google map with centerpoint as input address 
		and crimes populated in view window
	"""
	# get the address from homepage input
	street_adrs = request.args.get("address")
	city = request.args.get("city")
	state = request.args.get("state")
	zipcode = request.args.get("zip")
	address = " ".join([street_adrs, city, state, zipcode])

	print("\nAAAAAAAAAA")
	print(address)
	# create a geocoder object with input address as argument
	##### can I set Oakland, CA here?
	g = geocoder.google(address)
	print("\n GGGGGGGGGGGG")
	pprint(g)

	# get google map secret key for API call in JavaScript
	gkey = get_gkey();

	# These are hardcoded for now until I figure out how to get them from google's 
	# geocoder in map.html
	input_lat = 37.839535
	input_lng = -122.2684415
 
	return render_template(
						   "map.html",
						   gkey=gkey,
						   crime_data=get_crimedata_by_latlong_range(input_lat, input_lng),
						   homes_for_sale_data=get_homedata_by_latlong_range(input_lat, input_lng)
	 					   )

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
