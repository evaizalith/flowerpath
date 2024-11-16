import pygame as py 
import state_manager as state_manager
from abstract_screen import GameState
from constants_config import *

class TitleScreen(GameState):
    #An instance of the Gamestate class that displays title page
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.FONT = py.font.SysFont('georgia', 36)
        self.title = self.FONT.render("Garden Companion Planner", True, (py.Color("black")))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "forestgreen"
        self.next_state = "MAINPAGE"

        self.image = py.image.load("images/flowertitle.png")
        self.image = py.transform.scale(self.image, (500, 500))
        self.image_rect = self.image.get_rect(center=self.screen_rect.center)
        self.image_rect.y -= 100
        self.start_button = StartButton(box_x_position=300, box_y_position=550)
        

    def get_event(self, event):
        if event.type == py.QUIT:
            self.quit = True
        elif event.type == py.MOUSEBUTTONDOWN:
            mouse_position = py.mouse.get_pos()
            if self.start_button.check_start_button_click(mouse_position):
                self.done = True

    
    def draw(self, surface):
        surface.fill(WARM_SOFT_WHITE)
        self.start_button.render(surface)
        surface.blit(self.title, self.title_rect)
        surface.blit(self.image, self.image_rect)  

        spacing_line_color = (169, 169, 169)  
        start_of_line = (self.start_button.box_x_position, self.start_button.box_y_position - 25) 
        end_of_line = (self.start_button.box_x_position + self.start_button.info_box_width, self.start_button.box_y_position - 25) 
        py.draw.line(surface, spacing_line_color, start_of_line, end_of_line, 3)  

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
    


