import logging
from typing import Tuple, Optional

import xpybutil.ewmh
import xpybutil.util
import xpybutil.window

from ewmh_m2m.geometry import Geometry
from ewmh_m2m.ordinal import Ordinal
from ewmh_m2m.screen import get_screens, get_sibling_screen, get_sibling_screens


class ActiveWindow:
    """Class to manage the currently active window."""

    def __init__(self):
        cookie = xpybutil.ewmh.get_active_window()
        self.conn = cookie.cookie.conn
        self.window = cookie.reply()[0]
        self.logger = logging.getLogger(self.__name__)

    @property
    def geometry(self) -> Geometry:
        """Geometry of the window"""
        g = xpybutil.window.get_geometry(self.window)
        return Geometry(x=g[0], y=g[1], w=g[2], h=g[3])

    @geometry.setter
    def geometry(self, geometry: Geometry):
        xpybutil.window.moveresize(
            self.window,
            **geometry.__dict__
        )

    @property
    def maximized(self) -> Tuple[bool, bool]:
        """Is the window maximized.
        Returns a boolean 2-tuple: (horizontally maximized?, vertically maximized?)."""
        state = [xpybutil.util.get_atom_name(a) for a in xpybutil.ewmh.get_wm_state(self.window).reply()]
        return '_NET_WM_STATE_MAXIMIZED_HORZ' in state, '_NET_WM_STATE_MAXIMIZED_VERT' in state

    @maximized.setter
    def maximized(self, state: Tuple[Optional[bool], Optional[bool]]):
        """Set the maximized state of the window.
        Pass a boolean 2-tuple (see func:maximized) which can contain None to leave this state unchanged."""
        atom = xpybutil.util.get_atom
        if state[0] and state[1]:
            xpybutil.ewmh.request_wm_state(
                self.window, 1,
                atom('_NET_WM_STATE_MAXIMIZED_HORZ'), atom('_NET_WM_STATE_MAXIMIZED_VERT'))
        elif state[0]:
            xpybutil.ewmh.request_wm_state(self.window, 1, atom('_NET_WM_STATE_MAXIMIZED_HORZ'))
            if state[1] is not None:
                xpybutil.ewmh.request_wm_state(self.window, 0, atom('_NET_WM_STATE_MAXIMIZED_VERT'))
        elif state[1]:
            xpybutil.ewmh.request_wm_state(self.window, 1, atom('_NET_WM_STATE_MAXIMIZED_VERT'))
            if state[0] is not None:
                xpybutil.ewmh.request_wm_state(self.window, 0, atom('_NET_WM_STATE_MAXIMIZED_HORZ'))
        elif state[0] is not None and state[1] is not None:
            xpybutil.ewmh.request_wm_state(
                self.window, 0,
                atom('_NET_WM_STATE_MAXIMIZED_HORZ'), atom('_NET_WM_STATE_MAXIMIZED_VERT'))
        else:
            return

    def move_to_screen(self, direction: Ordinal, no_wrap: bool) -> None:
        """Move the window to another screen.

        :param direction: Direction to look for another screen
        :param no_wrap: Prevent last screen and first screen (in the given direction) to be seen as siblings
        """
        initial_window_geometry = self.geometry

        screens = get_screens()
        self.logger.debug("Detected screens: %s", screens)
        containing_screen = Geometry(*xpybutil.rect.get_monitor_area(
            initial_window_geometry, screens
        ))
        self.logger.debug("Containing screen: %s", containing_screen)

        window_state = self.maximized
        self.maximized = (False, False)
        window_geometry = self.geometry
        relative_geometry = window_geometry.build_relative(containing_screen)

        new_screen = get_sibling_screen(
            get_sibling_screens(containing_screen, screens),
            direction, no_wrap)
        if not new_screen:
            self.logger.fatal("No sibling screen found")
        else:
            new_window_geometry = relative_geometry.build_absolute(new_screen)
            self.logger.debug("New window geometry: %s", new_window_geometry)
            self.geometry = new_window_geometry
        self.maximized = window_state
        self.conn.flush()

