import mysql.connector 
class BookingsDAO:
  db=""
  def __init__(self):
    self.db = mysql.connector.connect( 
    host="localhost",
    user="root",
    password="root",
    database="bookings"
    )

  def create(self, values):
    cursor = self.db.cursor()
    sql="insert into student (name, age) values (%s,%s)" 
    cursor.execute(sql, values)
    self.db.commit() 
    return cursor.lastrowid

  def getAllRooms(self):
    cursor = self.db.cursor() 
    sql="select * from rooms" 
    cursor.execute(sql)
    results = cursor.fetchall() 
    returnArray = []
    for result in results:
      returnArray.append(self.roomsDict(result))
    return returnArray

  def findRoomByID(self, id):
    cursor = self.db.cursor()
    sql="select * from rooms where id = %s" 
    values = (id,)
    cursor.execute(sql, values) 
    result = cursor.fetchone() 
    return self.roomsDict(result)

  def update(self, values):
    cursor = self.db.cursor()
    sql="update student set name= %s, age=%s where id = %s" 
    cursor.execute(sql, values)
    self.db.commit()

  def delete(self, id):
    cursor = self.db.cursor()
    sql="delete from student where id = %s"
    values = (id,) 
    cursor.execute(sql, values)
    self.db.commit() 
    print("delete done")

  def getAllBookings(self):
    cursor = self.db.cursor() 
    sql="select * from bookings" 
    cursor.execute(sql)
    results = cursor.fetchall() 
    returnArray = []
    for result in results:
      returnArray.append(self.bookingsDict(result))
    return returnArray

  def findBookingsByID(self, id):
    cursor = self.db.cursor()
    sql="select * from bookings where id = %s" 
    values = (id,)
    cursor.execute(sql, values) 
    result = cursor.fetchone() 
    return self.bookingsDict(result)

    
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
    colnames = ['id', 'dateRequired','roomID', 'userName', 'reason']
    item ={}
    # check if there is a result, otherwise return empty {}
    if result:
      for i, colName in enumerate(colnames):
        value = result[i]
        item[colName] = value
    return item

bookingsDAO = BookingsDAO()
