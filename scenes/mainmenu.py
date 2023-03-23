import pygame
from actors.button import Button
from scenes.scene import Scene


class MainMenu(Scene):
    def __init__(self):
        super().__init__()

    def init(self):
        self.actors.append(Button("Szia uram", [100, 100], 5, 2, lambda event: None))
        super().init()

    def dispose(self):
        return super().dispose()
