"""
A baseline crosshair implementation that triggers a full canvas redraw.
Used to demonstrate the performance bottleneck of non-optimized interactions.
"""

import time
import matplotlib.pyplot as plt

class NaiveCrosshair:
    def __init__(self, ax, timer=None):
        self.ax = ax
        self.canvas = ax.figure.canvas
        self.timer = timer

        # Standard artists without 'animated=True'
        self.hline = ax.axhline(color="gray", linestyle="--", visible=False)
        self.vline = ax.axvline(color="gray", linestyle="--", visible=False)

        self.cid_move = self.canvas.mpl_connect("motion_notify_event", self._on_move)

    def _on_move(self, event):
        if event.inaxes is not self.ax:
            return
        
        start_time = time.perf_counter()

        # Update position
        self.hline.set_ydata([event.ydata, event.ydata])
        self.vline.set_xdata([event.xdata, event.xdata])
        self.hline.set_visible(True)
        self.vline.set_visible(True)

        # Trigger a full redraw of the entire figure (expensive)
        self.canvas.draw_idle()

        if self.timer:
            # Note: draw_idle is asynchronous, so this timing represents 
            # only the overhead of the update call itself.
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.timer.record(duration_ms)
