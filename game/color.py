import enum


class PieceColor(enum.Enum):
    WHITE = 0
    BLACK = 1

    def opposite(self) -> "PieceColor":
        return PieceColor(1 - self.value)
