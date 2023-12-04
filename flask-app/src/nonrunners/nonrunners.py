from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


nonrunners = Blueprint('nonrunners', __name__)

# Get all the volunteers from the database
@nonrunners.route('/volunteers', methods=['GET'])
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

# Get all the volunteers for a particular race from the database
@nonrunners.route('/registered/<raceID>', methods=['GET'])
def get_vols_from_race(raceID):
    # use cursor to query the database for a list of volunteers
    query = '''
    SELECT vol.firstName, vol.lastName, vol.volunteerID
    FROM Volunteer_RegistersFor_Race
    JOIN Volunteer AS vol
    ON Volunteer_RegistersFor_Race.volunteerID = vol.volunteerID
    WHERE raceID = 
    ''' + str(raceID)

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


# Get contact info for a particular volunteer from a particular race from the database
@nonrunners.route('/contactvol/<raceID>/<volunteerID>', methods=['GET'])
def get_contact_of_vol(raceID, volunteerID):
    # use cursor to query the database for a list of volunteers
    query = '''
    SELECT vol.firstName, vol.lastName, vol.phone, vol.email
    FROM Volunteer_RegistersFor_Race
    JOIN Volunteer AS vol
    ON Volunteer_RegistersFor_Race.volunteerID = vol.volunteerID
    WHERE raceID = ''' + str(raceID) + ''' AND
    vol.volunteerID = ''' + str(volunteerID)

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

# Get all volunteer stations from a particular race from the database
@nonrunners.route('/volstations/<raceID>', methods=['GET'])
def get_all_vol_stations(raceID):
    # use cursor to query the database for a list of volunteers
    query = '''
    SELECT stationID, venueSpot, services
    FROM FirstAidStation
    WHERE raceID = ''' + str(raceID) + '''

     UNION ALL

    SELECT stationID, venueSpot, amenities
    FROM RefuelStation
    WHERE raceID = ''' + str(raceID)

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


# Get all stations for a particular volunteer from a particular race from the database
@nonrunners.route('/volstations/<raceID>/<volunteerID>', methods=['GET'])
def get_vol_stations(raceID, volunteerID):
    # use cursor to query the database for a list of volunteers
    query = '''
    SELECT v.stationID, venueSpot, services
    FROM FirstAidStation AS f
    JOIN Volunteer_VolunteersFor_FirstAidStation AS v
    ON f.stationID = v.stationID
    WHERE v.raceID = %s AND v.volunteerID = %s

    UNION ALL

    SELECT v.stationID, venueSpot, amenities
    FROM RefuelStation AS r
    JOIN Volunteer_VolunteersFor_RefuelStation AS v
    ON r.stationID = v.stationID
    WHERE v.raceID = %s AND v.volunteerID = %s;
    '''

    cursor = db.get_db().cursor()
    # Execute the query with the provided parameters
    cursor.execute(query, (raceID, volunteerID, raceID, volunteerID))

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

@nonrunners.route('/firstaid', methods=['POST'])
def assign_new_firstaid_station():
    # Collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the variables
    vol = the_data['volunteerID']
    station = the_data['stationID']
    race = the_data['raceID']

    # Constructing the query
    query = 'INSERT INTO Volunteer_VolunteersFor_FirstAidStation VALUES ("'
    query += str(vol) + '", "'
    query += str(station) + '", "'
    query += str(race) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Return venue spot of a sponsor's promotional table at a race
@nonrunners.route('/stations/<raceID>/<sponsorID>', methods=['GET'])
def get_stations(raceID, sponsorID):
    cursor = db.get_db().cursor()
    cursor.execute('select raceID, sponsorID from Sponsor_Sponsors_Race')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#How to use raceID here to specify race? Is that even needed?
@nonrunners.route('/races/<raceID>/<organizerID>', methods=['GET'])
def get_contact_info(raceID, organizerID):
    cursor = db.get_db().cursor()
    query = '''
        SELECT name, email, phone
        FROM EventOrganizer
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Posting, updating, and deleting a sponsor's promotional post
@nonrunners.route('/races/<raceID>/<sponsorID>', methods=['POST'])
def create_post(raceID, sponsorID):
    cursor = db.get_db().cursor()
    query = '''
        INSERT INTO Post (title, content)
        VALUES (?, ?)
    '''
    cursor.execute(query, (request.json['title'], request.json['content']))
    db.get_db().commit()
    the_response = make_response(jsonify({'status': 'success'}))
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response

@nonrunners.route('/races/<raceID>/<sponsorID>', methods=['PUT'])
def update_post(raceID, sponsorID):
    cursor = db.get_db().cursor()
    query = '''
        UPDATE Post
        SET title = ?, content = ?
        WHERE id = postID
    '''
    cursor.execute(query, (request.json['title'], request.json['content'], request.json['id']))
    db.get_db().commit()
    the_response = make_response(jsonify({'status': 'success'}))
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response

@nonrunners.route('/races/<raceID>/<sponsorID>', methods=['DELETE'])
def delete_post(raceID, sponsorID):
    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM Post
        WHERE id = postID
    '''
    cursor.execute(query, (request.json['id'],))
    db.get_db().commit()
    the_response = make_response(jsonify({'status': 'success'}))
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response