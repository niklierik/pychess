import enum
import actors.board


class PieceColor(enum.Enum):
    WHITE = 0
    BLACK = 1


class Piece:
    def __init__(self, board: actors.board.Board, color: PieceColor) -> None:
        self.pos = (0, 0)
        self.color = color
        self.board = board

    def available_moves(self) -> list[int]:
        return []


class Pawn(Piece):
    def __init__(self, board: actors.board.Board, color: PieceColor, file: int) -> None:
        super().__init__(board, color)
        self.pos = (file, 1 if color == PieceColor.WHITE else 6)
        self.direction = 1 if color == PieceColor.WHITE else -1

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
