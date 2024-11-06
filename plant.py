import math
import pygame as py 

class Plant():
    def __init__(self, name, maxHeight, maxSize, germinationTime, matureTime, bloomTime, bloomStart, bloomEnd, fullSun, partialShade, fullShade, droughtTolerant, overwaterSensitive, color, perennial, texture1, texture2, texture3):
        self.name = name
        self.maxHeight = maxHeight 
        self.maxSize = maxSize
        self.germinationTime = germinationTime
        self.matureTime = matureTime
        self.bloomTime = bloomTime
        self.bloomStart = bloomStart
        self.bloomEnd = bloomEnd
        self.fullSun = fullSun
        self.partialShade = partialShade
        self.fullShade = fullShade
        self.droughtTolerant = droughtTolerant
        self.overwaterSensitive = overwaterSensitive
        self.color = color
        self.perennial = perennial

        self.texture1 = texture1
        self.texture2 = texture2
        self.texture3 = texture3

    # Pass age in days 
    def getHeight(self, age : int):
        # height = maxHeight / 1 + e^(-(age - bloomTime))
        height = self.maxHeight / (1 + math.exp(-(age - self.bloomTime)))

        return height

    # Retrieves a texture given id
    # Returns a null texture if unable to find it
    # Returns null value if unable to find null texure
    def getTexture(textureID : int):
        texture = None
        path = None
        err = None
        nullTexture = "placeholder_assets/pinkflower.jpg"

        if textureID == 0:
            path = self.texture1

        elif textureID == 1:
            path = self.texture2

        elif textureID == 2:
            path = self.texture3

        else:
            path = nullTexture
        
        try:
            texture = py.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading texture {path}")
            err = e2

        if err != None:
            try: 
                texture = py.image.load(nullTexture).convert_alpha()

            except pygame.error as e:
                print("Error loading null texture")
                return None

        return texture 

"""Schema of table Plants:
(0, 'id', 'INTEGER', 0, None, 1)
(1, 'name', 'VARCHAR', 0, None, 0)
(2, 'maxHeight', 'INTEGER', 0, None, 0)
(3, 'maxSize', 'INTEGER', 0, None, 0)
(4, 'germinationTime', 'INTEGER', 0, None, 0)
(5, 'matureTime', 'INTEGER', 0, None, 0)
(6, 'bloomTime', 'INTEGER', 0, None, 0)
(7, 'bloomStart', 'INTEGER', 0, None, 0)
(8, 'bloomEnd', 'INTEGER', 0, None, 0)
(9, 'fullSun', 'BOOLEAN', 0, None, 0)
(10, 'partialShade', 'BOOLEAN', 0, None, 0)
(11, 'fullShade', 'BOOLEAN', 0, None, 0)
(12, 'droughtTolerant', 'INTEGER', 0, None, 0)
(13, 'overwaterSensitive', 'BOOLEAN', 0, None, 0)
(14, 'color', 'VARCHAR', 0, None, 0)
(15, 'perennial', 'BOOLEAN', 0, None, 0)
(16, 'texture1', VARCHAR, 0, None, 0)
(17, 'texture2', VARCHAR, 0, None, 0)
(18, 'texture3', VARCHAR, 0, None, 0)"""
