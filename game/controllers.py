import scenes.gamescene
import game.color
import threading
import json
import typing


class Controller:
    def __init__(self, color: game.color.PieceColor, name: str) -> None:
        self.color = color
        self.name = name

    def init(self, scene: scenes.gamescene.GameScene) -> None:
        pass

    def update(self, scene: scenes.gamescene.GameScene) -> None:
        """
        Updates controller each tick if it is their turn
        """

    def dispose(self) -> None:
        pass


# The default player controller
class PlayerController(Controller):
    def update(self, scene) -> None:
        pass  # Handled by Board class


# Another player, whose moves coming from network
class NetworkController(Controller):
    pass


class CancellationToken:
    def __init__(self):
        self.is_cancelled = False
        self.cancelled = False

    def cancel(self):
        self.is_cancelled = True

    def finish(self):
        self.cancelled = True


ct = CancellationToken()


# For thread safety


# AI whose moves are generated by stockfish
class AIController(Controller):
    def __init__(self, color: game.color.PieceColor, lvl: int):
        super().__init__(color, f"AI lvl {lvl}")
        global ct
        ct = CancellationToken()
        self._lvl = lvl
        self.run = False
        self.scene: scenes.gamescene.GameScene = None  # type: ignore
        self.update_thread = threading.Thread(target=self.update_async, name="update")
        self.commonai: typing.Union[None, dict[str, typing.Any]] = None
        self.depth = 20
        self.time = 0.4

    def load(self):
        import os.path as path

        """
        Load common.json settings then lvl{lvl}.json settings, and combines them (lvl settings are stronger, and will override common settings) into one dictionary.
        """
        commonai: typing.Union[None, dict[str, typing.Any]] = None
        lvlai: typing.Union[None, dict[str, typing.Any]] = None
        with open(path.join("ai", "common.json")) as common_f:
            commonai = json.load(common_f)
        with open(path.join("ai", f"lvl{self.lvl}.json")) as lvl_f:
            lvlai = json.load(lvl_f)
        obj = {}
        if commonai is not None:
            for key, value in commonai.items():
                if key == "Depth":
                    self.depth = value
                    continue
                if key == "Time":
                    self.time = value
                    continue
                obj[key] = value
        if lvlai is not None:
            for key, value in lvlai.items():
                if key == "Depth":
                    self.depth = value
                    continue
                if key == "Time":
                    self.time = value
                    continue
                obj[key] = value
        return obj

    def init(self, scene):
        import chess.engine

        self.settings = self.load()
        print(self.settings)
        if self.settings is None:
            return
        self.scene = scene
        self.engine = chess.engine.SimpleEngine.popen_uci(
            self.scene.game.path_to_stockfish
        )
        self.engine.configure(self.settings)
        self.update_thread.start()

    @property
    def lvl(self):
        return self._lvl

    def update(self, scene) -> None:
        self.run = True

    def update_async(self):
        import chess.engine

        global ct
        while True:
            if ct.is_cancelled:
                ct.finish()
                self.engine.quit()
                return
            if self.run and self.scene is not None:
                try:
                    # print("AI thinking")
                    result = self.engine.play(
                        self.scene.board.chess_board,
                        chess.engine.Limit(time=self.time, depth=20),
                    )
                    # print(f"Result: {result}")
                    if result.move is not None:
                        self.scene.board.make_move_uci(result.move.uci())
                    else:
                        self.scene.board.game_over()
                except BaseException as e:
                    print(e)
                    pass

                self.scene.board.turn_of = self.color.opposite()
                self.run = False

    def dispose(self):
        print("Disposed")
        global ct
        ct.cancel()
        while not ct.cancelled:
            # wait for exiting AI thread
            pass


class InvalidAILvlException(ValueError):
    """Raised when the given AI level is invalid. (Less than 1 or greater than 5)"""
