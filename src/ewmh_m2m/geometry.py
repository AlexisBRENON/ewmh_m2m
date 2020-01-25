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

    def horizontally_overlap(self, other) -> bool:
        return self.y < other.y + other.h and self.y + self.h > other.y

    def vertically_overlap(self, other) -> bool:
        return self.x < other.x + other.w and self.x + self.w > other.x

    def overlap(self, other) -> bool:
        return self.horizontally_overlap(other) and self.vertically_overlap(other)

    def __eq__(self, other):
        return list(self) == list(other)

    def __repr__(self):
        return "Geometry({0.x}, {0.y}, {0.w}, {0.h})".format(self)

    def __hash__(self):
        return hash(tuple(self))
