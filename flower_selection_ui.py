import pygame as py
from flower_placeholder import Flower


class FlowerSelectionUI:
    def __init__(self, position=(50,50)):
        self.flowers = [Flower("Calendula"), Flower("Zinna"), Flower("Foxglove"), Flower("Nasturtium"), Flower("Annual Phlox"), Flower("Viola"), Flower("Snapdragon"), Flower("Cosmos"), Flower("Sweet Pea"), Flower("Baby's Breath"), Flower("Marigold"), Flower("Milkweed"), Flower("Larkspur"), Flower("Bleeding Heart"), Flower("Hostas"), Flower("Coral Bells")]
        self.position = position
        self.window_x_size = 20
        self.window_y_size = 20

    #This is the thing you call to get it on the main page
    def render(self, surface):
        font = py.font.Font(None, 24)
        first_column = len(self.flowers) // 2
        for i, flower in enumerate(self.flowers[:first_column]):
            flower_x_position = self.window_x_size
            flower_y_position = self.window_y_size + i * 100
            button = CertainFlowerButton(flower, flower_x_position, flower_y_position)
            button.render(surface)

        for i, flower in enumerate(self.flowers[first_column:]):
            flower_x_position = self.window_x_size + 90
            flower_y_position = self.window_y_size + i * 100
            button = CertainFlowerButton(flower, flower_x_position, flower_y_position)
            button.render(surface) 


class CertainFlowerButton: 
    def __init__(self, flower, button_x_position, button_y_position):
        self.flower = flower
        self.button_x_position = button_x_position
        self.button_y_position = button_y_position
        self.button_width = 55
        self.button_height = 55
        self.font = py.font.Font(None, 24)
        self.image = None
        self.image_path = "images\\pinkflower.jpg"

        if self.image_path:
            self.image = py.image.load(self.image_path).convert_alpha()
            self.image = py.transform.scale(self.image, (self.button_width, self.button_height))


    def render(self, surface):

        menu_background_surface = py.Rect(self.button_x_position - 5, self.button_y_position - 5, self.button_width + 10, self.button_height + 10)
        menu_background_color = (42, 42, 42) #Dark grey, Hex Code #2a2a2a
        py.draw.rect(surface, menu_background_color, menu_background_surface)

        #button_text_surface = self.font.render(self.flower.name, True, (0, 0, 0))
        button_rectangle_surface = py.Rect(self.button_x_position, self.button_y_position, self.button_height, self.button_width)
        button_background_color = (30, 14, 7) #Very dark brown, Hex Code #1e0e07
        py.draw.rect(surface, button_background_color, button_rectangle_surface, border_radius=2)

        if self.image:
            surface.blit(self.image, (self.button_x_position, self.button_y_position))

        #surface.blit(button_text_surface, button_rectangle_surface) 
        

