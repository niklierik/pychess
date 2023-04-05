from scenes.gamescene import GameScene
from scenes.scene import Scene
from game.color import PieceColor
import random


class MainMenu(Scene):
    import main
    from actors.button import ClickEvent

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
            (57 * 64 // 21, 64),
            self.game.assets.textures.buttons.play.ai,
            self.game.assets.textures.buttons.play.hover.ai,
            self.game.assets.textures.buttons.play.on_pressed.ai,
            self.on_show_ai_lvls,
        )
        self.play_player_btn = Button(
            self,
            (100, 10 + 70),
            (57 * 64 // 21, 64),
            self.game.assets.textures.buttons.play.player,
            self.game.assets.textures.buttons.play.hover.player,
            self.game.assets.textures.buttons.play.on_pressed.player,
            self.on_play_player,
        )
        self.analyse_btn = Button(
            self,
            (100, 10 + 2 * 70),
            (57 * 64 // 21, 64),
            self.game.assets.textures.buttons.play.analyse,
            self.game.assets.textures.buttons.play.hover.analyse,
            self.game.assets.textures.buttons.play.on_pressed.analyse,
            self.on_analyse,
        )
        self.play_buttons: list[Button] = [
            self.play_ai_btn,
            self.play_player_btn,
            self.analyse_btn,
        ]
        self.actors.extend(self.play_buttons)
        for btn in self.play_buttons:
            btn.hide()

    def init_play_ai_btns(self):
        from actors.button import Button

        self.play_ai_btns: list[Button] = []
        for lvl in range(0, 5):
            btn = Button(
                self,
                (300, 10 + lvl * 70),
                (57 * 64 // 21, 64),
                self.game.assets.textures.buttons.play.lvl[lvl],
                self.game.assets.textures.buttons.play.hover.lvl[lvl],
                self.game.assets.textures.buttons.play.on_pressed.lvl[lvl],
                self.on_play_ai,
            )
            btn.custom_vars["lvl"] = lvl + 1
            btn.custom_vars["color"] = PieceColor(random.randint(0, 1))
            self.play_ai_btns.append(btn)
        self.actors.extend(self.play_ai_btns)
        for btn in self.play_ai_btns:
            btn.hide()

    def init(self):
        self.init_main_btns()
        self.init_play_btns()
        self.init_play_ai_btns()
        super().init()

    def on_play_btn(self, event: ClickEvent) -> None:
        for btn in self.play_buttons:
            btn.show()

    def on_settings_btn(self, event: ClickEvent) -> None:
        self.hide_play_btns()

    def on_exit_btn(self, event: ClickEvent) -> None:
        self.game.quit()

    def on_show_ai_lvls(self, event: ClickEvent) -> None:
        self.hide_player_btns()
        for btn in self.play_ai_btns:
            btn.show()

    def on_analyse(self, event: ClickEvent) -> None:
        from game.controllers import PlayerController

        self.game.scene = GameScene(
            self.game,
            PlayerController(PieceColor.WHITE),
            PlayerController(PieceColor.BLACK),
        )

    def on_play_player(self, event: ClickEvent) -> None:
        self.hide_ai_btns()

    def on_play_ai(
        self,
        event: ClickEvent,
    ) -> None:
        from game.controllers import PlayerController, AIController
        from actors.button import Button

        btn = event.actor
        if not isinstance(btn, Button):
            return
        playersColor = btn.custom_vars["color"]
        lvl = btn.custom_vars["lvl"]
        player = PlayerController(playersColor)
        ai = AIController(playersColor.opposite(), lvl)
        self.game.scene = GameScene(
            self.game,
            player if playersColor == PieceColor.WHITE else ai,
            player if playersColor == PieceColor.BLACK else ai,
        )

    def hide_play_btns(self):
        for btn in self.play_buttons:
            btn.hide()
        self.hide_ai_btns()
        self.hide_player_btns()

    def hide_ai_btns(self):
        for btn in self.play_ai_btns:
            btn.hide()

    def hide_player_btns(self):
        pass

    def dispose(self):
        return super().dispose()
