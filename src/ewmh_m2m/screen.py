from typing import Set, Iterable, Dict, List, Optional

import xpybutil.xinerama

from ewmh_m2m.geometry import Geometry
from ewmh_m2m.ordinal import Ordinal


def get_screens() -> Set[Geometry]:
    """Get the list of active screens.
    Its geometry represents each screen."""
    return {Geometry(x=s[0], y=s[1], w=s[2], h=s[3]) for s in xpybutil.xinerama.get_monitors()}


def get_sibling_screens(current: Geometry, screens: Iterable[Geometry]) -> Dict[Ordinal, List[Geometry]]:
    """Given a screen and the list of active screens, return the sibling ones.

    Each list is ordered from the nearest screen to the furthest one.
    """
    horizontal_screens = [g for g in screens if current.horizontally_overlap(g)]
    vertical_screens = [g for g in screens if current.vertically_overlap(g)]
    return {
        Ordinal.SOUTH: sorted([g for g in vertical_screens if g.y > current.y], key=lambda g: g.y),
        Ordinal.NORTH: sorted([g for g in vertical_screens if g.y < current.y], key=lambda g: -1 * g.y),
        Ordinal.EAST: sorted([g for g in horizontal_screens if g.x > current.x], key=lambda g: g.x),
        Ordinal.WEST: sorted([g for g in horizontal_screens if g.x < current.x], key=lambda g: -1 * g.x)
    }


def get_sibling_screen(siblings: Dict[Ordinal, List[Geometry]],
                       direction: Ordinal,
                       no_wrap: bool) -> Optional[Geometry]:
    if siblings[direction]:
        return siblings[direction][0]
    else:
        if not no_wrap and siblings[direction.opposite]:
            return siblings[direction.opposite][-1]
    return None

