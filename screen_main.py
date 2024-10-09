import pygame as py 
from abstract_screen import GameState

class MainPage(GameState):
    #Another instance of a gamestate object 
    def __init__(self):
        super(MainPage, self).__init__()
        self.next_state = "TITLE"

    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = py.Color(color)
        if color == "blue":
            text = "Plot out your garden!" 
        self.text = self.FONT.render(text, True, py.Color("gray10"))
        self.title_rect = self.text.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        if event.type == py.QUIT:
            self.quit = True
        elif event.type == py.MOUSEBUTTONDOWN:
            self.title_rect.center = event.pos
            self.persist["screen_color"] = "forestgreen"
            self.done = True
    
    def draw(self, surface):
        surface.fill(self.screen_color)
        surface.blit(self.text, self.title_rect)