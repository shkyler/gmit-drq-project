import mysql.connector 
import dbconfig as cfg


class BookingsDAO:
  db=""
  def connectToDB(self):
    self.db = mysql.connector.connect(
      host=       cfg.mysql['host'],
      user=       cfg.mysql['user'],
      password=   cfg.mysql['password'],
      database=   cfg.mysql['database']
      )

  def __init__(self): 
    self.connectToDB()

  def getCursor(self):
    if not self.db.is_connected():
        self.connectToDB()
    return self.db.cursor()  

  def getAllRooms(self):
    cursor = self.getCursor()
    sql="select * from rooms" 
    cursor.execute(sql)
    results = cursor.fetchall() 
    returnArray = []
    for result in results:
      returnArray.append(self.roomsDict(result))
    cursor.close()
    return returnArray
    

  def findRoomByID(self, id):
    cursor = self.getCursor()
    sql="select * from rooms where id = %s" 
    values = (id,)
    cursor.execute(sql, values) 
    result = cursor.fetchone() 
    room = self.roomsDict(result)
    cursor.close()
    return room
    

  def createRoom(self, values):
    cursor = self.getCursor()
    sql="insert into rooms (name, colour) values (%s,%s)" 
    cursor.execute(sql, values)
    self.db.commit() 
    lastRowID = cursor.lastrowid
    cursor.close() 
    return lastRowID
     

  def updateRoom(self, values):
    cursor = self.getCursor()
    sql="update rooms set name= %s, colour=%s where id = %s" 
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close() 

  def deleteRoom(self, id):
    cursor = self.getCursor()
    sql="delete from rooms where id = %s"
    values = (id,) 
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close() 

  def getAllBookings(self):
    cursor = self.getCursor()
    sql="select * from bookings" 
    cursor.execute(sql)
    results = cursor.fetchall() 
    returnArray = []
    for result in results:
      returnArray.append(self.bookingsDict(result))
    cursor.close()
    return returnArray
    

  def findBookingsByID(self, id):
    cursor = self.getCursor()
    sql="select * from bookings where id = %s" 
    values = (id,)
    cursor.execute(sql, values) 
    result = cursor.fetchone() 
    booking = self.bookingsDict(result)
    cursor.close()
    return booking
    

  def createBooking(self, values):
    cursor = self.getCursor()
    sql="insert into bookings (roomID, dateRequired, userName, reason) values (%s,%s,%s,%s)" 
    cursor.execute(sql, values)
    self.db.commit() 
    lastRowID = cursor.lastrowid 
    cursor.close()
    return lastRowID 
    

  def updateBooking(self, values):
    cursor = self.getCursor()
    sql="update bookings set roomID= %s, dateRequired=%s, userName=%s, reason=%s where id = %s" 
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close()

  def deleteBooking(self, id):
    cursor = self.getCursor()
    sql="delete from bookings where id = %s"
    values = (id,) 
    cursor.execute(sql, values)
    self.db.commit()  
    cursor.close()

  # convert rooms result to a dictionary
  def roomsDict(self,result):
    colnames = ['id', 'name','colour']
    item ={}
    # check if there is a result, otherwise return empty {}
    if result:
      for i, colName in enumerate(colnames):
        value = result[i]
        item[colName] = value
    return item

  # convert bookings result to a dictionary
  def bookingsDict(self,result):
    colnames = ['roomID','dateRequired','userName','reason', 'id']
    item ={}
    # check if there is a result, otherwise return empty {}
    if result:
      for i, colName in enumerate(colnames):
        value = result[i]
        item[colName] = value
    return item

bookingsDAO = BookingsDAO()
