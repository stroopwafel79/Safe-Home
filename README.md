# HB_project
This app will take an address from the user and mark that as the center point on a map.
A query will be made to the postgreSQL database to get both details on the crimes committed
and homes for sale near the input address. Both crimes and homes for sale will be plotted on the
map and details about each can be accesses via clicking on the associated map marker. 

Filtering crimes by type and homes by sales price will be implemented if time permits.

The following is a list of important files and a description of their contents:

seed.py - contains the code for parsing and cleaning up both the crimes data (.tsv file) from
          Oakland's open data and the homes for sale data (.csv file) from Redfin.com. Running 
          this file will seed the database with the data provided in the specified files.
    
model.py - contains the datamodel for the postgreSQL database. Each class defines a table in the
           database and the associated column names and datatypes as well as any relationships between tables.
 
server.py - contains the flask routes for the webapp, the functions that are executed when the webpage is visited,
            as well as the HTML template to be rendered along with the date to be sent to the HTML template.
            Running this file, runs the server so the webapp is accessible.
            
module.py - contains all the helper functions that get called in the server.py file.


in the templates folder...

base.html - base file from with all other html files inherit from. This may no longer be needed as the number of
            html files used in the app has, thus far, been reduced to one.

map.html - this is the only html being used in the app. Currently, it also contains the JavaScript, will likely
           be separated into a .js file later.
           
All other files in the templates folder can be ignored

seed_data folder - contains data files used in seed.py
          
