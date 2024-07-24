from enum import Enum
import math

_HEXADAN = 360 / 16

class Ordinal(Enum):
    EAST = 0 * _HEXADAN
    NORTH = 4 * _HEXADAN
    WEST = 8 * _HEXADAN
    SOUTH = 12 * _HEXADAN

    NORTHEAST = 2 * _HEXADAN
    NORTHWEST = 6 * _HEXADAN
    SOUTHWEST = 10 * _HEXADAN
    SOUTHEAST = 14 * _HEXADAN

    EAST_NORTHEAST = 1 * _HEXADAN
    NORTH_NORTHEAST = 3 * _HEXADAN
    NORTH_NORTHWEST = 5 * _HEXADAN
    WEST_NORTHWEST = 7 * _HEXADAN
    WEST_SOUTHWEST = 9 * _HEXADAN
    SOUTH_SOUTHWEST = 11 * _HEXADAN
    SOUTH_SOUTHEAST = 13 * _HEXADAN
    EAST_SOUTHEAST = 15 * _HEXADAN

    def __init__(self, value) -> None:
        self.sin = round(math.sin(math.radians(value)), 6)
        self.cos = round(math.cos(math.radians(value)), 6)

    def __str__(self) -> str:
        return self.name

    @property
    def opposite(self):
        return Ordinal((self.value + 180) % 360)
