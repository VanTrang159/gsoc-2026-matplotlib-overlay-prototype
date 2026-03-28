"""
Naive crosshair implementation using full redraw.

This prototype updates crosshair lines on every mouse move and triggers a full canvas redraw using draw_idle(), 
serving as a baseline for comparison with optimized approaches such as blitting.
"""

import numpy as np
import matplotlib.pyplot as plt

class NaiveCrosshair:
    def __init__(self, ax):
        self.ax = ax
        self.canvas = ax.figure.canvas

        self.hline = ax.axhline(color="gray", linestyle="--", visible=False)
        self.vline = ax.axvline(color="gray", linestyle="--", visible=False)

        self.cid_move = self.canvas.mpl_connect("motion_notify_event", self._on_move)
        self.cid_leave = self.canvas.mpl_connect("axes_leave_event", self._on_leave)

    def _on_move(self, event):
        if event.inaxes is not self.ax:
            return
        if event.xdata is None or event.ydata is None:
            return

        self.hline.set_ydata([event.ydata, event.ydata])
        self.vline.set_xdata([event.xdata, event.xdata])
        self.hline.set_visible(True)
        self.vline.set_visible(True)

        # Full redraw
        self.canvas.draw_idle()

    def _on_leave(self, event):
        self.hline.set_visible(False)
        self.vline.set_visible(False)
        self.canvas.draw_idle()


def main():
    x = np.linspace(0, 10, 500)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Naive Crosshair (Full Redraw)")

    NaiveCrosshair(ax)
    plt.show()


if __name__ == "__main__":
    main()
