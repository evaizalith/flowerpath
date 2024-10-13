# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1080, 1080))
clock = pygame.time.Clock()
running = True
dt = 0

# inital location + size
rectX = 100
rectY = 100
rectSizeX = 500
rectSizeY = 200

# text boxes
base_font = pygame.font.Font(None, 32)
activeColor = pygame.Color((20, 40, 125))
inactiveColor = pygame.Color((20, 40, 75))

#
class ClickBox:

    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.fill = False

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.fill = not self.fill

    def draw(self, screen):
        if self.fill:
            pygame.draw.rect(screen, (255, 255, 255), self.rect)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 1) 


class TextBox:

    def __init__(self, x, y, w, h, direction, text=""):
        # Rect must be capitalized here
        self.rect = pygame.Rect(x, y, w, h)
        self.color = inactiveColor
        self.text = text
        self.textSurface = base_font.render(text, True, (255, 255, 255))
        self.active = False
        self.direction = direction
    
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = activeColor
            else:
                self.active = False
                self.color = inactiveColor
        if event.type == pygame.KEYDOWN:
            if self.active == True:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN: #enter
                    if self.text.isdigit():
                        sizeInt = int(self.text)
                        if sizeInt > 900:
                            sizeInt = 900
                            self.text = "900"
                        if sizeInt < 100:
                            sizeInt = 100
                            self.text = "100"
                        self.direction = sizeInt
                        rescaleCellNum(rowNum, colNum)
                    else:
                        print("Invalid integer!")

                else:
                    self.text += event.unicode
                self.textSurface = base_font.render(self.text, True, (255, 255, 255))

    def update(self):
        width = max(140, self.textSurface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.textSurface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

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
def rescale(rowNum, colNum):
    cells.clear()
    for x in range(rowNum):
        for y in range(colNum):
            cell = ClickBox(rectX + (textbox1.direction/rowNum * x), rectY + (textbox2.direction/colNum * y), textbox1.direction/rowNum, textbox2.direction/colNum)
            cells.append(cell)

# rescale that keeps the same number of cells, but changes their size.
# Saves individual cell data!
def rescaleCellNum(rowNum, colNum):
    adjust = 0
    for x in range(rowNum):
        for y in range(colNum):
            cellRect = pygame.Rect(rectX + (textbox1.direction/rowNum * x), rectY + (textbox2.direction/colNum * y), textbox1.direction/rowNum, textbox2.direction/colNum)
            cells[adjust].rect = cellRect
            adjust += 1


textbox1 = TextBox(50, 50, 140, 32, rectSizeX)
textbox2 = TextBox(240, 50, 140, 32, rectSizeY)
textboxes = [textbox1, textbox2]
cells = []
rowNum = 5
colNum = 5
rescale(rowNum, colNum)

active = False

while running:

    screen.fill((0,0,0))

    for box in textboxes:
        box.draw(screen)
    pygame.draw.rect(screen, (255, 255, 255), [rectX, rectY, textbox1.direction, textbox2.direction], 2)
    for cell in cells:
        cell.draw(screen)


    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for box in textboxes:
            box.handleEvent(event)
            box.update()
        for cell in cells:
            cell.handleEvent(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if(colNum > 1):
                    colNum -= 1
                    rescale(rowNum, colNum)
            if event.key == pygame.K_DOWN:
                if(colNum < 8):
                    colNum += 1
                    rescale(rowNum, colNum)
            if event.key == pygame.K_LEFT:
                if(rowNum > 1):
                    rowNum -= 1
                    rescale(rowNum, colNum)
            if event.key == pygame.K_RIGHT:
                if(rowNum < 8):
                    rowNum += 1
                    rescale(rowNum, colNum)


    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)

pygame.quit()
