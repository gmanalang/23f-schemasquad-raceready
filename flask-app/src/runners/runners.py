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
@runners.route('/registrations/<raceID>/<runnerID>', methods=['GET'])
def get_registered(raceID, runnerID):
    cursor = db.get_db().cursor()
    query = 'SELECT runnerID, raceID FROM Runner_RegistersFor_Race WHERE raceID = %s AND runnerID = %s'
    cursor.execute(query, (raceID, runnerID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
        
    if not json_data:
        # If json_data is empty, return an error response
        error_response = make_response(jsonify({"error": "Runner not registered for the specified race"}))
        error_response.status_code = 418  # You can choose an appropriate status code
        error_response.mimetype = 'application/json'
        return error_response
    
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Register runner for certain race
@runners.route('/registrations', methods=['POST'])
def register_runner_for_race():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    raceID = str(the_data['race_id'])
    runnerID = str(the_data['runner_id'])

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

# get all the registered races by runner
@runners.route('/registrations/<runnerID>', methods=['GET'])
def get_registered_races(runnerID):
    cursor = db.get_db().cursor()
    query = 'SELECT Race.* from Runner_RegistersFor_Race JOIN Race on Runner_RegistersFor_Race.raceID = Race.raceID WHERE Runner_RegistersFor_Race.runnerID = %s;'
    cursor.execute(query, (runnerID))
    db.get_db().commit()
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Remove a runner's registration for a race
@runners.route('/registrations/<raceID>/<runnerID>', methods=['DELETE'])
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

# Get a runner's profile details
@runners.route('/profiles/<runnerID>', methods=['GET'])
def get_profile(runnerID):
    cursor = db.get_db().cursor()
    query = 'SELECT firstName, lastName, gender, age, email, phone, street, city, state, country, zip FROM Runner WHERE runnerID = %s'
    cursor.execute(query, (runnerID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response 

# Update a runner's profile details
@runners.route('/profiles/<runnerID>', methods=['PUT'])
def update_profile(runnerID):
    the_data = request.json
    current_app.logger.info(the_data)

    firstName = the_data['first_name']
    lastName = the_data['last_name']
    
    the_query = 'UPDATE Runner SET '
    the_query += 'firstName = "' + firstName + '", '
    the_query += 'lastName = "' + lastName + '" '
    the_query += 'WHERE runnerID = {0};'.format(runnerID)

    current_app.logger.info(the_query)
    
    cursor = db.get_db().cursor()
    cursor.execute(the_query)
    db.get_db().commit()

    return "successfully editted runner #{0}!".format(runnerID)

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
        
    if not json_data:
        # If json_data is empty, return an error response
        error_response = make_response(jsonify({"error": "Runner did not run for the specified race"}))
        error_response.status_code = 418  # You can choose an appropriate status code
        error_response.mimetype = 'application/json'
        return error_response
        
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Return a list of all races with basic information like its name,
# location (city and state), date, and race length
@runners.route('/races', methods=['GET'])

def get_races():
  query = '''
  SELECT
  r.name, r.street, r.city, r.state, r.country, r.zip, r.date,
  r.terrainType, r.raceLength, r.maxRunners, r.checkInTime, r.raceID,
  o.name AS "hosted by", o.email, o.phone
  FROM Race AS r JOIN EventOrganizer AS o ON r.organizerID = o.organizerID
  '''
  current_app.logger.info(query)
  cursor = db.get_db().cursor()
  cursor.execute(query)

  column_headers = [x[0] for x in cursor.description]

  json_data = []
  theData = cursor.fetchall()
  
  for row in theData:
    json_data.append(dict(zip(column_headers, row)))
    
  return jsonify(json_data)

# Return more specific information about a specific race, including its
# amenities and its event organizer (with contact information)
@runners.route('/races/<raceID>', methods=['GET'])

def get_specific_race(raceID):
  query = '''
  SELECT
  r.name, r.street, r.city, r.state, r.country, r.zip, r.date, 
  r.terrainType, r.raceLength, r.maxRunners, r.checkInTime,
  o.name AS "hosted by", o.email, o.phone, fa.services, fa.venueSpot AS "first-aid venue spot",
  rs.amenities, rs.venueSpot AS "refuel station venue spot"
  FROM Race AS r JOIN EventOrganizer AS o ON r.organizerID = o.organizerID
  JOIN FirstAidStation AS fa ON r.raceID = fa.raceID
  JOIN RefuelStation AS rs ON r.raceID = rs.raceID
  WHERE r.raceID = ''' + str(raceID)
  
  current_app.logger.info(query)
  cursor = db.get_db().cursor()
  cursor.execute(query)

  column_headers = [x[0] for x in cursor.description]

  json_data = []
  theData = cursor.fetchall()
  
  for row in theData:
    json_data.append(dict(zip(column_headers, row)))

    if not json_data:
        # If json_data is empty, return an error response
        error_response = make_response(jsonify({"error": "Runner not registered for the specified race"}))
        error_response.status_code = 418  # You can choose an appropriate status code
        error_response.mimetype = 'application/json'
        return error_response
    
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response