import math
from typing import Set, Iterable, Dict, List, Optional

import xpybutil.xinerama

from ewmh_m2m.geometry import Geometry
from ewmh_m2m.ordinal import Ordinal


def get_screens() -> Set[Geometry]:
    """Get the list of active screens.
    Its geometry represents each screen."""
    return {
        Geometry(x=s[0], y=s[1], w=s[2], h=s[3])
        for s in xpybutil.xinerama.get_monitors()
    }


def get_sibling_screens(
    current: Geometry, screens: Iterable[Geometry]
) -> Dict[Ordinal, List[Geometry]]:
    """Given a screen and the list of active screens, return the sibling ones.

    Each list is ordered from the nearest screen to the furthest one.
    """
    directions = [(g, current.directions_to(g)) for g in screens if g != current]
    return {
        o: sorted(
            [g for g, dirs in directions if o in dirs],
            key=lambda g: (
                math.hypot(g.x - current.x, g.y - current.y),
                math.copysign(g.x, o.cos)
                if abs(o.cos) > abs(o.sin)
                else math.copysign(g.y, o.sin),
            ),
        )
        for o in Ordinal
    }


def get_sibling_screen(
    siblings: Dict[Ordinal, List[Geometry]], direction: Ordinal, no_wrap: bool
) -> Optional[Geometry]:
    if siblings[direction]:
        return siblings[direction][0]
    else:
        if not no_wrap and siblings[direction.opposite]:
            return siblings[direction.opposite][-1]
    return None
