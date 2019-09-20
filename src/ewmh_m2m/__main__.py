#! /usr/bin/env python3

import logging

from ewmh_m2m.screen import get_screens, get_next_screen
from ewmh_m2m.window import ActiveWindow


def main():
    logging.basicConfig(level=logging.DEBUG)
    window = ActiveWindow()
    initial_window_geometry = window.geometry

    screens = get_screens()
    logging.getLogger().debug("Detected screens: %s", screens)
    containing_screen = initial_window_geometry.get_containing(screens)
    logging.debug("Containing screen: %s", containing_screen)

    window_state = window.maximized
    window.maximized = (False, False)
    window_geometry = window.geometry
    relative_geometry = window_geometry.build_relative(containing_screen)

    try:
        new_screen = get_next_screen(containing_screen, screens)
    except IndexError:
        logging.fatal("No sibling screen found")
    else:
        new_window_geometry = relative_geometry.build_absolute(new_screen)
        logging.debug("New window geometry: %s", new_window_geometry)
        window.geometry = new_window_geometry
    window.maximized = window_state


if __name__ == "__main__":
    main()
