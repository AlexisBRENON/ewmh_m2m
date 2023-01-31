from contextlib import contextmanager
from typing import Tuple, Optional

from ewmh_m2m.geometry import Geometry
import xpybutil.ewmh
import xpybutil.util
import xpybutil.window


class ActiveWindow:
    """Class to manage the currently active window."""

    def __init__(self):
        cookie = xpybutil.ewmh.get_active_window()
        self.conn = cookie.cookie.conn
        self.window = cookie.reply()[0]

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
    def fullscreen(self) -> bool:
        """Is the window in fullscreen mode"""
        state =  [xpybutil.util.get_atom_name(a) for a in xpybutil.ewmh.get_wm_state(self.window).reply()]
        return '_NET_WM_STATE_FULLSCREEN' in state

    @fullscreen.setter
    def fullscreen(self, state: bool):
        xpybutil.ewmh.request_wm_state(
            self.window, int(state), xpybutil.util.get_atom('_NET_WM_STATE_FULLSCREEN')
        )

    @property
    def maximized(self) -> Tuple[bool, bool]:
        """Is the window maximized.
        Returns a boolean 2-tuple: (horizontally maximized?, vertically maximized?)."""
        state =  [xpybutil.util.get_atom_name(a) for a in xpybutil.ewmh.get_wm_state(self.window).reply()]
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

    @contextmanager
    def movable(self):
        """Context manager to prepare the window to be moved."""
        initial_maximized_state = self.maximized
        initial_fullscreen_state = self.fullscreen
        self.maximized = (False, False)
        self.fullscreen = False

        try:
            yield self
        finally:
            self.maximized = initial_maximized_state
            self.fullscreen = initial_fullscreen_state
            self.conn.flush()
