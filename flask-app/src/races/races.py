from flask import Blueprint, request, jsonify, make_response
import json
from src import db


races = Blueprint('races', __name__)

#How to use raceID here to specify race? Is that even needed?
@races.route('/races/<raceID>/<organizerID>', methods=['GET'])
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

#I know this won't work, but where should I get (post or do anything) this from if we don't have a post entity anymore?
@races.route('/races/<raceID>/<sponsorID>', methods=['GET'])
def get_post_content(raceID, sponsorID):
    cursor = db.get_db().cursor()
    query = '''
        SELECT title, content
        FROM Post
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

@races.route('/races/<raceID>/<sponsorID>', methods=['POST'])
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

@races.route('/races/<raceID>/<sponsorID>', methods=['PUT'])
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

@races.route('/races/<raceID>/<sponsorID>', methods=['DELETE'])
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