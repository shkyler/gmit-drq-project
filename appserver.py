from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from bookingsDAO import bookingsDAO

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# room id is auto incrementing
rooms=[
  {"id": 1, "name":"Conference Room 1", "colour":"blue"},
  {"id": 2, "name":"Conference Room 2", "colour":"yellow"},
  {"id": 3, "name":"Andrew Beatty Theatre", "colour":"green"}
]
nextRoomId=4

# the id of the booking is made from the roomID and the dateRequired  
bookings=[
  {"id": "1_171219", "roomID": 1, "dateRequired":"171219", "userName":"Joe Bloggs", "reason":"Exam revision"},
  {"id": "2_171219", "roomID": 2, "dateRequired":"171219", "userName":"Andrew Beatty", "reason":"Data Representation Lectures"},
]

#curl "http://127.0.0.1:5000/rooms"
@app.route('/rooms')
def get_all_rooms():
  results = bookingsDAO.getAllRooms()
  return jsonify(results)

#curl "http://127.0.0.1:5000/rooms/2"
@app.route('/rooms/<int:id>')
def find_roomById(id):
  foundRoom = bookingsDAO.findRoomByID(id)
  # check if the room exists
  if not foundRoom:
    abort(404)
  return jsonify(foundRoom)

#curl -i -H "Content-Type:application/json" -X POST -d '{"name":"The Purple Room", "colour":"purple"}' "http://127.0.0.1:5000/rooms"
@app.route('/rooms', methods=['POST'])
def create_room():
  global nextRoomId
  if not request.json:
      abort(400)
  room = {
      "id": nextRoomId,
      "name": request.json['name'],
      "colour": request.json['colour']
  }
  nextRoomId += 1
  rooms.append(room)
  return jsonify(room)

#curl -i -H "Content-Type:application/json" -X DELETE http://127.0.0.1:5000/rooms/4
@app.route('/rooms/<int:id>' , methods=['DELETE'])
def delete_room(id):
  foundRooms = list(filter(lambda t: t['id']== id, rooms))
  if (len(foundRooms) == 0):
      abort(404)
  rooms.remove(foundRooms[0])
  return jsonify({"done":True})

#curl -i -H "Content-Type:application/json" -X PUT -d '{"name":"The Purple Room", "colour":"purple"}' "http://127.0.0.1:5000/rooms/4"
@app.route('/rooms/<int:id>', methods =['PUT'])
def update_room(id):
  foundRooms=list(filter(lambda t : t['id'] == id, rooms))
  if len(foundRooms) == 0:
      abort(404)
  if not request.json:
      abort(400)
  if 'name' in request.json and type(request.json['name']) != str:
      abort(400)
  if 'colour' in request.json and type(request.json['colour']) is not str:
      abort(400)
  foundRooms[0]['name']  = request.json.get('name', foundRooms[0]['name'])
  foundRooms[0]['colour'] =request.json.get('colour', foundRooms[0]['colour'])
  return jsonify( {'room':foundRooms[0]})

#curl "http://127.0.0.1:5000/bookings"
@app.route('/bookings')
def get_all_bookings():
  results = bookingsDAO.getAllBookings()
  return jsonify(results)

#curl "http://127.0.0.1:5000/bookings/1_171219"
@app.route('/bookings/<string:id>')
def find_bookingbyId(id):
  foundBooking = bookingsDAO.findBookingsByID(id)
  # check if the booking exists
  if not foundBooking:
    abort(404)
  return jsonify(foundBooking)

#curl -i -H "Content-Type:application/json" -X POST -d '{"roomID": 2, "dateRequired":"171219", "userName":"Andrew Beatty", "reason":"Data Representation Lectures"}' "http://127.0.0.1:5000/bookings"
@app.route('/bookings', methods=['POST'])
def create_booking():
  # check to see if the room is already booked on that day
  bookingID = str(request.json['roomID']) + "_" + str(request.json['dateRequired'])
  foundBookings = list(filter(lambda t: t['id'] == bookingID, bookings))
  if len(foundBookings) != 0:
    abort(404)
  # check to see if the room is a valid room
  roomID = request.json['roomID']
  foundRooms=list(filter(lambda t : t['id'] == roomID, rooms))
  if len(foundRooms) == 0:
    abort(401)
  # check the request is valid json  
  if not request.json:
      abort(400)
  booking = {
      "id": bookingID,
      "roomID": roomID,
      "dateRequired": request.json['dateRequired'],
      "userName": request.json['userName'],
      "reason": request.json['reason']
  }
  bookings.append(booking)
  return jsonify(booking)

#curl -i -H "Content-Type:application/json" -X DELETE http://127.0.0.1:5000/bookings/2_171219
@app.route('/bookings/<string:id>' , methods=['DELETE'])
def delete_booking(id):
  foundBookings = list(filter(lambda t: t['id']== id, bookings))
  if (len(foundBookings) == 0):
      abort(404)
  bookings.remove(foundBookings[0])
  return jsonify({"done":True})

#curl -i -H "Content-Type:application/json" -X PUT -d '{"id": "1_171219", "roomID": 1, "dateRequired":"171219", "userName":"P Moore", "reason":"Testing"}' "http://127.0.0.1:5000/bookings/2_171219"
@app.route('/bookings/<string:id>', methods =['PUT'])
def update_booking(id):
  # check is the booking in the system
  foundBookings=list(filter(lambda t : t['id'] == id, bookings))
  if len(foundBookings) == 0:
      abort(404)
  # check to see if the room is already booked on that day
  newBookingID = str(request.json['roomID']) + "_" + str(request.json['dateRequired'])
  checkBookings = list(filter(lambda t: t['id'] == newBookingID, bookings))
  if len(checkBookings) != 0:
    abort(400)
  # check to see if the room is a valid room
  roomID = request.json['roomID']
  foundRooms=list(filter(lambda t : t['id'] == roomID, rooms))
  if len(foundRooms) == 0:
    abort(401)  
  # check the datatypes  
  if not request.json:
      abort(400)
  if 'roomID' in request.json and type(request.json['roomID']) != int:
      abort(400)
  if 'dateRequired' in request.json and type(request.json['dateRequired']) is not str:
      abort(400)
  if 'userName' in request.json and type(request.json['userName']) is not str:
      abort(400)  
  if 'reason' in request.json and type(request.json['reason']) is not str:
      abort(400)  
  # update the data        
  foundBookings[0]['id']  = newBookingID
  foundBookings[0]['roomID'] = roomID
  foundBookings[0]['dateRequired']  = request.json.get('dateRequired', foundBookings[0]['dateRequired'])
  foundBookings[0]['userName'] =request.json.get('userName', foundBookings[0]['userName'])
  foundBookings[0]['reason'] =request.json.get('reason', foundBookings[0]['reason'])
  return jsonify( {'room':foundBookings[0]})

if __name__ == '__main__' :
    app.run(debug= True)