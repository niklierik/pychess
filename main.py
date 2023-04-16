import json
import logging
import os.path as path
import platform
import shutil
import assets.asset

import pygame


class Game:
    def __init__(self) -> None:
        from scenes.scene import Scene

        self.load_settings()
        # Is the game running?
        self.running: bool = False
        # The current scene being rendered
        self._scene: Scene = None  # type: ignore
        # Screen used by pygame
        self.screen: pygame.Surface = None  # type: ignore
        # Clock used by pygame
        self.clock: pygame.time.Clock = None  # type: ignore

    def load_settings(self):
        try:
            with open("settings.json") as settings_f:
                self.settings = json.load(settings_f)
        except BaseException:
            self.settings = {
                "path_to_stockfish": "./stockfish",
                "player_name": "Player",
            }
        with open("settings.json", "w") as settings_f:
            json.dump(self.settings, settings_f)

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

    @property
    def path_to_stockfish(self) -> str:
        return self.settings["path_to_stockfish"]

    @property
    def player_name(self) -> str:
        return self.settings["player_name"]

    def init(self):
        """
        Initializes Window
        """
        from scenes.mainmenu import MainMenu
        from scenes.viewport import Viewport

        pygame.init()
        try:
            self.assets = assets.asset.Assets()
        except Exception as e:
            logging.error(
                "Unable to load required textures for the game: " + e.__str__()
            )
            exit(1)
            return
        pygame.display.set_caption("PyChess")
        pygame.display.set_icon(self.assets.textures.icon)
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE, vsync=1)
        self.viewport = Viewport(pygame.display.get_window_size())
        self.clock = pygame.time.Clock()
        self.running = True
        if not path.exists(self.path_to_stockfish):
            from scenes.install_stockfish import InstallStockfishScene

            self.scene = InstallStockfishScene(self)
            return
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
            if (
                event.type == pygame.WINDOWRESIZED
                or event.type == pygame.WINDOWRESTORED
                or event.type == pygame.WINDOWEXPOSED
            ):
                size = pygame.display.get_window_size()
                event.x = size[0]
                event.y = size[1]
                self.scene.on_window_resize(event)
                self.viewport.screen_size = (event.x, event.y)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                button = event.button
                self.scene.on_mouse_button_up(event, pos, button)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button = event.button
                self.scene.on_mouse_button_down(event, pos, button)

    def loop(self, delta: float):
        """
        Run game logic
        """
        if self.scene is not None:
            self.scene.loop(delta)

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
        if self.scene is not None:
            try:
                self.scene.dispose()
            except Exception as e:
                logging.error("Error happened while disposing game: " + e.__str__())
        pygame.quit()

    def quit(self):
        self.running = False


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
    delta = 0
    while game.running:
        game.events()
        game.loop(delta / 1000.0)
        game.render()
        delta = game.clock.tick(60)
    game.clean()
    exit(0)


if __name__ == "__main__":
    main()
