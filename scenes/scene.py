import pygame


class Scene:
    def __init__(self) -> None:
        from actors.actor import Actor

        self._actors: list[Actor] = []

    def init(self):
        for actor in self.actors:
            actor.init()

    @property
    def actors(self):
        return self._actors

    def loop(self):
        for actor in self.actors:
            actor.update()

    def render(self, screen: pygame.surface.Surface):
        for actor in self.actors:
            actor.render(screen)

    def on_mouse_button_down(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        for actor in self.actors:
            actor.on_mouse_button_down(event, pos, button)

    def on_mouse_button_up(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        for actor in self.actors:
            actor.on_mouse_button_up(event, pos, button)

    def dispose(self):
        for actor in self.actors:
            actor.dispose()
