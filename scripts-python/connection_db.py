import mysql.connector

class accessDB():
    def __init__(self, host='localhost', database='marveldb',
                 user='marvel', password='marvelpass'):
        
        self.host     = host
        self.database = database
        self.user     = user
        self.password = password

    def openConnection(self):
        self.cnn = mysql.connector.connect(host     = self.host,
                                           database = self.database,
                                           user     = self.user,
                                           password = self.password)

        self.cursor = self.cnn.cursor()

    def closeConnection(self):
        self.cnn.close()
   
    def executeDML(self, sql):
        self.cursor.execute(sql)
        self.cnn.commit()

    def executeDDL(self, sql):
        self.openConnection()
        self.cursor.execute(sql)
        self.closeConnection()