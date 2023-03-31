"""
  Viewport class is used to calculate the positions for the scenes so the game can be used for multiple displays.
"""

# Const, scenes will be made for this screen size
reference = (1920, 1080)


class Viewport:
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

    def get_position(self, reference_pos: tuple[int, int]) -> tuple[int, int]:
        return (
            self.width_offset + self.a[0] / reference[0] * reference_pos[0],
            self.a[1] / reference[1] * reference_pos[1],
        )
