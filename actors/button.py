from actors.actor import Actor
import pygame
from typing import Callable
import assets


class ButtonClickEvent:
    pos: tuple[int, int]
    up: bool
    button: int


class Button(Actor):
    def __init__(
        self,
        text: str,
        pos: tuple[int, int],
        border: int,
        padding: int,
        action: Callable[[ButtonClickEvent], None],
    ) -> None:
        self.action = action
        self.pos = pos
        self.text = text
        self.inside = False

        self.tint = "white"
        self.hover_tint = "darkgrey"
        self.active_tint = self.tint
        self.border = border
        self.padding = padding

    def init(self):
        self.texture = pygame.image.load("assets/textures/buttons/start.png")
        self.hover_texture = self.texture.copy()
        self.hover_texture.fill("darkgrey", special_flags=pygame.BLEND_MULT)
        self.active_texture = self.texture
        rect = self.active_texture.get_rect()
        rect.center = (self.pos[0] + rect.width // 2, self.pos[1] + rect.height // 2)
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
        event = ButtonClickEvent()
        event.pos = pos
        event.button = button
        event.up = False
        self.action(event)

    def on_mouse_button_up(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        if not self.bounds.collidepoint(pos[0], pos[1]):
            return
        if self.action is None:
            return
        event = ButtonClickEvent()
        event.pos = pos
        event.button = button
        event.up = True
        self.action(event)
