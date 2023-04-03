from scenes.scene import Scene
import typing
from game.color import PieceColor


class GameScene(Scene):
    def __init__(self, game, white_controller, black_controller) -> None:
        from game.controllers import Controller
        from actors.board import Board
        from actors.button import Button

        super().__init__(game)
        icons = self.game.assets.textures.buttons.icons
        self.board = Board(self)
        self.white_player: Controller = white_controller
        self.black_player: Controller = black_controller
        self.change_perspective_btn = Button(
            self,
            (self.board.bounds.right + 10, self.board.bounds.top),
            (64, 64),
            icons.refresh,
            icons.hover.refresh,
            icons.on_pressed.refresh,
            self.on_change_perspective,
        )
        self.promote_to_queen_btn = Button(
            self,
            (self.board.bounds.right + 10, self.board.bounds.top + 70),
            (64, 64),
            icons.queen,
            icons.hover.queen,
            icons.on_pressed.queen,
            lambda x: None,
        )

        self.promote_to_rook_btn = Button(
            self,
            (self.board.bounds.right + 10, self.board.bounds.top + 2 * 70),
            (64, 64),
            icons.rook,
            icons.hover.rook,
            icons.on_pressed.rook,
            lambda x: None,
        )

        self.promote_to_knight_btn = Button(
            self,
            (self.board.bounds.right + 10, self.board.bounds.top + 3 * 70),
            (64, 64),
            icons.knight,
            icons.hover.knight,
            icons.on_pressed.knight,
            lambda x: None,
        )

        self.promote_to_bishop_btn = Button(
            self,
            (self.board.bounds.right + 10, self.board.bounds.top + 4 * 70),
            (64, 64),
            icons.bishop,
            icons.hover.bishop,
            icons.on_pressed.bishop,
            lambda x: None,
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
        self.actors.extend(self.promotion_btns)
        return super().init()

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
