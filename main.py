
from screen_title import TitleScreen
from screen_main import MainPage
from state_manager import Game
from constants_config import WINDOW_SIZE_HEIGHT, WINDOW_SIZE_WIDTH
import pygame as py

if __name__ == "__main__":
    py.init()
    screen = py.display.set_mode((WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT))
    states = {"TITLE": TitleScreen(),
              "MAINPAGE": MainPage()}
    game = Game(screen, states, "TITLE")
    game.run()
    py.quit()

