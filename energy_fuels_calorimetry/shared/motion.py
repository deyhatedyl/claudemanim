"""Short explanatory motion. Energy markers are qualitative, not a joule scale."""
from __future__ import annotations

from manim import (ArcBetweenPoints, Dot, FadeIn, FadeOut, LaggedStart, Line,
                   MoveAlongPath, Succession, Create, linear)


def flow(scene, start, end, color, *, angle=0, run_time=1.6, markers=3):
    """Trace a transfer, then remove transient markers to keep the diagram clear."""
    path = ArcBetweenPoints(start, end, angle=angle) if angle else Line(start, end)
    dots = [Dot(start, radius=0.065, color=color).set_z_index(8) for _ in range(markers)]
    scene.play(LaggedStart(*[
        Succession(FadeIn(dot, run_time=0.12),
                   MoveAlongPath(dot, path, run_time=1.2, rate_func=linear),
                   FadeOut(dot, run_time=0.15)) for dot in dots
    ], lag_ratio=0.24), run_time=run_time)
    scene.remove(*dots)


def trace(scene, path, color, *, run_time=1.2):
    """Draw a model line with a moving pen, e.g. extrapolating back to mixing."""
    pen = Dot(path.get_start(), radius=0.07, color=color).set_z_index(8)
    # Create mutates the displayed path. Trace an independent copy; dashed
    # containers have no root points, so their underlying travel is a straight line.
    travel = path.copy() if path.has_points() else Line(path.get_start(), path.get_end())
    scene.add(pen)
    scene.play(Create(path), MoveAlongPath(pen, travel, rate_func=linear), run_time=run_time)
    scene.remove(pen)
