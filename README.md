# Safe@Home
This app will take an address from the user and mark that as the center point on a map.
A query will be made to the postgreSQL database to get both details on the crimes committed
and homes for sale in a predefined area around the input address. Both crimes and homes for 
sale will be plotted on the same Google map.  Clicking on each map marker will open an info
window with the details of the crime or house for sale at that location. Crimes can be filtered
by type and homes for sale can be filtered by price. 

The following is a list of important files and a description of their contents:

seed.py - contains the code for parsing and cleaning up both the crimes data (.tsv file) from
          Oakland's open data and the homes for sale data (.csv file) from Redfin.com. Running 
          this file will seed the database with the data provided in the specified files.
    
model.py - contains the data model for the postgreSQL database. Each class defines a table in the
           database and the associated column names and datatypes as well as any relationships between tables.
 
server.py - contains the flask routes for the webapp, the functions that are executed when the webpage is visited,
            as well as the HTML template to be rendered along with the data to be sent to the HTML template.
            Running this file, runs the server so the webapp is accessible.
            
module.py - contains all the helper functions that get called in the server.py file.


In the templates folder...

base.html - base file from with all other html files inherit from. 

homepage.html - contains content to be displayed on the homepage

map.html - contains content to be displayed on the map. Currently, it also contains all the JavaScript. Will
           be separated into a .js file later.
           
All other files in the templates folder can be ignored

seed_data folder - contains data files used in seed.py

static folder - contains style.css file and image files used in the app.
          
