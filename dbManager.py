import sqlite3
import plant as p 
import re

class databaseManager():
    def __init__(self, database):
        self.database = database
        self.cursor = None
        self.connection = None

        # Used for validating inputs
        self.validation = re.compile(r"[\w\s\-'+]+")
        self.intVal = re.compile(r"\d+")

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
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Plants(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, maxHeight INTEGER, maxSize INTEGER, germinationTime INTEGER, matureTime INTEGER, bloomTime INTEGER, bloomStart INTEGER, bloomEnd INTEGER, fullSun BOOLEAN, partialShade BOOLEAN, fullShade BOOLEAN, droughtTolerant INTEGER, overwaterSensitive BOOLEAN, color VARCHAR, perennial BOOLEAN, texture1 VARCHAR, texture2 VARCHAR, texture3 VARCHAR)")

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
    
    def fetch_all(self):
        fetch = [] 
        result = [] 
        err = None 

        try:
            fetch = self.cursor.execute("SELECT * FROM Plants")
            result = fetch.fetchall()
            if len(result) == 0:
                print("Result in fetch_all is empty")
        except sqlite3.Error as e:
            err = e

        return result, err

        
    def add(self, plant):
        success = True
        err = None

        try:
            self.cursor.execute(f"INSERT INTO Plants(name, maxHeight, maxSize, germinationTime, matureTime, bloomTime, bloomStart, bloomEnd, fullSun, partialShade, fullShade, droughtTolerant, overwaterSensitive, color, perennial, texture1, texture2, texture3) VALUES ('{plant.name}', '{plant.maxHeight}', '{plant.maxSize}', '{plant.germinationTime}', '{plant.matureTime}', '{plant.bloomTime}', '{plant.bloomStart}', '{plant.bloomEnd}', '{plant.fullSun}', '{plant.partialShade}', '{plant.fullShade}', '{plant.droughtTolerant}', '{plant.overwaterSensitive}', '{plant.color}', '{plant.perennial}', '{plant.texture1}', '{plant.texture2}', '{plant.texture3}')")
            print(f"Added Plant '{plant.name}' with texture1 path: {plant.texture1}")
        except sqlite3.Error as e:
            print("There was an error.")
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

    def loadDefaultDatabase(self):
        # Name, max height, max size, germination time, mature time, bloom time, start, end, full sun, partial shade, full shade, drought tolerant, overwater sensitive, color, perennial, texture1, texture2, texture3
        plant = p.Plant("Calendula", 15, 12, 14, 55, 60, 4, 9, 1, 1, 0, 1, 1, 0, 0, "images/calendula.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")
        
        plant = p.Plant("Benary`s Giant Zinna", 45, 12, 5, 90, 45, 6, 8, 1, 0, 0, 1, 1, 0, 0, "images/giantzinna.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Foxglove", 35, 12, 17, 135, 30, 5, 7, 1, 1, 0, 1, 1, 0, 0, "images/foxglove.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Nasturtium", 16, 15, 17, 60, 92, 6, 8, 1, 1, 0, 1, 1, 0, 0, "images/nasturtium.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Annual Phlox", 23, 12, 7, 57, 45, 6, 8, 1, 0, 0, 0, 1, 0, 0, "images/annualphlox.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Viola", 9, 7, 5, 57, 45, 5, 9, 1, 1, 0, 1, 1, 0, 0, "images/viola.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Snapdragon", 40, 8, 10, 115, 30, 6, 8, 1, 1, 0, 0, 1, 0, 0, "images/snapdragon.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Cosmos", 42, 10, 8, 82, 84, 6, 9, 1, 0, 0, 1, 1, 0, 0, "images/cosmos.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Sweet Pea", 82, 6, 17, 80, 42, 9, 10, 1, 0, 0, 0, 0, 0, 0, "images/sweetpea.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Baby`s Breath", 20, 8, 10, 47, 30, 6, 8, 1, 0, 0, 1, 0, 0, 0, "images/babysbreath.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Marigold", 10, 12, 7, 50, 60, 5, 8, 1, 0, 0, 1, 0, 0, 0, "images/marigold.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Milkweed", 40, 18, 17, 130, 60, 7, 8, 1, 0, 0, 1, 0, 0, 0, "images/milkweed.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Larkspur", 42, 14, 17, 85, 30, 5, 8, 1, 1, 0, 0, 0, 0, 0, "images/larkspur.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Bleeding Heart", 24, 30, 365, 379, 37, 5, 6, 0, 1, 1, 1, 1, 0, 1, "images/bleedingheart.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Hostas", 36, 50, 14, 48, 21, 6, 8, 0, 1, 1, 1, 0, 0, 1, "images/hostas.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        plant = p.Plant("Coral Bells", 18, 20, 28, 90, 45, 5, 7, 0, 1, 1, 0, 0, 0, 1, "images/coralbells.jpg", 0, 0)
        value, err = self.add(plant)
        print(f"db.add(Plant): {value}, Err: {err}")

        self.printAll()

        self.commit()

# Used for testing the database manager
if __name__ == "__main__":
    print("Testing databaseManager...")
    db = databaseManager("test")
    success, error = db.connect()
    print(f"db.connect() return: {success},{error}")

    # plant = p.Plant("testPlant", 
    #                     0, #max height
    #                     0, #max size
    #                     0, #germination time
    #                     0, #mature time
    #                     0, #bloom time
    #                     0, #bloom start
    #                     0, #bloom end
    #                     1, #full sun
    #                     0, #Partial shade
    #                     0, #full shade
    #                     0, #drought tolerant
    #                     0, #overwater sensitive
    #                     0, #color
    #                     0, #perennial
    #                     0, #texture1
    #                     0, #texture2
    #                     0) #texture3

    # value, err = db.fetch("testPlant")
    # print(f"db has: {value}, Err: {err}")

    # print("The contents of the database are: ")
    # db.printAll()

    # value, err = db.add(plant)
    # print(f"db.add(testPlant): {value}, Err: {err}")
    # value, err = db.fetch("testPlant")
    # print(f"db has: {value}, Err: {err}")

    # value, err = db.remove("testPlant")
    # print(f"db.remove(testPlant): {value}, Err: {err}")
    # value, err = db.fetch("testPlant")
    # print(f"db.fetch(testPlant): {value}, Err: {err}")

    # # test input validation
    # value, err = db.add(plant)
    # print(f"db.add(testPlant): {value}, Err: {err}")
    # value, err = db.remove("testPlant;")
    # print(f"db.remove(testPlant;): {value}, Err: {err}")

    # newPlant = p.Plant("testPlant;///++", 
    #                     12, #max height
    #                     0, #max size
    #                     0, #germination time
    #                     0, #mature time
    #                     75, #bloom time
    #                     0, #bloom start
    #                     0, #bloom end
    #                     1, #full sun
    #                     0, #Partial shade
    #                     0, #full shade
    #                     0, #drought tolerant
    #                     0, #overwater sensitive
    #                     0, #color
    #                     0, #perennial
    #                     0, #texture1
    #                     0, #texture2
    #                     0) #texture3
    # value, err = db.add(newPlant)
    # #print(f"db.add(testPlant;///++): {value}, Err: {err}")
    # value, err = db.remove("testPlant;///++")
    # #print(f"db.remove(testPlant;///++): {value}, Err {err}")

    # print("Print all:")
    # db.printAll()
    # #db.deleteAll()
    # #print("Print all after deleteAll():")
    # #db.printAll()

    db.commit()

    db.close()
