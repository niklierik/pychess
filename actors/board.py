from actors.actor import Actor
from actors.tile import Tile
import pygame
import typing
import game.color
import game.side

Color = game.color.PieceColor
Side = game.side.Side


class Board(Actor):
    def __init__(self, scene, perspective=Color.WHITE, width=8, height=8) -> None:
        super().__init__(scene)
        self.tiles: list[Tile] = []
        self.width = width
        self.height = height
        self._perspective = perspective

    @property
    def perspective(self):
        return self._perspective

    @perspective.setter
    def perspective(self, perspective: Color):
        from game.pieces import Piece

        self._perspective = perspective
        pieces: list[typing.Union[None, Piece]] = list(
            [None] * (self.width * self.height)
        )
        pieces = list(map(lambda tile: tile.piece, self.tiles))
        pieces.reverse()
        for tile in self.tiles:
            tile.refresh_texture()
            p = pieces[tile.index]
            tile.piece = p
            if p is not None:
                p.tile = tile

    def init(self):
        # got mixed up with the indicies and coordinates, therefore i pre-allocate the array and then fill up with the correct index-position pair
        self.tiles = [None] * 64  # type: ignore
        for x in range(0, 8):
            for y in range(0, 8):
                index = self.index(x, y)
                if index is None:
                    raise Exception("Shouldn't be possible")
                tile = Tile(self.scene, self, index, x, y, (50, (1080 - 64 * 8) // 2))
                self.tiles[index] = tile  # type: ignore
                tile.init()
        self.add_pieces()
        super().init()

    def add_pieces(self):
        import game.pieces

        pieces: list[game.pieces.Piece] = []
        for color in [Color.WHITE, Color.BLACK]:
            for file in range(0, 8):
                pieces.append(game.pieces.Pawn(self, color, file))
            for side in [Side.QUEEN, Side.KING]:
                pieces.append(game.pieces.Rook(self, color, side))
                pieces.append(game.pieces.Knight(self, color, side))
                pieces.append(game.pieces.Bishop(self, color, side))
            pieces.append(game.pieces.King(self, color))
            pieces.append(game.pieces.Queen(self, color))
        for piece in pieces:
            # registering the pieces to the board
            piece.tile._piece = piece  # type: ignore

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
