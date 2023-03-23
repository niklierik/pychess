import pygame
from scenes.scene import Scene


class Actor:
    def __init__(self, scene: Scene) -> None:
        self._scene = scene
        self._visible = False

    @property
    def scene(self) -> Scene:
        return self._scene

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        if value:
            self.show()
        else:
            self.hide()

    def init(self):
        ...

    def show(self):
        _visible = True
        ...

    def hide(self):
        _visible = False
        ...

    def dispose(self):
        ...

    def on_mouse_button_down(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        ...

    def on_mouse_button_up(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        ...

    def update(self):
        ...

    def render(self, screen: pygame.surface.Surface):
        ...
