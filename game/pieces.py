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

    def available_moves(self) -> list[int]:
        return []

    @property
    def tile(self):
        return self.board.tile(self.board.index(self.pos[0], self.pos[1]))

    @tile.setter
    def tile(self, t):
        from actors.tile import Tile

        tile: Tile = t
        if self.tile is not None:
            self.tile._piece = None
        if tile is not None:
            self.pos = (tile.x, tile.y)
            tile._piece = self
        else:
            self.pos = (-1, -1)

    @property
    def game(self):
        return self.board.game

    @property
    def assets(self):
        if self.game is None:
            return None
        return self.game.assets

    def dispose(self):
        self.pos = (-1, -1)

    def on_resize(self):
        if self.tile is not None and self.original_texture is not None:
            self.texture = pygame.transform.scale(
                self.original_texture, self.tile.render_bounds.size
            )

    def render(self, screen: pygame.Surface, anim_offset: tuple[float, float]):
        if self.game is None:
            return
        anim_offset = self.game.viewport.get_position(anim_offset)
        if self.tile is not None and self.texture is not None:
            screen.blit(
                self.texture,
                (
                    self.tile.render_bounds.topleft[0] + anim_offset[0],
                    self.tile.render_bounds.topleft[1] + anim_offset[1],
                ),
            )


class Pawn(Piece):
    def __init__(self, board: actors.board.Board, c: Color, file: int) -> None:

        super().__init__(board, c)
        self.pos = (file, 1 if c != board.perspective else 6)
        self.direction = 1 if c != board.perspective else -1
        self.promoted = False
        if self.game is not None and self.assets is not None:
            theme = self.assets.textures.pieces.regular
            self.original_texture = (
                theme.white.pawn if c == Color.WHITE else theme.black.pawn
            )
            self.on_resize()

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
                files[0] if side == Side.QUEEN else files[1],
                0 if c != board.perspective else 7,
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
        if self.game is not None:
            theme = self.game.assets.textures.pieces.regular
            self.original_texture = (
                theme.white.knight if c == Color.WHITE else theme.black.knight
            )
            self.on_resize()


class Bishop(DoublePiece):
    def __init__(
        self,
        board: actors.board.Board,
        c: Color,
        side: typing.Union[Side, None],
        pos: typing.Union[None, tuple[int, int]] = None,
    ) -> None:
        super().__init__(board, c, (2, 5), side, pos)
        if self.game is not None:
            theme = self.game.assets.textures.pieces.regular
            self.original_texture = (
                theme.white.bishop if c == Color.WHITE else theme.black.bishop
            )
            self.on_resize()


class Rook(DoublePiece):
    def __init__(
        self,
        board: actors.board.Board,
        c: Color,
        side: typing.Union[Side, None] = None,
        pos: typing.Union[None, tuple[int, int]] = None,
    ) -> None:
        super().__init__(board, c, (0, 7), side, pos)
        if self.game is not None:
            theme = self.game.assets.textures.pieces.regular
            self.original_texture = (
                theme.white.rook if c == Color.WHITE else theme.black.rook
            )
            self.on_resize()


class Queen(Piece):
    def __init__(self, board: actors.board.Board, c: Color) -> None:
        super().__init__(board, c)
        if self.game is not None:
            theme = self.game.assets.textures.pieces.regular
            self.original_texture = (
                theme.white.queen if c == Color.WHITE else theme.black.queen
            )
            self.pos = (
                3 if Color.WHITE == board.perspective else 4,
                0 if c != board.perspective else 7,
            )
            self.on_resize()


class King(Piece):
    def __init__(self, board: actors.board.Board, c: Color) -> None:
        super().__init__(board, c)
        if self.game is not None:
            theme = self.game.assets.textures.pieces.regular
            self.original_texture = (
                theme.white.king if c == Color.WHITE else theme.black.king
            )
            self.pos = (
                4 if Color.WHITE == board.perspective else 3,
                0 if c != board.perspective else 7,
            )
            self.on_resize()
