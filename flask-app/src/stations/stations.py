from flask import Blueprint, request, jsonify, make_response
import json
from src import db


stations = Blueprint('stations', __name__)

@stations.route('/stations/<raceID>/<sponsorID>', methods=['GET'])
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