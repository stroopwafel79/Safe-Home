"""Flask server to run my app on"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
				   session, url_for, jsonify)
from model import connect_to_db
from flask_debugtoolbar import DebugToolbarExtension
from module import (show_crimes, call_zillow, xml_to_dict,
					get_zillow_details)


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


@app.route("/results")
def get_form_data():
	"""Get data from the form and store it in a tuple"""
	street_adrs = request.args.get("address").title()
	
	zipcode = request.args.get("zip")

	# get crime data
	crimes_lst = show_crimes(street_adrs)

	# get zillow data
	zillow_resp = call_zillow(street_adrs, zipcode)
	zillow_dict = xml_to_dict(zillow_resp)

	zillow_tup = get_zillow_details(zillow_dict)
	zestimate = zillow_tup[0]
	home_details = zillow_tup[1]
	map_home = zillow_tup[2]

	return render_template("results.html", 
						   zestimate=zestimate,
						   home_details=home_details,
						   map_home=map_home,
						   street_adrs=street_adrs,
						   crimes_lst = crimes_lst)

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
