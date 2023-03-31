from scenes import Scene


class GameScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

    def init(self):
        from actors.board import Board

        board = Board(self)
        super().actors.append(board)
        return super().init()
