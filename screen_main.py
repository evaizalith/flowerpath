import pygame as py 
from abstract_screen import GameState
from flower_placeholder import Flower
from flower_selection_ui import FlowerSelectionUI, gardenFlower, timelineSlider
from garden_ui import ClickBox, TextBox, rescale, rescaleCellNum, drawLines, SunlightViabilityButton, SoilMoistureButton
from constants_config import *

class MainPage(GameState):
    #Another instance of a gamestate object 
    def __init__(self):
        super(MainPage, self).__init__()
        self.next_state = "TITLE"
        self.flower_selection_ui = FlowerSelectionUI(position=(100, 200))
        self.left_mouse_click = False
        self.rectX = 200
        self.rectY = 75
        self.rectSizeX = 540
        self.rectSizeY = 240
        self.user_selected_flower = None
        self.drawViable = False
        self.sunlight_selection_mode = False
        self.soil_moisture_selection_mode = False
        
        self.textbox1 = TextBox(200, 15, 140, 32, self.rectSizeX, "9")
        self.textbox2 = TextBox(390, 15, 140, 32, self.rectSizeY, "4")
        self.textboxes = [self.textbox1, self.textbox2]
        self.cells = []
        self.flowers = []
        self.rowNum = 9
        self.colNum = 4
        self.drawLines = True
        rescale(self, self.rowNum, self.colNum, self.cells)

        self.slider = timelineSlider(200, 665, 60)

        self.toggle = True
        self.days = 0

        timeline_button_position_y = 255
        timeline_button_x_spacing = 140
        timeline_button_y_spacing = 65
        timeline_button_position_x = WINDOW_SIZE_WIDTH - timeline_button_x_spacing
        timeline_button_width = 90
        timeline_button_height = 50

        self.minus_thirty_days_button = GenericButton(timeline_button_position_x, timeline_button_position_y, timeline_button_width, timeline_button_height, "< -30 Days")
        self.minus_seven_days_button = GenericButton(timeline_button_position_x, timeline_button_position_y + timeline_button_y_spacing, timeline_button_width, timeline_button_height, "< -7 Days")
        self.plus_seven_days_button = GenericButton(timeline_button_position_x, timeline_button_position_y + 2 * timeline_button_y_spacing, timeline_button_width, timeline_button_height, "+7 Days >")
        self.plus_thirty_days_button = GenericButton(timeline_button_position_x, timeline_button_position_y + 3 * timeline_button_y_spacing, timeline_button_width, timeline_button_height, "+30 Days >")
        self.show_day_button = ShowDayButton(self.days, timeline_button_position_x, timeline_button_position_y - timeline_button_y_spacing, timeline_button_width, timeline_button_height)

        garden_options_x_spacing = timeline_button_position_x - 15
        garden_options_width = 120
        garden_options_height = 50
        
        self.sunlight_button = SunlightViabilityButton(garden_options_x_spacing, 30, garden_options_width, garden_options_height, "Sunlight")
        self.soil_moisture_button = SoilMoistureButton(garden_options_x_spacing, 110, garden_options_width, garden_options_height, "Soil Drainage")


    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = WARM_SOFT_WHITE
        text = "" 
        self.text = self.FONT.render(text, True, py.Color("gray10"))
        self.title_rect = self.text.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        self.left_mouse_click = False
        # ends game loop and exits
        if event.type == py.QUIT:
            self.quit = True
        elif event.type == py.MOUSEBUTTONDOWN:
            self.title_rect.center = event.pos
            mouse_position = py.mouse.get_pos()
            self.left_mouse_click = True
            # Checks each add/sub days button
            # Cannot decrease below 0 or increase above 365 (1 year)
            # Updates slider position and display button
            if self.minus_thirty_days_button.check_button_click(py.mouse.get_pos()):
                self.days -= 30
                if self.days < 0:
                    self.days = 0
                self.show_day_button.update_days(self.days)
                self.slider.calculatePosition(self.days)
            if self.minus_seven_days_button.check_button_click(py.mouse.get_pos()):
                self.days -= 7
                if self.days < 0:
                    self.days = 0
                self.show_day_button.update_days(self.days)
                self.slider.calculatePosition(self.days)

            if self.plus_seven_days_button.check_button_click(py.mouse.get_pos()):
                self.days += 7
                if self.days > 365:
                    self.days = 365
                self.show_day_button.update_days(self.days)
                self.slider.calculatePosition(self.days)
            if self.plus_thirty_days_button.check_button_click(py.mouse.get_pos()):
                self.days += 30
                if self.days > 365:
                    self.days = 365
                self.show_day_button.update_days(self.days)
                self.slider.calculatePosition(self.days)

            # Buttons for adjusting sunlight and water level
            # Click on a button to select desired setting, then click]
            # on any tile in the planner to update
            if self.sunlight_button.check_button_click(py.mouse.get_pos()):
                self.sunlight_button.set_sunlight_level()
                self.sunlight_selection_mode = True
                self.soil_moisture_selection_mode = False
                #print("Sunlight selection mode is active")
            if self.soil_moisture_button.check_button_click(py.mouse.get_pos()):
                self.soil_moisture_button.set_water_level()
                self.sunlight_selection_mode = False
                self.soil_moisture_selection_mode = True

            # Cells check for clicks to be able to update
            for cell in self.cells:
                cell.handleEvent(event, self.sunlight_selection_mode, self.soil_moisture_selection_mode, self.sunlight_button.selected_sunlight_level, self.soil_moisture_button.selected_water_level)
                     

        #holds current flower selection - this is the getter
        #Returns plant object 
            user_selected_flower = self.flower_selection_ui.get_current_flower()
            if user_selected_flower:
                # drawViable enables coloring in of cells
                self.drawViable = True
                self.user_selected_flower = user_selected_flower
                if self.toggle:
                    # Creates new flower based off of user selection
                    self.flowers.append(gardenFlower(self.rectX + (self.rectSizeX/2), self.rectY + (self.rectSizeY/2), user_selected_flower))
                    self.toggle = False
                else:
                    self.toggle = True

            # for closing plant info window at bottom
            isClosed = self.flower_selection_ui.click_to_close(mouse_position)
            if isClosed:
                self.drawViable = False
                self.user_selected_flower = None
    
        #updates slider position and has it update self.days and button
        self.slider.handleEvent(event)
        self.days = self.slider.calculateDay()
        self.show_day_button.update_days(self.days)

        # textboxes check for clicks and keypresses
        for box in self.textboxes:
            box.handleEvent(event)
            # If enter was pressed on a textbox, update respective garden dimension
            if box.rescaleToggle:
                if box == self.textbox1:
                    self.rowNum = box.cellNum
                    rescale(self, self.rowNum, self.colNum, self.cells)
                    box.rescaleToggle = False
                if box == self.textbox2:
                    self.colNum = box.cellNum
                    rescale(self, self.rowNum, self.colNum, self.cells)
                    box.rescaleToggle = False
        # Move the flower, update its size, remove if necessary.
        for flower in self.flowers:
            flower.handleEvent(event)
            flower.update(self.days)
            if flower.deleteMark == True:
                self.flowers.remove(flower)
        # Change from yards to feet
        if event.type == py.KEYDOWN:
            if event.key == py.K_t:
                self.drawLines = not self.drawLines

    def draw(self, surface):
        #collision in the draw loop so its always calculated before drawing flowers
        for flower1 in self.flowers:
            flower1.collide = False
            for flower2 in self.flowers:
                if not flower1 == flower2:
                    if flower1.maxRect.colliderect(flower2.maxRect):
                        flower1.collide = True
        surface.fill(self.screen_color)
        surface.blit(self.text, self.title_rect)
        for box in self.textboxes:
            box.draw(surface)
        py.draw.rect(surface, (0, 0, 0), [self.rectX, self.rectY, self.textbox1.direction, self.textbox2.direction], 2)
        if self.drawLines:
            drawLines(self, surface, self.rowNum, self.colNum)
        for cell in self.cells:
            if self.drawViable:
                cell.viabilityDraw(surface, self.user_selected_flower)
            else:
                cell.draw(surface)
        for flower in self.flowers:
            flower.draw(surface)

        py.draw.line(surface, DARK_GREY, py.math.Vector2(200 , 725), py.math.Vector2(800, 725), 5)
        self.slider.draw(surface)

        mouse_position = py.mouse.get_pos()
        self.flower_selection_ui.render(surface, mouse_position, self.left_mouse_click)

        self.show_day_button.render(surface)
        self.show_day_button.update_days(self.days)
        self.minus_thirty_days_button.render(surface)
        self.minus_seven_days_button.render(surface)
        self.plus_seven_days_button.render(surface)
        self.plus_thirty_days_button.render(surface)
        
        self.sunlight_button.render(surface)
        self.soil_moisture_button.render(surface)

class GenericButton:
    def __init__(self, box_x_position, box_y_position, button_box_width, button_box_height, button_display_text):
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.button_box_width = button_box_width
        self.button_box_height = button_box_height
        self.button_display_text = button_display_text
        self.font = py.font.SysFont('georgia', 16)

    def render(self, surface):
        button_background_rect = py.Rect(self.box_x_position, self.box_y_position, self.button_box_width, self.button_box_height)
        button_background_color = MEDIUM_GREEN
        py.draw.rect(surface, button_background_color, button_background_rect, border_radius=20)
        button_rect = py.Rect(self.box_x_position + 5, self.box_y_position + 5, self.button_box_width - 10, self.button_box_height - 10)
        button_color = PURE_WHITE
        py.draw.rect(surface, button_color, button_rect, border_radius=20)
        
        button_text = self.font.render(self.button_display_text, True, PURE_BLACK)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        surface.blit(button_text, button_text_rect)

    def check_button_click(self, mouse_position):
        x, y = mouse_position
        if((self.box_x_position <= x <= self.box_x_position + self.button_box_width) and (self.box_y_position <= y <= self.box_y_position + self.button_box_height)):
            return True
        return False
    
class ShowDayButton:
    def __init__(self, days, box_x_position, box_y_position, button_box_width, button_box_height):
        self.days = days
        self.font = py.font.SysFont('georgia', 16)
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.button_box_width = button_box_width
        self.button_box_height = button_box_height
    def update_days(self, days):
        self.days = days
 
    def render(self, surface):
        button_background_rect = py.Rect(self.box_x_position, self.box_y_position, self.button_box_width, self.button_box_height)
        button_background_color = WARM_DARK_BROWN
        py.draw.rect(surface, button_background_color, button_background_rect, border_radius=20)
        button_rect = py.Rect(self.box_x_position + 5, self.box_y_position + 5, self.button_box_width - 10, self.button_box_height - 10)
        button_color = PURE_WHITE
        py.draw.rect(surface, button_color, button_rect, border_radius=20)

        button_text = self.font.render("Days:" + str(self.days), True, PURE_BLACK)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        surface.blit(button_text, button_text_rect)



            