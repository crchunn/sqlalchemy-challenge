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
        f"/api/v1.0/starttoend"
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



@app.route("/api/v1.0/start")
def start():
    #start_date = (2015, 9, 23)
   # end_date = (2015, 9, 28)
    sel = [func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)]
    beginning_results = session.query(*sel).\
        filter(Measure.date >= dt.date(2015, 9, 23)).\
        filter(Measure.date <= dt.date(2015, 9, 30)).all()
    session.close()

    weather = list(np.ravel(beginning_results))
    return jsonify(weather)
        # filter(mean(Measure.tobs)).all()
    
 
   

@app.route("/api/v1.0/starttoend")
def starttoend():
    offtime = []
    sel = [func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)]
    offtime = (dt.date(2015, 10, 23))
    # offtime = [{func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs), dt.date(2015, 10, 23)}, 
        #   {func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs), dt.date(2015, 10, 24)}, 
            # {func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs), dt.date(2015, 10, 25)}, 
            # {func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs), dt.date(2015, 10, 26)}]  
                  
    end_results = session.query(*sel, Measure.date).all()
        # filter(Measure.date, sel).all()

    session.close()

    for date, tobs in end_results:
        Measure_dict = {}
        Measure_dict["date"] = date
        Measure_dict["tobs"] = tobs
        
        offtime.append(Measure_dict)

    

    allweather = list(np.ravel(end_results))

    return jsonify(allweather)

   


# =active = session.query(Measure.station, func.count(Measure.station))\
    # .group_by(Measure.station)\
    # .order_by(func.count(Measure.station).desc()).all()
    




if __name__ == '__main__':
    app.run(debug=True)