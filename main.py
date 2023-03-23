import logging
import os.path as path
import platform
import shutil

import pygame
from stockfish import Stockfish

from scenes.mainmenu import MainMenu
from scenes.scene import Scene

# Is the game running?
running: bool = False
# The current scene being rendered
_scene: Scene = None
# Screen used by pygame
screen: pygame.Surface = None
# Clock used by pygame
clock: pygame.time.Clock = None

def set_scene(scene: Scene):
    global _scene
    if _scene is not None:
        _scene.dispose()
    _scene = scene
    if _scene is not None:
        _scene.init()


def init():
    """ 
    Initializes Window
    """

    global screen
    global clock
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    pygame.init()
    running = True


def events():
    """ 
    Runs PyGame events
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
        if _scene is None:
            continue
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            button = event.button
            _scene.on_mouse_button_up(event,pos, button)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            button = event.button
            _scene.on_mouse_button_down(event,pos,button)

def loop():
    """ 
    Run game logic
    """
    global _scene
    if _scene is not None:
        _scene.loop()


def render():
    """ 
    Renders game
    """
    global screen
    global _scene
    screen.fill("black")
    if _scene is not None:
        _scene.render()
    pygame.display.flip()


def try_installing_stockfish():
    """ 
    Installs Stockfish
    """
    if (path.isfile("./stockfish")):
        return
    logging.info("Stockfish was not found, installing it...")
    sys = platform.system()
    if sys == "Windows":
        shutil.copy(
            "./stockfish_versions/stockfish-windows-2022-x86-64-modern.exe", "stockfish"
        )
        logging.info("Installed Windows version of stockfish.")
        return
    if sys == "Linux":
        shutil.copy(
            "./stockfish_versions/stockfish-ubuntu-20.04-x86-64-modern", "stockfish"
        )
        logging.info("Installed Ubuntu version of stockfish.")
        return
    if sys == "Darwin":
        raise Exception(
            "Stockfish needs to be manually installed and placed into the game's folder on MacOS. Please download Stockfish and install the binary next to main.py as 'stockfish' without any extension. More info in 'stockfish_versions/readme.txt'."
        )
    raise Exception(
        "Stockfish cannot be installed. Please download Stockfish and install the binary next to main.py as 'stockfish' without any extension. More info in 'stockfish_versions/readme.txt'."
    )


def clean():
    """ 
    Disposing game
    """
    pygame.quit()


def main():
    """ 
    Entry point of game
    """
    init()
    while running:
        events()
        loop()
        render()
        clock.tick(60)
    clean()


if __name__ == "__main__":
    main()
