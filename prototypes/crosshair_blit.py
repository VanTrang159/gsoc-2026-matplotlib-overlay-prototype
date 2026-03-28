"""
An optimized crosshair cursor using Matplotlib's blitting technique. It decouples the interactive lines from the static background to
ensure smooth performance even with large datasets.
"""

import time
import matplotlib.pyplot as plt

class BlitCrosshair:
    def __init__(self, ax, timer=None):
        self.ax = ax
        self.canvas = ax.figure.canvas
        self.timer = timer
        self.background = None

        # Identify all linked axes (shared X or Y) to synchronize the crosshair
        self.shared_axes = list(set([ax] + 
                                    ax.get_shared_x_axes().get_siblings(ax) + 
                                    ax.get_shared_y_axes().get_siblings(ax)))

        # Initialize crosshair lines for all related axes
        self.lines = []
        for a in self.shared_axes:
            # animated=True excludes these artists from the standard static draw
            h = a.axhline(color="red", linestyle="--", visible=False, animated=True)
            v = a.axvline(color="red", linestyle="--", visible=False, animated=True)
            self.lines.append((a, h, v))

        # Connect Matplotlib events
        self.cid_draw = self.canvas.mpl_connect("draw_event", self._on_draw)
        self.cid_move = self.canvas.mpl_connect("motion_notify_event", self._on_move)

    def _on_draw(self, event):
        """Capture the static background when the figure is first drawn or resized."""
        if event is not None and event.canvas != self.canvas:
            return
        # Copy the pixel data of the entire figure area
        self.background = self.canvas.copy_from_bbox(self.ax.figure.bbox)

"""Handle mouse movement to update crosshair positions via blitting."""
    def _on_move(self, event):
        if event.inaxes is not self.ax or self.background is None:
            return
        
        # Performance tracking
        start_time = time.perf_counter()

        # Restore the clean background (removing previous crosshair positions)
        self.canvas.restore_region(self.background)

        # Update and redraw each crosshair artist on the overlay layer
        for a, h, v in self.lines:
            h.set_ydata([event.ydata, event.ydata])
            v.set_xdata([event.xdata, event.xdata])
            h.set_visible(True)
            v.set_visible(True)
            
            # Draw artists individually onto the restored background
            a.draw_artist(h)
            a.draw_artist(v)

        # Push the updated pixels to the screen
        self.canvas.blit(self.ax.figure.bbox)

        # Record metrics if a timer is provided
        if self.timer:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.timer.record(duration_ms)
