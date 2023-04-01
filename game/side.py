import enum


class Side(enum.Enum):
    QUEEN = 0
    KING = 1

    def opposite(self) -> "Side":
        return Side(1 - self.value)
