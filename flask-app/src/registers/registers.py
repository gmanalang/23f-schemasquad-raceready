from flask import Blueprint, request, jsonify, make_response
import json
from src import db


registers = Blueprint('registers', __name__)

# Get all registers from the DB
@registers.route('/registers/<raceID>/<runnerID>', methods=['GET'])
def get_registers(raceID, runnerID):
    cursor = db.get_db().cursor()
    cursor.execute('select runnerID, raceID from Runner_RegistersFor_Race')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get customer detail for customer with particular userID
@registers.route('/registers/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from registers where id = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response