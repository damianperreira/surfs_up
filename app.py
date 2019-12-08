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

# Setup flask
# define Flask app (Called "app")
app = Flask(__name__)


# Set up the database for the flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect database into our classes
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# create a variable for each of the classes
Measurements = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

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
    precipitation = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Stations Route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# Monthly obs route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurements.tobs).filter(Measurements.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# Statistics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats():
    sel = [func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)]
    if not end:
        results = session.query(*sel).filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
    results = session.query(*sel).\
           filter(Measurements.date >= start).\
     filter(Measurements.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

