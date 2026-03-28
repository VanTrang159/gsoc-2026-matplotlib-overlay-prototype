import matplotlib.pyplot as plt
import numpy as np


class OverlayElement:
    def __init__(self):
        self.enabled = True

    def update(self, event):
        pass

    def draw(self, ax):
        pass

    def clear(self):
        pass

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        self.clear()

    def toggle(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()


class OverlayManager:
    def __init__(self, ax):
        self.ax = ax
        self.canvas = ax.figure.canvas
        self.elements = {}
        self._bg = None

        self.canvas.mpl_connect("draw_event", self._on_full_draw)
        self.canvas.mpl_connect("motion_notify_event", self._on_mouse_move)
        self.canvas.mpl_connect("axes_leave_event", self._on_axes_leave)
        self.canvas.mpl_connect("key_press_event", self._on_key_press)

    def add(self, name, element):
        self.elements[name] = element

    def _on_full_draw(self, event):
        self._bg = self.canvas.copy_from_bbox(self.ax.bbox)
        self.render_all()

    def _on_mouse_move(self, event):
        if self._bg is None or event.inaxes != self.ax:
            return
        if event.xdata is None or event.ydata is None:
            return

        for el in self.elements.values():
            if el.enabled:
                el.update(event)

        self.render_all()

    def _on_axes_leave(self, event):
        if self._bg is None or event.inaxes != self.ax:
            return

        for el in self.elements.values():
            el.clear()

        self.render_all()

    def _on_key_press(self, event):
        if event.key == 'c' and 'crosshair' in self.elements:
            self.elements['crosshair'].toggle()
        elif event.key == 't' and 'text' in self.elements:
            self.elements['text'].toggle()

        self.render_all()

    def render_all(self):
        if self._bg is None:
            return

        self.canvas.restore_region(self._bg)

        for el in self.elements.values():
            if el.enabled:
                el.draw(self.ax)

        self.canvas.blit(self.ax.bbox)


class CrosshairOverlay(OverlayElement):
    def __init__(self, ax, color='red'):
        super().__init__()
        self.h_line = ax.axhline(
            0, color=color, lw=0.8, ls='--',
            animated=True, visible=False
        )
        self.v_line = ax.axvline(
            0, color=color, lw=0.8, ls='--',
            animated=True, visible=False
        )

    def update(self, event):
        self.h_line.set_ydata([event.ydata])
        self.v_line.set_xdata([event.xdata])
        self.h_line.set_visible(True)
        self.v_line.set_visible(True)

    def draw(self, ax):
        if self.h_line.get_visible():
            ax.draw_artist(self.h_line)
        if self.v_line.get_visible():
            ax.draw_artist(self.v_line)

    def clear(self):
        self.h_line.set_visible(False)
        self.v_line.set_visible(False)


class TextOverlay(OverlayElement):
    def __init__(self, ax):
        super().__init__()
        self.txt = ax.text(
            0.05, 0.95, '',
            transform=ax.transAxes,
            animated=True,
            visible=False,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.7)
        )

    def update(self, event):
        self.txt.set_text(f'x={event.xdata:.2f}\ny={event.ydata:.2f}')
        self.txt.set_visible(True)

    def draw(self, ax):
        if self.txt.get_visible():
            ax.draw_artist(self.txt)

    def clear(self):
        self.txt.set_visible(False)


fig, ax = plt.subplots()
x = np.linspace(0, 10, 1000)
ax.plot(x, np.sin(x))

manager = OverlayManager(ax)
manager.add('crosshair', CrosshairOverlay(ax, color='blue'))
manager.add('text', TextOverlay(ax))

print("Press 'c' to switch on/off crosshair, 't' to switch on/off text")
plt.show()
