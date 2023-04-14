from ewmh_m2m.geometry import Geometry
from ewmh_m2m.ordinal import Ordinal


class TestGeometry:

    def test_horizontally_not_overlap(self):
        g1 = Geometry(0, 0, 1, 1)
        g2 = Geometry(10, 10, 1, 1)

        assert not g1.horizontally_overlap(g2)
        assert not g2.horizontally_overlap(g1)

    def test_horizontally_overlap(self):
        g1 = Geometry(0, 0, 10, 10)
        g2 = Geometry(100, 0, 10, 10)

        assert g1.horizontally_overlap(g2)
        assert g2.horizontally_overlap(g1)

    def test_vertically_not_overlap(self):
        g1 = Geometry(0, 0, 10, 10)
        g2 = Geometry(100, 100, 10, 10)

        assert not g1.vertically_overlap(g2)
        assert not g2.vertically_overlap(g1)

    def test_vertically_overlap(self):
        g1 = Geometry(0, 0, 10, 10)
        g2 = Geometry(0, 100, 10, 10)

        assert g1.vertically_overlap(g2)
        assert g2.vertically_overlap(g1)

    def test_not_overlap(self):
        g1 = Geometry(0, 0, 10, 10)
        g2 = Geometry(100, 0, 10, 10)
        g3 = Geometry(0, 100, 10, 10)

        assert not g1.overlap(g2)
        assert not g2.overlap(g1)
        assert not g1.overlap(g3)
        assert not g3.overlap(g1)

    def test_overlap(self):
        g1 = Geometry(0, 0, 10, 10)
        g2 = Geometry(1, 1, 8, 8)

        assert g1.overlap(g2)
        assert g2.overlap(g1)

    def test_directions_aligned(self):
        g1 = Geometry(0, 0, 1, 1)
        g2 = Geometry(1, 0, 1, 1)

        assert g1.directions_to(g2) == {Ordinal.EAST, Ordinal.EAST_NORTHEAST, Ordinal.EAST_SOUTHEAST}

    def test_directions_not_aligned(self):
        g1 = Geometry(0, 0, 1, 1)
        g2 = Geometry(1, 1, 1, 1)

        assert g1.directions_to(g2) == {Ordinal.SOUTH_SOUTHEAST, Ordinal.SOUTHEAST, Ordinal.EAST_SOUTHEAST}
