from dataclasses import dataclass


@dataclass(frozen=True)
class Geometry:
    """Data class to manipulate rectangles defined as (x, y, w, h)"""
    x: float = 0
    y: float = 0
    w: float = 0
    h: float = 0

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

    def get_containing(self, containers):
        """Give a list of possible containers, find the one containing self.

        Args:
            containers (Iterable[Geometry]): List of possible containers
        Returns:
            The containing geometry
        """
        container_xs = list({g.x for g in containers})
        container_ys = list({g.y for g in containers})
        container_x = sorted([x for x in container_xs if x < self.x + self.w / 2])[-1]
        container_y = sorted([y for y in container_ys if y <= self.y + self.h / 2])[-1]

        return [s for s in containers if s.x == container_x and s.y == container_y][0]

