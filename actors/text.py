from actors.actor import Actor
from scenes.scene import Scene
import pygame
import typing

# From pygame
RGBAOutput = tuple[int, int, int, int]
ColorValue = typing.Union[
    pygame.Color, int, str, tuple[int, int, int], RGBAOutput, typing.Sequence[int]
]


class Text(Actor):
    def __init__(
        self,
        scene: Scene,
        text: str,
        color: ColorValue,
        bgr_color: typing.Union[ColorValue, None],
        bounds: pygame.Rect,
    ) -> None:
        super().__init__(scene)
        self.color = color
        self.bgr_color = bgr_color
        self.bounds = bounds
        self.text = text

    @property
    def text(self):
        return self._text

    @property
    def orig_texture(self):
        return self._orig_texture

    @property
    def texture(self):
        return self._texture

    @text.setter
    def text(self, txt: str):
        self._text = txt
        if self.game is not None:
            self._orig_texture = self.game.assets.fonts.main.render(
                txt, False, self.color, self.bgr_color
            )
        self.on_window_resize(None)

    @property
    def render_bounds(self):
        if self.game is None:
            return pygame.Rect(0, 0, 0, 0)
        return self.game.viewport.get_rect(self.bounds)

    def on_window_resize(self, _: typing.Union[None, pygame.event.Event]):
        self._texture = pygame.transform.scale(
            self._orig_texture, self.render_bounds.size
        )

    def render(self, screen: pygame.surface.Surface):
        super().render(screen)
        screen.blit(self.texture, self.render_bounds.topleft)
