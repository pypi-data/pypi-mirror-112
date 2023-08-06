import sqlite3
from pathlib import Path
import pkg_resources
class Unpack:
    def __init__(self):
        try:
            self.stream=pkg_resources.resource_stream(__name__,'SQLite_Python.db')
        except:
            return self.pkg_resorces_exc

    def pkg_resorces_exc(self):
        print('Module Error : pkg_resources Not Available')

    def writeTofile(self,data, filename):
    # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

    def readBlobData(self,im_nme,path):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sql_fetch_blob_query = """SELECT * from data_encode where im_nme = ?"""
            cursor.execute(sql_fetch_blob_query, (im_nme,))
            record = cursor.fetchall()
            path=Path(path)
            for row in record:
                print("Aadhar_Name = ", row[0])
                image1 = row[1]

                name=row[0] + '.jpg'
                photoPath = path/name
                #print
                self.writeTofile(image1, photoPath)

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read blob data from sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("sqlite connection is Running")
    def img_sv(self,val,path):
        im_nme='aadhar (' + str(val)+')'
        self.readBlobData(im_nme,path)

    def img_sv_all(self,val,path):
        for i in range(1,100):
            self.img_sv(i,path)

