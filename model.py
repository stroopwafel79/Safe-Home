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
	lat_long
	
	def __repr__(self):
		"""Provide useful representation when printed"""

		return f"<Address: address_id={self.address_id} street_adrs={self.street_adrs}>"

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

	# Upon running the file every time:
	# First, delete the test table(start with a new slate)
	# Second, create the test database anew
	os.system("dropdb test")
	os.system("createdb test")	

	# Connect the Flask app to the database
	connect_to_db(app)

	# Will print when run interactively
	print("Connected to DB")

	# Make tables
	db.create_all()

	# Add crimetypes
	theft = CrimeType("Theft")
	robbery = CrimeType("Robbery")

	# Add crimes and associate them with crimetypes
	crime1 = Crime()  # instantiate the Crime object
	crime1.crime_type = theft  # set the crime_type instance attribute to the type specified above
	crime1.date_time = 2018-01-05 12:12:12
	crime1.beat = 11X
	crime1.case_num = 18-123344
	crime1.description = "Grand theft auto"
	crime2 = Crime()
	crime2.crime_type = robbery


	# Add addresses
	address1 = Address(street_adrs="123 Dover street")
	crime1.address = address1
	address2 = Address(street_adrs="1801 Shattuck Ave.")
	crime2.address = address2

	db.session.add(theft)
	db.session.add(robbery)
	db.session.add(crime1)
	db.session.add(crime2)
	db.session.add(address1)
	db.session.add(address2)
	db.session.commit()



