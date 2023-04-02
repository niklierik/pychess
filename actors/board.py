from actors.actor import Actor
from actors.tile import Tile
import pygame
import typing
import game.color
import game.side

Color = game.color.PieceColor
Side = game.side.Side


class Board(Actor):
    def __init__(self, scene, width=8, height=8) -> None:
        super().__init__(scene)
        self.tiles: list[Tile] = []
        self.width = width
        self.height = height
        self.player = Color.WHITE

    def init(self):
        for index in range(0, self.width * self.height):
            xy = self.xy(index)
            if xy is None:
                raise Exception("Shouldn't be possible")
            tile = Tile(self.scene, index, xy[0], xy[1], (50, (1080 - 64 * 8) // 2))
            self.tiles.append(tile)
            tile.init()
        self.add_pieces()
        super().init()

    def add_pieces(self):
        import game.pieces

        for color in [Color.WHITE, Color.BLACK]:
            for file in range(0, 8):
                game.pieces.Pawn(self, color, file)
            for side in [Side.QUEEN, Side.KING]:
                game.pieces.Rook(self, color, side)
                game.pieces.Knight(self, color, side)
                game.pieces.Bishop(self, color, side)

    def xy(self, index: typing.Union[None, int]):
        if index is None:
            return None
        return (index % self.width, index // self.width)

    def index(self, x: int, y: int):
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return None
        return x * self.width + y

    def tile(self, index: typing.Union[None, int]):
        if index is None:
            return None
        return self.tiles[index]

    def render(self, screen):
        for tile in self.tiles:
            tile.render(screen)

    def on_window_resize(self, event: pygame.event.Event):
        for tile in self.tiles:
            tile.on_window_resize(event)

    def dispose(self):
        for tile in self.tiles:
            tile.dispose()
