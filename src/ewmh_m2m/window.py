import logging
from typing import Tuple, Optional

import xpybutil.ewmh
import xpybutil.rect
import xpybutil.util
import xpybutil.window

from ewmh_m2m import M2MOptions
from ewmh_m2m.geometry import Geometry
from ewmh_m2m.screen import get_screens, get_sibling_screen, get_sibling_screens


class Window:
    """Class to manage a window."""

    def __init__(self, window_id: Optional[int] = None):
        cookie = xpybutil.ewmh.get_active_window()
        self.conn = cookie.cookie.conn
        if window_id is None:
            self.window = cookie.reply()[0]
        else:
            self.window = window_id
        self.logger = logging.getLogger(type(self).__name__)

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

    @property
    def is_active(self) -> bool:
        return xpybutil.ewmh.get_active_window().reply()[0] == self.window

    @is_active.setter
    def is_active(self, value: bool):
        if value:
            xpybutil.ewmh.request_active_window(self.window)
        else:
            xpybutil.ewmh.request_active_window(0)

    @property
    def is_focused(self) -> bool:
        return ('_NET_WM_STATE_FOCUSED' in
                [xpybutil.util.get_atom_name(a) for a in xpybutil.ewmh.get_wm_state(self.window).reply()])

    @is_focused.setter
    def is_focused(self, value: bool) -> None:
        xpybutil.ewmh.request_wm_state(
            self.window, 1 if value else 0,
            xpybutil.util.get_atom('_NET_WM_STATE_FOCUSED'))

    def move_to_screen(self, options: M2MOptions) -> None:
        """Move the window to another screen.

        :param options: Behavior control options
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
            options.direction, options.no_wrap)
        if not new_screen:
            self.logger.fatal("No sibling screen found")
        else:
            new_window_geometry = relative_geometry.build_absolute(new_screen)
            self.logger.debug("New window geometry: %s", new_window_geometry)
            self.geometry = new_window_geometry
        self.maximized = window_state
        self.is_focused = True
        self.conn.flush()

