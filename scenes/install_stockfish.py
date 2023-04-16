from actors.button import Button
from actors.text import Text
from scenes.scene import Scene
import pygame


class InstallStockfishScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

    def init(self):
        self.actors.append(
            Text(
                self,
                "Stockfish is not installed!",
                "white",
                "black",
                pygame.Rect(20, 20, 700, 50),
            )
        )
        self.actors.append(
            Text(
                self,
                "Please read the README.md file for more info.",
                "white",
                "black",
                pygame.Rect(20, 100, 700, 20),
            )
        )
        icons = self.game.assets.textures.buttons.icons
        self.actors.append(
            Button(
                self,
                (20, 150),
                (64, 64),
                icons.close,
                icons.hover.close,
                icons.on_pressed.close,
                lambda _: self.game.quit(),
            )
        )
        super().init()
