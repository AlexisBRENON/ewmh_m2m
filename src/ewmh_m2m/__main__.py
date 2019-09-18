#! /usr/bin/env python3
import argparse
import logging

from ewmh_m2m.ordinal import Ordinal
from ewmh_m2m.screen import get_screens, get_next_screen
from ewmh_m2m.window import ActiveWindow


def move_to_screen(args):
    window = ActiveWindow()
    initial_window_geometry = window.geometry

    screens = get_screens()
    logging.debug("Detected screens: %s", screens)
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
    window.conn.flush()


def main():
    logging.basicConfig(level=logging.DEBUG)
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--direction", "-d",
        action="store",
        type=Ordinal.get,
        choices=list(Ordinal),
        default=Ordinal.EAST.name.capitalize(),
        help="Direction in which to move the window (default: %(default)s)")
    arg_parser.add_argument("--no-wrap", "-W", action="store_true", help="Do not go back if no screen found.")
    print(arg_parser.parse_args())
    # move_to_screen(arg_parser.parse_args())


if __name__ == "__main__":
    main()
