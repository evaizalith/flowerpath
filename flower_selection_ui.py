import pygame as py
from dbManager import databaseManager
from file_print_functions import writeToCsvFile, addToTxtFile
from plant import Plant
from constants_config import *

#Controls the left UI bar containing Flower Selection Buttons 
class FlowerSelectionUI:
    def __init__(self, position=(50,50), dp_path="test"):
        self.db_manager_connection_success = False
        self.buttons = []
        self.position = position
        self.window_x_size = 20
        self.window_y_size = 40
        self.button_vertical_spacing = 60
        self.column_separation_margin = 60
        self.font = py.font.Font(None, 24)
        self.hovered_flower = None
        self.flower_information_box = None
        self.user_selected_flower = None

        self.db_manager = databaseManager("test")

        success, err = self.db_manager.connect()

        if not success:
            self.db_manager_connection_success = False
            print(f"Error connecting to database: {err}")

            #Crash gracefully by providing an error log
            addToTxtFile(f"Error Log", f"Database connection error: {err} \n")
            
        else: 
            print("Connected to database successfully")
            self.db_manager_connection_success = True
            self.flowers = self.load_flowers_from_database() 

    def render(self, surface, mouse_position, mouse_click):
        font = py.font.Font(None, 24)
        first_column = len(self.flowers) // 2
        
        #Renders first column of flower selection buttons 
        for i, flower in enumerate(self.flowers[:first_column]):
            flower_x_position = self.window_x_size
            flower_y_position = self.window_y_size + i * self.button_vertical_spacing
            button = CertainFlowerButton(flower, flower_x_position, flower_y_position)
            button.render(surface)

            if button.check_if_hovered(mouse_position):
                self.hovered_flower = flower
                button.set_hovered(True)
            else:
                button.set_hovered(False)

            #Return flower object when user clicks on that flower's selection buttons 
            get_selected_flower = button.get_flower(mouse_position, mouse_click)
            if get_selected_flower:
                self.user_selected_flower = get_selected_flower  

        #Renders second column of flower selection buttons 
        for i, flower in enumerate(self.flowers[first_column:]):
            flower_x_position = self.window_x_size + self.column_separation_margin
            flower_y_position = self.window_y_size + i * self.button_vertical_spacing
            button = CertainFlowerButton(flower, flower_x_position, flower_y_position)
            button.render(surface)
        
            if button.check_if_hovered(mouse_position):
                self.hovered_flower = flower
                button.set_hovered(True)
            else:
                button.set_hovered(False)
                
            get_selected_flower = button.get_flower(mouse_position, mouse_click)
            if get_selected_flower:
                self.user_selected_flower = get_selected_flower

        #Display flower information page 
        if self.hovered_flower:
            self.flower_information_box = FlowerInformationBox(surface, self.hovered_flower)
            self.flower_information_box.is_visible = True
            self.flower_information_box.render(surface)

    #Getter for user selected 
    def get_current_flower(self):
        retrieved_flower = self.user_selected_flower
        self.user_selected_flower = None
        return retrieved_flower
    
    #Closes information box
    def click_to_close(self, mouse_position):
        isClosed = False
        if (self.flower_information_box != None) and self.flower_information_box.is_visible:
            if self.flower_information_box.check_exit_button_click(mouse_position):
                self.flower_information_box.is_visible = False
                self.hovered_flower = None
                isClosed = True
        return isClosed

    def load_flowers_from_database(self):
        flowers = []
        if self.db_manager_connection_success:
            all_flowers, err = self.db_manager.fetch_all()
            if err:
                print(f"Error fetching flowers from database: {err}")
            elif len(all_flowers) == 0:
                print(f"No flowers were retreived from the database")
                print("Loading Default database...")
                self.db_manager.loadDefaultDatabase()
                all_flowers, err = self.db_manager.fetch_all()
                if err:
                    print(f"Error fetching flowers from database: {err}")
            else:
                for flower in all_flowers:
                    name = flower[1]
                    max_height = flower[2]
                    max_size = flower[3]
                    germination_time = flower[4]
                    mature_time = flower[5]
                    bloom_time = flower[6]
                    bloom_start = flower[7]
                    bloom_end = flower[8]
                    full_sun = flower[9]
                    partial_shade = flower[10] 
                    full_shade = flower[11]
                    drought_tolerant = flower[12]
                    overwater_sensitive = flower[13]
                    color = flower[14]
                    perennial = flower[15]
                    texture1 = flower[16]
                    texture2 = flower[17]
                    texture3 = flower[18]
                    plant = Plant(name, max_height, max_size, germination_time, mature_time, bloom_time, bloom_start, bloom_end, full_sun, partial_shade, full_shade, drought_tolerant, overwater_sensitive, color, perennial, texture1, texture2, texture3)
                    flowers.append(plant)
        return flowers
    
#Creates each individual flower button 
class CertainFlowerButton: 
    #Dictionary as image cache
    image_cache = {}

    def __init__(self, flower, button_x_position, button_y_position):
        self.flower = flower
        self.button_x_position = button_x_position
        self.button_y_position = button_y_position
        self.button_width = BUTTON_SIZE
        self.button_height = BUTTON_SIZE
        self.font = py.font.Font(None, 24)
        self.texture1 = flower.texture1
        self.is_button_clicked = False
        self.image = None
        self.is_hovered = False
        self.button_width_offset = 5
        self.button_height_offset = 10

        if self.texture1 in self.image_cache:
            self.image = self.image_cache[self.texture1]
        else:
            self.image = py.image.load(self.texture1).convert_alpha()
            self.image = py.transform.scale(self.image, (self.button_width, self.button_height))
            self.image_cache[self.texture1] = self.image  

    def render(self, surface):
        menu_background_surface = py.Rect(self.button_x_position - self.button_width_offset, self.button_y_position - self.button_width_offset, self.button_width + self.button_height_offset, self.button_height + self.button_height_offset)
        menu_background_color = WARM_DARK_BROWN
        py.draw.rect(surface, menu_background_color, menu_background_surface, border_radius=10)

        button_rectangle_surface = py.Rect(self.button_x_position, self.button_y_position, self.button_height, self.button_width)
        button_background_color = WARM_DARK_BROWN
        py.draw.rect(surface, button_background_color, button_rectangle_surface, border_radius=10)

        if self.image:
            surface.blit(self.image, (self.button_x_position, self.button_y_position))
    
    def check_if_hovered(self, mouse_position):
        x, y = mouse_position
        is_hovered = (self.button_x_position < x < self.button_x_position + self.button_width) and (self.button_y_position < y < self.button_y_position + self.button_height)
        return is_hovered 
    
    #Select flower user is hovered over 
    def set_hovered(self, hovered):
        self.is_hovered = hovered
    
    def get_flower(self, mouse_position, mouse_click):
        if self.check_if_hovered(mouse_position) and mouse_click:
            return self.flower
        return None


class FlowerInformationBox:
    def __init__(self, surface, hovered_flower, 
                 box_x_position=INFO_BOX_SPECS["x"], 
                 box_y_position=INFO_BOX_SPECS["y"], 
                 outline_width=INFO_BOX_SPECS["outline"], 
                 info_box_width=INFO_BOX_SPECS["w"], 
                 info_box_height=INFO_BOX_SPECS["h"]):
        self.info_box_width = info_box_width
        self.info_box_height = info_box_height
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.outline_width = outline_width
        self.inner_box_offset = 2 * outline_width  
        self.font = py.font.Font(None, 24)
        self.hovered_flower = hovered_flower
        self.is_visible = False 
        
    def render(self, surface):
        if not self.is_visible:
            return 
        
        info_box_background = py.Rect(self.box_x_position, self.box_y_position, self.info_box_width, self.info_box_height)
        info_background_color = WARM_DARK_BROWN
        py.draw.rect(surface, info_background_color, info_box_background, border_radius=10)
            
        info_box_surface = py.Rect(self.box_x_position + self.outline_width, self.box_y_position + self.outline_width, self.info_box_width - self.inner_box_offset, self.info_box_height - self.inner_box_offset)
        info_box_surface_color = LIGHT_BLUE
        py.draw.rect(surface, info_box_surface_color, info_box_surface, border_radius=10)

        info_box_text = self.font.render(self.hovered_flower.name, True, (0, 0, 0))
        info_box_text_surface = info_box_text.get_rect(center=info_box_surface.center)
        surface.blit(info_box_text, info_box_text_surface)

        exit_button_surface = py.Rect(self.box_x_position + self.info_box_width - 25, self.box_y_position + 5, 20, 20)
        exit_button_surface_color = EXIT_BUTTON_RED
        exit_button_text = self.font.render("X", True, (0, 0, 0))
        exit_button_text_surface = exit_button_text.get_rect(center=exit_button_surface.center)

        py.draw.rect(surface, exit_button_surface_color, exit_button_surface, border_radius=2)
        surface.blit(exit_button_text, exit_button_text_surface)

    def check_exit_button_click(self, mouse_position):
        x, y = mouse_position
        if((self.box_x_position + self.info_box_width - 25 <= x <= self.box_x_position + self.info_box_width) and (self.box_y_position + 5 <= y <= self.box_y_position + 25)):
            return True
        return False

#Actual spawnable flower image     
class gardenFlower:
    image_cache = {}
    
    def __init__(self, x, y, flower):
        self.minSize = 15
        self.flower = flower
        maxSize = (flower.maxHeight/12) * 60
        self.maxRect = py.Rect(x, y, maxSize, maxSize)
        self.rect = py.Rect(self.maxRect.x + (self.maxRect.width/2) - (self.minSize/2), self.maxRect.y + (self.maxRect.height/2) - (self.minSize/2), self.minSize, self.minSize)
        self.isMoving = False
        self.offsetX = 0
        self.offsetY = 0
        self.collide = False
        self.image = None
        self.deleteMark = False
        self.texture1 = "images/Generic/seed.jpg"
        print("created flower object")

        if self.texture1 in self.image_cache:
            self.image = self.image_cache[self.texture1]
        else:
            self.image = py.image.load(self.texture1).convert_alpha()
            self.image = py.transform.scale(self.image, (self.rect.width, self.rect.height))
            self.image_cache[self.texture1] = self.image  

    def handleEvent(self, event):
        if event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                # check for mouse collision, then save offsets for later
                if self.rect.collidepoint(event.pos):
                    self.isMoving = True
                    mouseX, mouseY = event.pos
                    self.offsetX = self.rect.x - mouseX
                    self.offsetY = self.rect.y - mouseY
            if event.button == 2:
                # deletes on middle mouse
                if self.rect.collidepoint(event.pos):
                    self.deleteMark = True

        elif event.type == py.MOUSEBUTTONUP:
            if event.button == 1:
                self.isMoving = False

        if event.type == py.MOUSEMOTION:
            # offset keeps rectangle centered and not moving unpredictably
            if self.isMoving:
                mouseX, mouseY = event.pos
                self.rect.x = mouseX + self.offsetX
                self.rect.y = mouseY + self.offsetY
                self.maxRect.x = self.rect.x - (self.maxRect.width/2) + (self.rect.width/2)
                self.maxRect.y = self.rect.y - (self.maxRect.height/2) + (self.rect.height/2)

    def draw(self, screen):
        if self.collide:
            py.draw.rect(screen, BRIGHT_RED, self.maxRect, 1)
        else:
            py.draw.rect(screen, MEDIUM_BLUE, self.maxRect, 1)
        py.draw.rect(screen, MEDIUM_GREEN, self.rect)

        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, days):
        # calculates growth, gets percentage grown from plant.py's growth function
        size = self.flower.getHeight(days)
        growthPercent = size/self.flower.maxHeight
        pxSize = (self.flower.maxHeight/12) * FEET_TO_PIXELS # 1 ft = 60 px
        pxSize = growthPercent * pxSize
        # minimum 15 square pixels for easier dragging
        if pxSize < 15:
            pxSize = 15
        # variable for keeping track of updating image for performance
        # only update image if rectangle changes in size or stage
        rectChange = False
        if not pxSize == self.rect.width:
            rectChange = True
            self.rect.width = pxSize
            self.rect.height = pxSize
        
        #recenters the max rectangle to the new plant rectangle size
        self.rect.x = self.maxRect.x + (self.maxRect.width/2) - (self.rect.width/2)
        self.rect.y = self.maxRect.y + (self.maxRect.height/2) - (self.rect.height/2)

        """ Keeps track of what image the flower should display
            Compares the current day of the program (days) to each flower's unique growing stages
            Flowers start as seeds, and remain seeds until reaching germination time
            Flowers become sprouts after reaching germination time, and remain so until mature time
            Both the seed and sprout images are the same for all flowers
            Once the flower has matured, it displays a unique bloom image for its bloomTime
            After that, the generic sprout is displayed again"""
        if days <= self.flower.germinationTime:
            self.texture1 = "images/Generic/seed.jpg"
            rectChange = True
        elif days <= self.flower.matureTime:
            self.texture1 = "images/Generic/sprout.jpg"
            rectChange = True

        if days > self.flower.matureTime and days <= (self.flower.matureTime + self.flower.bloomTime):
            self.texture1 = self.flower.texture1
        if days > (self.flower.matureTime + self.flower.bloomTime):
            self.texture1 = "images/Generic/sprout.jpg"
            rectChange = True

        # Caches certain flower textures to improve performance
        if self.texture1 in self.image_cache:
            self.image = self.image_cache[self.texture1]
        # changes chache if rectChange is true
        if rectChange:
            self.image = py.image.load(self.texture1).convert_alpha()
            self.image = py.transform.scale(self.image, (self.rect.width, self.rect.height))
            self.image_cache[self.texture1] = self.image  


class timelineSlider:
    def __init__(self, x, y, size):
        self.rect = py.Rect(x - (size/2), y + (size/2), size, size)
        self.isMoving = False
        self.offsetX = 0
        self.offsetY = 0

    def handleEvent(self, event):
    # Very similar to flowers, but only moves on x axis
        if event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.isMoving = True
                    mouseX, mouseY = event.pos
                    self.offsetX = self.rect.x - mouseX

        elif event.type == py.MOUSEBUTTONUP:
            if event.button == 1:
                self.isMoving = False

        if event.type == py.MOUSEMOTION:
            if self.isMoving:
                mouseX, mouseY = event.pos
                self.rect.x = mouseX + self.offsetX
                if self.rect.x < 170:
                    self.rect.x = 170
                if self.rect.x > 770:
                    self.rect.x = 770

    def draw(self, screen):
        if self.isMoving:
            py.draw.rect(screen, LIGHT_BLUE, self.rect)
        else:
            py.draw.rect(screen, MEDIUM_BLUE, self.rect)

    # for calculating the day from the slider's position
    def calculateDay(self):
        growPercent = ((self.rect.x - 170) / 600)
        days = round(growPercent * 365)
        return days
    
    # for calculating the slider's position from the days
    # called when buttons are clicked
    def calculatePosition(self, days):
        sliderPercent = days/365
        self.rect.x = 170 + round(sliderPercent * 600)

    


