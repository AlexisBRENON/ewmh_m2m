#! /usr/bin/env python3
import argparse
import logging

import ewmh_m2m
from ewmh_m2m.ordinal import Ordinal
from ewmh_m2m.window import ActiveWindow

_logger = logging.getLogger(__name__)


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
    ActiveWindow().move_to_screen(args.direction, args.no_wrap)


if __name__ == "__main__":
    main()
