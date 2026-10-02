"""
Reusable visual components shared by all episodes.

Every component returns ordinary Manim mobjects so scenes can animate their parts freely.
"""
from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from manim import (DL, DOWN, DR, LEFT, ORIGIN, RIGHT, UL, UP, UR, Arrow, Circle, CurvedArrow,
                   DashedLine, DashedVMobject, Dot, Line, MathTex, Polygon, Rectangle,
                   RoundedRectangle, Text, VGroup, VMobject, WHITE)

from .style import (ATOM_COLORS, BAD, BG, BODY, EQ, EQ_SMALL, FAINT, GOOD, LABEL, LOSS, MUTED, PANEL,
                    SMALL, SYSTEM, TEXT, UNKNOWN, M, T, TB, chip, panel)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "questions"))
from bank import BY_ID  # noqa: E402


# ------------------------------------------------------------------ text layout
@lru_cache(maxsize=4096)
def _w(s: str, size: int) -> float:
    return T(s, size=size).width


def wrap(s: str, size: int = LABEL, width: float = 11.5) -> list[str]:
    """Greedy word wrap using measured text widths."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if cur and _w(cand, size) > width:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def wrapped(s: str, size: int = LABEL, width: float = 11.5, color: str = TEXT, buff: float = 0.12,
            weight: str = "NORMAL") -> VGroup:
    g = VGroup(*[T(l, size=size, color=color, weight=weight) for l in wrap(s, size, width)])
    return g.arrange(DOWN, aligned_edge=LEFT, buff=buff)


def bullets(items: list[str], size: int = LABEL, width: float = 11.0, color: str = TEXT,
            bullet: str = "•", buff: float = 0.22) -> VGroup:
    rows = VGroup()
    for it in items:
        b = T(bullet, size=size, color=MUTED)
        body = wrapped(it, size=size, width=width - 0.5, color=color)
        b.next_to(body, LEFT, buff=0.2)
        b.set_y(body[0].get_y())
        rows.add(VGroup(b, body))
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)


# ------------------------------------------------------------------ title card
def title_card(ep_num: int, title: str, subtitle: str = "VCE Chemistry · Energy, fuels and calorimetry") -> VGroup:
    k = T(subtitle, size=LABEL, color=MUTED)
    n = TB(f"Episode {ep_num:02d}", size=30, color=SYSTEM)
    t = VGroup(*[TB(l, size=46) for l in wrap(title, 46, 12.0)]).arrange(DOWN, buff=0.15)
    g = VGroup(k, n, t).arrange(DOWN, buff=0.35)
    line = Line(LEFT * 3, RIGHT * 3, color=SYSTEM, stroke_width=3).next_to(g, DOWN, buff=0.4)
    return VGroup(g, line).move_to(ORIGIN + 0.3 * UP)


# ------------------------------------------------------------------ question card
def question_card(qid: str, width: float = 12.6, size: int = LABEL, show_parts: bool = True,
                  parts: list[str] | None = None) -> VGroup:
    """The full prompt of an anchor question with its marks (no answers)."""
    q = BY_ID[qid]
    total = sum(p[2] for p in q["parts"])
    head = VGroup(TB(f"{qid}", size=size + 4, color=SYSTEM),
                  T(q["title"], size=size, color=TEXT),
                  T(f"{total} marks", size=size, color=MUTED)).arrange(RIGHT, buff=0.35)
    body = wrapped(q["stem"], size=size, width=width - 0.6)
    rows = VGroup(head, body)
    if show_parts:
        for lab, txt, mk in q["parts"]:
            if parts and lab not in parts:
                continue
            letter = TB(f"{lab}.", size=size, color=SYSTEM)
            t = wrapped(txt, size=size, width=width - 2.2)
            m = T(f"[{mk}]", size=size, color=MUTED)
            t.next_to(letter, RIGHT, buff=0.2, aligned_edge=UP)
            m.next_to(t, RIGHT, buff=0.2, aligned_edge=UP)
            rows.add(VGroup(letter, t, m))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    bg = panel(rows, color=FAINT, buff=0.3)
    return VGroup(bg, rows)


# ------------------------------------------------------------------ working lines
def eq_line(*parts: str, size: int = EQ, color: str = TEXT) -> MathTex:
    return M(*parts, size=size, color=color)


def align_eq(lines: list[MathTex], eq_index: int | list[int] = 1, buff: float = 0.35) -> VGroup:
    """Stack equation lines so their '=' signs line up. eq_index: index of the '=' part in each."""
    g = VGroup(*lines).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    idx = eq_index if isinstance(eq_index, list) else [eq_index] * len(lines)
    x0 = lines[0][idx[0]].get_center()[0]
    for ln, i in zip(lines[1:], idx[1:]):
        ln.shift((x0 - ln[i].get_center()[0]) * RIGHT)
    return g


def strike(mob, color: str = BAD, width: float = 4) -> Line:
    """Diagonal cancellation stroke across a unit."""
    return Line(mob.get_corner(DL) + 0.04 * (DL), mob.get_corner(UR) + 0.04 * UR, color=color, stroke_width=width)


def fraction(num: list[str], den: list[str], size: int = EQ, color: str = TEXT) -> VGroup:
    """A built fraction whose numerator/denominator parts can be individually struck out.
    Returns VGroup(numerator MathTex, bar Line, denominator MathTex)."""
    n = M(*num, size=size, color=color)
    d = M(*den, size=size, color=color)
    w = max(n.width, d.width) + 0.2
    bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=3, color=color)
    n.next_to(bar, UP, buff=0.12)
    d.next_to(bar, DOWN, buff=0.12)
    return VGroup(n, bar, d)


def result_box(mob, color: str = GOOD) -> RoundedRectangle:
    r = RoundedRectangle(width=mob.width + 0.35, height=mob.height + 0.3, corner_radius=0.1,
                         stroke_color=color, stroke_width=3, fill_opacity=0)
    return r.move_to(mob)


# ------------------------------------------------------------------ given / asked
def given_asked(given: list[str], asked: list[str], size: int = SMALL + 2, width: float = 5.8) -> VGroup:
    def col(title, items, color):
        h = TB(title, size=size + 2, color=color)
        rows = VGroup(*[wrapped(i, size=size, width=width - 0.4) for i in items])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        g = VGroup(h, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        return VGroup(panel(g, color=color, buff=0.22, stroke=2), g)
    a = col("Given", given, MUTED)
    b = col("Asked", asked, UNKNOWN)
    return VGroup(a, b).arrange(RIGHT, buff=0.35, aligned_edge=UP)


# ------------------------------------------------------------------ marks
def mark_tally(rows: list[tuple[int, str]], size: int = LABEL, width: float = 7.5, title: str = "Indicative marks") -> VGroup:
    head = TB(title, size=size + 2, color=GOOD)
    lines = VGroup()
    for mk, txt in rows:
        box = RoundedRectangle(width=0.55, height=0.42, corner_radius=0.08, stroke_color=GOOD, stroke_width=2)
        n = T(str(mk), size=size, color=GOOD).move_to(box)
        body = wrapped(txt, size=size, width=width - 1.0)
        body.next_to(box, RIGHT, buff=0.22, aligned_edge=UP)
        lines.add(VGroup(VGroup(box, n), body))
    lines.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    total = sum(r[0] for r in rows)
    tot = T(f"Total: {total} marks", size=size, color=GOOD, weight="BOLD")
    g = VGroup(head, lines, tot).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    return VGroup(panel(g, color=GOOD, buff=0.25), g)


def wrong_panel(title: str, lines: list, note: str | None = None, size: int = LABEL, width: float = 6.0) -> VGroup:
    """'Tempting but incorrect' panel: dashed red border, cross icon, and a diagnosis line."""
    cross = TB("✗", size=size + 6, color=BAD)
    head = VGroup(cross, TB(title, size=size + 2, color=BAD)).arrange(RIGHT, buff=0.2)
    body = VGroup(*[l if not isinstance(l, str) else wrapped(l, size=size, width=width) for l in lines])
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    parts = [head, body]
    if note:
        parts.append(wrapped(note, size=size, width=width, color=UNKNOWN))
    g = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    r = RoundedRectangle(width=g.width + 0.5, height=g.height + 0.45, corner_radius=0.15,
                         stroke_color=BAD, stroke_width=3, fill_color=PANEL, fill_opacity=0.92)
    r.move_to(g)
    border = DashedVMobject(r, num_dashes=40)
    fill = r.copy().set_stroke(width=0)
    return VGroup(fill, border, g)


def right_panel(title: str, lines: list, size: int = LABEL, width: float = 6.0, color: str = GOOD) -> VGroup:
    tick = TB("✓", size=size + 6, color=color)
    head = VGroup(tick, TB(title, size=size + 2, color=color)).arrange(RIGHT, buff=0.2)
    body = VGroup(*[l if not isinstance(l, str) else wrapped(l, size=size, width=width) for l in lines])
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    g = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    return VGroup(panel(g, color=color, buff=0.25, stroke=3), g)


# ------------------------------------------------------------------ simple table
def table(rows: list[list], col_widths: list[float], size: int = LABEL, header_color: str = SYSTEM,
          row_h: float | None = None, line_color: str = FAINT, pad: float = 0.14) -> VGroup:
    """Rows of strings (or mobjects). First row is the header. Text wraps within column widths."""
    built = []
    for r_i, row in enumerate(rows):
        cells = []
        for c_i, cell in enumerate(row):
            if isinstance(cell, str):
                col = header_color if r_i == 0 else TEXT
                m = wrapped(cell, size=size, width=col_widths[c_i] - 2 * pad, color=col,
                            weight="BOLD" if r_i == 0 else "NORMAL")
            else:
                m = cell
            cells.append(m)
        built.append(cells)
    heights = [max(c.height for c in cells) + 2 * pad for cells in built]
    if row_h:
        heights = [max(h, row_h) for h in heights]
    total_w = sum(col_widths)
    out = VGroup()
    y = 0.0
    for r_i, cells in enumerate(built):
        x = 0.0
        for c_i, m in enumerate(cells):
            m.move_to([x + pad + m.width / 2, y - heights[r_i] / 2, 0])
            out.add(m)
            x += col_widths[c_i]
        y -= heights[r_i]
    grid = VGroup()
    yy = 0.0
    for r_i, h in enumerate(heights + [None]):
        grid.add(Line([0, yy, 0], [total_w, yy, 0], color=line_color if r_i not in (1,) else header_color,
                      stroke_width=2 if r_i != 1 else 3))
        if h is not None:
            yy -= h
    xx = 0.0
    for w in col_widths[:-1]:
        xx += w
        grid.add(Line([xx, 0, 0], [xx, yy, 0], color=line_color, stroke_width=1.5))
    g = VGroup(grid, out)
    g.cell_rows = built
    return g.move_to(ORIGIN)


# ------------------------------------------------------------------ apparatus: flask
def flask(width: float = 2.2, height: float = 2.6, liquid: str = "#5DADE2", level: float = 0.45,
          outline: str = TEXT) -> VGroup:
    """Schematic conical flask. level = fraction of the body filled."""
    nw = width * 0.28
    neck_h = height * 0.3
    body_h = height - neck_h
    pts = [(-nw / 2, height / 2), (-nw / 2, height / 2 - neck_h), (-width / 2, -height / 2),
           (width / 2, -height / 2), (nw / 2, height / 2 - neck_h), (nw / 2, height / 2)]
    glass = VMobject(stroke_color=outline, stroke_width=3)
    glass.set_points_as_corners([np.array([x, y, 0]) for x, y in pts])
    yl = -height / 2 + body_h * level
    # liquid is the trapezium under the level line
    def xat(y):
        t = (y + height / 2) / body_h
        return width / 2 * (1 - t) + nw / 2 * t
    liq = Polygon([-width / 2, -height / 2, 0], [width / 2, -height / 2, 0], [xat(yl), yl, 0],
                  [-xat(yl), yl, 0], stroke_width=0, fill_color=liquid, fill_opacity=0.55)
    return VGroup(liq, glass)


def tag(label: str, value: str, color: str, size: int = LABEL) -> VGroup:
    """A luggage-tag style label: coloured quantity name chip + value."""
    c = chip(label, color, size=SMALL)
    v = T(value, size=size, color=TEXT)
    g = VGroup(c, v).arrange(RIGHT, buff=0.18)
    r = RoundedRectangle(width=g.width + 0.3, height=g.height + 0.24, corner_radius=0.1,
                         stroke_color=color, stroke_width=2, fill_color=PANEL, fill_opacity=0.95)
    r.move_to(g)
    return VGroup(r, g)


# ------------------------------------------------------------------ unit ladder
def ladder(units: list[str], factors: list[str], color: str = TEXT, size: int = LABEL + 2,
           rung_w: float = 1.9, gap: float = 0.95, down_label: str = "×", up_label: str = "÷") -> VGroup:
    """Vertical ladder: largest unit at the top. Arrows on the left go down (×f), on the right up (÷f)."""
    rungs = VGroup()
    for u in units:
        t = TB(u, size=size, color=color)
        r = RoundedRectangle(width=rung_w, height=0.75, corner_radius=0.12, stroke_color=color,
                             stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
        rungs.add(VGroup(r, t.move_to(r)))
    rungs.arrange(DOWN, buff=gap)
    arrows = VGroup()
    for i, f in enumerate(factors):
        a, b = rungs[i], rungs[i + 1]
        dn = Arrow(a.get_bottom() + LEFT * 0.45, b.get_top() + LEFT * 0.45, buff=0.06, color=GOOD,
                   stroke_width=4, max_tip_length_to_length_ratio=0.3)
        up = Arrow(b.get_top() + RIGHT * 0.45, a.get_bottom() + RIGHT * 0.45, buff=0.06, color=SYSTEM,
                   stroke_width=4, max_tip_length_to_length_ratio=0.3)
        ld = T(f"{down_label}{f}", size=SMALL, color=GOOD).next_to(dn, LEFT, buff=0.12)
        lu = T(f"{up_label}{f}", size=SMALL, color=SYSTEM).next_to(up, RIGHT, buff=0.12)
        arrows.add(VGroup(dn, ld, up, lu))
    return VGroup(rungs, arrows)


# ------------------------------------------------------------------ molecules (schematic)
ATOM_R = {"H": 0.17, "C": 0.26, "O": 0.25, "N": 0.25, "Cl": 0.3, "Na": 0.3, "S": 0.3}


def atom(el: str, scale: float = 1.0) -> VGroup:
    r = ATOM_R.get(el, 0.25) * scale
    c = Circle(radius=r, stroke_color=WHITE if el != "H" else "#9AA5B1", stroke_width=1.5,
               fill_color=ATOM_COLORS.get(el, "#888888"), fill_opacity=1)
    lab_col = BG if el in ("H", "S", "Cl") else WHITE
    t = TB(el, size=max(12, int(20 * scale * (0.85 if len(el) > 1 else 1))), color=lab_col).move_to(c)
    g = VGroup(c, t)
    g.element = el
    return g


def molecule(spec: list[tuple[str, tuple[float, float]]], bonds: list[tuple[int, int, int]] = (),
             scale: float = 1.0) -> VGroup:
    """spec: [(element, (x, y)), ...]; bonds: [(i, j, order)]. Returns VGroup(bonds_group, atoms_group)."""
    atoms = VGroup()
    for el, (x, y) in spec:
        a = atom(el, scale)
        a.move_to(np.array([x, y, 0]) * scale)
        atoms.add(a)
    bg = VGroup()
    for i, j, order in bonds:
        p, q = atoms[i].get_center(), atoms[j].get_center()
        d = q - p
        n = np.array([-d[1], d[0], 0])
        n = n / (np.linalg.norm(n) + 1e-9) * 0.06 * scale
        offs = [0] if order == 1 else ([-1, 1] if order == 2 else [-1.6, 0, 1.6])
        for o in offs:
            bg.add(Line(p + n * o, q + n * o, color="#C8D0DA", stroke_width=3.5 * scale))
    m = VGroup(bg, atoms)
    m.bonds, m.atoms = bg, atoms
    return m


def mol_H2(s=1.0):
    return molecule([("H", (-0.22, 0)), ("H", (0.22, 0))], [(0, 1, 1)], s)


def mol_O2(s=1.0):
    return molecule([("O", (-0.3, 0)), ("O", (0.3, 0))], [(0, 1, 2)], s)


def mol_Cl2(s=1.0):
    return molecule([("Cl", (-0.34, 0)), ("Cl", (0.34, 0))], [(0, 1, 1)], s)


def mol_HCl(s=1.0):
    return molecule([("H", (-0.3, 0)), ("Cl", (0.18, 0))], [(0, 1, 1)], s)


def mol_H2O(s=1.0):
    return molecule([("O", (0, 0.1)), ("H", (-0.36, -0.2)), ("H", (0.36, -0.2))], [(0, 1, 1), (0, 2, 1)], s)


def mol_CO2(s=1.0):
    return molecule([("O", (-0.58, 0)), ("C", (0, 0)), ("O", (0.58, 0))], [(0, 1, 2), (1, 2, 2)], s)


def mol_CO(s=1.0):
    return molecule([("C", (-0.27, 0)), ("O", (0.27, 0))], [(0, 1, 3)], s)


def mol_CH4(s=1.0):
    return molecule([("C", (0, 0)), ("H", (0, 0.5)), ("H", (0, -0.5)), ("H", (-0.5, 0)), ("H", (0.5, 0))],
                    [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)], s)


def mol_CH3OH(s=1.0):
    return molecule([("C", (-0.3, 0)), ("H", (-0.3, 0.5)), ("H", (-0.3, -0.5)), ("H", (-0.8, 0)),
                     ("O", (0.3, 0)), ("H", (0.7, 0.3))],
                    [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (4, 5, 1)], s)


def mol_C2H5OH(s=1.0):
    return molecule([("C", (-0.55, 0)), ("C", (0.05, 0)), ("O", (0.62, 0.0)), ("H", (1.0, 0.3)),
                     ("H", (-0.55, 0.5)), ("H", (-0.55, -0.5)), ("H", (-1.05, 0)),
                     ("H", (0.05, 0.5)), ("H", (0.05, -0.5))],
                    [(0, 1, 1), (1, 2, 1), (2, 3, 1), (0, 4, 1), (0, 5, 1), (0, 6, 1), (1, 7, 1), (1, 8, 1)], s)


def formula_counter(counts: dict[str, int | float], size: int = LABEL) -> VGroup:
    """Row of coloured element counters, e.g. C 2 | H 6 | O 7."""
    g = VGroup()
    for el, n in counts.items():
        a = atom(el, 0.8)
        v = TB(f"{n:g}", size=size)
        g.add(VGroup(a, v).arrange(RIGHT, buff=0.12))
    return g.arrange(RIGHT, buff=0.4)


# ------------------------------------------------------------------ misc
def arrow_label(start, end, text: str, color: str = TEXT, size: int = SMALL, side=UP, dashed: bool = False,
                stroke: float = 5) -> VGroup:
    a = Arrow(start, end, buff=0.05, color=color, stroke_width=stroke, max_tip_length_to_length_ratio=0.15)
    if dashed:
        a = DashedVMobject(a, num_dashes=14)
    t = T(text, size=size, color=color).next_to(a, side, buff=0.1)
    return VGroup(a, t)


def number_badge(n: int | str, color: str = SYSTEM, size: int = LABEL) -> VGroup:
    c = Circle(radius=0.24, stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1)
    return VGroup(c, TB(str(n), size=size, color=color).move_to(c))


def hladder(units: list[str], factors: list[str], color: str = TEXT, size: int = LABEL, box_w: float = 1.25,
            gap: float = 1.35) -> VGroup:
    """Horizontal unit ladder: largest unit on the left; top arrows go right (×f), bottom arrows go left (÷f)."""
    boxes = VGroup()
    for u in units:
        r = RoundedRectangle(width=box_w, height=0.62, corner_radius=0.1, stroke_color=color, stroke_width=2.5,
                             fill_color=PANEL, fill_opacity=1)
        boxes.add(VGroup(r, TB(u, size=size, color=color).move_to(r)))
    boxes.arrange(RIGHT, buff=gap)
    arrows = VGroup()
    for i, f in enumerate(factors):
        a, b = boxes[i], boxes[i + 1]
        r = Arrow(a.get_right() + UP * 0.14, b.get_left() + UP * 0.14, buff=0.06, color=GOOD, stroke_width=4,
                  max_tip_length_to_length_ratio=0.25)
        l = Arrow(b.get_left() + DOWN * 0.14, a.get_right() + DOWN * 0.14, buff=0.06, color=SYSTEM, stroke_width=4,
                  max_tip_length_to_length_ratio=0.25)
        tr = T(f"×{f}", size=SMALL, color=GOOD).next_to(r, UP, buff=0.06)
        tl = T(f"÷{f}", size=SMALL, color=SYSTEM).next_to(l, DOWN, buff=0.06)
        arrows.add(VGroup(r, tr, l, tl))
    return VGroup(boxes, arrows)
