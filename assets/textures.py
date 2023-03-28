# Path mapping for textures
class Textures:
    def __init__(self):
        self.board = Board()


class Board:
    def __init__(self):
        self.wooden = WoodenBoard()


class WoodenBoard:
    def __init__(self):
        self.bright = "assets/textures/board/wooden/light.png"
        self.dark = "assets/textures/board/wooden/dark.png"


class RegularBoard:
    def __init__(self):
        self.bright = "assets/textures/board/regular/light.png"
        self.dark = "assets/textures/board/regular/dark.png"
