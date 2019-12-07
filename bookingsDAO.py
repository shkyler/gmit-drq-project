import mysql.connector 
import dbconfig as cfg


class BookingsDAO:
  db=""
  def __init__(self):
    self.db = mysql.connector.connect( 
    host=cfg.mysql['host'],
    user=cfg.mysql['user'],
    password=cfg.mysql['password'],
    database=cfg.mysql['database']
    )

  def getAllRooms(self):
    cursor = self.db.cursor() 
    sql="select * from rooms" 
    cursor.execute(sql)
    results = cursor.fetchall() 
    returnArray = []
    for result in results:
      returnArray.append(self.roomsDict(result))
    return returnArray
    cursor.close()

  def findRoomByID(self, id):
    cursor = self.db.cursor()
    sql="select * from rooms where id = %s" 
    values = (id,)
    cursor.execute(sql, values) 
    result = cursor.fetchone() 
    return self.roomsDict(result)
    cursor.close()

  def createRoom(self, values):
    cursor = self.db.cursor()
    sql="insert into rooms (name, colour) values (%s,%s)" 
    cursor.execute(sql, values)
    self.db.commit() 
    return cursor.lastrowid
    cursor.close()  

  def updateRoom(self, values):
    cursor = self.db.cursor()
    sql="update rooms set name= %s, colour=%s where id = %s" 
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close()

  def deleteRoom(self, id):
    cursor = self.db.cursor()
    sql="delete from rooms where id = %s"
    values = (id,) 
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close() 

  def getAllBookings(self):
    cursor = self.db.cursor() 
    sql="select * from bookings" 
    cursor.execute(sql)
    results = cursor.fetchall() 
    returnArray = []
    for result in results:
      returnArray.append(self.bookingsDict(result))
    return returnArray
    cursor.close()

  def findBookingsByID(self, id):
    cursor = self.db.cursor()
    sql="select * from bookings where id = %s" 
    values = (id,)
    cursor.execute(sql, values) 
    result = cursor.fetchone() 
    return self.bookingsDict(result)
    cursor.close()

  def createBooking(self, values):
    cursor = self.db.cursor()
    sql="insert into bookings (roomID, dateRequired, userName, reason) values (%s,%s,%s,%s)" 
    cursor.execute(sql, values)
    self.db.commit() 
    return cursor.lastrowid  
    cursor.close()

  def updateBooking(self, values):
    cursor = self.db.cursor()
    sql="update bookings set roomID= %s, dateRequired=%s, userName=%s, reason=%s where id = %s" 
    cursor.execute(sql, values)
    self.db.commit()
    cursor.close()

  def deleteBooking(self, id):
    cursor = self.db.cursor()
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
