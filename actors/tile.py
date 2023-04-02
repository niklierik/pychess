from actors.actor import Actor
import pygame
import typing


ANIM_HEIGHT = 16
ANIM_SPEED = 2


class Tile(Actor):
    def __init__(
        self, scene, board, index: int, x: int, y: int, offset: tuple[int, int]
    ) -> None:
        from actors.board import Board
        import game.pieces
        import math

        super().__init__(scene)
        self.board: Board = board
        self.x = x
        self.y = y
        self.index = index
        self.bounds = pygame.Rect(x * 64 + offset[0], y * 64 + offset[1], 64, 64)
        self.texture = None
        self.offset = offset
        self.marked = False
        self.piece_anim_offset = math.pi / 2.0
        self.selected = False
        self.color = 1 if self.x % 2 != self.y % 2 else 0
        self._piece: typing.Union[None, game.pieces.Piece] = None
        self.can_move_there = False
        if self.game is None:
            return
        self.orig_shadow = self.game.assets.textures.pieces.shadow
        self.orig_circle = self.game.assets.textures.pieces.circle
        if self.color == 0:
            self.orig_texture = (
                self.unmarked_texture
            ) = self.game.assets.textures.board.regular.light
            self.marked_texture = self.game.assets.textures.board.wooden.light
        else:
            self.orig_texture = (
                self.unmarked_texture
            ) = self.game.assets.textures.board.regular.dark
            self.marked_texture = self.game.assets.textures.board.wooden.dark

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
        self.on_window_resize(None)

    def render(self, screen: pygame.surface.Surface):
        import math

        if self.texture is not None:
            screen.blit(self.texture, self.render_bounds.topleft)
        if self.shadow is not None and self.selected:
            screen.blit(self.shadow, self.render_bounds.topleft)
        if self.circle is not None and self.can_move_there:
            screen.blit(self.circle, self.render_bounds.topleft)
        if self.piece is not None:
            self.piece.render(
                screen,
                (
                    0,
                    math.sin(self.piece_anim_offset) * ANIM_HEIGHT
                    - ANIM_HEIGHT,  # animation
                ),
            )

    def update(self, delta):
        import math

        # print(delta)
        if self.selected:
            self.piece_anim_offset = self.piece_anim_offset - delta * ANIM_SPEED
        else:
            self.piece_anim_offset = (
                math.pi / 2.0
            )  # sin(PI/2) = 1 => sin(PI/2) * 32 - 32 = 0, see # animation, we don't need to check if animation offset is needed (otherwise +ANIM_HEIGHT would shift the texture over when animation is not happening)

    @property
    def render_bounds(self):
        if self.game is None:
            return pygame.Rect(0, 0, 0, 0)
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
        from game.color import PieceColor

        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        if self.board.perspective == PieceColor.BLACK:
            files.reverse()
        rank = 1 + self.y if self.board.perspective == PieceColor.BLACK else 8 - self.y
        return f"{files[self.x]}{rank}"

    def on_window_resize(self, event: typing.Union[None, pygame.event.Event]):
        self.texture = pygame.transform.scale(
            self.orig_texture, self.render_bounds.size
        )
        self.shadow = pygame.transform.scale(self.orig_shadow, self.render_bounds.size)
        self.circle = pygame.transform.scale(self.orig_circle, self.render_bounds.size)
        if self.piece is not None:
            self.piece.on_resize()

    def on_mouse_button_up(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        #
        if button == 1:
            print(self.__str__() + " selected")
            for tile in self.board.tiles:
                tile.selected = False
            self.selected = True
        if button == 3:
            self.marked = not self.marked
            un = "" if self.marked else "un"
            print(self.__str__() + f" {un}marked")
            self.orig_texture = (
                self.marked_texture if self.marked else self.unmarked_texture
            ).copy()
            self.refresh_texture()

    def dispose(self):
        if self.piece is not None:
            self.piece.dispose()
