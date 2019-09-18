import subprocess
from typing import Tuple, Optional

from ewmh import EWMH
from ewmh_m2m.geometry import Geometry


class ActiveWindow:
    def __init__(self):
        self.ewmh = EWMH()
        self.window = self.ewmh.getActiveWindow()

    @property
    def geometry(self) -> Geometry:
        for line in subprocess.run(["wmctrl", "-l", "-G"], capture_output=True, text=True).stdout.split('\n'):
            splits = line.strip().split()
            if int(splits[0], 16) == self.window.id:
                return Geometry(
                    x=int(splits[2]),
                    y=int(splits[3]),
                    w=int(splits[4]),
                    h=int(splits[5]))

    @geometry.setter
    def geometry(self, geometry: Geometry):
        args = [
            "wmctrl", "-i",
            "-r", hex(self.window.id),
            "-e", "0,{0.x:.0f},{0.y:.0f},{0.w:.0f},{0.h:.0f}".format(geometry)
        ]
        subprocess.run(args)

    @property
    def maximized(self) -> Tuple[bool, bool]:
        state = self.ewmh.getWmState(self.window, str=True)
        return '_NET_WM_STATE_MAXIMIZED_HORZ' in state, '_NET_WM_STATE_MAXIMIZED_VERT' in state

    @maximized.setter
    def maximized(self, state: Tuple[Optional[bool], Optional[bool]]):
        if state[0] and state[1]:
            self.ewmh.setWmState(self.window, 1, '_NET_WM_STATE_MAXIMIZED_HORZ', '_NET_WM_STATE_MAXIMIZED_VERT')
        elif state[0]:
            self.ewmh.setWmState(self.window, 1, '_NET_WM_STATE_MAXIMIZED_HORZ')
            if state[1] is not None:
                self.ewmh.setWmState(self.window, 0, '_NET_WM_STATE_MAXIMIZED_VERT')
        elif state[1]:
            self.ewmh.setWmState(self.window, 1, '_NET_WM_STATE_MAXIMIZED_VERT')
            if state[0] is not None:
                self.ewmh.setWmState(self.window, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
        elif state[0] is not None and state[1] is not None:
            self.ewmh.setWmState(self.window, 0, '_NET_WM_STATE_MAXIMIZED_HORZ', '_NET_WM_STATE_MAXIMIZED_VERT')
        else:
            return
        self.ewmh.display.flush()
