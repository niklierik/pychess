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
        texture: pygame.Surface,
        hover_texture: pygame.Surface,
        on_pressed_texture: pygame.Surface,
        action: Callable[[ButtonClickEvent], None],
        only_on_up: bool = True,
    ) -> None:
        super().__init__(scene)
        self.action = action
        self.pos = pos
        self.inside = False
        self.pressed = False
        self.size = size
        self.only_on_up = only_on_up
        self.original_texture = self.texture = texture.copy()
        self.original_hover_texture = self.hover_texture = hover_texture.copy()
        self.original_on_pressed_texture = (
            self.on_pressed_texture
        ) = on_pressed_texture.copy()

    def init(self):
        self.bounds = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        # rect = self.game.viewport.get_rect(rect)
        self.on_window_resize(None)
        # self.active_texture = self.texture
        super().init()

    @property
    def render_bounds(self):
        return self.game.viewport.get_rect(self.bounds)

    @property
    def active_texture(self):
        if self.pressed:
            return self.on_pressed_texture
        if self.inside:
            return self.hover_texture
        return self.texture

    def render(self, screen: pygame.surface.Surface):
        super().render(screen)
        screen.blit(self.active_texture, self.render_bounds.topleft)

    def on_window_resize(self, event: pygame.event.Event):
        self.texture = pygame.transform.scale(
            self.original_texture,
            pygame.Vector2(self.render_bounds.size[0], self.render_bounds.size[1]),
        )
        self.hover_texture = pygame.transform.scale(
            self.original_hover_texture,
            pygame.Vector2(self.render_bounds.size[0], self.render_bounds.size[1]),
        )
        self.on_pressed_texture = pygame.transform.scale(
            self.original_on_pressed_texture,
            pygame.Vector2(self.render_bounds.size[0], self.render_bounds.size[1]),
        )
        # self.active_texture = self.texture
        # print(self.active_texture)
        return super().on_window_resize(event)

    def update(self):
        mousepos = pygame.mouse.get_pos()
        if not self.inside and self.render_bounds.collidepoint(mousepos):
            self.on_mouse_enters(mousepos)
            self.inside = True
        if self.inside and not self.render_bounds.collidepoint(mousepos):
            self.on_mouse_exits(mousepos)
            self.inside = False
        super().update()

    def on_mouse_enters(self, pos: tuple[int, int]):
        # self.active_texture = self.hover_texture
        ...

    def on_mouse_exits(self, pos: tuple[int, int]):
        # self.active_texture = self.texture
        ...

    def on_mouse_button_down(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        if not self.render_bounds.collidepoint(pos[0], pos[1]):
            return
        event = ButtonClickEvent(event.pos, False, event.button)
        # self.active_texture = self.on_pressed_texture
        self.pressed = True
        if not self.only_on_up and self.action is not None:
            self.action(event)

    def on_mouse_button_up(
        self, event: pygame.event.Event, pos: tuple[int, int], button: int
    ):
        event = ButtonClickEvent(event.pos, True, event.button)
        # self.active_texture = self.hover_texture
        self.pressed = False
        if self.action is not None and self.render_bounds.collidepoint(pos[0], pos[1]):
            self.action(event)
