from actors.actor import Actor
import pygame
from typing import Callable
from scenes.scene import Scene


class ButtonClickEvent:
    def __init__(self, pos: tuple[int, int], up: bool, button: int):
        self.pos = pos
        self.up = up
        self.button = button


class Button(Actor):
    def __init__(
        self,
        scene: Scene,
        pos: tuple[int, int],
        size: tuple[int, int],
        border: int,
        padding: int,
        texture: pygame.Surface,
        hover_texture: pygame.Surface,
        action: Callable[[ButtonClickEvent], None],
    ) -> None:
        super().__init__(scene)
        self.action = action
        self.pos = pos
        self.inside = False
        self.border = border
        self.padding = padding
        self.size = size
        self.texture = texture.copy()
        self.hover_texture = hover_texture.copy()

    def init(self):
        rect = self.texture.get_rect()
        rect.width = self.size[0]
        rect.height = self.size[1]
        rect.center = (self.pos[0] + rect.width // 2, self.pos[1] + rect.height // 2)
        self.texture = pygame.transform.scale(self.texture, (rect.width, rect.height))
        self.hover_texture = pygame.transform.scale(
            self.hover_texture, (rect.width, rect.height)
        )
        self.active_texture = self.texture
        self.bounds = pygame.Rect(self.pos[0], self.pos[1], rect.width, rect.height)
        super().init()

    def render(self, screen: pygame.surface.Surface):
        super().render(screen)
        screen.blit(self.active_texture, self.bounds)

    def update(self):
        mousepos = pygame.mouse.get_pos()
        if not self.inside and self.bounds.collidepoint(mousepos):
            self.on_mouse_enters(mousepos)
            self.inside = True
        if self.inside and not self.bounds.collidepoint(mousepos):
            self.on_mouse_exits(mousepos)
            self.inside = False
        super().update()

    def on_mouse_enters(self, pos: tuple[int, int]):
        self.active_texture = self.hover_texture

    def on_mouse_exits(self, pos: tuple[int, int]):
        self.active_texture = self.texture

    def on_mouse_button_down(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        if not self.bounds.collidepoint(pos[0], pos[1]):
            return
        if self.action is None:
            return
        event = ButtonClickEvent(event.pos, False, event.button)
        self.action(event)

    def on_mouse_button_up(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        if not self.bounds.collidepoint(pos[0], pos[1]):
            return
        if self.action is None:
            return
        event = ButtonClickEvent(event.pos, True, event.button)
        self.action(event)
