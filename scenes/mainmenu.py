from scenes.gamescene import GameScene
from scenes.scene import Scene
from game.color import PieceColor
import random


class MainMenu(Scene):
    import main as main
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
        self.exit_btn = Button(
            self,
            (10, 10 + 70),
            (64, 64),
            self.game.assets.textures.buttons.icons.close,
            self.game.assets.textures.buttons.icons.hover.close,
            self.game.assets.textures.buttons.icons.on_pressed.close,
            self.on_exit_btn,
        )
        empty: list[Button] = []
        self.play_ai_btns_lvl = [empty] * 5
        self.actors.append(self.play_btn)
        self.actors.append(self.exit_btn)

    def init_play_btns(self):
        from actors.button import Button
        from actors.text import Text
        import pygame

        self.play_ai_btn = Button(
            self,
            (100, 10),
            (57 * 64 // 21, 64),
            self.game.assets.textures.buttons.play.ai,
            self.game.assets.textures.buttons.play.hover.ai,
            self.game.assets.textures.buttons.play.on_pressed.ai,
            self.on_show_ai_lvls,
        )
        """
        self.play_player_btn = Button(
            self,
            (100, 10 + 70),
            (57 * 64 // 21, 64),
            self.game.assets.textures.buttons.play.player,
            self.game.assets.textures.buttons.play.hover.player,
            self.game.assets.textures.buttons.play.on_pressed.player,
            self.on_play_player,
        )
        """
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
            # self.play_player_btn,
            self.analyse_btn,
        ]
        self.actors.extend(self.play_buttons)
        self.actors.append(
            Text(
                self,
                "Made by: Erik Nikli",
                (255, 255, 255),
                None,
                pygame.Rect(10, 1020, 300, 20),
            )
        )
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
                self.show_play_btns,
            )
            btn.custom_vars["lvl"] = lvl + 1
            # btn.custom_vars["color"] = PieceColor(random.randint(0, 1))
            self.play_ai_btns.append(btn)
            self.create_ai_btns_for(lvl)
        self.actors.extend(self.play_ai_btns)
        for btn in self.play_ai_btns:
            btn.hide()

    def init(self):
        self.init_main_btns()
        self.init_play_btns()
        self.init_play_ai_btns()
        super().init()

    def on_play_btn(self, _: ClickEvent) -> None:
        for btn in self.play_buttons:
            btn.show()

    def hide_color_picking(self):
        for btn in self.play_ai_btns_lvl:
            for b in btn:
                b.hide()

    def show_play_btns(self, event: ClickEvent) -> None:
        from actors.button import Button

        assert isinstance(event.actor, Button)
        lvl: int = event.actor.custom_vars["lvl"] - 1
        btns = self.play_ai_btns_lvl[lvl]
        self.hide_color_picking()
        for btn in btns:
            btn.show()

    def on_settings_btn(self, _: ClickEvent) -> None:
        self.hide_play_btns()

    def on_exit_btn(self, _: ClickEvent) -> None:
        self.game.quit()

    def on_show_ai_lvls(self, _: ClickEvent) -> None:
        self.hide_player_btns()
        for btn in self.play_ai_btns:
            btn.show()

    def on_analyse(self, _: ClickEvent) -> None:
        from game.controllers import PlayerController

        self.game.scene = GameScene(
            self.game,
            PlayerController(PieceColor.WHITE, "White"),
            PlayerController(PieceColor.BLACK, "Black"),
        )

    def on_play_player(self, _: ClickEvent) -> None:
        self.hide_ai_btns()

    def create_ai_btns_for(self, lvl: int):
        from actors.button import Button

        white = Button(
            self,
            (500, 10 + lvl * 70),
            (64, 64),
            self.game.assets.textures.buttons.icons.play_white,
            self.game.assets.textures.buttons.icons.hover.play_white,
            self.game.assets.textures.buttons.icons.on_pressed.play_white,
            self.on_play_ai,
        )
        rnd = Button(
            self,
            (500 + 70, 10 + lvl * 70),
            (64, 64),
            self.game.assets.textures.buttons.icons.play_random,
            self.game.assets.textures.buttons.icons.hover.play_random,
            self.game.assets.textures.buttons.icons.on_pressed.play_random,
            self.on_play_ai,
        )

        black = Button(
            self,
            (500 + 2 * 70, 10 + lvl * 70),
            (64, 64),
            self.game.assets.textures.buttons.icons.play_black,
            self.game.assets.textures.buttons.icons.hover.play_black,
            self.game.assets.textures.buttons.icons.on_pressed.play_black,
            self.on_play_ai,
        )
        black.custom_vars["lvl"] = white.custom_vars["lvl"] = rnd.custom_vars["lvl"] = (
            lvl + 1
        )
        white.custom_vars["color"] = PieceColor.WHITE
        black.custom_vars["color"] = PieceColor.BLACK
        rnd.custom_vars["color"] = PieceColor(random.randint(0, 1))

        btns: list[Button] = [white, black, rnd]
        self.play_ai_btns_lvl[lvl] = btns
        self.actors.extend(btns)
        for btn in btns:
            btn.hide()

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
        print(f"Playing AI {lvl}:")
        player = PlayerController(playersColor, self.game.player_name)
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
        self.hide_color_picking()

    def hide_ai_btns(self):
        for btn in self.play_ai_btns:
            btn.hide()
        self.hide_color_picking()

    def hide_player_btns(self):
        pass

    def dispose(self):
        return super().dispose()
