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

# # Get all police departments assisting a specific race
# @organizers.route('/police/<raceID>', methods=['GET'])
# def get_police_department_names(raceID):
#     query = 'SELECT p.name FROM Vendor JOIN WHERE vendorID = ' + str(vendorID)
#     query = '''
#       SELECT DISTINCT p.name
#       FROM Race r JOIN EventOrganizer e ON r JOIN Organizer_CommunicatesWith_Police ocwp ON e.raceID
#       WHERE category IS NOT NULL
#       ORDER BY category
#     '''
#     current_app.logger.info(query)
#     cursor = db.get_db().cursor()
#     cursor.execute(query)

#     column_headers = [x[0] for x in cursor.description]

#     json_data = []
#     the_data = cursor.fetchall()

#     for row in the_data:
#         json_data.append(dict(zip(column_headers, row)))
#     return jsonify(json_data)
