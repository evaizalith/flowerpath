import pygame as py
from flower_placeholder import Flower


class FlowerSelectionUI:
    def __init__(self, position=(50,50)):
        self.flowers = [Flower("Calendula"), Flower("Zinna"), Flower("Foxglove"), Flower("Nasturtium"), Flower("Annual Phlox"), Flower("Viola"), Flower("Snapdragon"), Flower("Cosmos"), Flower("Sweet Pea"), Flower("Baby's Breath"), Flower("Marigold"), Flower("Milkweed"), Flower("Larkspur"), Flower("Bleeding Heart"), Flower("Hostas"), Flower("Coral Bells")]
        self.position = position
        self.window_x_size = 50
        self.window_y_size = 50

    #This is the thing you call to get it on the main page
    def render(self, surface):
        font = py.font.Font(None, 24) 
        for i, flower in enumerate(self.flowers):
            flower_x_position = self.window_x_size
            flower_y_position = self.window_y_size + i * 30
            button = CertainFlowerButton(flower, flower_x_position, flower_y_position)
            button.render(surface)


class CertainFlowerButton: 
    def __init__(self, flower, button_x_position, button_y_position):
        self.flower = flower
        self.button_x_position = button_x_position
        self.button_y_position = button_y_position
        self.font = py.font.Font(None, 24)

    def render(self, surface):
        button_surface = self.font.render(self.flower.name, True, (0, 0, 0))
        button_rectangle = button_surface.get_rect(topleft=(self.button_x_position, self.button_y_position))
        surface.blit(button_surface, button_rectangle) 

