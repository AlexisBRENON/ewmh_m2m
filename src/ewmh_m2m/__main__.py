#! /usr/bin/env python3
import argparse
import logging

import xpybutil.rect

import ewmh_m2m
from ewmh_m2m.ordinal import Ordinal
from ewmh_m2m.screen import get_screens, get_sibling_screens, get_sibling_screen
from ewmh_m2m.window import ActiveWindow
from ewmh_m2m.geometry import Geometry


_logger = logging.getLogger(__name__)


def move_to_screen(args):
    window = ActiveWindow()
    initial_window_geometry = window.geometry

    screens = get_screens()
    _logger.debug("Detected screens: %s", screens)
    containing_screen = Geometry(*xpybutil.rect.get_monitor_area(
        initial_window_geometry, screens
    ))
    _logger.debug("Containing screen: %s", containing_screen)

    with window.movable() as win:
        window_geometry = win.geometry
        relative_geometry = window_geometry.build_relative(containing_screen)

        new_screen = get_sibling_screen(
            get_sibling_screens(containing_screen, screens),
            args.direction, args.no_wrap)
        if not new_screen:
            raise ValueError("No sibling screen found")

        new_window_geometry = relative_geometry.build_absolute(new_screen)
        _logger.debug("New window geometry: %s", new_window_geometry)
        win.geometry = new_window_geometry


def setup_log(args):
    log_level = logging.WARNING + logging.DEBUG * (args.quiet - args.verbose)
    logging.basicConfig(level=log_level)


def main():
    arg_parser = argparse.ArgumentParser(
        epilog="""Version information: {}""".format(ewmh_m2m.__version__)
    )
    arg_parser.add_argument("--verbose", "-v", action="count", default=0, help="Increase verbosity (may be repeated)")
    arg_parser.add_argument("--quiet", "-q", action="count", default=0, help="Decrease verbosity (may be repeated)")
    arg_parser.add_argument(
        "--direction", "-d",
        action="store",
        type=Ordinal.get,
        choices=list(Ordinal),
        default=Ordinal.EAST.name.capitalize(),
        help="Direction in which to move the window (default: %(default)s)")
    arg_parser.add_argument("--no-wrap", "-W", action="store_true", help="Do not go back if no screen found.")

    args = arg_parser.parse_args()
    setup_log(args)
    move_to_screen(args)


if __name__ == "__main__":
    main()
