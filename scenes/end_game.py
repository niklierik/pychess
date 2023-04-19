from scenes.scene import Scene
from enum import Enum
from actors.board import Board
from chess import Outcome
import pygame


class EndGameScene(Scene):
    def __init__(self, game, board: Board, outcome: Outcome) -> None:
        super().__init__(game)
        self.board = board
        self.outcome = outcome

    def init(self):
        from actors.text import Text
        from actors.button import Button
        from chess import WHITE

        self.actors.append(
            Text(self, "Vége", "white", None, pygame.Rect(20, 20, 500, 40))
        )
        text = "Döntetlen."
        if self.outcome.winner is not None:
            text = (
                "Fehér" if self.outcome.winner == WHITE else "Fekete"
            ) + " nyert sakmattal."
        self.actors.append(
            Text(self, text, "white", None, pygame.Rect(20, 100, len(text) * 50, 50))
        )
        icons = self.game.assets.textures.buttons.icons
        self.actors.append(
            Button(
                self,
                (200, 20),
                (64, 64),
                icons.close,
                icons.hover.close,
                icons.on_pressed.close,
                lambda _: self.to_main_menu(),
            )
        )

    def to_main_menu(self):
        from scenes.mainmenu import MainMenu

        self.game.scene = MainMenu(self.game)
