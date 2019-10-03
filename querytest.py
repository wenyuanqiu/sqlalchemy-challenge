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

# Precipitation Route
query_result = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
dates = []
prcps = []
for record in query_result:
    dates.append(record.date)
    prcps.append(record.prcp)
response_dict = {'Date': dates, 'Prcp': prcps}

# Stations
query_result = session.query(Measurement.station).distinct().all()
stations = []
for record in query_result:
    stations.append(record.station)

# Tobs
# Calculate the date 1 year ago from the last data point in the database
query_result = engine.execute('SELECT * FROM measurement ORDER BY measurement.date desc LIMIT 1').fetchall()
last_date_in_data = query_result[0][2]
start_date_of_query = dt.datetime.strptime(last_date_in_data, '%Y-%m-%d') - dt.timedelta(days=366)

# Perform a query to retrieve the data and precipitation scores
query_result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date_of_query).order_by(Measurement.date).all()
dates = []
prcps = []
for record in query_result:
    dates.append(record.date)
    prcps.append(record.prcp)
response_dict = {'Date': dates, 'Prcp': prcps}


# Start Date
start_date = '2012-01-01'
session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()