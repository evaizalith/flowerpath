
from screen_title import SplashScreen
from screen_main import Gameplay
from state_manager import Game
import pygame as py

if __name__ == "__main__":
    py.init()
    screen = py.display.set_mode((800, 600))
    states = {"SPLASH": SplashScreen(),
              "GAMEPLAY": Gameplay()}
    game = Game(screen, states, "SPLASH")
    game.run()
    py.quit()