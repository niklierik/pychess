from scenes.scene import Scene


class MainMenu(Scene):
    import main
    from actors.button import ButtonClickEvent

    def __init__(self, game: main.Game):
        from actors.button import Button

        super().__init__(game)
        self.main_menu_btn = Button(
            self,
            (100, 100),
            (64, 64),
            5,
            2,
            self.game.textures.buttons.icons.play,
            self.game.textures.buttons.icons.hover.play,
            self.on_main_menu_btn,
        )

    def init(self):
        self.actors.append(self.main_menu_btn)
        super().init()

    def on_main_menu_btn(self, event: ButtonClickEvent) -> None:
        if event.up:
            self.main_menu_btn.hide()

    def dispose(self):
        return super().dispose()
