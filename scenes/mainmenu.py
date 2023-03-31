from scenes.scene import Scene


class MainMenu(Scene):
    import main
    from actors.button import ButtonClickEvent

    def __init__(self, game: main.Game):
        super().__init__(game)

    def init_main_btns(self):
        from actors.button import Button

        self.play_btn = Button(
            self,
            (10, 10),
            (64, 64),
            self.game.assets.textures.buttons.icons.play,
            self.game.assets.textures.buttons.icons.hover.play,
            self.game.assets.textures.buttons.icons.on_pressed.play,
            self.on_play_btn,
        )
        self.settings_btn = Button(
            self,
            (10, 10 + 70),
            (64, 64),
            self.game.assets.textures.buttons.icons.settings,
            self.game.assets.textures.buttons.icons.hover.settings,
            self.game.assets.textures.buttons.icons.on_pressed.settings,
            self.on_settings_btn,
        )
        self.exit_btn = Button(
            self,
            (10, 10 + 2 * 70),
            (64, 64),
            self.game.assets.textures.buttons.icons.close,
            self.game.assets.textures.buttons.icons.hover.close,
            self.game.assets.textures.buttons.icons.on_pressed.close,
            self.on_exit_btn,
        )
        self.actors.append(self.play_btn)
        self.actors.append(self.settings_btn)
        self.actors.append(self.exit_btn)

    def init_play_btns(self):
        from actors.button import Button

        self.play_ai_btn = Button(
            self,
            (100, 10),
            (57 * 64 / 21, 64),
            self.game.assets.textures.buttons.play.ai,
            self.game.assets.textures.buttons.play.hover.ai,
            self.game.assets.textures.buttons.play.on_pressed.ai,
            self.on_show_ai_lvls,
        )
        self.play_player_btn = Button(
            self,
            (100, 80),
            (57 * 64 / 21, 64),
            self.game.assets.textures.buttons.play.player,
            self.game.assets.textures.buttons.play.hover.player,
            self.game.assets.textures.buttons.play.on_pressed.player,
            self.on_play_player,
        )
        self.play_buttons: list[Button] = [self.play_ai_btn, self.play_player_btn]
        self.actors.extend(self.play_buttons)
        for btn in self.play_buttons:
            btn.hide()

    def init_play_ai_btns(self):
        from actors.button import Button

        self.play_ai_btns: list[Button] = []
        for i in range(0, 5):
            self.play_ai_btns.append(
                Button(
                    self,
                    (300, 10 + i * 70),
                    (57 * 64 / 21, 64),
                    self.game.assets.textures.buttons.play.lvl[i],
                    self.game.assets.textures.buttons.play.hover.lvl[i],
                    self.game.assets.textures.buttons.play.on_pressed.lvl[i],
                    lambda event: self.on_play_ai(event, i + 1),
                )
            )
        self.actors.extend(self.play_ai_btns)
        for btn in self.play_ai_btns:
            btn.hide()

    def init(self):
        self.init_main_btns()
        self.init_play_btns()
        self.init_play_ai_btns()
        super().init()

    def on_play_btn(self, event: ButtonClickEvent) -> None:
        for btn in self.play_buttons:
            btn.show()

    def on_settings_btn(self, event: ButtonClickEvent) -> None:
        self.hide_play_btns()

    def on_exit_btn(self, event: ButtonClickEvent) -> None:
        self.game.quit()

    def on_show_ai_lvls(self, event: ButtonClickEvent) -> None:
        self.hide_player_btns()
        for btn in self.play_ai_btns:
            btn.show()

    def on_play_player(self, event: ButtonClickEvent) -> None:
        self.hide_ai_btns()

    def on_play_ai(self, event: ButtonClickEvent, lvl: int) -> None:
        ...

    def hide_play_btns(self):
        for btn in self.play_buttons:
            btn.hide()
        self.hide_ai_btns()
        self.hide_player_btns()

    def hide_ai_btns(self):
        for btn in self.play_ai_btns:
            btn.hide()

    def hide_player_btns(self):
        ...

    def dispose(self):
        return super().dispose()
