# Flask
from flask import Flask, jsonify

# Data Manipulation Related Dependencies
import numpy as np
import pandas as pd
import datetime as dt

# SQL Alchemy Related Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Dictionary of Routes
routes = [
    {'Precipitation': '/api/v1.0/precipitation'},
    {'Stations': '/api/v1.0/stations'},
    {'Temperatures': '/api/v1.0/tobs'},
    {'Temp Start': '/api/v1.0/<start>'},
    {'Temp Start and End': '/api/v1.0/<start>/<end>'}
    ]

# Flask Set Up
app = Flask(__name__)

# Home Page
@app.route('/')
def welcome():
    return(f'Welcome to the climate app!<br/>'
    f'Here are the possible routes:</br>'
    r'Welcome to the climate app!<br/>'
    r'Here are the possible routes:</br>'
    r'Precipitation: /api/v1.0/precipitation</br>'
    r'Stations: /api/v1.0/stations</br>'
    r'Temperatures: /api/v1.0/tobs</br>'        
    f'Temp Start: /api/v1.0/(enter start date yyyy-mm-dd)</br>'
    r'Temp Start and End: /api/v1.0/(enter start date yyyy-mm-dd)/(enter end date yyyy-mm-dd)</br>')

def set_up_connection():
    # Establish Connection
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    # Set Up Base
    Base = automap_base()
    # Reflect Tables
    Base.prepare(engine, reflect=True)
    # Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    # Set Up Session For Queries
    session = Session(engine)
    return engine, session, Measurement, Station

# Precipitation Route
@app.route('/api/v1.0/precipitation')
def precipitation():
    engine, session, Measurement, Station = set_up_connection()
    query_result = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    dates = []
    prcps = []
    for record in query_result:
        dates.append(record.date)
        prcps.append(record.prcp)
    response_dict = {'Date': dates, 'Prcp': prcps}
    return jsonify(response_dict)

# Station Route
@app.route('/api/v1.0/stations')
def stations():
    engine, session, Measurement, Station = set_up_connection()
    query_result = session.query(Measurement.station).distinct().all()
    stations = []
    for record in query_result:
        stations.append(record.station)
    response_list = stations
    return jsonify(response_list)

# Tobs Route
@app.route('/api/v1.0/tobs')
def tobs():
    engine, session, Measurement, Station = set_up_connection()
    # Calculate the date 1 year ago from the last data point in the database
    query_result = engine.execute('SELECT * FROM measurement ORDER BY measurement.date desc LIMIT 1').fetchall()
    last_date_in_data = query_result[0][2]
    start_date_of_query = dt.datetime.strptime(last_date_in_data, '%Y-%m-%d') - dt.timedelta(days=366)

    # Perform a query to retrieve the data and temp scores
    query_result = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.date >= start_date_of_query).order_by(Measurement.date).all()
    dates = []
    tobs = []
    for record in query_result:
        dates.append(record.date)
        tobs.append(record.tobs)
    response_dict = {'Date': dates, 'Tobs': tobs}
    return jsonify(response_dict)

# Start Date Route
@app.route('/api/v1.0/<start>')
def start_temps(start):
    engine, session, Measurement, Station = set_up_connection()
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all())

# Start Date + End Date Route Route
@app.route('/api/v1.0/<start>/<end>')
def start_end_temps(start, end):
    # return f'{start} and {end}'
    engine, session, Measurement, Station = set_up_connection()
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all())


if __name__ == '__main__':
    app.run(debug=True)