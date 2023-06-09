from scenes.scene import Scene
from game.color import PieceColor
import pygame
from typing import Union


class GameScene(Scene):
    def __init__(self, game, white_controller, black_controller) -> None:
        from game.controllers import Controller, PlayerController
        from actors.board import Board
        from actors.button import Button
        from actors.text import Text

        super().__init__(game)
        icons = self.game.assets.textures.buttons.icons
        self.board = Board(self)

        self.white_player_text: Union[None, Text] = None
        self.black_player_text: Union[None, Text] = None
        self.white_player: Controller = white_controller
        self.black_player: Controller = black_controller
        self.generate_texts()
        if not isinstance(white_controller, PlayerController) and isinstance(
            black_controller, PlayerController
        ):
            self.board.perspective = PieceColor.BLACK
        self.change_perspective_btn = Button(
            self,
            (self.board.bounds.right + 80, self.board.bounds.top),
            (64, 64),
            icons.refresh,
            icons.hover.refresh,
            icons.on_pressed.refresh,
            self.on_change_perspective,
        )
        self.to_main_menu_btn = Button(
            self,
            (self.board.bounds.right + 80, self.board.bounds.top + 70),
            (64, 64),
            icons.close,
            icons.hover.close,
            icons.on_pressed.close,
            self.to_main_menu,
        )
        self.promote_to_queen_btn = Button(
            self,
            (self.board.bounds.right + 10, self.board.bounds.top),
            (64, 64),
            icons.queen,
            icons.hover.queen,
            icons.on_pressed.queen,
            lambda x: None,
        )

        self.promote_to_rook_btn = Button(
            self,
            (self.board.bounds.right + 10, self.board.bounds.top + 1 * 70),
            (64, 64),
            icons.rook,
            icons.hover.rook,
            icons.on_pressed.rook,
            lambda x: None,
        )

        self.promote_to_knight_btn = Button(
            self,
            (self.board.bounds.right + 10, self.board.bounds.top + 2 * 70),
            (64, 64),
            icons.knight,
            icons.hover.knight,
            icons.on_pressed.knight,
            lambda x: None,
        )

        self.promote_to_bishop_btn = Button(
            self,
            (self.board.bounds.right + 10, self.board.bounds.top + 3 * 70),
            (64, 64),
            icons.bishop,
            icons.hover.bishop,
            icons.on_pressed.bishop,
            lambda x: None,
        )
        self.game_over_title = Text(
            self,
            "Vége",
            "white",
            "black",
            pygame.Rect(self.board.bounds.right + 160, self.board.bounds.top, 300, 50),
        )
        self.game_over_subtitle = Text(
            self,
            "Döntetlen",
            "white",
            "black",
            pygame.Rect(
                self.board.bounds.right + 160, self.board.bounds.top + 70, 300, 20
            ),
        )

    def game_over(self):
        import chess

        board = self.board.chess_board
        outcome = board.outcome()
        assert outcome is not None
        self.actors.append(self.game_over_title)
        self.game_over_subtitle.text = (
            "Döntetlen"
            if outcome.winner is None
            else ("Fehér nyert" if outcome.winner == chess.WHITE else "Fekete nyert")
        )
        self.actors.append(self.game_over_subtitle)

    def generate_texts(self):
        from actors.text import Text

        text_pos = self.board.bounds.bottomleft
        self.white_player_text = Text(
            self,
            self.white_player.name,
            (255, 255, 255),
            None,
            pygame.Rect(
                text_pos[0], text_pos[1] + 50, len(self.white_player.name) * 20, 30
            ),
        )
        text_pos = self.board.bounds.topleft
        self.black_player_text = Text(
            self,
            self.black_player.name,
            (255, 255, 255),
            None,
            pygame.Rect(
                text_pos[0], text_pos[1] - 50, len(self.black_player.name) * 20, 30
            ),
        )

    def init(self):
        self.promotion_btns = [
            self.promote_to_queen_btn,
            self.promote_to_rook_btn,
            self.promote_to_knight_btn,
            self.promote_to_bishop_btn,
        ]
        for btn in self.promotion_btns:
            btn.hide()
        self.actors.append(self.board)
        self.actors.append(self.change_perspective_btn)
        self.actors.append(self.to_main_menu_btn)
        self.actors.extend(self.promotion_btns)
        assert self.white_player_text is not None and self.black_player_text is not None
        self.actors.append(self.white_player_text)
        self.actors.append(self.black_player_text)
        for c in self.controllers:
            c.init(self)
        super().init()

    def reverse(self):
        assert self.white_player_text is not None and self.black_player_text is not None
        a = self.white_player_text.text
        b = self.black_player_text.text
        text_pos = self.board.bounds.bottomleft
        self.white_player_text.set_text(
            b,
            pygame.Rect(text_pos[0], text_pos[1] + 50, len(b) * 20, 30),
        )
        text_pos = self.board.bounds.topleft
        self.black_player_text.set_text(
            a,
            pygame.Rect(text_pos[0], text_pos[1] - 50, len(a) * 20, 30),
        )
        # self.generate_texts()

    def loop(self, delta: float):
        super().loop(delta)
        if self.board.turn_of == PieceColor.WHITE:
            self.white_player.update(self)
        else:
            self.black_player.update(self)
        if self.board.chess_board.is_game_over():
            self.board.game_over()

    @property
    def controllers(self):
        return [self.white_player, self.black_player]

    def controller_of(self, color: PieceColor):
        return self.controllers[color.value]

    def on_change_perspective(self, _):
        self.board.perspective = self.board.perspective.opposite()
        if self.board.selected is None:
            return
        self.board.selected.selected = False
        self.board.selected = None
        for tile in self.board.tiles:
            tile.can_move_there = False

    def to_main_menu(self, _):
        from scenes.mainmenu import MainMenu

        self.game.scene = MainMenu(self.game)

    def dispose(self):
        super().dispose()
        for c in self.controllers:
            c.dispose()
