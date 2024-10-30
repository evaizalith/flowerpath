import sqlite3
import plant

class databaseManager():
    def __init__(self, database):
        self.database = database
        self.cursor = None
        self.connection = None

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
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Plants(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, maxHeight INTEGER, maxSize INTEGER, germinationTime INTEGER, matureTime INTEGER, bloomTime INTEGER, bloomStart INTEGER, bloomEnd INTEGER, fullSun BOOLEAN, partialShade BOOLEAN, fullShade BOOLEAN, droughtTolerant INTEGER, overwaterSensitive BOOLEAN, color VARCHAR, perennial BOOLEAN)")

        return success, err

    def fetch(self, plantName : str):
        fetch = []
        result = []
        err = None

        try:
            fetch = self.cursor.execute(f"SELECT * FROM Plants WHERE Name=\"{plantName}\"")
            result = fetch.fetchall()
        except sqlite3.Error as e: 
            err = e 

        return result, err 
    
    def fetch_all(self):
        fetch = [] 
        result = [] 
        err = None 

        try:
            fetch = self.cursor.execute("SELECT * FROM Plants")
            result = fetch.fetchall()
        except sqlite3.Error as e:
            err = e

        return result, err

        
    def add(self, plant):
        success = True
        err = None

        try:
            self.cursor.execute(f"INSERT INTO Plants(name, maxHeight, maxSize, germinationTime, matureTime, bloomTime, bloomStart, bloomEnd, fullSun, partialShade, fullShade, droughtTolerant, overwaterSensitive, color, perennial) VALUES ('{plant.name}', '{plant.maxHeight}', '{plant.maxSize}', '{plant.germinationTime}', '{plant.matureTime}', '{plant.bloomTime}', '{plant.bloomStart}', '{plant.bloomEnd}', '{plant.fullSun}', '{plant.partialShade}', '{plant.fullShade}', '{plant.droughtTolerant}', '{plant.overwaterSensitive}', '{plant.color}', '{plant.perennial}')")
        except sqlite3.Error as e:
            success = False 
            err = e 

        if (success):
            self.connection.commit()

        return success, err 

    def close(self):
        self.connection.close()

# Used for testing the database manager
if __name__ == "__main__":
    print("Testing databaseManager...")
    db = databaseManager("test")
    success, error = db.connect()
    print(f"db.connect() return: {success},{error}")

    plant = plant.Plant("testPlant", 
                        0, #max height
                        0, #max size
                        0, #germination time
                        0, #mature time
                        0, #bloom time
                        0, #bloom start
                        0, #bloom end
                        1, #full sun
                        0, #Partial shade
                        0, #full shade
                        0, #drought tolerant
                        0, #overwater sensitive
                        0, #color
                        0) #perennial

    value, err = db.fetch("testPlant")
    print(f"db has: {value}, Err: {err}")

    value, err = db.add(plant)
    print(f"db.add(): {value}, Err: {err}")
    value, err = db.fetch("testPlant")
    print(f"db has: {value}, Err: {err}")

    db.close()
