from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

organizers = Blueprint('organizers', __name__)

# Get all vendors from the database
@organizers.route('/vendors', methods=['GET'])
def get_vendors():
  cursor = db.get_db().cursor()
  cursor.execute('SELECT name, vendorType FROM Vendor')

  column_headers = [x[0] for x in cursor.description]

  json_data = []
  theData = cursor.fetchall()
  
  for row in theData:
    json_data.append(dict(zip(column_headers, row)))
    
  return jsonify(json_data)

# Get all relevant details of a particular vendor from the database
@organizers.route('/vendors/<vendorID>', methods=['GET'])
def get_vendor_details(vendorID):
    query = 'SELECT name, email, phone, vendorType FROM Vendor WHERE vendorID = ' + str(vendorID)
    current_app.logger.info(query)
    cursor = db.get_db().cursor()
    cursor.execute(query)

    column_headers = [x[0] for x in cursor.description]

    json_data = []
    the_data = cursor.fetchall()

    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)

# Get all police departments assisting a specific race
@organizers.route('/police/<raceID>', methods=['GET'])
def get_police_department_names(raceID):
    query = '''
      SELECT p.name, p.phone
      FROM Police AS p
      JOIN Organizer_CommunicatesWith_Police AS o
      ON p.policeID = o.policeID
      JOIN EventOrganizer AS org
      ON o.organizerID = org.organizerID
      JOIN Race AS r
      ON org.organizerID = r.organizerID
      WHERE r.raceID = ''' + str(raceID)
    
    current_app.logger.info(query)
    cursor = db.get_db().cursor()
    cursor.execute(query)

    column_headers = [x[0] for x in cursor.description]

    json_data = []
    the_data = cursor.fetchall()

    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# Create a race post
@organizers.route('/races', methods=['POST'])
def event_organizer_creates_race():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    raceName = the_data['race_name']
    raceStreet = the_data['street']
    raceCity = the_data['city']
    raceState = the_data['state']
    raceCountry = the_data['country']
    raceZip = the_data['zip']
    raceDate = the_data['race_date']
    terrainType = the_data['terrain_type']
    raceLength = the_data['race_length']
    maxRunners = the_data['max_runners']
    checkInTime = the_data['check_in_time']
    organizerID = the_data['organizer_id']

    # Constructing the query
    query = 'insert into Race (name, street, city, state, country, zip, date, terrainType, raceLength, maxRunners, checkInTime, organizerID) values ("'
    query += raceName + '", "'
    query += raceStreet + '", "'
    query += raceCity + '", "'
    query += raceState + '", "'
    query += raceCountry + '", "'
    query += raceZip + '", "'
    query += str(raceDate) + '", "'
    query += terrainType + '", "'
    query += str(raceLength) + '", "'
    query += str(maxRunners) + '", "'
    query += str(checkInTime) + '", "'
    query += str(organizerID) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Successfully created a race post!'

# Update some of the details of a race
@organizers.route('/races/<raceID>', methods=['PUT'])
def update_race_post(raceID):
    
    the_data = request.json
    current_app.logger.info(the_data)
    
    newRaceDate = the_data['date']
    newMaxRunners = the_data['maxRunners']
    newCheckInTime = the_data['checkInTime']

    query = 'UPDATE Race SET '
    query += 'date = "' + str(newRaceDate) + '", '
    query += 'maxRunners = "' + str(newMaxRunners) + '", '
    query += 'checkInTime = "' + str(newCheckInTime) + '" '
    query += 'WHERE raceID = ' + str(raceID)

    current_app.logger.info(query)

    # executing and committing the update statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Successfully updated the race!'

# Delete a race post from the website if a race is no longer happening
@organizers.route('/races/<raceID>', methods=['DELETE'])
def delete_race_post(raceID):
    query = 'DELETE FROM Race WHERE raceID = ' + str(raceID) + ';'
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Successfully deleted a race post!'

# @organizers.route('/results/<raceID>/<runnerID>', methods=['GET'])
# def get_race_results_of_runner(raceID, runnerID):
#   query = '''
#   SELECT
#   r.firstName, r.lastName, rr.bibNumber, rr.finishTime, ms.marker, ms.mileSplit
#   FROM Runner AS r JOIN Runner_RunsIn_Race AS rrir ON r.runnerID = rrir.runnerID
#   JOIN Race As ra ON rrir.raceID = ra.raceID
#   JOIN RaceResults As rr ON ra.raceID = rr.raceID
#   JOIN MileSplits AS ms ON rr.raceID = ms.raceID
#   WHERE ra.raceID = ''' + str(raceID)
#   query += ' AND r.runnerID = ' + str(runnerID)
  
#   current_app.logger.info(query)
#   cursor = db.get_db().cursor()
#   cursor.execute(query)
#   column_headers = [x[0] for x in cursor.description]

#   json_data = []
#   the_data = cursor.fetchall()

#   for row in the_data:
#     json_data.append(dict(zip(column_headers, row)))
#   return jsonify(json_data)

# Upload race results of a specific runner
@organizers.route('/results', methods=['POST'])
def event_organizer_uploads_race_results():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    organizerID = the_data['organizer_id']
    raceID = the_data['race_id']
    runnerID = the_data['runner_id']
    bibNumber = the_data['bib_number']
    finishTime = the_data['finish_time']
    mileSplit1 = the_data['mile_split_1']
    mileSplit2 = the_data['mile_split_2']
    mileSplit3 = the_data['mile_split_3']
    mileSplit4 = the_data['mile_split_4']
    mileSplit5 = the_data['mile_split_5']

    # Constructing the first query (inserting into RaceResults table)
    query = 'INSERT INTO RaceResults (runnerID, bibNumber, finishTime, raceID, organizerID) values ("'
    query += str(runnerID) + '", "'
    query += str(bibNumber) + '", "'
    query += str(finishTime) + '", "'
    query += str(raceID) + '", "'
    query += str(organizerID) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    # Constructing the second query (inserting into MileSplits table)
    query2 = 'INSERT INTO MileSplits (runnerID, bibNumber, raceID, organizerID, marker, mileSplit) values ("'
    query2 += str(runnerID) + '", "'
    query2 += str(bibNumber) + '", "'
    query2 += str(raceID) + '", "'
    query2 += str(organizerID) + '", "Mile 5", "'
    query2 += str(mileSplit1) + '"), ("'
    query2 += str(runnerID) + '", "'
    query2 += str(bibNumber) + '", "'
    query2 += str(raceID) + '", "'
    query2 += str(organizerID) + '", "Mile 10", "'
    query2 += str(mileSplit2) + '"), ("'
    query2 += str(runnerID) + '", "'
    query2 += str(bibNumber) + '", "'
    query2 += str(raceID) + '", "'
    query2 += str(organizerID) + '", "Mile 13.1", "'
    query2 += str(mileSplit3) + '"), ("'
    query2 += str(runnerID) + '", "'
    query2 += str(bibNumber) + '", "'
    query2 += str(raceID) + '", "'
    query2 += str(organizerID) + '", "Mile 20", "'
    query2 += str(mileSplit4) + '"), ("'
    query2 += str(runnerID) + '", "'
    query2 += str(bibNumber) + '", "'
    query2 += str(raceID) + '", "'
    query2 += str(organizerID) + '", "Mile 25", "'
    query2 += str(mileSplit5) + '")'
    current_app.logger.info(query2)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query2)
    db.get_db().commit()
    
    return 'Successfuly uploaded race results for this runner!'