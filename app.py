from flask import Flask, jsonify

import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Set up database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


#Launch Flask
app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"SQLAlchemy Homework<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    #Return date and precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').all()
       
    session.close()
    
    prcp_list = []
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict)

  
    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    #Return list of stations
    results = session.query(Station.station).all()

    session.close()
    
    station_list = list(np.ravel(results))
  
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #Return dates and temps
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > '2016-08-23').\
    filter(Measurement.station == 'USC00519281').all()

    session.close()

    tobs_list = []
    for date,tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temp"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start_date>")
def summary(start_date):
  
    session = Session(engine)

    tmin = session.query(func.min(Measurement.tobs).filter(Measurement.date >= start_date)).first()
    tmax = session.query(func.max(Measurement.tobs).filter(Measurement.date >= start_date)).first()
    tavg = session.query(func.avg(Measurement.tobs).filter(Measurement.date >= start_date)).first()

    session.close()

    temp_dict = {"min":tmin[0], "avg": tavg[0], "max":tmax[0]}

    return jsonify(temp_dict)

@app.route("/api/v1.0/<start_date>/<end_date>")
def between(start_date,end_date):
  
    session = Session(engine)

    tmin = session.query(func.min(Measurement.tobs).filter(Measurement.date >= start_date)).filter(Measurement.date <= end_date).first()
    tmax = session.query(func.max(Measurement.tobs).filter(Measurement.date >= start_date)).filter(Measurement.date <= end_date).first()
    tavg = session.query(func.avg(Measurement.tobs).filter(Measurement.date >= start_date)).filter(Measurement.date <= end_date).first()

    session.close()

    temp_dict = {"min":tmin[0], "avg": tavg[0], "max":tmax[0]}

    return jsonify(temp_dict)
   

if __name__ == "__main__":
    app.run(debug=True)