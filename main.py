import logging
import os.path as path
import platform
import shutil
import assets
import scenes

import pygame
from stockfish import Stockfish


class Game:
    def __init__(self) -> None:
        from scenes import Scene

        # Is the game running?
        self.running: bool = False
        # The current scene being rendered
        self._scene: Scene = None
        # Screen used by pygame
        self.screen: pygame.Surface = None
        # Clock used by pygame
        self.clock: pygame.time.Clock = None
        # Textures
        self.textures = assets.Textures()

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, scene):
        if self._scene is not None:
            self._scene.dispose()
        self._scene = scene
        if self._scene is not None:
            self._scene.init()

    def init(self):
        """
        Initializes Window
        """
        from scenes.mainmenu import MainMenu

        try:
            self.textures = assets.Textures()
        except Exception as e:
            logging.error(
                "Unable to load required textures for the game: " + e.__str__()
            )
            exit(1)
            return
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = MainMenu(self)

    def events(self):
        """
        Runs PyGame events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.scene is None:
                continue
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                button = event.button
                self.scene.on_mouse_button_up(event, pos, button)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button = event.button
                self.scene.on_mouse_button_down(event, pos, button)

    def loop(self):
        """
        Run game logic
        """
        if self.scene is not None:
            self.scene.loop()

    def render(self):
        """
        Renders game
        """
        self.screen.fill("black")
        if self.scene is not None:
            self.scene.render(self.screen)
        pygame.display.flip()

    def clean(self):
        """
        Disposing game
        """
        pygame.quit()


def try_installing_stockfish():
    """
    Installs Stockfish
    """
    if path.isfile("./stockfish"):
        return
    logging.info("Stockfish was not found, installing it...")
    sys = platform.system()
    if sys == "Windows":
        shutil.copy(
            "./stockfish_versions/stockfish-windows-2022-x86-64-modern.exe",
            "stockfish",
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


def main():
    """
    Entry point of game
    """
    game = Game()
    game.init()
    while game.running:
        game.events()
        game.loop()
        game.render()
        game.clock.tick(60)
    game.clean()


if __name__ == "__main__":
    main()
