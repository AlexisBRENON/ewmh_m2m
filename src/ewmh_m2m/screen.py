import re
import subprocess
from typing import Set, Iterable

from ewmh_m2m.geometry import Geometry


def get_screens() -> Set[Geometry]:
    screens = set()
    for line in subprocess.run(["xrandr", "--query"], capture_output=True, text=True).stdout.split('\n'):
        matching = re.match(r"^[^ ]* connected (?P<w>\d*)x(?P<h>\d*)\+(?P<x>\d*)\+(?P<y>\d*) .*", line)
        if matching:
            screens.add(Geometry(**dict(map(lambda i: (i[0], float(i[1])), matching.groupdict().items()))))
    return screens


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

