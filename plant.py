class Plant():
    def __init__(self, name, maxHeight, maxSize, germinationTime, matureTime, bloomTime, bloomStart, bloomEnd, fullSun, partialShade, fullShade, droughtTolerant, overwaterSensitive, color, perennial):
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
(15, 'perennial', 'BOOLEAN', 0, None, 0)"""
