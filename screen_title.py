import pygame as py 
import state_manager as state_manager
from abstract_screen import GameState

class SplashScreen(GameState):
    #An instance of the Gamestate class that displays a main menu 
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.title = self.FONT.render("Garden Companion Planner", True, (py.Color("black")))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        #An example of storing data in the persist dictionary
        #This data can now be accessed from all screens - it is shared between all states
        self.persist["screen_color"] = "forestgreen"
        self.next_state = "GAMEPLAY"

    def get_event(self, event):
        if event.type == py.QUIT:
            self.quit = True
        elif event.type == py.MOUSEBUTTONDOWN:
            self.persist["screen_color"] = "blue"
            self.done = True

    
    def draw(self, surface):
        surface.fill(py.Color(self.persist["screen_color"]))
        surface.blit(self.title, self.title_rect)