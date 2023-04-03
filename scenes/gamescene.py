from scenes.scene import Scene
import typing
from game.color import PieceColor


class GameScene(Scene):
    def __init__(self, game) -> None:
        from game.controllers import Controller, PlayerController
        from actors.board import Board

        super().__init__(game)
        self.board = Board(self)
        self.white_player: Controller = PlayerController(self.board)
        self.black_player: Controller = PlayerController(self.board)

    def init(self):
        from actors.button import Button

        icons = self.game.assets.textures.buttons.icons
        self.change_perspective_btn = Button(
            self,
            (self.board.bounds.right + 10, self.board.bounds.top),
            (64, 64),
            icons.refresh,
            icons.hover.refresh,
            icons.on_pressed.refresh,
            self.on_change_perspective,
        )
        self.actors.append(self.board)
        self.actors.append(self.change_perspective_btn)
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
