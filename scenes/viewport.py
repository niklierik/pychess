import pygame

# Const, scenes will be made for this screen size
reference = (1920, 1080)


class Viewport:
    """
    Viewport class is used to calculate the positions for the scenes so the game can be used for multiple displays.
    """

    def __init__(self, screen_size: tuple[int, int]) -> None:
        self.screen_size = screen_size

    @property
    def screen_size(self) -> None:
        return self._screen_size

    @screen_size.setter
    def screen_size(self, screen_size: tuple[int, int]) -> None:
        self._screen_size = screen_size
        self.a = (
            int(reference[0] / reference[1] * self._screen_size[1]),
            int(self._screen_size[1]),
        )
        self.width_dif = self._screen_size[0] - self.a[0]
        if self.width_dif < 0:
            self.width_offset = 0
            self.width_dif = 0
            self.a = (
                int(self._screen_size[0]),
                int(reference[1] / reference[0] * self._screen_size[0]),
            )
            self.height_dif = self.screen_size[1] - self.a[1]
            self.height_offset = self.height_dif / 2.0
        else:
            self.width_offset = self.width_dif / 2.0
            self.height_offset = 0
            self.height_dif = 0

    def get_position(self, reference_pos: tuple[int, int]) -> tuple[float, float]:
        return (
            float(self.a[0]) / float(reference[0]) * float(reference_pos[0]),
            float(self.a[1]) / float(reference[1]) * float(reference_pos[1]),
        )

    def get_rect(self, rect: pygame.Rect) -> pygame.Rect:
        pos = self.get_position(rect.topleft)
        pos = (pos[0] + self.width_offset, pos[1] + self.height_offset)
        size = self.get_position(rect.size)
        return pygame.Rect(pos[0], pos[1], size[0], size[1])
