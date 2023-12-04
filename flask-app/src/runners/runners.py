from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


runners = Blueprint('runners', __name__)

# Check if runner is registered for certain race
@runners.route('/runners/<raceID>/<runnerID>', methods=['GET'])
def get_registered(raceID, runnerID):
    cursor = db.get_db().cursor()
    query = 'SELECT runnerID, raceID FROM Runner_RegistersFor_Race WHERE raceID = %s AND runnerID = %s'
    cursor.execute(query, (raceID, runnerID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@runners.route('/runners', methods=['POST'])
def register_runner_for_race():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    raceID = the_data['race_id']
    runnerID = the_data['runner_id']

    # Constructing the query
    query = 'insert into Runner_RegistersFor_Race (runnerID, raceID) values ("'
    query += runnerID + '", "'
    query += raceID + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
