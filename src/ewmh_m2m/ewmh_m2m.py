#! /usr/bin/env python3

import subprocess
import time
from dataclasses import dataclass
from typing import Set, Iterable, Tuple
import re
import logging

import Xlib
from ewmh import EWMH

ewmh = EWMH()

logging.basicConfig(level=logging.DEBUG)


@dataclass(frozen=True)
class Geometry:
    w: float
    h: float
    x: float
    y: float


def get_screens() -> Set[Geometry]:
    screens = set()
    for line in subprocess.run(["xrandr", "--query"], capture_output=True, text=True).stdout.split('\n'):
        matching = re.match(r"^[^ ]* connected (?P<w>\d*)x(?P<h>\d*)\+(?P<x>\d*)\+(?P<y>\d*) .*", line)
        if matching:
            screens.add(Geometry(**dict(map(lambda i: (i[0], float(i[1])), matching.groupdict().items()))))
    logging.getLogger().debug("Detected screens: %s", screens)
    return screens


def get_active_window():
    return ewmh.getActiveWindow()


def get_window_geometry(window) -> Geometry:
    for line in subprocess.run(["wmctrl", "-l", "-G"], capture_output=True, text=True).stdout.split('\n'):
        splits = line.strip().split()
        if int(splits[0], 16) == window.id:
            return Geometry(
                x=int(splits[2]),
                y=int(splits[3]),
                w=int(splits[4]),
                h=int(splits[5]))


def is_window_maximized(window):
    state = ewmh.getWmState(window, str=True)
    return '_NET_WM_STATE_MAXIMIZED_HORZ' in state, '_NET_WM_STATE_MAXIMIZED_VERT' in state


def set_window_maximized(window, state: Tuple[bool, bool]):
    if state[0] and state[1]:
        ewmh.setWmState(window, 1, '_NET_WM_STATE_MAXIMIZED_HORZ', '_NET_WM_STATE_MAXIMIZED_VERT')
    elif state[0]:
        ewmh.setWmState(window, 1, '_NET_WM_STATE_MAXIMIZED_HORZ')
        if state[1] is not None:
            ewmh.setWmState(window, 0, '_NET_WM_STATE_MAXIMIZED_VERT')
    elif state[1]:
        ewmh.setWmState(window, 1, '_NET_WM_STATE_MAXIMIZED_VERT')
        if state[0] is not None:
            ewmh.setWmState(window, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
    elif state[0] is not None and state[1] is not None:
        ewmh.setWmState(window, 0, '_NET_WM_STATE_MAXIMIZED_HORZ', '_NET_WM_STATE_MAXIMIZED_VERT')
    else:
        return
    ewmh.display.flush()


def set_window_geometry(window, geometry: Geometry):
    args = [
        "wmctrl", "-i",
        "-r", hex(window.id),
        "-e", "0,{0.x:.0f},{0.y:.0f},{0.w:.0f},{0.h:.0f}".format(geometry)
    ]
    logging.getLogger().info("Window move command: %s", " ".join(args))
    subprocess.run(args)


def get_containing_screen(window_geometry: Geometry, screens: Iterable[Geometry]):
    screen_xs = sorted(list({g.x for g in screens}))
    screen_ys = sorted(list({g.y for g in screens}))
    window_screen_x = [x for x in screen_xs if x <= window_geometry.x][-1]
    window_screen_y = [y for y in screen_ys if y <= window_geometry.y][-1]

    return [s for s in screens if s.x == window_screen_x and s.y == window_screen_y][0]


def get_relative_geometry(window: Geometry, screen: Geometry) -> Geometry:
    return Geometry(
        w=window.w / screen.w,
        h=window.h / screen.h,
        x=(window.x - screen.x) / screen.w,
        y=(window.y - screen.y) / screen.h
    )


def get_next_screen(current: Geometry, screens: Iterable[Geometry]) -> Geometry:
    sibblings_screens = sorted([
        g for g in screens
        if (g.x > current.x and g.y == current.y) or (g.y > current.y and g.x == current.x)
    ], key=lambda g: (g.x, g.y))
    logging.getLogger().debug("Next screens: %s", sibblings_screens)
    if len(sibblings_screens) == 0:
        sibblings_screens = sorted([
            g for g in screens
            if (g.x < current.x and g.y == current.y) or (g.y < current.y and g.x == current.x)
        ], key=lambda g: (g.x, g.y))
        logging.getLogger().debug("Previous screens: %s", sibblings_screens)
    return sibblings_screens[0]


def get_absolute_geometry(relative: Geometry, screen: Geometry):
    return Geometry(
        w=relative.w * screen.w,
        h=relative.h * screen.h,
        x=screen.x + relative.x * screen.w,
        y=screen.y + relative.y * screen.h
    )


def main():
    window = get_active_window()
    window_state = is_window_maximized(window)
    set_window_maximized(window, (False, False))
    window_geometry = get_window_geometry(window)
    logging.debug("Window geometry: %s", window_geometry)
    screens = get_screens()
    containing_screen = get_containing_screen(window_geometry, screens)
    logging.debug("Containing screen: %s", containing_screen)
    relative_geometry = get_relative_geometry(window_geometry, containing_screen)
    try:
        new_screen = get_next_screen(containing_screen, screens)
    except IndexError as exc:
        logging.fatal("No sibling screen found")
        # return
        new_screen = containing_screen
    new_window_geometry = get_absolute_geometry(relative_geometry, new_screen)
    logging.debug("New window geometry: %s", new_window_geometry)
    set_window_geometry(window, new_window_geometry)
    set_window_maximized(window, window_state)


if __name__ == "__main__":
    main()
