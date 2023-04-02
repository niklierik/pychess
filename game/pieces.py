import actors.board
import pygame
import typing
import game.color
import game.side

Side = game.side.Side
Color = game.color.PieceColor


class Piece:
    def __init__(self, board: actors.board.Board, color: Color) -> None:
        self.pos = (0, 0)
        self.color = color
        self.board = board
        self.original_texture: typing.Union[None, pygame.Surface] = None

    def add_to_board(self, board: actors.board.Board):
        if self.tile is not None:
            self.tile.piece = self

    def available_moves(self) -> list[int]:
        return []

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

    def on_resize(self):
        if self.tile is not None and self.original_texture is not None:
            self.texture = pygame.transform.scale(
                self.original_texture, self.tile.render_bounds.size
            )

    def render(self, screen: pygame.Surface):
        if self.tile is not None and self.texture is not None:
            screen.blit(self.texture, self.tile.render_bounds.topleft)


class Pawn(Piece):
    def __init__(self, board: actors.board.Board, c: Color, file: int) -> None:
        super().__init__(board, c)
        self.pos = (1 if c != board.perspective else 6, file)
        self.direction = 1 if c != board.perspective else -1
        theme = self.assets.textures.pieces.regular
        self.original_texture = (
            theme.white.pawn if c == Color.WHITE else theme.black.pawn
        )
        self.on_resize()
        self.add_to_board(board)

    def available_moves(self) -> list[int]:
        moves = []
        forward = self.board.index(self.pos[0] + self.direction, self.pos[1])
        forward_tile = self.board.tile(forward)
        if forward_tile is not None and forward_tile.piece is None:
            moves.append(forward)
        if self.pos[0] == (1 if self.color != self.board.perspective else 6):
            moves.append(
                self.board.index(self.pos[0] + 2 * self.direction, self.pos[1])
            )

        return moves


# Pieces that can be found on the board 2 times (rooks, knights, bishops)
# Has its own class because common placing mechanism


class DoublePiece(Piece):
    def __init__(
        self,
        board: actors.board.Board,
        c: Color,
        files: tuple[int, int],
        side: typing.Union[Side, None],
        pos: typing.Union[None, tuple[int, int]] = None,
    ) -> None:
        super().__init__(board, c)
        if pos is None:
            if side is None:
                raise Exception(
                    "Both side and pos is undefined. This should not happen."
                )
            pos = (
                0 if c != board.perspective else 7,
                files[0] if side == Side.QUEEN else files[1],
            )
        self.pos = pos


class Knight(DoublePiece):
    def __init__(
        self,
        board: actors.board.Board,
        c: Color,
        side: typing.Union[Side, None],
        pos: typing.Union[None, tuple[int, int]] = None,
    ) -> None:
        super().__init__(board, c, (1, 6), side, pos)
        theme = self.game.assets.textures.pieces.regular
        self.original_texture = (
            theme.white.knight if c == Color.WHITE else theme.black.knight
        )
        self.on_resize()
        self.add_to_board(board)


class Bishop(DoublePiece):
    def __init__(
        self,
        board: actors.board.Board,
        c: Color,
        side: typing.Union[Side, None],
        pos: typing.Union[None, tuple[int, int]] = None,
    ) -> None:
        super().__init__(board, c, (2, 5), side, pos)
        theme = self.game.assets.textures.pieces.regular
        self.original_texture = (
            theme.white.bishop if c == Color.WHITE else theme.black.bishop
        )
        self.on_resize()
        self.add_to_board(board)


class Rook(DoublePiece):
    def __init__(
        self,
        board: actors.board.Board,
        c: Color,
        side: typing.Union[Side, None] = None,
        pos: typing.Union[None, tuple[int, int]] = None,
    ) -> None:
        super().__init__(board, c, (0, 7), side, pos)

        theme = self.game.assets.textures.pieces.regular
        self.original_texture = (
            theme.white.rook if c == Color.WHITE else theme.black.rook
        )
        self.on_resize()
        self.add_to_board(board)


class Queen(Piece):
    def __init__(self, board: actors.board.Board, c: Color) -> None:
        super().__init__(board, c)
        theme = self.game.assets.textures.pieces.regular
        self.original_texture = (
            theme.white.queen if c == Color.WHITE else theme.black.queen
        )
        self.pos = (
            0 if c != board.perspective else 7,
            3 if Color.WHITE == board.perspective else 4,
        )
        self.on_resize()
        self.add_to_board(board)


class King(Piece):
    def __init__(self, board: actors.board.Board, c: Color) -> None:
        super().__init__(board, c)
        theme = self.game.assets.textures.pieces.regular
        self.original_texture = (
            theme.white.king if c == Color.WHITE else theme.black.king
        )
        self.pos = (
            0 if c != board.perspective else 7,
            4 if Color.WHITE == board.perspective else 3,
        )
        self.on_resize()
        self.add_to_board(board)
