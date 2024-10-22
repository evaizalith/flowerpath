import sqlite3

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
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Plants()")

        return success, err

    def fetch(self, plantName : str):
        result = []
        err = None

        try:
            result = self.cursor.execute(f"SELECT * FROM Plants WHERE Name=\"{plantName}\"")
        except sqlite3.Error as e: 
            err = e 

        return result, err 
        
    def add(self, plantName : str, maxHeight : int):
        success = True
        err = None

        try:
            self.cursor.execute(f"INSERT INTO Plants VALUES ('{plantName}', '{maxHeight}');")
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
    db.connect()

    value = db.fetch("testPlant")
    print(f"db has: {value}")

    db.add("fetchPlant", 2)
    value = db.fetch("testPlant")
    print(f"db has: {value}")

    db.close()
