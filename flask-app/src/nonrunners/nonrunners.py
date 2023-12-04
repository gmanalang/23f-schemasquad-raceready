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
def get_vols(raceID):
    # use cursor to query the database for a list of volunteers
    query = 'SELECT Volunteer.volunteerID FROM Volunteer_RegistersFor_Race JOIN Volunteer WHERE raceID =' + str(raceID)
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