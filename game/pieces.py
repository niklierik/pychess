import enum


class PieceColor(enum.Enum):
    WHITE = 0
    BLACK = 1


class Piece:
    def __init__(self, color: PieceColor) -> None:
        self.pos = (0, 0)
        self.color = color
