import actors.actor
import typing


class TextureActor(actors.actor.Actor):
    def __init__(self, scene, texture, bounds) -> None:
        import pygame

        super().__init__(scene)
        self.bounds = bounds
        self.orig_texture = pygame.transform.scale(texture, bounds.size)
        self.on_window_resize(None)

    def on_window_resize(self, _):
        import pygame

        self.render_bounds = self.game.viewport.get_rect(self.bounds)
        self.texture = pygame.transform.scale(
            self.orig_texture, self.render_bounds.size
        )

    def render(self, screen):
        super().render(screen)
        screen.blit(self.texture, self.render_bounds)
