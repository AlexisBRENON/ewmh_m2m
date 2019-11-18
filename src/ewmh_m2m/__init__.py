# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound


class M2MOptions:
    """Data class of options accepted by the move to monitor utility."""
    from ewmh_m2m.ordinal import Ordinal

    def __init__(self, direction: Ordinal, no_wrap: bool):
        """
        :param direction: Direction to look for another screen
        :param no_wrap: Prevent last screen and first screen (in the given direction) to be seen as siblings
        """
        self.direction = direction
        self.no_wrap = no_wrap
