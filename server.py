"""Flask server to run my app on"""
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
				   session, url_for, jsonify)
from model import connect_to_db
from flask_debugtoolbar import DebugToolbarExtension
from module import (get_gkey, get_crimedata_by_latlong_range,
					get_homedata_by_latlong_range)
from pprint import pprint

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
def get_gmap():
	""" 
		Get google map with centerpoint as input address 
		and crimes populated in view window
	"""
	#### I think the url will contain this info after the gmap call
	
	# get google map secret key for API call in JavaScript
	gkey = get_gkey();
 
	return render_template(
						   "map.html",
						   gkey=gkey,
						   # crime_data=get_crimedata_by_latlong_range(input_lat, input_lng),
						   # input_lat=input_lat,
						   # input_lng=input_lng,
						   # homes_for_sale_data=get_homedata_by_latlong_range(input_lat, input_lng)
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
