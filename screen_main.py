import pygame as py 
from abstract_screen import GameState
from flower_placeholder import Flower
from flower_selection_ui import FlowerSelectionUI
from garden_ui import ClickBox, TextBox, rescale, rescaleCellNum

class MainPage(GameState):
    #Another instance of a gamestate object 
    def __init__(self):
        super(MainPage, self).__init__()
        self.next_state = "TITLE"
        self.flower_selection_ui = FlowerSelectionUI(position=(100, 200))
        self.rectX = 250
        self.rectY = 100
        self.rectSizeX = 500
        self.rectSizeY = 200
        
        self.textbox1 = TextBox(200, 50, 140, 32, self.rectSizeX)
        self.textbox2 = TextBox(390, 50, 140, 32, self.rectSizeY)
        self.textboxes = [self.textbox1, self.textbox2]
        self.cells = []
        self.rowNum = 5
        self.colNum = 5
        rescale(self.rowNum, self.colNum, self.cells)

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

        for box in self.textboxes:
            box.handleEvent(event)
            box.update()
            if box.rescaleToggle:
                rescaleCellNum(self.rowNum, self.colNum, self.cells)
        for cell in self.cells:
            cell.handleEvent(event)
        if event.type == py.KEYDOWN:
            if event.key == py.K_UP:
                if(self.colNum > 1):
                    self.colNum -= 1
                    rescale(self.rowNum, self.colNum, self.cells)
            if event.key == py.K_DOWN:
                if(self.colNum < 8):
                    self.colNum += 1
                    rescale(self.rowNum, self.colNum, self.cells)
            if event.key == py.K_LEFT:
                if(self.rowNum > 1):
                    self.rowNum -= 1
                    rescale(self.rowNum, self.colNum, self.cells)
            if event.key == py.K_RIGHT:
                if(self.rowNum < 8):
                    self.rowNum += 1
                    rescale(self.rowNum, self.colNum, self.cells)
            #self.persist["screen_color"] = "forestgreen"
            #self.done = True
    
    def draw(self, surface):
        surface.fill(self.screen_color)
        surface.blit(self.text, self.title_rect)
        for box in self.textboxes:
            box.draw(surface)
        py.draw.rect(surface, (0, 0, 0), [self.rectX, self.rectY, self.textbox1.direction, self.textbox2.direction], 2)
        for cell in self.cells:
            cell.draw(surface)
        mouse_position = py.mouse.get_pos()
        self.flower_selection_ui.render(surface, mouse_position)
            