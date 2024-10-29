import pygame as py 
from constants_config import *


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
        self.idle_screen = False
        self.idle_timer = 0
        self.idle_notification_active = False
        
        self.start_button = StartButton(box_x_position=300, box_y_position=550)
        self.idle_notification = IdleNotification(box_x_position=300, box_y_position=550)

    def event_loop(self):
        #processes events and passes them to the current state 
        for event in py.event.get():
            if self.idle_screen:
                if event.type == py.QUIT:
                    self.done = True
                elif event.type == py.MOUSEBUTTONDOWN:
                    mouse_position = py.mouse.get_pos()
                    if self.start_button.check_start_button_click(mouse_position):
                        self.idle_screen = False
                        self.idle_notification_active = False
                        self.idle_timer = 0
            else:
                if event.type in (py.MOUSEMOTION, py.MOUSEBUTTONDOWN, py.KEYDOWN):
                    self.idle_timer = 0
                    self.idle_notification_active = False
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
        self.idle_timer = self.idle_timer + (dt / 1000)
        print(f"Idle Timer: {self.idle_timer:.2f} seconds")

        if self.idle_timer > TIME_TO_IDLE_WARNING:
            self.idle_notification_active = True

        if self.idle_timer > TIME_TO_TIMEOUT:
            self.idle_screen = True
            self.idle_notification_active = False

        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        #draws the current state to the screen
        self.state.draw(self.screen)

        if self.idle_notification_active:
            self.idle_notification.render(self.screen)

        if self.idle_screen:
            idle_screen_color = LIGHT_BLUE
            idle_screen_rect = self.screen.get_rect()
            py.draw.rect(self.screen, idle_screen_color, idle_screen_rect)

            self.start_button.render(self.screen)

    def run(self):
        #main game loop
        #Controls updating the game, processing events, and drawing the screen 
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            py.display.update()

class StartButton:
    def __init__(self, box_x_position=152, box_y_position=1200, info_box_width=400, info_box_height=67):
        self.info_box_width = info_box_width
        self.info_box_height = info_box_height
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.font = py.font.SysFont('georgia', 36)

    def render(self, surface):
        button_rect = py.Rect(self.box_x_position, self.box_y_position, self.info_box_width, self.info_box_height)
        button_color = MEDIUM_GREEN 
        py.draw.rect(surface, button_color, button_rect, border_radius=20)
        
        button_text = self.font.render("Start", True, WARM_SOFT_WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        surface.blit(button_text, button_text_rect)

    def check_start_button_click(self, mouse_position):
        x, y = mouse_position
        if((self.box_x_position <= x <= self.box_x_position + self.info_box_width) and (self.box_y_position <= y <= self.box_y_position + self.info_box_height)):
            return True
        return False
    
class IdleNotification:
    def __init__(self, box_x_position=152, box_y_position=1200, info_box_width=400, info_box_height=67):
        self.info_box_width = info_box_width
        self.info_box_height = info_box_height
        self.box_x_position = box_x_position
        self.box_y_position = box_y_position
        self.font = py.font.SysFont('georgia', 18)

    def render(self, surface):
        button_rect = py.Rect(self.box_x_position, self.box_y_position, self.info_box_width, self.info_box_height)
        button_color = MEDIUM_GREEN 
        py.draw.rect(surface, button_color, button_rect, border_radius=20)
        
        button_text = self.font.render("You have been idle too long. Idle timeout in 5 seconds...", True, WARM_SOFT_WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        surface.blit(button_text, button_text_rect)

    def check_start_button_click(self, mouse_position):
        x, y = mouse_position
        if((self.box_x_position <= x <= self.box_x_position + self.info_box_width) and (self.box_y_position <= y <= self.box_y_position + self.info_box_height)):
            return True
        return False
    