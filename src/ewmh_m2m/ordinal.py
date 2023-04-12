from enum import Enum


class Ordinal(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    NEXT = 4
    PREV = 5

    @classmethod
    def get(cls, v: str):
        if v.upper()[0] == 'E':
            return Ordinal.EAST
        if v.upper()[0] == 'W':
            return Ordinal.WEST
        if v.upper()[0:2] == 'NO':
            return Ordinal.NORTH
        if v.upper()[0] == 'S':
            return Ordinal.SOUTH
        if v.upper()[0:2] == 'NE':
            return Ordinal.NEXT
        if v.upper()[0] == 'P':
            return Ordinal.PREV
        raise TypeError("No direction match with '{}'".format(v))

    def __str__(self):
        return self.name

    @property
    def opposite(self):
        if self is Ordinal.NORTH:
            return Ordinal.SOUTH
        if self is Ordinal.SOUTH:
            return Ordinal.NORTH
        if self is Ordinal.EAST:
            return Ordinal.WEST
        if self is Ordinal.WEST:
            return Ordinal.EAST
        if self is Ordinal.NEXT:
            return Ordinal.PREV
        if self is Ordinal.PREV:
            return Ordinal.NEXT
