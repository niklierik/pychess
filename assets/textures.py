# Path mapping for textures


class Textures:
    def __init__(self):
        self.board = Board()
        self.buttons = Buttons()

    def __str__(self):
        return "assets/textures/"


class Buttons:
    def __init__(self):
        self.icons = Icons()

    def __str__(self):
        return "assets/textures/buttons/"


class Icons:
    def __init__(self):
        self.add = self.__str__() + "add.png"
        self.close = self.__str__() + "close.png"
        self.help = self.__str__() + "help.png"
        self.pause = self.__str__() + "pause.png"
        self.play = self.__str__() + "play.png"
        self.remove = self.__str__() + "remove.png"
        self.restart = self.__str__() + "restart.png"
        self.settings = self.__str__() + "settings.png"
        self.volume_down = self.__str__() + "volume_down.png"
        self.volume_up = self.__str__() + "volume_up.png"

    def __str__(self):
        return "assets/textures/buttons/icons/"


class Board:
    def __init__(self):
        self.wooden = WoodenBoard()
        self.regular = RegularBoard()

    def __str__(self):
        return "assets/textures/board/"


class WoodenBoard:
    def __init__(self):
        self.light = self.__str__() + "light.png"
        self.dark = self.__str__() + "dark.png"

    def __str__(self):
        return "assets/textures/board/wooden/"


class RegularBoard:
    def __init__(self):
        self.light = self.__str__() + "light.png"
        self.dark = self.__str__() + "dark.png"

    def __str__(self):
        return "assets/textures/board/regular/"
