import pygame as py 
from abstract_screen import GameState
from flower_placeholder import Flower
from flower_selection_ui import FlowerSelectionUI
from garden_ui import ClickBox, TextBox, rescale, rescaleCellNum
from constants_config import *

class MainPage(GameState):
    #Another instance of a gamestate object 
    def __init__(self):
        super(MainPage, self).__init__()
        self.next_state = "TITLE"
        self.flower_selection_ui = FlowerSelectionUI(position=(100, 200))
        self.left_mouse_click = False
        self.rectX = 200
        self.rectY = 75
        self.rectSizeX = 500
        self.rectSizeY = 200
        self.user_selected_flower = None
        self.drawViable = False
        
        self.textbox1 = TextBox(200, 15, 140, 32, self.rectSizeX)
        self.textbox2 = TextBox(390, 15, 140, 32, self.rectSizeY)
        self.textboxes = [self.textbox1, self.textbox2]
        self.cells = []
        self.rowNum = 5
        self.colNum = 5
        rescale(self, self.rowNum, self.colNum, self.cells)

    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = WARM_SOFT_WHITE
        text = "" 
        self.text = self.FONT.render(text, True, py.Color("gray10"))
        self.title_rect = self.text.get_rect(center=self.screen_rect.center)

        

    def get_event(self, event):
        self.left_mouse_click = False
        if event.type == py.QUIT:
            self.quit = True
        elif event.type == py.MOUSEBUTTONDOWN:
            self.title_rect.center = event.pos
            mouse_position = py.mouse.get_pos()
            self.left_mouse_click = True
            print("mouse button down detected")

        #holds current flower selection - this is the getter
        #Returns plant object 
            user_selected_flower = self.flower_selection_ui.get_current_flower()
            if user_selected_flower:
                print(f"User selected flower on the main page: {user_selected_flower.name}")
                self.drawViable = True
                self.user_selected_flower = user_selected_flower

            isClosed = self.flower_selection_ui.click_to_close(mouse_position)
            if isClosed:
                self.drawViable = False
                self.user_selected_flower = None

        for box in self.textboxes:
            box.handleEvent(event)
            box.update()
            if box.rescaleToggle:
                rescaleCellNum(self, self.rowNum, self.colNum, self.cells)
                box.rescaleToggle = False
        for cell in self.cells:
            cell.handleEvent(event)
        if event.type == py.KEYDOWN:
            if event.key == py.K_UP:
                if(self.colNum > 1):
                    self.colNum -= 1
                    rescale(self, self.rowNum, self.colNum, self.cells)
            if event.key == py.K_DOWN:
                if(self.colNum < 8):
                    self.colNum += 1
                    rescale(self, self.rowNum, self.colNum, self.cells)
            if event.key == py.K_LEFT:
                if(self.rowNum > 1):
                    self.rowNum -= 1
                    rescale(self, self.rowNum, self.colNum, self.cells)
            if event.key == py.K_RIGHT:
                if(self.rowNum < 8):
                    self.rowNum += 1
                    rescale(self, self.rowNum, self.colNum, self.cells)

    
    def draw(self, surface):
        surface.fill(self.screen_color)
        surface.blit(self.text, self.title_rect)
        for box in self.textboxes:
            box.draw(surface)
        py.draw.rect(surface, (0, 0, 0), [self.rectX, self.rectY, self.textbox1.direction, self.textbox2.direction], 2)
        for cell in self.cells:
            if self.drawViable:
                cell.viabilityDraw(surface, self.user_selected_flower)
            else:
                cell.draw(surface)
        mouse_position = py.mouse.get_pos()
        self.flower_selection_ui.render(surface, mouse_position, self.left_mouse_click)


            