from collections import namedtuple
from dataclasses import dataclass

import numpy as np

CoordsLists = namedtuple('CoordsLists', 'x y')


class ParseError(Exception):
    pass


@dataclass(order=True, frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self, other):
        if type(other) is type(self):
            return Coord(self.x + other.x, self.y + other.y)
        else:
            return Coord(self.x + other, self.y + other)

    def __sub__(self, other):
        return Coord(self[0] - other[0], self[1] - other[1])

    def __iter__(self):
        yield self.x
        yield self.y

    def __mul__(self, scalar):
        return Coord(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return Coord(self.x * scalar, self.y * scalar)

    def __getitem__(self, index):
        if index == 'x' or index == 0:
            return self.x
        elif index == 'y' or index == 1:
            return self.y
        else:
            raise IndexError('Unknown index.')
