from actors.button import Button
from scenes.scene import Scene


class MainMenu(Scene):
    import main

    def __init__(self, game: main.Game):
        super().__init__(game)

    def init(self):
        self.actors.append(
            Button(
                self,
                "Szia uram",
                (100, 100),
                (64, 64),
                5,
                2,
                self.game.textures.buttons.icons.play,
                self.game.textures.buttons.icons.hover.play,
                lambda event: None,
            )
        )
        super().init()

    def dispose(self):
        return super().dispose()
