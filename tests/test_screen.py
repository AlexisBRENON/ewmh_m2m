# -*- coding: utf-8 -*-
import random

import ewmh_m2m.screen
from ewmh_m2m.geometry import Geometry
from ewmh_m2m.ordinal import Ordinal

__author__ = "Alexis BRENON"
__copyright__ = "Alexis BRENON"
__license__ = "mit"


class TestScreen:

    def test_siblings_single_screen(self):
        current = Geometry(0, 0, 10, 10)
        screens = [current]

        siblings = ewmh_m2m.screen.get_sibling_screens(current, screens)

        assert siblings == {o: [] for o in list(Ordinal)}

    def test_siblings_horizontal(self):
        current = Geometry(20, 0, 10, 10)
        screens = sorted([
            Geometry(0, 0, 10, 10), Geometry(10, 0, 10, 10),
            current,
            Geometry(30, 0, 10, 10), Geometry(40, 0, 10, 10)
        ],
            key=lambda g: random.random()
        )

        siblings = ewmh_m2m.screen.get_sibling_screens(current, screens)

        assert siblings[Ordinal.EAST] == [Geometry(30, 0, 10, 10), Geometry(40, 0, 10, 10)]
        assert siblings[Ordinal.WEST] == [Geometry(10, 0, 10, 10), Geometry(0, 0, 10, 10)]

    def test_siblings_vertical(self):
        current = Geometry(0, 20, 10, 10)
        screens = sorted([
            Geometry(0, 0, 10, 10), Geometry(0, 10, 10, 10),
            current,
            Geometry(0, 30, 10, 10), Geometry(0, 40, 10, 10)
        ],
            key=lambda g: random.random()
        )

        siblings = ewmh_m2m.screen.get_sibling_screens(current, screens)

        assert siblings[Ordinal.SOUTH] == [Geometry(0, 30, 10, 10), Geometry(0, 40, 10, 10)]
        assert siblings[Ordinal.NORTH] == [Geometry(0, 10, 10, 10), Geometry(0, 0, 10, 10)]

    def test_siblings(self):
        screens = sorted(
            [Geometry(x, y, 1, 1) for x in range(5) for y in range(5)],
            key=lambda g: random.random())
        current = Geometry(2, 2, 1, 1)

        siblings = ewmh_m2m.screen.get_sibling_screens(current, screens)

        assert siblings[Ordinal.NORTH] == [Geometry(2, 1, 1, 1), Geometry(2, 0, 1, 1)]
        assert siblings[Ordinal.EAST] == [Geometry(3, 2, 1, 1), Geometry(4, 2, 1, 1)]
        assert siblings[Ordinal.SOUTH] == [Geometry(2, 3, 1, 1), Geometry(2, 4, 1, 1)]
        assert siblings[Ordinal.WEST] == [Geometry(1, 2, 1, 1), Geometry(0, 2, 1, 1)]

        assert siblings[Ordinal.NORTHEAST] == [Geometry(3, 1, 1, 1), Geometry(3, 0, 1, 1), Geometry(4, 1, 1, 1), Geometry(4, 0, 1, 1)]
        assert siblings[Ordinal.NORTHWEST] == [Geometry(1, 1, 1, 1), Geometry(1, 0, 1, 1), Geometry(0, 1, 1, 1), Geometry(0, 0, 1, 1)]
        assert siblings[Ordinal.SOUTHWEST] == [Geometry(1, 3, 1, 1), Geometry(1, 4, 1, 1), Geometry(0, 3, 1, 1), Geometry(0, 4, 1, 1)]
        assert siblings[Ordinal.SOUTHEAST] == [Geometry(3, 3, 1, 1), Geometry(3, 4, 1, 1), Geometry(4, 3, 1, 1), Geometry(4, 4, 1, 1)]

        assert set(siblings[Ordinal.EAST_NORTHEAST]) == set(siblings[Ordinal.EAST] + siblings[Ordinal.NORTHEAST])
        assert set(siblings[Ordinal.NORTH_NORTHEAST]) == set(siblings[Ordinal.NORTH] + siblings[Ordinal.NORTHEAST])
        assert set(siblings[Ordinal.NORTH_NORTHWEST]) == set(siblings[Ordinal.NORTH] + siblings[Ordinal.NORTHWEST])
        assert set(siblings[Ordinal.WEST_NORTHWEST]) == set(siblings[Ordinal.WEST] + siblings[Ordinal.NORTHWEST])
        assert set(siblings[Ordinal.WEST_SOUTHWEST]) == set(siblings[Ordinal.WEST] + siblings[Ordinal.SOUTHWEST])
        assert set(siblings[Ordinal.SOUTH_SOUTHWEST]) == set(siblings[Ordinal.SOUTH] + siblings[Ordinal.SOUTHWEST])
        assert set(siblings[Ordinal.SOUTH_SOUTHEAST]) == set(siblings[Ordinal.SOUTH] + siblings[Ordinal.SOUTHEAST])
        assert set(siblings[Ordinal.EAST_SOUTHEAST]) == set(siblings[Ordinal.EAST] + siblings[Ordinal.SOUTHEAST])



    def test_siblings_gh_issue_14(self):
        """
        Inspired by issue 14: https://github.com/AlexisBRENON/ewmh_m2m/issues/14
        """
        screens = {Geometry(2960, 0, 1920, 1200), Geometry(0, 176, 1280, 1024), Geometry(1280, 150, 1680, 1050)}
        current = Geometry(0, 176, 1280, 1024)

        siblings = ewmh_m2m.screen.get_sibling_screens(current, screens)

        assert siblings[Ordinal.EAST] == [Geometry(1280, 150, 1680, 1050), Geometry(2960, 0, 1920, 1200)]

    def test_sibling_nominal(self):
        siblings = {
            Ordinal.EAST: [Geometry(1, 0, 1, 1), Geometry(2, 0, 1, 1)]
        }

        assert ewmh_m2m.screen.get_sibling_screen(siblings, Ordinal.EAST, no_wrap=False) == Geometry(1, 0, 1, 1)

    def test_sibling_wrap(self):
        siblings = {
            Ordinal.EAST: [Geometry(1, 0, 1, 1), Geometry(2, 0, 1, 1)],
            Ordinal.WEST: []
        }

        assert ewmh_m2m.screen.get_sibling_screen(siblings, Ordinal.WEST, no_wrap=False) == Geometry(2, 0, 1, 1)

    def test_sibling_no_wrap(self):
        siblings = {
            Ordinal.EAST: [Geometry(1, 0, 1, 1), Geometry(2, 0, 1, 1)],
            Ordinal.WEST: []
        }

        assert ewmh_m2m.screen.get_sibling_screen(siblings, Ordinal.WEST, no_wrap=True) is None
