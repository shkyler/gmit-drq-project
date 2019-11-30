from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from bookingsDAO import bookingsDAO

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

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
  if not request.json:
      abort(400)
  room = {
      "name": request.json['name'],
      "colour": request.json['colour']
  }
  values = (room['name'], room['colour'])
  newID = bookingsDAO.createRoom(values)
  room['id'] = newID
  return jsonify(room)

#curl -i -H "Content-Type:application/json" -X DELETE http://127.0.0.1:5000/rooms/4
@app.route('/rooms/<int:id>' , methods=['DELETE'])
def delete_room(id):
  bookingsDAO.deleteRoom(id)
  return jsonify({"done":True})

#curl -i -H "Content-Type:application/json" -X PUT -d '{"name":"The Purple Room", "colour":"purple"}' "http://127.0.0.1:5000/rooms/4"
@app.route('/rooms/<int:id>', methods =['PUT'])
def update_room(id):
  foundRoom = bookingsDAO.findRoomByID(id)
  if not foundRoom:
    abort(404)
  if not request.json:
    abort(400)
  reqJson = request.json    
  if 'name' in reqJson and type(reqJson['name']) != str:
    abort(400)
  if 'colour' in reqJson and type(reqJson['colour']) is not str:
    abort(400)
  if 'name' in reqJson:
    foundRoom['name'] = reqJson['name']
  if 'colour' in reqJson:
    foundRoom['colour'] = reqJson['colour']
  values = (foundRoom['name'], foundRoom['colour'], foundRoom['id'])
  bookingsDAO.updateRoom(values)
  return jsonify(foundRoom)

#curl "http://127.0.0.1:5000/bookings"
@app.route('/bookings')
def get_all_bookings():
  results = bookingsDAO.getAllBookings()
  return jsonify(results)

#curl "http://127.0.0.1:5000/bookings/1"
@app.route('/bookings/<int:id>')
def find_bookingbyId(id):
  foundBooking = bookingsDAO.findBookingsByID(id)
  # check if the booking exists
  if not foundBooking:
    abort(404)
  return jsonify(foundBooking)

#curl -i -H "Content-Type:application/json" -X POST -d '{"roomID": 2, "dateRequired":"171219", "userName":"Andrew Beatty", "reason":"Data Representation Lectures"}' "http://127.0.0.1:5000/bookings"
@app.route('/bookings', methods=['POST'])
def create_booking():
  if not request.json:
      abort(400)
  booking = {
      "roomID": request.json['roomID'],
      "dateRequired": request.json['dateRequired'],
      "userName": request.json['userName'],
      "reason": request.json['reason']
  }
  values = (booking['roomID'], booking['dateRequired'], booking['userName'], booking['reason'])
  newID = bookingsDAO.createBooking(values)
  booking['id'] = newID
  return jsonify(booking)

#curl -i -H "Content-Type:application/json" -X DELETE http://127.0.0.1:5000/bookings/2_171219
@app.route('/bookings/<string:id>' , methods=['DELETE'])
def delete_booking(id):
  bookingsDAO.deleteBooking(id)
  return jsonify({"done":True})

#curl -i -H "Content-Type:application/json" -X PUT -d '{"id": "1_171219", "roomID": 1, "dateRequired":"171219", "userName":"P Moore", "reason":"Testing"}' "http://127.0.0.1:5000/bookings/2_171219"
@app.route('/bookings/<string:id>', methods =['PUT'])
def update_booking(id):
  foundBooking = bookingsDAO.findBookingsByID(id)
  if not foundBooking:
    abort(404)
  if not request.json:
    abort(400)
  reqJson = request.json  
  # validate the JSON
  if 'roomID' in reqJson and type(reqJson['roomID']) != int:
    abort(400)
  if 'dateRequired' in reqJson and type(reqJson['dateRequired']) is not str:
    abort(400)
  if 'userName' in reqJson and type(reqJson['userName']) is not str:
    abort(400)
  if 'reason' in reqJson and type(reqJson['reason']) is not str:
    abort(400) 
  # update the booking
  if 'roomID' in reqJson:
    foundBooking['roomID'] = reqJson['roomID']
  if 'dateRequired' in reqJson:
    foundBooking['dateRequired'] = reqJson['dateRequired']
  if 'userName' in reqJson:
    foundBooking['userName'] = reqJson['userName']
  if 'reason' in reqJson:
    foundBooking['reason'] = reqJson['reason']

  values = (foundBooking['roomID'], foundBooking['dateRequired'], foundBooking['userName'], foundBooking['reason'], foundBooking['id'])
  bookingsDAO.updateBooking(values)
  return jsonify(foundBooking)

if __name__ == '__main__' :
    app.run(debug= True)