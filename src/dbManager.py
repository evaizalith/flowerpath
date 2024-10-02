import mysql.connector
from mysql.connector import Error

class databaseManager():
    def __init__(user, password, host, database):
        config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database,
            'raise_on_warnings': True
        }
        connection = None

    def connect():
        success = True
        err = None

        try:
            connection = mysql.connector.connect(**config)
        except Error as e:
            success = False
            err = e

        return success, err

    def fetch(plantName : String):
        result = []
        err = None

        try:
            result = connection.cmd_query(f"SELECT * FROM Plants WHERE Name=\"{plantName}\";")
        except Error as e: 
            err = e 

        return result, err 
        
    def add(plantName : String, maxHeight : int):
        success = True
        err = None

        try:
            connection.cmd_query(f"INSERT INTO Plants VALUES ('{plantName}', '{maxHeight}');")
        except Error as e:
            err = e 

        return success, err 
