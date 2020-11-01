import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all prcp values based on the date
    results = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()
    session.close()
    
    # Convert the query results to a dictionary using date as the key and prcp as the value
    prcp_date = []
    for date, prcp in results:
        prcp_date_dict = {}
        prcp_date_dict["date"] = date
        prcp_date_dict["prcp"] = prcp
        prcp_date.append(prcp_date_dict)
    
    # Return the JSON representation of the dictionary
    return jsonify(prcp_date)


@app.route('/api/v1.0/stations')
def stations():
    Session = Session(engine)
    results2 = session.query(Station.station, Station.name).all()
    session.close()

    # Return a JSON list of stations from the dataset
    station_list = []
    for station, name in results2:
        station_list_dict = {}
        station_list_dict["station"] = station
        station_list_dict["name"] = name
        station_list.append(station_list_dict)
    
    # Return the JSON representation of the dictionary
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    date = dt.datetime(2016, 8, 17)
    date2 = dt.datetime(2017, 8, 19)

    Session = Session(engine)
    results3 = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > date).filter(Measurement.date < date2).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()
    session.close()

    # Return a JSON list of stations from the dataset
    tobs_list = []
    for date, tobs in results3:
        tobs_list_dict = {}
        tobs_list_dict["date"] = date
        tobs_list_dict["tobs"] = tobs
        tobs_list.append(tobs_list_dict)
    
    # Return the JSON representation of the dictionary
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def Start(start):
    session = Session(engine)

    results4 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_date = []
    for date, min, avg, max in results4:
        start_date_dict = {}
        start_date_dict["date"] = date
        start_date_dict["TMIN"] = min
        start_date_dict["TAVG"] = avg
        start_date_dict["TMAX"] = max
        start_date.append(start_date_dict) 
    return jsonify(start_date)

@app.route("/api/v1.0/<start>/<end>")
def Start_end(start, end):
    session = Session(engine)

    results5 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_end_date = []
    for date, min, avg, max in results5:
        start_end_date_dict = {}
        start_end_date_dict["date"] = date
        start_end_date_dict["TMIN"] = min
        start_end_date_dict["TAVG"] = avg
        start_end_date_dict["TMAX"] = max
        start_end_date.append(start_end_date_dict) 
    return jsonify(start_end_date)

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
