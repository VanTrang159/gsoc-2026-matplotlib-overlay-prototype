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


def main():
    # Tăng lên 1 triệu điểm để ép CPU phải render nặng
    n_points = 1_000_000 
    x = np.linspace(0, 10, n_points)
    y = np.sin(x) + np.random.randn(n_points) * 0.1

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex='col')
    fig.suptitle(f"Benchmark: {n_points:,} points with Shared Axes", fontsize=14)

    axes[0, 0].set_title("Naive (Full Redraw)")
    axes[0, 0].plot(x, y, color='blue', lw=0.5)
    axes[1, 0].plot(x, y, color='blue', lw=0.5)

    axes[0, 1].set_title("Blit (Overlay Layer)")
    axes[0, 1].plot(x, y, color='green', lw=0.5)
    axes[1, 1].plot(x, y, color='green', lw=0.5)

    naive_timer = Timer("Naive")
    blit_timer = Timer("Blit")

    NaiveCrosshair(axes[0, 0], timer=naive_timer)
    BlitCrosshair(axes[0, 1], timer=blit_timer)
    anim = attach_stats(fig, {
        "Naive": naive_timer,
        "Blit": blit_timer,
    })

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    plt.show()


if __name__ == "__main__":
    main()
