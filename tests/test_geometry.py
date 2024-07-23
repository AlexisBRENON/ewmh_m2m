from ewmh_m2m.geometry import Geometry
from ewmh_m2m.ordinal import Ordinal


class TestGeometry:

    def test_directions_aligned(self):
        """
          0    1    2
        0 +----+----+
          | g1 | g2 |
        1 +----+----+
        """
        g1 = Geometry(0, 0, 1, 1)
        g2 = Geometry(1, 0, 1, 1)

        assert list(g1.directions_to(g2)) == [Ordinal.EAST]

    def test_directions_not_aligned(self):
        """
          0    1    2
        0 +----+
          | g1 |
        1 +----+----+
               | g2 |
        2      +----+
        """
        g1 = Geometry(0, 0, 1, 1)
        g2 = Geometry(1, 1, 1, 1)

        assert list(g1.directions_to(g2)) == [Ordinal.SOUTHEAST]

    def test_directions_overlap(self):
        """
          0    2    4
        0 +----+
        1 | g1 +----+
        2 +----+ g2 |
        3      +----+
        """
        g1 = Geometry(0, 0, 2, 2)
        g2 = Geometry(2, 1, 2, 2)

        assert list(g1.directions_to(g2)) == [
            Ordinal.EAST_SOUTHEAST,
            Ordinal.SOUTHEAST,
        ]

    def test_gleb_setup(self):
        """
        https://github.com/AlexisBRENON/ewmh_m2m/pull/25
             0    1080     3000
        0          ┌─────────┐
        130  ┌─────┤         │
             │     │    g1   │
             │     │         │
        1080 │  g2 ├─────────┤
             │     │         │
             │     │    g3   │
        2050 └─────┤         │
        2160       └─────────┘
        """
        g1 = Geometry(1080, 0, 1920, 1080)
        g2 = Geometry(0, 130, 1080, 1920)
        g3 = Geometry(1080, 1080, 1920, 1080)

        assert list(g1.directions_to(g2)) == [Ordinal.WEST_SOUTHWEST, Ordinal.WEST]
        assert list(g1.directions_to(g3)) == [Ordinal.SOUTH]
        assert list(g2.directions_to(g1)) == [Ordinal.EAST_NORTHEAST, Ordinal.EAST]
        assert list(g2.directions_to(g3)) == [Ordinal.EAST_SOUTHEAST, Ordinal.EAST]
        assert list(g3.directions_to(g1)) == [Ordinal.NORTH]
        assert list(g3.directions_to(g2)) == [Ordinal.WEST_NORTHWEST, Ordinal.WEST]
