from enum import Enum, auto


class Ordinal(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    @classmethod
    def get(cls, v: str):
        if v.upper()[0] == 'E':
            return Ordinal.EAST
        if v.upper()[0] == 'W':
            return Ordinal.WEST
        if v.upper()[0] == 'N':
            return Ordinal.NORTH
        if v.upper()[0] == 'S':
            return Ordinal.SOUTH
        raise TypeError("No direction match with '{}'".format(v))

    def __str__(self):
        return self.name
