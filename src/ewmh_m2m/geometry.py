from dataclasses import dataclass


@dataclass(frozen=True)
class Geometry:
    """Data class to manipulate rectangles defined as (x, y, w, h)"""
    x: float = 0
    y: float = 0
    w: float = 0
    h: float = 0

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

