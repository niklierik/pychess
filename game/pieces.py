import enum
import actors.board
import pygame


class PieceColor(enum.Enum):
    WHITE = 0
    BLACK = 1


class Side(enum.Enum):
    QUEEN = 0
    KING = 1


class Piece:
    def __init__(self, board: actors.board.Board, color: PieceColor) -> None:
        self.pos = (0, 0)
        self.color = color
        self.board = board

    def available_moves(self) -> list[int]:
        return []

    def render(self, screen: pygame.Surface):
        ...

    @property
    def tile(self):
        return self.board.tile(self.board.index(self.pos[0], self.pos[1]))

    @property
    def game(self):
        return self.board.scene.game

    @property
    def assets(self):
        return self.game.assets

    def dispose(self):
        self.pos = (-1, -1)


class Pawn(Piece):
    def __init__(self, board: actors.board.Board, color: PieceColor, file: int) -> None:
        super().__init__(board, color)
        self.pos = (file, 1 if color == PieceColor.WHITE else 6)
        self.direction = 1 if color == PieceColor.WHITE else -1
        theme = self.assets.textures.pieces.regular
        self.original_texture = (
            theme.white.pawn if color == PieceColor.WHITE else theme.black.pawn
        )
        self.on_resize()
        if self.tile is not None:
            self.tile.piece = self

    def available_moves(self) -> list[int]:
        moves = []
        forward = self.board.index(self.pos[0] + self.direction, self.pos[1])
        forwardT = self.board.tile(forward)
        if forwardT is not None and forwardT.piece is None:
            moves.append(forward)
        if self.pos[0] == (1 if self.color == PieceColor.WHITE else 6):
            moves.append(
                self.board.index(self.pos[0] + 2 * self.direction, self.pos[1])
            )

        return moves

    def on_resize(self):
        if self.tile is not None:
            self.texture = pygame.transform.scale(
                self.original_texture, self.tile.render_bounds.size
            )

    def render(self, screen: pygame.Surface):
        if self.tile is not None:
            screen.blit(self.texture, self.tile.render_bounds.topleft)
