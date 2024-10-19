import pygame as py 
from abstract_screen import GameState
from flower_placeholder import Flower
from flower_selection_ui import FlowerSelectionUI

class MainPage(GameState):
    #Another instance of a gamestate object 
    def __init__(self):
        super(MainPage, self).__init__()
        self.next_state = "TITLE"
        self.flower_selection_ui = FlowerSelectionUI(position=(100, 200))

    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = py.Color("white")
        text = "" 
        self.text = self.FONT.render(text, True, py.Color("gray10"))
        self.title_rect = self.text.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        if event.type == py.QUIT:
            self.quit = True
        elif event.type == py.MOUSEBUTTONDOWN:
            self.title_rect.center = event.pos
            mouse_position = py.mouse.get_pos()
            print("mouse button down detected")
            self.flower_selection_ui.click_to_close(mouse_position)
    
    def draw(self, surface):
        surface.fill(self.screen_color)
        surface.blit(self.text, self.title_rect)

        mouse_position = py.mouse.get_pos()
        self.flower_selection_ui.render(surface, mouse_position)