from actors.actor import Actor
import pygame
import typing
import scenes.gamescene


ANIM_HEIGHT = 8
ANIM_SPEED = 3


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
        self.legal_moves = []
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
        for tile in self.board.tiles:
            tile.find_legal_moves()
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
                    math.sin(self.piece_anim_offset) * float(ANIM_HEIGHT)
                    - ANIM_HEIGHT,  # animation
                ),
            )

    def find_legal_moves(self):
        if self.piece is None:
            self.legal_moves = []
            return
        self.legal_moves = self.board.get_moves_from(self)

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
        if self.scene is None:
            return
        self.texture = pygame.transform.scale(
            self.orig_texture, self.render_bounds.size
        )
        self.shadow = pygame.transform.scale(self.orig_shadow, self.render_bounds.size)
        self.circle = pygame.transform.scale(self.orig_circle, self.render_bounds.size)
        if self.piece is not None:
            self.piece.on_resize()

    @property
    def scene(self) -> scenes.gamescene.GameScene:
        return super().scene  # type: ignore

    def promotion(
        self,
        _from: typing.Union[None, "Tile"],  # typing bs...
        to: "Tile",
        promote_to: str,
    ):
        assert _from is not None  # typing bs...
        self.board.make_move(_from, to, promote_to)
        for btn in self.scene.promotion_btns:
            btn.hide()
        pass

    def on_mouse_button_up(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        from game.controllers import PlayerController
        from game.pieces import Pawn

        #

        if button == 1:  # Left Click
            if self.selected:
                self.board.clear_selection()
                return
            if self.can_move_there and self.board.selected is not None:
                promote = ""
                if (
                    isinstance(self.board.selected.piece, Pawn)
                    and (self.y == 0 or self.y == 7)
                    and not self.board.selected.piece.promoted
                ):
                    self.scene.promote_to_queen_btn.action = lambda _: self.promotion(
                        self.board.selected, self, "q"
                    )
                    self.scene.promote_to_bishop_btn.action = lambda _: self.promotion(
                        self.board.selected, self, "b"
                    )
                    self.scene.promote_to_knight_btn.action = lambda _: self.promotion(
                        self.board.selected, self, "k"
                    )
                    self.scene.promote_to_rook_btn.action = lambda _: self.promotion(
                        self.board.selected, self, "r"
                    )
                    for btn in self.scene.promotion_btns:
                        btn.show()
                    return
                self.board.make_move(self.board.selected, self, promote)
                return
            self.board.clear_selection()
            if self.piece is None:
                return
            if (
                not isinstance(
                    self.scene.controller_of(self.piece.color), PlayerController
                )
                or self.piece.color != self.board.turn_of
            ):
                self.board.clear_selection()
                return
            # print(self.__str__() + " selected")
            for move in self.legal_moves:
                to = self.board.find_tile(move.uci()[2:4])
                if to is None:
                    continue
                to.can_move_there = True
            self.selected = True
            self.board.selected = self
        if button == 3:  # Right Click
            self.marked = not self.marked
            # un = "" if self.marked else "un"
            # print(f"{self.__str__()} {un}marked")
            self.orig_texture = (
                self.marked_texture if self.marked else self.unmarked_texture
            ).copy()
            self.refresh_texture()

    def dispose(self):
        if self.piece is not None:
            self.piece.dispose()
