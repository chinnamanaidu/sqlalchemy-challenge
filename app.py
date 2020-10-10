import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Create an engine that can talk to the database
database_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

#engine = create_engine("sqlite:///titanic.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

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
        f"/api/v1.0/start_date  date in yyyy-mm-dd format<br/>"
        f"/api/v1.0/start_date/end_date   date in yyyy-mm-dd format<br/>"
     )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    # Create a dictionary from the row data and append to a list of all_passengers
    all_dates = []
    
    for date, prcp in results:
        dates_dict = {}
        dates_dict["date"] = date
        dates_dict["prcp"] = prcp
        all_dates.append(dates_dict)

    # Convert list of tuples into normal list
    #all_dates = list(np.ravel(results))

    return jsonify(all_dates)
    


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(results))

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query( Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date > "2016-08-17").all()

    session.close()
    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for date, tobs in results:
        dates_tobs = {}
        dates_tobs["date"] = date
        dates_tobs["tobs"] = tobs
        all_tobs.append(dates_tobs)

    # Convert list of tuples into normal list
    #all_dates = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<startdt>")
def startDate(startdt):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    sel = [Measurement.station, 
       Station.name, 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.station == Station.station).\
        filter(Measurement.date > startdt ).\
        group_by(Measurement.station).\
        order_by(func.count(1).desc()).all()

    session.close()
    # Create a dictionary from the row data and append to a list of all_passengers
    all_temp = []
    for station, name, minTemp, maxTemp, avgTemp in results:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["name"] = name
        temp_dict["minTemp"] = minTemp
        temp_dict["maxTemp"] = maxTemp
        temp_dict["avgTemp"] = avgTemp
        all_temp.append(temp_dict)

    # Convert list of tuples into normal list
    #all_dates = list(np.ravel(results))

    return jsonify(all_temp)


@app.route("/api/v1.0/<startdt>/<enddt>")
def startEndDate(startdt, enddt):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    sel = [Measurement.station, 
       Station.name, 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.station == Station.station).\
        filter(Measurement.date > startdt ).\
        filter(Measurement.date < enddt ).\
        group_by(Measurement.station).\
        order_by(func.count(1).desc()).all()

    session.close()
    # Create a dictionary from the row data and append to a list of all_passengers
    all_temp = []
    for station, name, minTemp, maxTemp, avgTemp in results:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["name"] = name
        temp_dict["minTemp"] = minTemp
        temp_dict["maxTemp"] = maxTemp
        temp_dict["avgTemp"] = avgTemp
        all_temp.append(temp_dict)

    # Convert list of tuples into normal list
    #all_dates = list(np.ravel(results))

    return jsonify(all_temp)


if __name__ == '__main__':
    app.run(debug=True)
