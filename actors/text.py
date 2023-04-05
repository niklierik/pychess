from actors.actor import Actor
from scenes.scene import Scene
import pygame


class Text(Actor):
    def __init__(self, scene: Scene, text: str) -> None:
        super().__init__(scene)
        self.text = text

    @property
    def text(self):
        return self._text

    @property
    def texture(self):
        return self._texture

    @text.setter
    def text(self, txt: str):
        self._text = txt
        self._texture = None

    def render(self, screen: pygame.surface.Surface):
        super().render(screen)
