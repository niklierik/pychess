import pygame


class Scene:
    from main import Game

    def __init__(self, game: Game) -> None:
        from actors.actor import Actor

        self._game = game
        self._actors: list[Actor] = []

    def init(self):
        for actor in self.actors:
            actor.init()

    @property
    def game(self):
        return self._game

    @property
    def actors(self):
        return self._actors

    def loop(self):
        for actor in self.actors:
            actor.update()

    def render(self, screen: pygame.surface.Surface):
        for actor in self.actors:
            if actor.visible:
                actor.render(screen)

    def on_mouse_button_down(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        for actor in self.actors:
            if actor.visible:
                actor.on_mouse_button_down(event, pos, button)

    def on_mouse_button_up(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        for actor in self.actors:
            if actor.visible:
                actor.on_mouse_button_up(event, pos, button)

    def on_window_resize(self, event: pygame.event.Event):
        for actor in self.actors:
            actor.on_window_resize(event)

    def dispose(self):
        for actor in self.actors:
            actor.dispose()
