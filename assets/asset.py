# Loading of textures


import pygame
import os.path as path


class Assets:
    def __init__(self) -> None:
        self.textures = Textures()
        self.fonts = Fonts()

    @staticmethod
    def __str__() -> str:
        return "assets"


class Fonts:
    def __init__(self) -> None:
        self.main = pygame.font.Font(path.join(Fonts.__str__(), "main.ttf"), 20)

    @staticmethod
    def __str__() -> str:
        return path.join(Assets.__str__(), "fonts")


class Textures:
    def __init__(self):
        self.board = Board()
        self.buttons = Buttons()
        self.pieces = Pieces()
        self.icon = pygame.image.load(path.join(Textures.__str__(), "icon.png"))
        self.chars = Chars()

    @staticmethod
    def __str__():
        return path.join(Assets.__str__(), "textures")


class Chars:
    def __init__(self) -> None:
        self.a = pygame.image.load(path.join(Chars.__str__(), "a.png"))
        self.b = pygame.image.load(path.join(Chars.__str__(), "b.png"))
        self.c = pygame.image.load(path.join(Chars.__str__(), "c.png"))
        self.d = pygame.image.load(path.join(Chars.__str__(), "d.png"))
        self.e = pygame.image.load(path.join(Chars.__str__(), "e.png"))
        self.f = pygame.image.load(path.join(Chars.__str__(), "f.png"))
        self.g = pygame.image.load(path.join(Chars.__str__(), "g.png"))
        self.h = pygame.image.load(path.join(Chars.__str__(), "h.png"))
        self._1 = pygame.image.load(path.join(Chars.__str__(), "1.png"))
        self._2 = pygame.image.load(path.join(Chars.__str__(), "2.png"))
        self._3 = pygame.image.load(path.join(Chars.__str__(), "3.png"))
        self._4 = pygame.image.load(path.join(Chars.__str__(), "4.png"))
        self._5 = pygame.image.load(path.join(Chars.__str__(), "5.png"))
        self._6 = pygame.image.load(path.join(Chars.__str__(), "6.png"))
        self._7 = pygame.image.load(path.join(Chars.__str__(), "7.png"))
        self._8 = pygame.image.load(path.join(Chars.__str__(), "8.png"))
        self.files = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        self.ranks = [
            self._1,
            self._2,
            self._3,
            self._4,
            self._5,
            self._6,
            self._7,
            self._8,
        ]

    @staticmethod
    def __str__():
        return path.join(Textures.__str__(), "chars")


class Buttons:
    def __init__(self):
        self.icons = Icons(path.join(self.__str__(), "icons"), True)
        self.play = PlayButtons(path.join(self.__str__(), "play"), True)

    def __str__(self):
        return path.join(Textures.__str__(), "buttons")


class PlayButtons:
    def __init__(self, parent: str, create_subs: bool):
        self.parent = parent
        if create_subs:
            self.hover = PlayButtons(path.join(self.__str__(), "hover"), False)
        if create_subs:
            self.on_pressed = PlayButtons(
                path.join(self.__str__(), "on_pressed"), False
            )
        self.ai = pygame.image.load(path.join(self.__str__(), "ai.png"))
        self.analyse = pygame.image.load(path.join(self.__str__(), "analyse.png"))
        self.player = pygame.image.load(path.join(self.__str__(), "player.png"))
        self.lvl1 = pygame.image.load(path.join(self.__str__(), "lvl1.png"))
        self.lvl2 = pygame.image.load(path.join(self.__str__(), "lvl2.png"))
        self.lvl3 = pygame.image.load(path.join(self.__str__(), "lvl3.png"))
        self.lvl4 = pygame.image.load(path.join(self.__str__(), "lvl4.png"))
        self.lvl5 = pygame.image.load(path.join(self.__str__(), "lvl5.png"))
        self.lvl = [self.lvl1, self.lvl2, self.lvl3, self.lvl4, self.lvl5]

    def __str__(self) -> str:
        return self.parent


class Icons:
    def __init__(self, parent, create_subs: bool):
        self.parent = parent
        if create_subs:
            self.hover = Icons(path.join(self.__str__(), "hover"), False)
            self.on_pressed = Icons(path.join(self.__str__(), "on_pressed"), False)
        self.add = pygame.image.load(path.join(self.__str__(), "add.png"))
        self.close = pygame.image.load(path.join(self.__str__(), "close.png"))
        self.help = pygame.image.load(path.join(self.__str__(), "help.png"))
        self.pause = pygame.image.load(path.join(self.__str__(), "pause.png"))
        self.play = pygame.image.load(path.join(self.__str__(), "play.png"))
        self.remove = pygame.image.load(path.join(self.__str__(), "remove.png"))
        self.restart = pygame.image.load(path.join(self.__str__(), "restart.png"))
        self.refresh = pygame.image.load(path.join(self.__str__(), "refresh.png"))
        self.settings = pygame.image.load(path.join(self.__str__(), "settings.png"))
        self.volume_down = pygame.image.load(
            path.join(self.__str__(), "volume_down.png")
        )
        self.volume_up = pygame.image.load(path.join(self.__str__(), "volume_up.png"))

    def __str__(self):
        return self.parent


class Pieces:
    def __init__(self):
        self.regular = PiecesTheme(path.join(Pieces.__str__(), "regular"))
        self.wooden = PiecesTheme(path.join(Pieces.__str__(), "wooden"))

    @staticmethod
    def __str__():
        return path.join(Textures.__str__(), "pieces")


class PiecesTheme:
    def __init__(self, parent: str):
        self.parent = parent
        self.white = PiecesTextures(path.join(parent, "white"))
        self.black = PiecesTextures(path.join(parent, "black"))

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
        self.wooden = BoardTheme(path.join(self.__str__(), "wooden"))
        self.regular = BoardTheme(path.join(self.__str__(), "regular"))

    def __str__(self):
        return path.join(Textures.__str__(), "board")


class BoardTheme:
    def __init__(self, parent: str):
        self.parent = parent
        self.light = pygame.image.load(path.join(self.__str__(), "light.png"))
        self.dark = pygame.image.load(path.join(self.__str__(), "dark.png"))

    def __str__(self):
        return self.parent
