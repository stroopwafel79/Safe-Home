"""Flask server to run my app on"""
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, url_for, jsonify)
from model import connect_to_db
from flask_debugtoolbar import DebugToolbarExtension
from module import (get_api_key, get_crimedata_by_latlong_range,
                    get_homedata_by_latlong_range,
                    get_crimetype_chart_data,
                    get_crimetype_chart_labels)
from pprint import pprint
import googlemaps

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
    address = " ".join([street_adrs, "Oakland, CA"])



    # create a google maps object
    gmaps = googlemaps.Client(key=get_api_key("GKEY"))

    # Geocoding an address
    geocode_result = gmaps.geocode(address)
    
    # get lat/lng (as float) of input address from geocode results
    input_lat = geocode_result[0]["geometry"]["location"]["lat"]
    input_lng = geocode_result[0]["geometry"]["location"]["lng"]

    crime_data = get_crimedata_by_latlong_range(input_lat, input_lng)
    crime_chart_data = get_crimetype_chart_data(crime_data)
    
    return render_template(
                           "map.html",
                           gkey=get_api_key("GKEY"),
                           tkey=get_api_key("TKEY"),
                           input_lat=input_lat,
                           input_lng=input_lng,
                           crime_data=crime_data,
                           chart_dict=get_crimetype_chart_labels(crime_chart_data),
                           homes_for_sale_data=get_homedata_by_latlong_range(input_lat, input_lng)
                           )

#####Fiddling with AJAX resume if there's time
# @app.route("/crime-chart.json")
# def get_crimetypes_data(crime_data): # how get crime data here?
#     """Take in crimedata filtered by lat/lng range, gleen info 
#        needed for table, and return dict in format for Chart.js"""
#     crime_chart_data = get_crimetype_chart_data(crime_data)
#     crime_chart_labels = get_crimetype_chart_labels(crime_chart_data)
#     chart_dict = make_chart_dict(crime_chart_data)

#     return jsonify(chart_dict)

# @app.route("/phone")
# def get_phone_number:
#   """ 
#   Get user's phone number if they click the link to get the 
#   info in the info widow texted to their phone
#   """
#   pass


######################################################################
if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    #DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
