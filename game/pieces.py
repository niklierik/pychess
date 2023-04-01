import enum
import actors.board


class PieceColor(enum.Enum):
    WHITE = 0
    BLACK = 1


class Piece:
    def __init__(self, color: PieceColor) -> None:
        self.pos = (0, 0)
        self.color = color

    def available_moves(self) -> list[int]:
        return []


class Pawn(Piece):
    def __init__(self, color: PieceColor, file: int) -> None:
        super().__init__(color)
        self.pos = (file, 1 if color == PieceColor.WHITE else 6)
        self.direction = 1 if color == PieceColor.WHITE else -1

    def available_moves(self, board: actors.board.Board) -> list[int]:
        moves = []
        moves.append(board.index(self.pos[0] + self.direction, self.pos[1]))
        if self.pos[0] == (1 if self.color == PieceColor.WHITE else 6):
            moves.append(board.index(self.pos[0] + 2 * self.direction, self.pos[1]))
        return moves
