import pygame as py
from flower_placeholder import Flower
from constants_config import *


class FlowerSelectionUI:
    def __init__(self, position=(50,50)):
        self.flowers = [Flower("Calendula"), Flower("Zinna"), Flower("Foxglove"), Flower("Nasturtium"), Flower("Annual Phlox"), Flower("Viola"), Flower("Snapdragon"), Flower("Cosmos"), Flower("Sweet Pea"), Flower("Baby's Breath"), Flower("Marigold"), Flower("Milkweed"), Flower("Larkspur"), Flower("Bleeding Heart"), Flower("Hostas"), Flower("Coral Bells")]
        self.position = position
        self.window_x_size = 20
        self.window_y_size = 40
        self.button_vertical_spacing = 70
        self.column_separation_margin = 70
        self.font = py.font.Font(None, 24)
        self.attached_image = py.image.load("placeholders_assets/pinkflower.jpg").convert_alpha()
        self.hovered_flower = None
        self.flower_information_box = None

    #This is the thing you call to get it on the main page
    def render(self, surface, mouse_position):
        font = py.font.Font(None, 24)
        first_column = len(self.flowers) // 2
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

        for i, flower in enumerate(self.flowers[first_column:]):
            flower_x_position = self.window_x_size + self.column_separation_margin
            flower_y_position = self.window_y_size + i * self.button_vertical_spacing
            button = CertainFlowerButton(flower, flower_x_position, flower_y_position)
            button.render(surface)
        
            if button.check_if_hovered(mouse_position):
                self.hovered_flower = flower

        if self.hovered_flower:
            self.flower_information_box = FlowerInformationBox(surface, self.hovered_flower)
            self.flower_information_box.is_visible = True
            self.flower_information_box.render(surface)

    
    def click_to_close(self, mouse_position):
        if (self.flower_information_box != None) and self.flower_information_box.is_visible:
            if self.flower_information_box.check_exit_button_click(mouse_position):
                self.flower_information_box.is_visible = False
                self.hovered_flower = None


class CertainFlowerButton: 
    def __init__(self, flower, button_x_position, button_y_position):
        self.flower = flower
        self.button_x_position = button_x_position
        self.button_y_position = button_y_position
        self.button_width = 55
        self.button_height = 55
        self.font = py.font.Font(None, 24)
        self.image = None
        self.image_path = "placeholders_assets/pinkflower.jpg"
        self.is_button_clicked = False
        self.is_hovered = False
        self.button_width_offset = 5
        self.button_height_offset = 10

        if self.image_path:
            self.image = py.image.load(self.image_path).convert_alpha()
            self.image = py.transform.scale(self.image, (self.button_width, self.button_height))


    def render(self, surface):

        menu_background_surface = py.Rect(self.button_x_position - self.button_width_offset, self.button_y_position - self.button_width_offset, self.button_width + self.button_height_offset, self.button_height + self.button_height_offset)
        menu_background_color = WARM_DARK_BROWN
        py.draw.rect(surface, menu_background_color, menu_background_surface, border_radius=10)

        #button_text_surface = self.font.render(self.flower.name, True, (0, 0, 0))
        button_rectangle_surface = py.Rect(self.button_x_position, self.button_y_position, self.button_height, self.button_width)
        button_background_color = WARM_DARK_BROWN
        py.draw.rect(surface, button_background_color, button_rectangle_surface, border_radius=10)

        if self.image:
            surface.blit(self.image, (self.button_x_position, self.button_y_position))

        #surface.blit(button_text_surface, button_rectangle_surface) 

    def check_if_hovered(self, mouse_position):
        x, y = mouse_position
        is_hovered = (self.button_x_position < x < self.button_x_position + self.button_width) and (self.button_y_position < y < self.button_y_position + self.button_height)
        return is_hovered 
    
    def set_hovered(self, hovered):
        self.is_hovered = hovered


class FlowerInformationBox:
    def __init__(self, surface, hovered_flower, box_x_position=15, box_y_position=620, outline_width=10, info_box_width=975, info_box_height=150):
        self.info_box_width = info_box_width
        self.info_box_height = info_box_height
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.outline_width = outline_width
        self.inner_box_offset = 2 * outline_width #Accounts for margins on each side 
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
        exit_button_surface_color = (255, 81, 57)
        exit_button_text = self.font.render("X", True, (0, 0, 0))
        exit_button_text_surface = exit_button_text.get_rect(center=exit_button_surface.center)

        py.draw.rect(surface, exit_button_surface_color, exit_button_surface, border_radius=2)
        surface.blit(exit_button_text, exit_button_text_surface)

    def check_exit_button_click(self, mouse_position):
        x, y = mouse_position
        if((self.box_x_position + self.info_box_width - 25 <= x <= self.box_x_position + self.info_box_width) and (self.box_y_position + 5 <= y <= self.box_y_position + 25)):
            return True
        return False

