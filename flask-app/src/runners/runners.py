from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

def format_timedelta(td):
    # Calculate total seconds
    total_seconds = td.total_seconds()

    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format as HH:MM:SS
    formatted_time = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    return formatted_time

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

# Register runner for certain race
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

# Remove a runner's registration for a race
@runners.route('/runners/<raceID>/<runnerID>', methods=['DELETE'])
def unregister_runner_for_race(raceID, runnerID):
    cursor = db.get_db().cursor()
    query = 'DELETE FROM Runner_RegistersFor_Race WHERE raceID = %s AND runnerID = %s'
    cursor.execute(query, (raceID, runnerID))
    db.get_db().commit()
    
    return 'Success! Runner unregistered for the race.'

# Check if runner is checked in for certain race
@runners.route('/checkIns/<raceID>/<runnerID>', methods=['GET'])
def get_checkedin(raceID, runnerID):
    cursor = db.get_db().cursor()
    query = 'SELECT runnerID, raceID, bib_number FROM Runner_ChecksInto_Race WHERE raceID = %s AND runnerID = %s'
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

# Check in runner for certain race
@runners.route('/checkIns', methods=['POST'])
def checkin_runner_for_race():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    raceID = the_data['race_id']
    runnerID = the_data['runner_id']
    bibNumber = the_data['bib_number']

    # Constructing the query
    query = 'insert into Runner_ChecksInto_Race (runnerID, raceID, bib_number) values ("'
    query += runnerID + '", "'
    query += raceID + '", "'
    query += bibNumber + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Check result for a certain race
@runners.route('/results/<raceID>/<runnerID>', methods=['GET'])
def get_result(raceID, runnerID):
    cursor = db.get_db().cursor()
    query = 'SELECT finishTime FROM RaceResults WHERE raceID = %s AND runnerID = %s'
    cursor.execute(query, (raceID, runnerID))
    # row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        # Convert timedelta to string using the custom function
        formatted_time = format_timedelta(row[0])
        json_data.append({'finishTime': formatted_time})
        
    cursor = db.get_db().cursor()
    query = 'SELECT marker, mileSplit FROM MileSplits WHERE raceID = %s AND runnerID = %s'
    cursor.execute(query, (raceID, runnerID))
    # row_headers = [x[0] for x in cursor.description]
    theData = cursor.fetchall()
    for row in theData:
        marker_name = row[0]
        # Convert timedelta to string using the custom function
        formatted_time = format_timedelta(row[1])
        json_data.append({marker_name: formatted_time})
        
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Return a list of all races with basic information like its name,
# location (city and state), date, and race length
@runners.route('/races', methods=['GET'])

def get_races():
  cursor = db.get_db().cursor()
  cursor.execute('SELECT name, city, state, date, raceLength FROM Race')

  column_headers = [x[0] for x in cursor.description]

  json_data = []
  theData = cursor.fetchall()
  
  for row in theData:
    json_data.append(dict(zip(column_headers, row)))
    
  return jsonify(json_data)

# Return more specific information about a specific race
@runners.route('/races/<raceID>', methods=['GET'])

def get_specific_race(raceID):
  query = '''
    SELECT 
    r.name, r.street, r.city, r.state, r.country, r.zip, r.date, 
    r.terrainType, r.raceLength, r.maxRunners, r.checkInTime, o.name AS "hosted by:"
    FROM Race AS r JOIN EventOrganizer AS o
    ON r.organizerID = o.organizerID
    WHERE r.raceID = ''' + str(raceID)
  
  current_app.logger.info(query)
  cursor = db.get_db().cursor()
  cursor.execute(query)

  column_headers = [x[0] for x in cursor.description]

  json_data = []
  theData = cursor.fetchall()
  
  for row in theData:
    json_data.append(dict(zip(column_headers, row)))
    
  return jsonify(json_data)