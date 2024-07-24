import math
import typing
from ewmh_m2m.ordinal import Ordinal


class Geometry:
    """Data class to manipulate rectangles defined as (x, y, w, h)"""
    def __init__(self, x: float = 0, y: float = 0, w: float = 0, h: float = 0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.w
        yield self.h

    def build_relative(self, container):
        """Build a new Geometry, representing self, relative to the "parent" container"""
        return Geometry(
            w=self.w / container.w,
            h=self.h / container.h,
            x=(self.x - container.x) / container.w,
            y=(self.y - container.y) / container.h
        )

    def build_absolute(self, container):
        """Build a new Geometry, representing self, which is relative to container"""
        return Geometry(
            w=int(self.w * container.w),
            h=int(self.h * container.h),
            x=int(container.x + self.x * container.w),
            y=int(container.y + self.y * container.h)
        )

    @property
    def center(self) -> "Geometry":
        return Geometry(x=self.x + self.w / 2, y=self.y + self.h / 2)

    def directions_to(self, other: "Geometry") -> typing.Collection[Ordinal]:
        vector = Geometry(
            other.center.x - self.center.x, other.center.y - self.center.y
        )
        vector_norm = math.sqrt(vector.x**2 + vector.y**2)
        vector_cos = vector.x / vector_norm
        vector_sin = -vector.y / vector_norm

        res = list(
            sorted(
                [
                    (
                        (o.cos - vector_cos) ** 2 + (o.sin - vector_sin) ** 2,
                        o,
                    )
                    for o in list(Ordinal)
                ],
                key=lambda t: t[0],
            )
        )
        return [t[1] for t in res if t[0] <= 0.152]

    def __eq__(self, other):
        return list(self) == list(other)

    def __repr__(self):
        return "Geometry({0.x}, {0.y}, {0.w}, {0.h})".format(self)

    def __hash__(self):
        return hash(tuple(self))
