# import dependencies

import datetime as dt
import numpy as np
import pandas as pd

# SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# flask
from flask import Flask, jsonify

# Set up the database for the flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# create a variable for each of the classes
measurement = Base.classes.measurement
station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# Setup flask
# define Flask app (Called "app")
app = Flask(__name__)

# Create welcome route (root dir) (All routes should go after the app = Flask(__name__) line of code)
@app.route("/")

# add the precipitation, stations, tobs, and temp routes
def welcome():
	return(
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end<br/>"
	)

# Precipitation Route and function
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
#create a dictionary with the date as the key and the precipitation as the value
precip = {date: prcp for date, prcp in precipitation}
# Use jsonify() to format our results into a JSON structured file
return jsonify(precip)