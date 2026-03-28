'''
This repository includes a simple benchmark comparing:
- a naive crosshair that triggers `draw_idle()` on every mouse move
- a blit-based crosshair that only redraws the affected region
'''

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from crosshair_naive import NaiveCrosshair
from crosshair_blit import BlitCrosshair


class Timer:
    def __init__(self, name):
        self.name = name
        self.times = []
        self.updates = 0
        self.full_redraws = 0

    def record(self, duration_ms, full_redraw=False):
        self.times.append(duration_ms)
        self.updates += 1
        if full_redraw:
            self.full_redraws += 1

    def avg_ms(self):
        if not self.times:
            return 0.0
        return sum(self.times) / len(self.times)

    def fps(self):
        avg = self.avg_ms()
        return 1000.0 / avg if avg > 0 else 0.0


def attach_stats(fig, timers, interval=500):
    text = fig.text(
        0.5, 0.02, "",
        ha="center",
        va="bottom",
        fontsize=9,
        family="monospace",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#f0f0f0", alpha=0.9)
    )

    def update(_):
        lines = []
        for name, timer in timers.items():
            if timer.updates == 0:
                lines.append(f"{name}: waiting...")
            else:
                lines.append(
                    f"{name}: avg={timer.avg_ms():.3f} ms | "
                    f"fps~{timer.fps():.1f} | "
                    f"updates={timer.updates} | "
                    f"full_redraws={timer.full_redraws}"
                )
        text.set_text("\n".join(lines))
        fig.canvas.draw_idle()

    return FuncAnimation(fig, update, interval=interval, cache_frame_data=False)


def main():
    x = np.linspace(0, 10, 1000)
    y = np.sin(x) + 0.1 * np.random.randn(len(x))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Crosshair Benchmark: Naive vs Blit", fontsize=13)

    for ax in axes:
        ax.plot(x, y, color="steelblue", linewidth=1)
        ax.set_xlabel("x")
        ax.set_ylabel("y")

    axes[0].set_title("Naive Crosshair (draw_idle)")
    axes[1].set_title("Blit Crosshair")

    naive_timer = Timer("Naive")
    blit_timer = Timer("Blit")

    NaiveCrosshair(axes[0], timer=naive_timer)
    BlitCrosshair(axes[1], timer=blit_timer)

    anim = attach_stats(fig, {
        "Naive": naive_timer,
        "Blit": blit_timer,
    })

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    plt.show()


if __name__ == "__main__":
    main()
