import pygame as py
from constants_config import *
from plant import Plant

class ClickBox:

    def __init__(self, x, y, w, h, fullSun = True, partialShade = False, fullShade = False, droughtRes = 0):
        self.rect = py.Rect(x, y, w, h)
        self.color = (0, 0, 0)
        self.fill = False
        self.fullSun = fullSun
        self.partialShade = partialShade
        self.fullShade = fullShade
        self.droughtRes = droughtRes

    def handleEvent(self, event):
        if event.type == py.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.fill = not self.fill

    def draw(self, screen):
        if self.fill:
            py.draw.rect(screen, (0, 0, 0), self.rect)
        else:
            py.draw.rect(screen, (0, 0, 0), self.rect, 1)

    """ 
    Logic for via draw:
    viability starts at 0 (neutral), and can become 1 (good) or -1 (bad)
    A neutral cell passes no good or bad check
    if cell drought resistance is not neutral, compare resistance.
    if it matches, viability becomes 1, if not, viability becomes -1
    if viability is not failed, check sun level.
    If sun level matches anywhere, viability becomes 1 (if not already)
    If there are no matches, compare opposites.
    If an opposite exists, viability becomes -1.
    Boxes are drawn green for viable and red for not viable.
    Neutral boxes are drawn the same as normal.
    """   
    def viabilityDraw(self, screen, selectedFlower):
        viability = 0
        if not self.droughtRes == 0:
            if self.droughtRes == selectedFlower.droughtTolerant:
                viability = 1
            else: 
                viability = -1
        if not viability == -1:
            if self.fullSun == True and selectedFlower.fullSun == True:
                viability = 1
            elif self.partialShade == True and selectedFlower.partialShade == True:
                viability = 1
            elif self.fullShade == True and selectedFlower.fullShade == True:
                viability = 1
        if not viability == 1:
            if self.fullSun == True and selectedFlower.fullShade == True:
                viability == -1
            if self.fullShade == True and selectedFlower.fullSun == True:
                viability = -1
        match viability:
            case 1:
                py.draw.rect(screen, DARK_GREEN, self.rect)
            case 0:
                py.draw.rect(screen, PURE_BLACK, self.rect, 3)
            case -1:
                py.draw.rect(screen, DARK_RED, self.rect)
            case _:
                py.draw.rect(screen, PURE_BLACK, self.rect, 1)
            
                

class TextBox:

    def __init__(self, x, y, w, h, direction, text=""):
        # Rect must be capitalized here
        self.rect = py.Rect(x, y, w, h)
        self.color = py.Color((20, 40, 75))
        self.text = text
        self.textSurface = py.font.Font(None, 32).render(text, True, (0, 0, 0))
        self.active = False
        self.direction = direction
        self.rescaleToggle = False
    
    def handleEvent(self, event):
        if event.type == py.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = py.Color((40, 60, 200))
            else:
                self.active = False
                self.color = py.Color((20, 40, 75))
        if event.type == py.KEYDOWN:
            if self.active == True:
                if event.key == py.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == py.K_RETURN: #enter
                    # 1ft = 30 pixels
                    # max 10 ft, min 3 ft
                    if self.text.isdigit():
                        sizeInt = int(self.text) * 60
                        if sizeInt > 600:
                            sizeInt = 600
                            self.text = "10"
                        if sizeInt < 180:
                            sizeInt = 180
                            self.text = "3"
                        self.direction = sizeInt
                        self.rescaleToggle = True
                    else:
                        print("Invalid integer!")
                else:
                    if len(self.text) < 8:
                        self.text += event.unicode
                self.textSurface = py.font.Font(None, 32).render(self.text, True, (0, 0, 0))

    def draw(self, screen):
        screen.blit(self.textSurface, (self.rect.x + 5, self.rect.y + 5))
        if(self.active):
            py.draw.rect(screen, self.color, self.rect, 4)
        else:
            py.draw.rect(screen, self.color, self.rect, 2)

# old rescale, attempted to handle math within the for loop
# this was clean, but created weird outlier cases where an extra row would be created
# due to float rounding
"""
def rescale(rowNum, colNum):
    cells.clear()
    for x in range(rectX, rectX + textbox1.direction, int(textbox1.direction/rowNum)):
        for y in range(rectY, rectY + textbox2.direction, int(textbox2.direction/colNum)):
            cell = ClickBox(x, y, textbox1.direction/rowNum, textbox2.direction/colNum)
            cells.append(cell)
"""
# the new rescale, now handles everything out of the for loop
# less pretty, but works 100% of the time due to no floats in loop

def rescale(self, rowNum, colNum, cells):
    cells.clear()
    for x in range(rowNum):
        for y in range(colNum):
            cell = ClickBox(self.rectX + (self.textbox1.direction/rowNum * x), self.rectY + (self.textbox2.direction/colNum * y), self.textbox1.direction/rowNum, self.textbox2.direction/colNum)
            cells.append(cell)

# rescale that keeps the same number of cells, but changes their size.
# Saves individual cell data!
def rescaleCellNum(self, rowNum, colNum, cells):
    adjust = 0
    for x in range(rowNum):
        for y in range(colNum):
            cellRect = py.Rect(self.rectX + (self.textbox1.direction/rowNum * x), self.rectY + (self.textbox2.direction/colNum * y), self.textbox1.direction/rowNum, self.textbox2.direction/colNum)
            cells[adjust].rect = cellRect
            adjust += 1