from actors.actor import Actor
from actors.tile import Tile
import pygame
import typing


class Board(Actor):
    def __init__(self, scene, width=8, height=8) -> None:
        super().__init__(scene)
        self.tiles: list[Tile] = []
        self.width = width
        self.height = height

    def init(self):
        for index in range(0, self.width * self.height):
            xy = self.xy(index)
            if xy is None:
                raise Exception("Shouldn't be possible")
            tile = Tile(self.scene, index, xy[0], xy[1], (50, (1080 - 64 * 8) // 2))
            self.tiles.append(tile)
            tile.init()
        return super().init()

    def add_pieces(self):
        ...

    def xy(self, index: typing.Union[None, int]):
        if index is None:
            return None
        return (index % self.width, index // self.width)

    def index(self, x: int, y: int):
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return None
        return x * self.width + y

    def tile(self, index: typing.Union[None, int]):
        if index is None:
            return None
        return self.tiles[index]

    def render(self, screen):
        for tile in self.tiles:
            tile.render(screen)

    def on_window_resize(self, event: pygame.event.Event):
        for tile in self.tiles:
            tile.on_window_resize(event)
