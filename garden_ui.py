import pygame as py
from constants_config import *
from plant import Plant

class ClickBox:

    def __init__(self, x, y, w, h, fullSun = True, partialShade = False, fullShade = False, droughtRes = 0):
        self.rect = py.Rect(x, y, w, h)
        self.color = (0, 0, 0)
        self.fill = False
        self.count = 0
        self.fullSun = fullSun
        self.partialShade = partialShade
        self.fullShade = fullShade
        self.droughtRes = droughtRes

    def handleEvent(self, event, selection_mode, sunlight_level):
        if event.type == py.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if selection_mode:
                    print(f"Cell {self.rect.topleft} clicked in selection mode")
                    if sunlight_level == 0:
                        self.color = FULL_SUN_COLOR
                        self.fill = True
                        self.fullSun = True
                        self.partialShade = False 
                        self.fullShade = False
                        print("Set to Full Sun")
                    elif sunlight_level == 1:
                        self.color = PARTIAL_SHADE_COLOR
                        self.fill = True
                        self.fullSun = False
                        self.partialShade = True
                        self.fullShade = False
                        print("Set to Partial Shade")
                    elif sunlight_level == 2:
                        self.color = FULL_SHADE_COLOR
                        self.fill = True 
                        self.fullSun = False
                        self.partialShade = False 
                        self.fullShade = True
                        print("Set to Full Shade")

    def draw(self, screen):
        # give some feedback while viability draw is down
        if self.fill:
            self.count += 1
            py.draw.rect(screen, MEDIUM_GREY, self.rect)
            if self.count >= 10:
                self.fill = False
                self.count = 0
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
                py.draw.rect(screen, PURE_BLACK, self.rect, 1)
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
        self.cellNum = 0
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
                        self.cellNum = int(self.text)
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

def drawLines(self, surface, rowNum, colNum):
    #cell size is always 60 now
    #Places one line 1/3 of the way through a cell, and then a 2nd line 2/3 of the way. Continues for whole row/column
    for x in range(rowNum):
        py.draw.line(surface, DARK_GREY, py.math.Vector2(self.rectX + 20 + (60 * x - 1) , self.rectY), py.math.Vector2(self.rectX + 20 + (60 * x - 1), self.rectY + self.textbox2.direction))
        py.draw.line(surface, DARK_GREY, py.math.Vector2(self.rectX + 40 + (60 * x - 1) , self.rectY), py.math.Vector2(self.rectX + 40 + (60 * x - 1), self.rectY + self.textbox2.direction))
    for y in range(colNum):
        py.draw.line(surface, DARK_GREY, py.math.Vector2(self.rectX, self.rectY + 20 + (60 * y - 1)), py.math.Vector2(self.rectX + self.textbox1.direction, self.rectY + 20 + (60 * y - 1)))
        py.draw.line(surface, DARK_GREY, py.math.Vector2(self.rectX, self.rectY + 40 + (60 * y - 1)), py.math.Vector2(self.rectX + self.textbox1.direction, self.rectY + 40 + (60 * y - 1)))

class SunlightViabilityButton:
    def __init__(self, box_x_position, box_y_position, button_box_width, button_box_height, button_display_text):
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.button_box_width = button_box_width
        self.button_box_height = button_box_height
        self.button_display_text = button_display_text
        self.font = py.font.SysFont('georgia', 16)
        
        self.sunlight_levels = ["Full Sun", "Partial Shade", "Full Shade"]
        self.selected_sunlight_level = 0
        
    def render(self, surface):
        sunlight_button_rect = py.Rect(self.box_x_position, self.box_y_position, self.button_box_width, self.button_box_height)
        
        if self.selected_sunlight_level == 0:
            sunlight_button_color = FULL_SUN_COLOR
        elif self.selected_sunlight_level == 1:
            sunlight_button_color = PARTIAL_SHADE_COLOR
        else:
            sunlight_button_color = FULL_SHADE_COLOR

        py.draw.rect(surface, sunlight_button_color, sunlight_button_rect, border_radius=20)
        sunlight_button_text = self.font.render("Sunlight Level", True, PURE_BLACK)
        sunlight_button_text_rect = sunlight_button_text.get_rect(center=sunlight_button_rect.center)
        surface.blit(sunlight_button_text, sunlight_button_text_rect)

        selected_text = self.sunlight_levels[self.selected_sunlight_level]
        sunlight_level_text = self.font.render(selected_text, True, PURE_BLACK)
        sunlight_level_text_rect = sunlight_level_text.get_rect(center=(self.box_x_position + self.button_box_width // 2, self.box_y_position + self.button_box_height + 10))
        surface.blit(sunlight_level_text, sunlight_level_text_rect)


    def set_sunlight_level(self):
        self.selected_sunlight_level = (self.selected_sunlight_level + 1) % 3

    def get_sunlight_level(self):
        return self.sunlight_levels[self.selected_sunlight_level]
        
    def check_button_click(self, mouse_position):
        x, y = mouse_position
        if((self.box_x_position <= x <= self.box_x_position + self.button_box_width) and (self.box_y_position <= y <= self.box_y_position + self.button_box_height)):
            return True
        return False

class SoilMoistureButton:
    def __init__(self, box_x_position, box_y_position, button_box_width, button_box_height, button_display_text):
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.button_box_width = button_box_width
        self.button_box_height = button_box_height
        self.button_display_text = button_display_text
        self.font = py.font.SysFont('georgia', 16)
        
        self.water_levels = ["Normal Drainage", "Dry Soil"]
        self.selected_water_level = 0
        
    def render(self, surface):
        water_level_rect = py.Rect(self.box_x_position, self.box_y_position, self.button_box_width, self.button_box_height)
        
        if self.selected_water_level == 0:
            water_button_color = NORMAL_SOIL_MOISTURE_COLOR
        else:
            self.selected_water_level == 1
            water_button_color = PARTIAL_SHADE_COLOR

        py.draw.rect(surface, water_button_color, water_level_rect, border_radius=20)
        water_button_text = self.font.render("Soil Moisture", True, PURE_BLACK)
        water_button_text_rect = water_button_text.get_rect(center=water_level_rect.center)
        surface.blit(water_button_text, water_button_text_rect)

        selected_text = self.water_levels[self.selected_water_level]
        water_level_text = self.font.render(selected_text, True, PURE_BLACK)
        water_level_text_rect = water_level_text.get_rect(center=(self.box_x_position + self.button_box_width // 2, self.box_y_position + self.button_box_height + 10))
        surface.blit(water_level_text, water_level_text_rect)

    def set_water_level(self):
        self.selected_water_level = (self.selected_water_level + 1) % 2

    def get_sunlight_level(self):
        return self.water_levels[self.selected_water_level]
        
    def check_button_click(self, mouse_position):
        x, y = mouse_position
        if((self.box_x_position <= x <= self.box_x_position + self.button_box_width) and (self.box_y_position <= y <= self.box_y_position + self.button_box_height)):
            return True
        return False


