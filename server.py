"""BLHA"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
				   session, url_for)

from model import CrimeType, Crime, Address, connect_to_db, connect_to_db
from flask_debugtoolbar import DebugToolbarExtension

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

