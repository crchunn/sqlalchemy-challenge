from flask import Flask, jsonify
import numpy as np
from scipy import stats

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measure = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")

def home():
    "Hawaii Surf's Up!"
    """Here are all the available API routes"""
    return (
        "Hawaii Surf's Up!<br/>"
        "Here are all the available API Routes!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    previous_year = (dt.date(2017, 8, 23) - dt.timedelta(days=365))
    results = session.query(Measure.date, Measure.prcp).\
        filter(Measure.date >= previous_year).all()
    precip = {date: prcp for date, prcp in results}

    session.close() 

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.name).all()

    session.close()

    all_stations = list(np.ravel(stations))
    return jsonify(all_stations)




@app.route("/api/v1.0/tobs")
def tobs():
    tobresults = session.query(Measure.date, Measure.tobs).all()

    session.close()

    temps = list(np.ravel(tobresults))
    return jsonify(temps)



@app.route("/api/v1.0/<start>")
def start(start):
    #start_date = (2015, 9, 23)
   # end_date = (2015, 9, 28)
    sel = [func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)]
    beginning_results = session.query(*sel).\
        filter(Measure.date >= start).all()

    session.close()

    weather = list(np.ravel(beginning_results))
    return jsonify(weather)
        # filter(mean(Measure.tobs)).all()
    
 
   

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    end_results =  session.query(func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).\
        filter(Measure.date >= start).filter(Measure.date <= end).all()
                  
    # end_results = session.query(*sel, Measure.date).all()
        # filter(Measure.date, sel).all()

    session.close()


    allweather = list(np.ravel(end_results))

    return jsonify(allweather)

   


# =active = session.query(Measure.station, func.count(Measure.station))\
    # .group_by(Measure.station)\
    # .order_by(func.count(Measure.station).desc()).all()
    




if __name__ == '__main__':
    app.run(debug=True)