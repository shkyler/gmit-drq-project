import mysql.connector 
import dbconfig as cfg


class BookingsDAO:
  
  def initConnectToDB(self):
    db = mysql.connector.connect(
      host=       cfg.mysql['host'],
      user=       cfg.mysql['user'],
      password=   cfg.mysql['password'],
      database=   cfg.mysql['database'],
      pool_name='my_connection_pool',
      # max pool size allowed by pythonanywhere
      pool_size=3
    )
    return db  

  def getConnection(self):
    db = mysql.connector.connect(
      pool_name='my_connection_pool'
    )
    return db 

  def __init__(self):
    db=self.initConnectToDB()
    db.close()

  def getAllRooms(self):
    db = self.getConnection()
    cursor = db.cursor()
    sql="select * from rooms" 
    cursor.execute(sql)
    results = cursor.fetchall() 
    returnArray = []
    for result in results:
      returnArray.append(self.roomsDict(result))
    db.close()
    return returnArray
    

  def findRoomByID(self, id):
    db = self.getConnection()
    cursor = db.cursor()
    sql="select * from rooms where id = %s" 
    values = (id,)
    cursor.execute(sql, values) 
    result = cursor.fetchone() 
    room = self.roomsDict(result)
    db.close()
    return room
    

  def createRoom(self, values):
    db = self.getConnection()
    cursor = db.cursor()
    sql="insert into rooms (name, colour) values (%s,%s)" 
    cursor.execute(sql, values)
    db.commit() 
    lastRowID = cursor.lastrowid
    db.close() 
    return lastRowID
     

  def updateRoom(self, values):
    db = self.getConnection()
    cursor = db.cursor()
    sql="update rooms set name= %s, colour=%s where id = %s" 
    cursor.execute(sql, values)
    db.commit()
    db.close() 

  def deleteRoom(self, id):
    db = self.getConnection()
    cursor = db.cursor()
    sql="delete from rooms where id = %s"
    values = (id,) 
    cursor.execute(sql, values)
    db.commit()
    db.close() 

  def getAllBookings(self):
    db = self.getConnection()
    cursor = db.cursor()
    sql="select * from bookings" 
    cursor.execute(sql)
    results = cursor.fetchall() 
    returnArray = []
    for result in results:
      returnArray.append(self.bookingsDict(result))
    db.close()
    return returnArray
    

  def findBookingsByID(self, id):
    db = self.getConnection()
    cursor = db.cursor()
    sql="select * from bookings where id = %s" 
    values = (id,)
    cursor.execute(sql, values) 
    result = cursor.fetchone() 
    booking = self.bookingsDict(result)
    db.close()
    return booking
    

  def createBooking(self, values):
    db = self.getConnection()
    cursor = db.cursor()
    sql="insert into bookings (roomID, dateRequired, userName, reason) values (%s,%s,%s,%s)" 
    cursor.execute(sql, values)
    db.commit() 
    lastRowID = cursor.lastrowid 
    db.close()
    return lastRowID 
    

  def updateBooking(self, values):
    db = self.getConnection()
    cursor = db.cursor()
    sql="update bookings set roomID= %s, dateRequired=%s, userName=%s, reason=%s where id = %s" 
    cursor.execute(sql, values)
    db.commit()
    db.close()

  def deleteBooking(self, id):
    db = self.getConnection()
    cursor = db.cursor()
    sql="delete from bookings where id = %s"
    values = (id,) 
    cursor.execute(sql, values)
    db.commit()  
    db.close()

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
