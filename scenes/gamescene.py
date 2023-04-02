from scenes.scene import Scene


class GameScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

    def init(self):
        from actors.board import Board
        from actors.button import Button

        self.board = Board(self)
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

    def on_change_perspective(self, _):
        self.board.perspective = self.board.perspective.opposite()
        if self.board.selected is None:
            return
        self.board.selected.selected = False
        self.board.selected = None
        for tile in self.board.tiles:
            tile.can_move_there = False
