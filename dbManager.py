import sqlite3
import plant as p 
import re

class databaseManager():
    def __init__(self, database):
        self.database = database
        self.cursor = None
        self.connection = None

        # Used for validating inputs
        self.validation = re.compile("[\w\s\-]+")
        self.intVal = re.compile("\d+")

    def connect(self):
        success = True
        err = None

        try:
            self.connection = sqlite3.connect(self.database)
        except sqlite3.Error as e:
            success = False
            err = e

        if (success):
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Plants(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, maxHeight INTEGER, maxSize INTEGER, germinationTime INTEGER, matureTime INTEGER, bloomTime INTEGER, bloomStart INTEGER, bloomEnd INTEGER, fullSun BOOLEAN, partialShade BOOLEAN, fullShade BOOLEAN, droughtTolerant INTEGER, overwaterSensitive BOOLEAN, color VARCHAR, perennial BOOLEAN, texture0 VARCHAR, texture1 VARCHAR, texture2 VARCHAR, texture3 VARCHAR)")

        return success, err

    def fetch(self, plantName : str):
        fetch = []
        result = []
        err = None

        plantName = self.validation.match(plantName).group(0)

        try:
            fetch = self.cursor.execute(f"SELECT * FROM Plants WHERE Name=\"{plantName}\"")
            result = fetch.fetchall()
        except sqlite3.Error as e: 
            err = e 

        return result, err 
        
    def add(self, plant):
        success = True
        err = None

        try:
            self.cursor.execute(f"INSERT INTO Plants(name, maxHeight, maxSize, germinationTime, matureTime, bloomTime, bloomStart, bloomEnd, fullSun, partialShade, fullShade, droughtTolerant, overwaterSensitive, color, perennial) VALUES ('{plant.name}', '{plant.maxHeight}', '{plant.maxSize}', '{plant.germinationTime}', '{plant.matureTime}', '{plant.bloomTime}', '{plant.bloomStart}', '{plant.bloomEnd}', '{plant.fullSun}', '{plant.partialShade}', '{plant.fullShade}', '{plant.droughtTolerant}', '{plant.overwaterSensitive}', '{plant.color}', '{plant.perennial}', '{plant.texture1}', '{plant.texture2}', '{plant.texture3}')")
        except sqlite3.Error as e:
            success = False 
            err = e 

        if (success):
            self.connection.commit()

        return success, err 

    def remove(self, plantName):
        success = True
        err = None

        plantName = self.validation.match(plantName).group(0)

        try:
            self.cursor.execute(f"DELETE FROM Plants WHERE name = '{plantName}'")
            self.connection.commit()
        except sqlite3.Error as e:
            success = False
            err = e

        return success, err

    # Prints every item in database
    def printAll(self):
        fetch = self.cursor.execute(f"SELECT * FROM Plants")

        for item in fetch:
            print({item})

    # WARNING
    # DELETES EVERY ITEM IN DATABASE
    # Does not auto-save, call commit() if you want to save changes made via this function
    def deleteAll(self):
        success = True
        err = None

        try:
            self.cursor.execute(f"DELETE FROM Plants")
        except sqlite3.Error as e:
            success = False
            err = e

        return success, err

    # Saves changes 
    def commit(self):
        success = True
        err = None

        try:
            self.connection.commit()
        except sqlite3.Error as e:
            success = False
            err = e

        return success, err

    def close(self):
        self.connection.close()

    def __del__(self):
        self.close()

# Used for testing the database manager
if __name__ == "__main__":
    print("Testing databaseManager...")
    db = databaseManager("test")
    success, error = db.connect()
    print(f"db.connect() return: {success},{error}")

    plant = p.Plant("testPlant", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    value, err = db.fetch("testPlant")
    print(f"db has: {value}, Err: {err}")

    value, err = db.add(plant)
    print(f"db.add(testPlant): {value}, Err: {err}")
    value, err = db.fetch("testPlant")
    print(f"db has: {value}, Err: {err}")

    value, err = db.remove("testPlant")
    print(f"db.remove(testPlant): {value}, Err: {err}")
    value, err = db.fetch("testPlant")
    print(f"db.fetch(testPlant): {value}, Err: {err}")

    # test input validation
    value, err = db.add(plant)
    print(f"db.add(testPlant): {value}, Err: {err}")
    value, err = db.remove("testPlant;")
    print(f"db.remove(testPlant;): {value}, Err: {err}")

    newPlant = p.Plant("testPlant;///++", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    value, err = db.add(newPlant)
    print(f"db.add(testPlant;///++): {value}, Err: {err}")
    value, err = db.remove("testPlant;///++")
    print(f"db.remove(testPlant;///++): {value}, Err {err}")

    print("Print all:")
    db.printAll()
    db.deleteAll()
    print("Print all after deleteAll():")
    db.printAll()

    db.commit()

    db.close()
