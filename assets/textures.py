# Loading of textures


import pygame
import os.path as path


class Textures:
    def __init__(self):
        self.board = Board()
        self.buttons = Buttons()

    def __str__(self):
        return "assets/textures/"


class Buttons:
    def __init__(self):
        self.icons = Icons(path.join(self.__str__(), "icons"), True)
        self.play = PlayButtons(path.join(self.__str__(), "play"), True)

    def __str__(self):
        return "assets/textures/buttons/"


class PlayButtons:
    def __init__(self, parent: str, create_hover: bool):
        self.parent = parent
        if create_hover:
            self.hover = PlayButtons(path.join(self.__str__(), "hover"), False)
        self.ai = pygame.image.load(path.join(self.__str__(), "ai.png"))
        self.ai = pygame.image.load(path.join(self.__str__(), "player.png"))
        self.ai = pygame.image.load(path.join(self.__str__(), "lvl1.png"))
        self.ai = pygame.image.load(path.join(self.__str__(), "lvl2.png"))
        self.ai = pygame.image.load(path.join(self.__str__(), "lvl3.png"))
        self.ai = pygame.image.load(path.join(self.__str__(), "lvl4.png"))
        self.ai = pygame.image.load(path.join(self.__str__(), "lvl5.png"))

    def __str__(self) -> str:
        return self.parent


class Icons:
    def __init__(self, parent, create_hover: bool):
        self.parent = parent
        self.add = pygame.image.load(path.join(self.__str__(), "add.png"))
        self.close = pygame.image.load(path.join(self.__str__(), "close.png"))
        self.help = pygame.image.load(path.join(self.__str__(), "help.png"))
        self.pause = pygame.image.load(path.join(self.__str__(), "pause.png"))
        self.play = pygame.image.load(path.join(self.__str__(), "play.png"))
        self.remove = pygame.image.load(path.join(self.__str__(), "remove.png"))
        self.restart = pygame.image.load(path.join(self.__str__(), "restart.png"))
        self.settings = pygame.image.load(path.join(self.__str__(), "settings.png"))
        self.volume_down = pygame.image.load(
            path.join(self.__str__(), "volume_down.png")
        )
        self.volume_up = pygame.image.load(path.join(self.__str__(), "volume_up.png"))
        if create_hover:
            self.hover = Icons(path.join(self.__str__(), "hover"), False)

    def __str__(self):
        return self.parent


class Pieces:
    def __init__(self):
        self.regular = PiecesTheme(path.join(self.__str__(), "regular"))

    def __str__(self):
        return "assets/textures/pieces"


class PiecesTheme:
    def __init__(self, parent: str):
        self.parent = parent
        self.white = PiecesTextures()
        self.black = PiecesTextures()

    def __str__(self) -> str:
        return self.parent


class PiecesTextures:
    def __init__(self, parent: str):
        self.parent = parent
        self.bishop = pygame.image.load(path.join(self.__str__(), "bishop.png"))
        self.king = pygame.image.load(path.join(self.__str__(), "king.png"))
        self.knight = pygame.image.load(path.join(self.__str__(), "knight.png"))
        self.pawn = pygame.image.load(path.join(self.__str__(), "pawn.png"))
        self.queen = pygame.image.load(path.join(self.__str__(), "queen.png"))
        self.rook = pygame.image.load(path.join(self.__str__(), "rook.png"))

    def __str__(self):
        return self.parent


class Board:
    def __init__(self):
        self.wooden = BoardTheme(path.join(self.__str__(), "wooden/"))
        self.regular = BoardTheme(path.join(self.__str__(), "regular/"))

    def __str__(self):
        return "assets/textures/board/"


class BoardTheme:
    def __init__(self, parent: str):
        self.parent = parent
        self.light = pygame.image.load(path.join(self.__str__(), "light.png"))
        self.dark = pygame.image.load(path.join(self.__str__(), "dark.png"))

    def __str__(self):
        return self.parent
