import pygame as py

class GameState(object):
    #An actual parent class for individual game states to inherit from

    def __init__(self):
        #Flag to signal when the state is complete and ready to transistion to the next state 
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = py.display.get_surface().get_rect()
        self.persist = {}
        self.FONT = py.font.Font(None, 24)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt):
        #Update the state. Called by the Game object once per frame
        pass

    def draw(self, surface):
        #Draws the state to the screen
        pass