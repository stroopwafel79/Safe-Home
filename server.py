"""Flask server to run my app on"""
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, url_for, jsonify)
from model import connect_to_db
from flask_debugtoolbar import DebugToolbarExtension
from module import (get_api_key, get_crimedata_by_latlong_range,
                    get_homedata_by_latlong_range,
                    get_crimetype_chart_data,
                    get_crimetype_chart_labels,
                    format_phone_num)
from pprint import pprint
import googlemaps
import random
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

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

    # crime_chart_data example {'Robbery': 13, 'Theft/Larceny': 86, 
    #                           'Motor Vehicle Theft': 20, 'Dui': 3, 
    #                           'Assault': 29, 'Vandalism': 25, 'Fraud': 3, 
    #                           'Disturbing The Peace': 3, 'Burglary': 10}
    crime_chart_data = get_crimetype_chart_data(crime_data)
    
    # get phone number from input and send text if exists
    phone_num = request.args.get("phone")
    if phone_num:
      send_sms(phone_num, crime_chart_data)
    # TODO use regex to check for valid phone number
      #((\(\d{3}\) ?)|(\d{3}-))?\d{3}-\d{4}
    
    return render_template(
                           "map.html",
                           gkey=get_api_key("GKEY"),
                           tkey=get_api_key("TKEY"),
                           t_auth_token=get_api_key("TAUTHTOKEN"),
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


#@app.route("/phone")
def send_sms(phone_num, data):
  """ 
  Send sms via Twilio to phone number. incoming data is in JSON format.
  """
  # Code from Twilio to send text
  ##################
  # TODO get data to send properly. It's truncating after first key
  account_sid = get_api_key("TKEY")
  auth_token = get_api_key("TAUTHTOKEN")
  client = Client(account_sid, auth_token)

  message = client.messages.create(
                                   from_='+14083594778',
                                   body=data,
                                   to=phone_num
                                  )
                                  

  print(message.sid)



@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    
    fact1 = "Oakland's Lake Merritt is a natural saltwater lake with its own Oak-ness Monster"
    fact2 = "Oakland is one of the most diverse cities in the US."
    fact3 = "One of Oakland’s most popular parks is a cemetery - Mountain View Cemetery"
    fact4 = "Disneyland was inspired by Oakland’s Fairyland."
    fact5 = "Oakland has its own redwoods - Redwood Regional Park"
    oak_facts = [fact1, fact2, fact3, fact4, fact5]

    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message(random.choice(oak_facts))

    return str(resp)

 

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

