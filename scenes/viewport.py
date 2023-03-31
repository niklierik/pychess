import pygame

# Const, scenes will be made for this screen size
reference = (1920, 1080)


class Viewport:
    """
    Viewport class is used to calculate the positions for the scenes so the game can be used for multiple displays.
    """

    def __init__(self, screen_size: tuple[int, int]) -> None:
        self.screen_size = screen_size
        # Screen size with aspect ratio kept (height kept, width scaled)
        self.a = (reference[0] / reference[1] * screen_size[1], screen_size[1])
        self.width_dif = screen_size[0] - self.a[0]
        if self.width_dif < 0:
            raise ValueError(
                "Difference between aspect ration kept screen size and real screen size is negative. This should not happen."
            )
        # Keeping aspect ration means that we need to offset the scenes horizontally
        self.width_offset = self.width_dif / 2.0

    def get_position(self, reference_pos: tuple[int, int]) -> tuple[float, float]:
        return (
            float(self.width_offset)
            + float(self.a[0]) / float(reference[0]) * float(reference_pos[0]),
            float(self.a[1]) / float(reference[1]) * float(reference_pos[1]),
        )

    def get_rect(self, rect: pygame.Rect) -> pygame.Rect:
        pos = self.get_position(rect.topleft)
        pos2 = self.get_position(rect.bottomright)
        size = (pos2[0] - pos[0], pos2[1] - pos[1])
        return pygame.Rect(int(pos[0]), int(pos[1]), int(size[0]), int(size[1]))
