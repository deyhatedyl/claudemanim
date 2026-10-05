"""Exam-style stimulus figures shown before students attempt a graph question.

Only givens appear here: no activation-energy arrows, cooling fits, corrected
temperatures or worked answers. The same bank data are used for the solutions.
"""
from __future__ import annotations

import numpy as np
from manim import (Axes, DashedLine, DashedVMobject, Dot, DOWN, LEFT, Line,
                   RIGHT, UP, VGroup)
from .style import (TEXT, MUTED, FAINT, SYSTEM, UNKNOWN, MOL_C, SMALL,
                    T, TB, panel, fit_content)


def energy_figure(spec):
    from .components import profile_curve
    ax = Axes(x_range=[0, 10, 1], y_range=[0, 175, 25], x_length=5.4, y_length=3.0,
              axis_config=dict(color=MUTED, stroke_width=1.5, include_tip=False,
                               font_size=17, label_constructor=T),
              x_axis_config=dict(include_ticks=False),
              y_axis_config=dict(numbers_to_include=[0, 25, 50, 75, 100, 125, 150, 175]))
    r, p, peak, cat = (spec[k] for k in ("reactants", "products", "uncatalysed", "catalysed"))
    solid = profile_curve(ax, r, peak, p)
    dashed = profile_curve(ax, r, cat, p, color=MOL_C, dashed=True)
    guides = VGroup(*[DashedLine(ax.c2p(0, v), ax.c2p(x, v), color=col,
                                stroke_width=1, dash_length=0.06)
                      for v, x, col in ((r, 2, MUTED), (p, 8, MUTED),
                                        (peak, 5, MUTED), (cat, 5, MOL_C))])
    labels = VGroup(*[T(str(v), size=16, color=col).next_to(ax.c2p(x, v), UP, buff=0.05)
                      for v, x, col in ((r, 1.2, TEXT), (p, 9, TEXT),
                                        (peak, 5, TEXT), (cat, 5, MOL_C))])
    xl = T("Reaction progress", size=17, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.16)
    yl = T("Enthalpy (kJ mol⁻¹ of reaction)", size=16, color=MUTED).rotate(np.pi / 2)
    yl.next_to(ax.y_axis, LEFT, buff=0.55)
    legend = VGroup(
        VGroup(Line(LEFT * 0.18, RIGHT * 0.18, color=TEXT, stroke_width=3),
               T("uncatalysed", size=16)).arrange(RIGHT, buff=0.1),
        VGroup(DashedLine(LEFT * 0.18, RIGHT * 0.18, color=MOL_C, stroke_width=3),
               T("catalysed", size=16)).arrange(RIGHT, buff=0.1)
    ).arrange(RIGHT, buff=0.35).next_to(ax, UP, buff=0.25)
    rt = T("reactants", size=16).next_to(ax.c2p(1.2, r), DOWN, buff=0.12)
    pt = T("products", size=16).next_to(ax.c2p(9, p), UP, buff=0.32)
    return VGroup(ax, solid, dashed, guides, labels, xl, yl, legend, rt, pt)


def temperature_figure(spec):
    times = [p[0] for p in spec["points"]]
    values = [p[1] for p in spec["points"]] + [spec["baseline"]]
    xmax = max(times) + 60
    ymin, ymax = np.floor(min(values)) - 1, np.ceil(max(values)) + 1
    ax = Axes(x_range=[0, xmax, 60], y_range=[ymin, ymax, 1], x_length=5.4, y_length=2.85,
              axis_config=dict(color=MUTED, stroke_width=1.5, include_tip=False,
                               font_size=16, label_constructor=T),
              x_axis_config=dict(numbers_to_include=np.arange(0, xmax + 1, 60)),
              y_axis_config=dict(numbers_to_include=np.arange(ymin, ymax + 1, 1)))
    grid = VGroup(*[Line(ax.c2p(0, y), ax.c2p(xmax, y), color=FAINT,
                        stroke_width=0.6, stroke_opacity=0.4)
                    for y in np.arange(ymin + 0.2, ymax + 0.01, 0.2)])
    pts = VGroup(*[Dot(ax.c2p(t, v), radius=0.055, color=TEXT) for t, v in spec["points"]])
    baseline = Line(ax.c2p(0, spec["baseline"]), ax.c2p(spec["mixing_time"], spec["baseline"]),
                    color=MUTED, stroke_width=1.8)
    mixing = DashedLine(ax.c2p(spec["mixing_time"], ymin), ax.c2p(spec["mixing_time"], ymax),
                        color=UNKNOWN, stroke_width=1.5)
    mt = T(f"mixing: {spec['mixing_time']} s", size=16, color=UNKNOWN).next_to(mixing, UP, buff=0.08)
    xl = T("Time (s)", size=17, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.2)
    yl = T("Temperature (°C)", size=17, color=MUTED).rotate(np.pi / 2)
    yl.next_to(ax.y_axis, LEFT, buff=0.55)
    from .components import table
    readings = [p for p in spec["points"] if p[0] >= spec["cooling_start"]]
    data = table([["t (s)"] + [str(p[0]) for p in readings],
                  ["T (°C)"] + [f"{p[1]:.1f}" for p in readings]],
                 [1.15] * (len(readings) + 1), size=15, row_h=0.35, pad=0.1)
    data.next_to(xl, DOWN, buff=0.18)
    dl = T("Measured cooling readings", size=14, color=MUTED).next_to(data, DOWN, buff=0.08)
    return VGroup(grid, ax, pts, baseline, mixing, mt, xl, yl, data, dl)


def visual_question(q, width=12.6, size=22, parts=None, tight=False):
    from .components import wrapped, table
    spec = q["visual"]
    if spec["type"] == "energy_profile":
        figure = energy_figure(spec)
    elif spec["type"] == "temperature":
        figure = temperature_figure(spec)
    else:
        figure = table(spec["rows"], spec["column_widths"], size=size - 1,
                       row_h=0.55, pad=0.13)
    figure.scale_to_fit_width(6.0)
    rows = VGroup()
    for letter, text, marks in q["parts"]:
        if parts and letter not in parts:
            continue
        label = TB(f"{letter}.", size=size, color=SYSTEM)
        body = wrapped(f"{text} [{marks}]", size=size, width=5.65, buff=0.09)
        body.next_to(label, RIGHT, buff=0.15, aligned_edge=UP)
        rows.add(VGroup(label, body))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    content = VGroup(figure, rows).arrange(RIGHT, buff=0.4, aligned_edge=UP)
    given = wrapped(spec["prompt"], size=size, width=width - 0.7, buff=0.09)
    heading = VGroup(TB(q["id"], size=size + 3, color=SYSTEM),
                     T("Original VCAA-style practice", size=17, color=MUTED),
                     T(f"{sum(p[2] for p in q['parts'])} marks", size=size, color=MUTED)
                     ).arrange(RIGHT, buff=0.28)
    layout = VGroup(heading, given, content).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    bg = panel(layout, color=FAINT, buff=0.23)
    return fit_content(VGroup(bg, layout), max_width=width,
                       max_height=5.95 if tight else 4.95)
