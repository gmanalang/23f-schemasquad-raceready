from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


volunteers = Blueprint('volunteers', __name__)

# Get all the volunteers from the database
@volunteers.route('/volunteers', methods=['GET'])
def get_volunteers():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of volunteers
    cursor.execute('SELECT volunteerID FROM Volunteer')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# Get all the volunteers from the database
@volunteers.route('/registered/<raceID>', methods=['GET'])
def get_vols(raceID):
    # use cursor to query the database for a list of volunteers
    query = 'SELECT volunteerID FROM Volunteer_RegistersFor_Race WHERE raceID =' + str(raceID)
    current_app.logger.info(query)
    cursor = db.get_db().cursor()
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)