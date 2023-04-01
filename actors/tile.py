from actors.actor import Actor
import pygame
import typing


class Tile(Actor):
    def __init__(
        self, scene, index: int, x: int, y: int, offset: tuple[int, int]
    ) -> None:
        import game.pieces

        super().__init__(scene)
        self.x = x
        self.y = y
        self.index = index
        self.bounds = pygame.Rect(x * 64, y * 64, 64, 64)
        self.texture = None
        self.offset = offset
        self.piece: typing.Union[None, game.pieces.Piece] = None

    def init(self):
        if self.x % 2 != self.y % 2:
            self.orig_texture = self.game.assets.textures.board.regular.light
        else:
            self.orig_texture = self.game.assets.textures.board.regular.dark
        self.on_window_resize(None)

    def render(self, screen: pygame.surface.Surface):
        if self.texture is not None:
            screen.blit(self.texture, self.render_bounds.topleft)

    @property
    def render_bounds(self):
        rect = self.bounds.copy()
        rect.topleft = (
            rect.topleft[0] + self.offset[0],
            rect.topleft[1] + self.offset[1],
        )
        rect = self.game.viewport.get_rect(rect)
        return pygame.Rect(
            rect.topleft[0],
            rect.topleft[1],
            # extending size with one removes black border due to float precision errors
            rect.size[0] + 1,
            rect.size[1] + 1,
        )

    def on_window_resize(self, event: typing.Union[None, pygame.event.Event]):
        self.texture = pygame.transform.scale(
            self.orig_texture, self.render_bounds.size
        )

    def dispose(self):
        if self.piece is not None:
            self.piece.dispose()
