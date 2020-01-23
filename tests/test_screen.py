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

        assert siblings == {
            Ordinal.SOUTH: [], Ordinal.NORTH: [],
            Ordinal.EAST: [Geometry(30, 0, 10, 10), Geometry(40, 0, 10, 10)],
            Ordinal.WEST: [Geometry(10, 0, 10, 10), Geometry(0, 0, 10, 10)]
        }

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

        assert siblings == {
            Ordinal.EAST: [], Ordinal.WEST: [],
            Ordinal.SOUTH: [Geometry(0, 30, 10, 10), Geometry(0, 40, 10, 10)],
            Ordinal.NORTH: [Geometry(0, 10, 10, 10), Geometry(0, 0, 10, 10)]
        }

    def test_siblings(self):
        screens = sorted(
            [Geometry(x, y, 1, 1) for x in range(5) for y in range(5)],
            key=lambda g: random.random())
        current = Geometry(2, 2, 1, 1)

        siblings = ewmh_m2m.screen.get_sibling_screens(current, screens)

        assert siblings == {
            Ordinal.NORTH: [Geometry(2, 1, 1, 1), Geometry(2, 0, 1, 1)],
            Ordinal.EAST: [Geometry(3, 2, 1, 1), Geometry(4, 2, 1, 1)],
            Ordinal.SOUTH: [Geometry(2, 3, 1, 1), Geometry(2, 4, 1, 1)],
            Ordinal.WEST: [Geometry(1, 2, 1, 1), Geometry(0, 2, 1, 1)]
        }

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
