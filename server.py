"""Flask server to run my app on"""
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
				   session, url_for, jsonify)
from model import connect_to_db
from flask_debugtoolbar import DebugToolbarExtension
from module import (show_crimes, call_zillow, xml_to_dict,
					get_zillow_details, get_gkey,
					get_crimedata_by_latlong_range)
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


@app.route('/')
def show_form():
	"""Show form on homepage for entering search criteria"""
	return render_template("homepage.html")


# @app.route("/results")
# def get_form_data():
# 	"""Get data from the form and store it in a tuple"""
# 	# print("\nLLLLLLLLLLLLL")
# 	# pprint(get_crime_latlong())
# 	# print(type(get_crime_latlong()))

# 	street_adrs = request.args.get("address").title()
	
# 	zipcode = request.args.get("zip")

# 	# # get crime data
# 	# crimes_lst = show_crimes(street_adrs)

# 	# get zillow data
# 	zillow_resp = call_zillow(street_adrs, zipcode)
# 	zillow_dict = xml_to_dict(zillow_resp)
# 	zillow_data = get_zillow_details(zillow_dict)
# 	zestimate = zillow_data[0]
# 	home_details = zillow_data[1]
# 	map_home = zillow_data[2]
# 	latitude = zillow_data[-2]
# 	longitude = zillow_data[-1]

# 	return render_template("results.html", 
# 						   zestimate=zestimate,
# 						   home_details=home_details,
# 						   map_home=map_home,
# 						   street_adrs=street_adrs,
# 						   #crimes_lst=crimes_lst,
# 						   latitude=latitude,
# 						   longitude=longitude
# 						   )

@app.route("/map")
def get_gmap():
	"""Get google map with centerpoint as input address and crimes populated in view window"""

	# get street address and zipcode from input on homepage
	street_adrs = request.args.get("address").title()
	zipcode = request.args.get("zip")

	# get zillow data
	zillow_resp = call_zillow(street_adrs, zipcode) # (api call in python)
	zillow_dict = xml_to_dict(zillow_resp)
	zillow_data = get_zillow_details(zillow_dict)
	zestimate = zillow_data[0]
	home_details = zillow_data[1]
	map_home = zillow_data[2]
	input_lat = zillow_data[-2]
	input_lng = zillow_data[-1]
	crime_data=get_crimedata_by_latlong_range(input_lat, input_lng)
	print("\nCCCCCCCCCCCCCCCCC")
	pprint(crime_data)
	# get google map secret key for API call in JavaScript
	gkey = get_gkey();

	# get crime data per location within the range
	# loop over locations list and query db for crime data
	# for loc in locations:
	# 	# query db for crime_type, datetime, case_num where
	# # 	# lat/lng == location
	#crime_data = db.session.query(CrimeType.crime_type, Crime.date_time, Crime.case_num).join(Crime).join(Address).filter(Address.latitude == 37.83918, Address.longitude == -122.267245).all()
		
	#[('Assault', datetime.datetime(2018, 8, 17, 7, 30), '18-041355'), ('Motor Vehicle Theft', datetime.datetime(2018, 9, 19, 5, 30), '18-048754')]# # SQL version of above query
		# SELECT crimetypes.crime_type, crimes.date_time, crimes.case_num, crimes.description
		# FROM crimetypes
		# JOIN crimes ON crimetypes.crime_type_id = crimes.crime_type_id 
		# JOIN addresses ON crimes.address_id = addresses.address_id
		# WHERE addresses.latitude = loc['lat'] AND addresses.longitude = loc['lng']

 
	return render_template(
						   "map.html",
						   gkey=gkey,
						   crime_data=get_crimedata_by_latlong_range(input_lat, input_lng),
						   input_lat=input_lat,
						   input_lng=input_lng
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
