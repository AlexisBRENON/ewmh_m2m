from typing import Set, Iterable

import xpybutil.xinerama

from ewmh_m2m.geometry import Geometry


def get_screens() -> Set[Geometry]:
    return {Geometry(x=s[0], y=s[1], w=s[2], h=s[3]) for s in xpybutil.xinerama.get_monitors()}


def get_next_screen(current: Geometry, screens: Iterable[Geometry]) -> Geometry:
    siblings_screens = sorted([
        g for g in screens
        if (g.x > current.x and g.y == current.y) or (g.y > current.y and g.x == current.x)
    ], key=lambda g: (g.x, g.y))
    if len(siblings_screens) == 0:
        siblings_screens = sorted([
            g for g in screens
            if (g.x < current.x and g.y == current.y) or (g.y < current.y and g.x == current.x)
        ], key=lambda g: (g.x, g.y))
    return siblings_screens[0]

