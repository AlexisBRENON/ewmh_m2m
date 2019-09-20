from typing import Tuple, Optional

from ewmh_m2m.geometry import Geometry
import xpybutil.ewmh
import xpybutil.util
import xpybutil.window


class ActiveWindow:
    def __init__(self):
        self.window = xpybutil.ewmh.get_active_window().reply()[0]

    @property
    def geometry(self) -> Geometry:
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
        state =  [xpybutil.util.get_atom_name(a) for a in xpybutil.ewmh.get_wm_state(self.window).reply()]
        return '_NET_WM_STATE_MAXIMIZED_HORZ' in state, '_NET_WM_STATE_MAXIMIZED_VERT' in state

    @maximized.setter
    def maximized(self, state: Tuple[Optional[bool], Optional[bool]]):
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
