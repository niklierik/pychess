from actors.actor import Actor
from actors.tile import Tile
import pygame


class Board(Actor):
    def __init__(self, scene, width=8, height=8) -> None:
        super().__init__(scene)
        self.tiles: list[Tile] = []
        self.width = 8
        self.height = 8

    def init(self):
        for index in range(0, self.width * self.height):
            xy = self.xy(index)
            tile = Tile(self.scene, index, xy[0], xy[1], (50, (1080 - 64 * 8) // 2))
            self.tiles.append(tile)
            tile.init()
        return super().init()

    def xy(self, index: int) -> tuple[int, int]:
        return (index % self.width, index // self.width)

    def index(self, x: int, y: int):
        return x * self.width + y

    def tile(self, index: int):
        return self.tiles[index]

    def render(self, screen):
        for tile in self.tiles:
            tile.render(screen)

    def on_window_resize(self, event: pygame.event.Event):
        for tile in self.tiles:
            tile.on_window_resize(event)
