from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
    """Here are all the available API routes"""
    return (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/tobs"
        f"/api/v1.0/stations"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measure.prcp).all()

    session.close()

    precip = list(np.ravel(results))
    return jsonify(precip)


if __name__ == '__main__':
    app.run(debug=True)
