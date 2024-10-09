
from screen_title import TitleScreen
from screen_main import MainPage
from state_manager import Game
import pygame as py

if __name__ == "__main__":
    py.init()
    screen = py.display.set_mode((800, 600))
    states = {"TITLE": TitleScreen(),
              "MAINPAGE": MainPage()}
    game = Game(screen, states, "TITLE")
    game.run()
    py.quit()

