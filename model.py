"""Models and database functions for HB personal project"""

from flask_sqlalchemy import SQLAlchemy 

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can find
# the "session" object, where we do most of our interactions (committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class CrimeType(db.Model):
	"""Types of crimes by category"""

	__tablename__ = "crimetypes"

	crime_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	crime_type = db.Column(db.String(100), nullable=False)  # Ex: Theft, Robbery, etc.

	def __init__(self, crime_type):
		self.crime_type = crime_type

	def __repr__(self):
		"""Provide helpful representation when printed"""
		return f"<CrimeType: crime_type_id={self.crime_type_id} crime_type={self.crime_type}>"


class Address(db.Model):
	"""Address info including street address and latitude and longditude"""

	__tablename__ = "addresses"

	address_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	street_adrs = db.Column(db.String(200), nullable=False)
	latitude = db.Column(db.Float, nullable=False)
	longitude = db.Column(db.Float, nullable=False)
	
	def __repr__(self):
		"""Provide useful representation when printed"""
		return f"<Address: lat={self.latitude} lng={self.longitude} street_adrs={self.street_adrs}>"

class Crime(db.Model):
	"""Individual crime events"""

	__tablename__ = "crimes"

	crime_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	crime_type_id = db.Column(db.Integer, db.ForeignKey("crimetypes.crime_type_id"))
	address_id = db.Column(db.Integer, db.ForeignKey("addresses.address_id"))

	date_time = db.Column(db.DateTime, nullable=False)

	case_num = db.Column(db.String(25), nullable=False)
	description = db.Column(db.String(200), nullable=True)
	beat = db.Column(db.String(10), nullable=False)

	address = db.relationship("Address", backref="crimes")
	crime_type = db.relationship("CrimeType", backref="crimes")

	def __repr__(self):
		"""Provide useful representation when printed"""
		return f"<Crime: crime_id={self.crime_id} crime_type_id={self.crime_type_id} address_id={self.address_id}>"

### class created to spoof actual sales data. Will make it relational if I have time
class HomesForSale(db.Model):
	"""Homes for Sale"""
	__tablename__ = "sales"

	mls_num = db.Column(db.String(100), primary_key=True)
	street_adrs = db.Column(db.String(200), nullable=False)
	city = db.Column(db.String(200), nullable=False)
	state = db.Column(db.String(100), nullable=False)
	zipcode = db.Column(db.String(30), nullable=False)
	price = db.Column(db.String(100), nullable=False)
	#zestimate = db.Column(db.Integer, nullable=False)
	property_type = db.Column(db.String(200), nullable=False)
	neighborhood = db.Column(db.String(200), nullable=False)
	year_built = db.Column(db.String(15), nullable=False)
	sq_ft = db.Column(db.String(100), nullable=False)
	price_per_sqft = db.Column(db.String(100), nullable=False)
	lot_size = db.Column(db.String(100), nullable=False)
	num_bed = db.Column(db.String(10), nullable=True)
	num_bath = db.Column(db.String(10), nullable=False)
	days_on_market = db.Column(db.String(100), nullable=False)
	hoa_per_month = db.Column(db.String(50), nullable=True)
	# last_sold_date = db.Column(db.Date, nullable=False)
	# last_sold_price = db.Column(db.Date, nullable=False)
	latitude = db.Column(db.Float, nullable=False)
	longitude = db.Column(db.Float, nullable=False)

	def __repr__(self):
		"""Provide useful representation when printed"""
		return f"<ForSale: address={self.street_adrs}, price={self.price}>"


################################################################################
# Helper functions

def connect_to_db(app):
	"""Connect the database to our Flask app"""

	# Configure to use our PostgreSQL database
	app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///test"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.app = app
	db.init_app(app)

if __name__ == "__main__":
	# As a convenience, if we run this module interactiverly, it will leave
	# you in a state of being able to work with the database directly.
	import os
	from server import app

	# Connect the Flask app to the database
	connect_to_db(app)

	# Will print when run interactively
	print("Connected to DB")

	# Make tables
	db.create_all()


