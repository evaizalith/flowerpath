import pygame as py 


class Game(object):
    #single instance of this class is responsible for managing the individual gamestate

    def __init__(self, screen, states, start_state):
        self.done = False
        #The display surface that the game will be drawn on 
        self.screen = screen
        self.clock = py.time.Clock()
        self.fps = 60
        # A dictionary mapping state anems to game state objects
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        #processes events and passes them to the current state 
        for event in py.event.get():
            self.state.get_event(event)

    def flip_state(self):
        #actually switches to the next game state and passes persistant data to the new state
        current_state = self.state_name
        next_state = self.state.next_state
        #Marks the screen as NOT done before transistioning, so a return to that screen will not cause immediate exit
        self.state.done = False
        self.state_name = next_state
        self.state = self.states[self.state_name]
        self.state.startup(self.states[current_state].persist)

    def update(self, dt):
        #checks for state flip and updates the current active state
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        #draws the current state to the screen
        self.state.draw(self.screen)
        
    def run(self):
        #main game loop
        #Controls updating the game, processing events, and drawing the screen 
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            py.display.update()