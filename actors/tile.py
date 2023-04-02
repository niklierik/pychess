from actors.actor import Actor
import pygame
import typing


class Tile(Actor):
    def __init__(
        self, scene, board, index: int, x: int, y: int, offset: tuple[int, int]
    ) -> None:
        from actors.board import Board
        import game.pieces

        super().__init__(scene)
        self.board: Board = board
        self.x = x
        self.y = y
        self.index = index
        self.bounds = pygame.Rect(x * 64 + offset[0], y * 64 + offset[1], 64, 64)
        self.texture = None
        self.offset = offset
        self.color = 1 if self.x % 2 != self.y % 2 else 0
        self._piece: typing.Union[None, game.pieces.Piece] = None

    @property
    def piece(self):
        return self._piece

    @piece.setter
    def piece(self, p):
        if self._piece is not None:
            self._piece.tile = None
        self._piece = p
        if self._piece is not None:
            self._piece.tile = self

    def init(self):
        self.refresh_texture()

    def refresh_texture(self):
        from game.color import PieceColor

        if self.color == 0:
            self.orig_texture = self.game.assets.textures.board.regular.light
        else:
            self.orig_texture = self.game.assets.textures.board.regular.dark
        self.on_window_resize(None)

    def render(self, screen: pygame.surface.Surface):
        if self.texture is not None:
            screen.blit(self.texture, self.render_bounds.topleft)
        if self.piece is not None:
            self.piece.render(screen)

    @property
    def render_bounds(self):
        rect = self.bounds
        rect = self.game.viewport.get_rect(rect)
        return pygame.Rect(
            rect.topleft[0],
            rect.topleft[1],
            # extending size with one removes black border due to float precision errors
            rect.size[0] + 1,
            rect.size[1] + 1,
        )

    def __str__(self) -> str:
        self.board.perspective
        return ""

    def on_window_resize(self, event: typing.Union[None, pygame.event.Event]):
        self.texture = pygame.transform.scale(
            self.orig_texture, self.render_bounds.size
        )
        if self.piece is not None:
            self.piece.on_resize()

    def dispose(self):
        if self.piece is not None:
            self.piece.dispose()
