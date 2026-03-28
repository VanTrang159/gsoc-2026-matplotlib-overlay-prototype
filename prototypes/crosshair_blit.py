"""
Minimal blit-based crosshair prototype for Matplotlib.

This prototype updates a crosshair cursor using background restoration
and canvas blitting instead of full figure redraw on every mouse move.
"""

import numpy as np
import matplotlib.pyplot as plt

class BlitCrosshair:
    def __init__(self, ax):
        self.ax = ax
        self.canvas = ax.figure.canvas
        self.background = None

        self.hline = ax.axhline(color="gray", linestyle="--", visible=False)
        self.vline = ax.axvline(color="gray", linestyle="--", visible=False)

        self.cid_draw = self.canvas.mpl_connect("draw_event", self._on_draw)
        self.cid_move = self.canvas.mpl_connect("motion_notify_event", self._on_move)
        self.cid_leave = self.canvas.mpl_connect("axes_leave_event", self._on_leave)

    def _on_draw(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)

    def _on_move(self, event):
        if event.inaxes is not self.ax or self.background is None:
            return
        if event.xdata is None or event.ydata is None:
            return

        self.canvas.restore_region(self.background)

        self.hline.set_ydata([event.ydata, event.ydata])
        self.vline.set_xdata([event.xdata, event.xdata])
        self.hline.set_visible(True)
        self.vline.set_visible(True)

        self.ax.draw_artist(self.hline)
        self.ax.draw_artist(self.vline)
        self.canvas.blit(self.ax.bbox)

    def _on_leave(self, event):
        if self.background is None:
            return

        self.hline.set_visible(False)
        self.vline.set_visible(False)
        self.canvas.restore_region(self.background)
        self.canvas.blit(self.ax.bbox)

    def disconnect(self):
        self.canvas.mpl_disconnect(self.cid_draw)
        self.canvas.mpl_disconnect(self.cid_move)
        self.canvas.mpl_disconnect(self.cid_leave)


def main():
    x = np.linspace(0, 10, 500)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Blit-based Crosshair Prototype")

    BlitCrosshair(ax)
    plt.show()


if __name__ == "__main__":
    main()
