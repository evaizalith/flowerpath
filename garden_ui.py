import pygame as py

class ClickBox:

    def __init__(self, x, y, w, h):
        self.rect = py.Rect(x, y, w, h)
        self.color = (0, 0, 0)
        self.fill = False

    def handleEvent(self, event):
        if event.type == py.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.fill = not self.fill

    def draw(self, screen):
        if self.fill:
            py.draw.rect(screen, (0, 0, 0), self.rect)
        else:
            py.draw.rect(screen, (0, 0, 0), self.rect, 1) 

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
                self.color = py.Color((20, 40, 125))
            else:
                self.active = False
                self.color = py.Color((20, 40, 75))
        if event.type == py.KEYDOWN:
            if self.active == True:
                if event.key == py.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == py.K_RETURN: #enter
                    if self.text.isdigit():
                        sizeInt = int(self.text)
                        if sizeInt > 800:
                            sizeInt = 800
                            self.text = "800"
                        if sizeInt < 100:
                            sizeInt = 100
                            self.text = "100"
                        self.direction = sizeInt
                        self.rescaleToggle = True
                    else:
                        print("Invalid integer!")
                else:
                    self.text += event.unicode
                self.textSurface = py.font.Font(None, 32).render(self.text, True, (0, 0, 0))

    def update(self):
        width = max(140, self.textSurface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.textSurface, (self.rect.x + 5, self.rect.y + 5))
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
"""
def rescale(rowNum, colNum, cells):
    cells.clear()
    for x in range(rowNum):
        for y in range(colNum):
            cell = ClickBox(self.rectX + (self.textbox1.direction/rowNum * x), self.rectY + (self.textbox2.direction/colNum * y), self.textbox1.direction/rowNum, self.textbox2.direction/colNum)
            cells.append(cell)

# rescale that keeps the same number of cells, but changes their size.
# Saves individual cell data!
def rescaleCellNum(rowNum, colNum, cells):
    adjust = 0
    for x in range(rowNum):
        for y in range(colNum):
            cellRect = py.Rect(self.rectX + (self.textbox1.direction/rowNum * x), self.rectY + (self.textbox2.direction/colNum * y), self.textbox1.direction/rowNum, self.textbox2.direction/colNum)
            cells[adjust].rect = cellRect
            adjust += 1
"""
def rescale(rowNum, colNum, cells):
    print("hello1")

def rescaleCellNum(rowNum, colNum, cells):
    print("hello2")