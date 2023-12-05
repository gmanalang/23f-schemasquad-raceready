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
      SELECT p.Name, p.phone
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


# # Getting a sponsor's promotional post for a race post
# @organizers.route('/races/<raceID>/<sponsorID>', methods=['GET'])
# def get_post_content(raceID, sponsorID):
#     cursor = db.get_db().cursor()
#     query = '''
#         SELECT title, content
#         FROM Post
#     '''
#     cursor.execute(query)
#     row_headers = [x[0] for x in cursor.description]
#     json_data = []
#     theData = cursor.fetchall()
#     for row in theData:
#         json_data.append(dict(zip(row_headers, row)))
#     the_response = make_response(jsonify(json_data))
#     the_response.status_code = 200
#     the_response.mimetype = 'application/json'
#     return the_response

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
    
    return 'Success!'

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

    # executing and committing the insert statement 
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
    
    return 'Success! Race post deleted.'
