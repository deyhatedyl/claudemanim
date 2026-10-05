"""
Reusable visual components shared by all episodes.

Every component returns ordinary Manim mobjects so scenes can animate their parts freely.
"""
from __future__ import annotations

import re
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from manim import (DL, DOWN, DR, LEFT, ORIGIN, RIGHT, UL, UP, UR, Arrow, Circle, CurvedArrow,
                   DashedLine, DashedVMobject, Dot, Line, MathTex, Polygon, Rectangle,
                   RoundedRectangle, Text, VGroup, VMobject, WHITE)

from .style import (ATOM_COLORS, BAD, BG, BODY, EQ, EQ_SMALL, FAINT, GOOD, LABEL, LOSS, MUTED, PANEL,
                    SMALL, SYSTEM, TEXT, UNKNOWN, M, T, TB, chip, panel, fit_content)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "questions"))
from bank import BY_ID  # noqa: E402


# ------------------------------------------------------------------ text layout
@lru_cache(maxsize=4096)
def _w(s: str, size: int, weight: str = "NORMAL") -> float:
    return T(s, size=size, weight=weight).width


def wrap(s: str, size: int = LABEL, width: float = 11.5, weight: str = "NORMAL") -> list[str]:
    """Greedy word wrap using measured text widths. A number stays on the same line as its unit."""
    s = re.sub(r"(\d)\s+(kJ|MJ|J|g|kg|mg|mol|L|mL|°C|%|K|s|kPa)\b", "\\1\u00a0\\2", s)
    words, lines, cur = [w for w in s.split(" ") if w], [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if cur and _w(cand, size, weight) > width:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def wrapped(s: str, size: int = LABEL, width: float = 11.5, color: str = TEXT, buff: float = 0.12,
            weight: str = "NORMAL") -> VGroup:
    if weight == "NORMAL" and color not in (TEXT, MUTED, FAINT, BG):
        weight = "SEMIBOLD"
    g = VGroup(*[T(l, size=size, color=color, weight=weight) for l in wrap(s, size, width, weight)])
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
                  parts: list[str] | None = None, cols: int = 1, side: bool = False, split: float = 0.5,
                  inline_marks: bool = False, tight: bool = False, balance: bool = False) -> VGroup:
    """The full prompt of an anchor question with its marks (no answers). cols=2 lays parts out in two columns;
    side=True puts the stem on the left and a single column of parts on the right (for long questions)."""
    q = BY_ID[qid]
    if q.get("visual") and show_parts:
        from .question_visuals import visual_question
        return visual_question(q, width=width, size=size, parts=parts, tight=tight)
    total = sum(p[2] for p in q["parts"])
    head = VGroup(TB(f"{qid}", size=size + 4, color=SYSTEM),
                  T(q["title"], size=size, color=TEXT),
                  T(f"{total} marks", size=size, color=MUTED)).arrange(RIGHT, buff=0.35)
    lb = 0.06 if tight else 0.12          # gap between wrapped lines
    half = (width - 1.0) * split
    pcol = (width - 1.0) - half
    body = wrapped(q["stem"], size=size, width=half if side else width - 0.6, buff=lb)
    rows = VGroup(head, body)
    if show_parts and side:
        built = VGroup()
        for lab, txt, mk in q["parts"]:
            if parts and lab not in parts:
                continue
            letter = TB(f"{lab}.", size=size, color=SYSTEM)
            t = wrapped(txt, size=size, width=pcol - 1.2)
            m = T(f"[{mk}]", size=size, color=MUTED)
            t.next_to(letter, RIGHT, buff=0.2, aligned_edge=UP)
            m.next_to(t, RIGHT, buff=0.2, aligned_edge=UP)
            built.add(VGroup(letter, t, m))
        built.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        sep = Line(UP, DOWN, color=FAINT, stroke_width=1.5)
        two = VGroup(body, built).arrange(RIGHT, buff=0.4, aligned_edge=UP)
        built.align_to(body, LEFT).shift(RIGHT * (half + 0.4))
        sep.stretch_to_fit_height(max(body.height, built.height)).move_to(two).align_to(two, UP)
        sep.set_x(body.get_left()[0] + half + 0.2)
        rows = VGroup(head, VGroup(body, sep, built))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        bg = panel(rows, color=FAINT, buff=0.3)
        return fit_content(VGroup(bg, rows), max_height=4.9)
    if show_parts:
        pw = (width - 0.6) / cols
        built = VGroup()
        for lab, txt, mk in q["parts"]:
            if parts and lab not in parts:
                continue
            letter = TB(f"{lab}.", size=size, color=SYSTEM)
            if inline_marks:            # marks at the end of the text: narrower cards for long questions
                t = wrapped(f"{txt} [{mk}]", size=size, width=pw - 0.75, buff=lb)
                t[-1][-len(f"[{mk}]"):].set_color(MUTED)
                t.next_to(letter, RIGHT, buff=0.2, aligned_edge=UP)
                built.add(VGroup(letter, t))
                continue
            t = wrapped(txt, size=size, width=pw - 1.4)
            m = T(f"[{mk}]", size=size, color=MUTED)
            t.next_to(letter, RIGHT, buff=0.2, aligned_edge=UP)
            m.next_to(t, RIGHT, buff=0.2, aligned_edge=UP)
            built.add(VGroup(letter, t, m))
        if cols == 1:
            rows.add(*built)
        else:
            per = -(-len(built) // cols)
            if balance and cols == 2:          # split (order kept) where the taller column is shortest
                per = min(range(1, len(built)), key=lambda k: max(sum(p.height for p in built[:k]),
                                                                   sum(p.height for p in built[k:])))
            pb = 0.12 if tight else 0.18
            columns = VGroup(VGroup(*built[:per]).arrange(DOWN, aligned_edge=LEFT, buff=pb),
                             VGroup(*built[per:]).arrange(DOWN, aligned_edge=LEFT, buff=pb)) if cols == 2 else \
                VGroup(*[VGroup(*built[i * per:(i + 1) * per]).arrange(DOWN, aligned_edge=LEFT, buff=pb)
                         for i in range(cols)])
            columns.arrange(RIGHT, buff=0.4, aligned_edge=UP)
            for i, c in enumerate(columns[1:], 1):
                c.align_to(columns[0], LEFT).shift(RIGHT * pw * i)
            rows.add(columns)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16 if tight else 0.22)
    bg = panel(rows, color=FAINT, buff=0.24 if tight else 0.3)
    return fit_content(VGroup(bg, rows), max_height=4.9)


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
        box = Circle(radius=0.18, stroke_width=0, fill_color=GOOD, fill_opacity=1)
        n = T(str(mk), size=min(size, 20), color=BG, weight="SEMIBOLD").move_to(box)
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
    c = Circle(radius=0.19, stroke_width=0, fill_color=GOOD, fill_opacity=1)
    return VGroup(c, TB(str(n), size=min(size, 20), color=BG).move_to(c))


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


# ------------------------------------------------------------------ calorimetry apparatus
class Thermometer(VGroup):
    """Schematic thermometer whose liquid column follows self.level (a ValueTracker, 0..1)."""

    def __init__(self, height: float = 2.4, level: float = 0.35, color: str = "#F1948A", **kw):
        from manim import ValueTracker, always_redraw
        super().__init__(**kw)
        self.h = height
        tube = RoundedRectangle(width=0.2, height=height, corner_radius=0.1, stroke_color=TEXT, stroke_width=2.5,
                                fill_color=BG, fill_opacity=1)
        bulb = Circle(radius=0.17, stroke_color=TEXT, stroke_width=2.5, fill_color=color, fill_opacity=1)
        bulb.move_to(tube.get_bottom() + 0.05 * UP)
        self.tube, self.bulb = tube, bulb
        self.level = ValueTracker(level)
        base = bulb.get_center()

        def col():
            hh = max(0.02, self.level.get_value() * (height - 0.25))
            r = Rectangle(width=0.1, height=hh, stroke_width=0, fill_color=color, fill_opacity=1)
            r.move_to(self.bulb.get_center() + UP * hh / 2)
            return r
        self.column = always_redraw(col)
        ticks = VGroup(*[Line(LEFT * 0.05, RIGHT * 0.05, color=MUTED, stroke_width=1.5)
                         .move_to(tube.get_bottom() + UP * (0.35 + i * (height - 0.5) / 6) + RIGHT * 0.17)
                         for i in range(7)])
        self.add(tube, ticks, self.column, bulb)


def calorimeter(width: float = 3.2, height: float = 2.6, water_level: float = 0.65, heater: bool = False,
                system: bool = False, thermometer: bool = True, stirrer: bool = True, lid: bool = True) -> VGroup:
    """Schematic insulated cup calorimeter. Parts: .cup .water .lid .thermo .stirrer .heater .system"""
    from .style import SURR, SYSTEM as SYS
    bw = width * 0.82
    outer = Polygon([-width / 2, height / 2, 0], [width / 2, height / 2, 0], [bw / 2, -height / 2, 0],
                    [-bw / 2, -height / 2, 0], stroke_color=SURR, stroke_width=3, fill_color=PANEL, fill_opacity=1)
    inner = outer.copy().scale(0.9).set_stroke(SURR, 1.5).set_fill(BG, 1)
    yl = -height / 2 * 0.9 + height * 0.9 * water_level

    def xat(y):
        t = (y + height * 0.45) / (height * 0.9)
        return (bw * 0.9 / 2) * (1 - t) + (width * 0.9 / 2) * t
    water = Polygon([-bw * 0.45, -height * 0.45, 0], [bw * 0.45, -height * 0.45, 0], [xat(yl), yl, 0],
                    [-xat(yl), yl, 0], stroke_width=0, fill_color=SURR, fill_opacity=0.35)
    g = VGroup(outer, inner, water)
    g.cup, g.water = VGroup(outer, inner), water
    g.lid = g.thermo = g.stirrer = g.heater = g.system = None
    if lid:
        lid_m = RoundedRectangle(width=width * 1.08, height=0.2, corner_radius=0.05, stroke_color=SURR,
                                 stroke_width=2.5, fill_color=PANEL, fill_opacity=1).next_to(outer, UP, buff=0)
        g.add(lid_m)
        g.lid = lid_m
    if thermometer:
        th = Thermometer(height=height * 1.0)
        th.move_to([width * 0.22, -height * 0.05, 0]).align_to(water, DOWN).shift(0.15 * UP)
        g.add(th)
        g.thermo = th
    if stirrer:
        st = VGroup(Line([-width * 0.25, height / 2 + 0.6, 0], [-width * 0.25, -height * 0.32, 0], color=MUTED,
                         stroke_width=3),
                    Circle(radius=0.16, color=MUTED, stroke_width=3).move_to([-width * 0.25, -height * 0.32, 0]))
        g.add(st)
        g.stirrer = st
    if heater:
        pts = [np.array([-0.05 + 0.18 * np.sin(k * np.pi / 2), -height * 0.3 + 0.12 * k, 0]) for k in range(9)]
        coil = VMobject(stroke_color=SYSTEM, stroke_width=4).set_points_smoothly(pts)
        leads = VGroup(Line(pts[-1], [-0.05, height / 2 + 0.6, 0], color=SYSTEM, stroke_width=3),
                       Line(pts[0] + 0.0 * UP, [0.25, height / 2 + 0.6, 0], color=SYSTEM, stroke_width=3))
        h = VGroup(coil, leads)
        g.add(h)
        g.heater = h
    if system:
        from .style import SYSTEM as SC
        sysb = DashedVMobject(Circle(radius=min(width, height) * 0.2, color=SC, stroke_width=3), num_dashes=20)
        sysb.move_to([-0.15, -height * 0.18, 0])
        g.add(sysb)
        g.system = sysb
    return g


def enthalpy_axis(height: float = 4.2, label: str = "Enthalpy, H") -> VGroup:
    ax = Arrow([0, -height / 2, 0], [0, height / 2, 0], buff=0, color=TEXT, stroke_width=3,
               max_tip_length_to_length_ratio=0.06)
    t = T(label, size=SMALL + 2).rotate(np.pi / 2).next_to(ax, LEFT, buff=0.15)
    return VGroup(ax, t)


def level(width: float, label: str, color: str = TEXT, size: int = LABEL, side=RIGHT) -> VGroup:
    ln = Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=5)
    t = T(label, size=size, color=color).next_to(ln, side, buff=0.2)
    g = VGroup(ln, t)
    g.line, g.label = ln, t
    return g


def dH_arrow(y_from: float, y_to: float, x: float, text: str, color: str = UNKNOWN, size: int = LABEL,
             side=RIGHT) -> VGroup:
    a = Arrow([x, y_from, 0], [x, y_to, 0], buff=0, color=color, stroke_width=5,
              max_tip_length_to_length_ratio=0.12)
    t = T(text, size=size, color=color).next_to(a, side, buff=0.15)
    return VGroup(a, t)


def ledger(broken: list[tuple[str, str]], formed: list[tuple[str, str]], broken_total: str, formed_total: str,
           width: float = 5.6, size: int = LABEL) -> VGroup:
    """Two-column bond ledger. Each column: header, rows (desc, value), total.
    Returns VGroup(left, right) with attributes .rows and .total on each column."""
    from .style import SYSTEM as SC, USEFUL

    def col(title, sub, rows, total, color):
        h1 = TB(title, size=size + 2, color=color)
        h2 = T(sub, size=SMALL, color=color)
        hd = VGroup(h1, h2).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        rr = VGroup()
        for d, v in rows:
            dt = T(d, size=size)
            vt = T(v, size=size) if v else Dot(radius=0.001, fill_opacity=0, stroke_width=0)
            vt.move_to([width / 2 - 0.3 - vt.width / 2, 0, 0])
            dt.move_to([-width / 2 + 0.3 + dt.width / 2, 0, 0])
            rr.add(VGroup(dt, vt))
        rr.arrange(DOWN, buff=0.18)
        for r in rr:
            r[0].align_to([-width / 2 + 0.3, 0, 0], LEFT)
            r[1].align_to([width / 2 - 0.3, 0, 0], RIGHT)
        tl = Line(LEFT * (width / 2 - 0.2), RIGHT * (width / 2 - 0.2), color=color, stroke_width=2)
        tt = VGroup(TB("Total", size=size, color=color), TB(total, size=size, color=color))
        tt[0].align_to([-width / 2 + 0.3, 0, 0], LEFT)
        tt[1].align_to([width / 2 - 0.3, 0, 0], RIGHT)
        body = VGroup(hd, rr, tl, tt).arrange(DOWN, buff=0.2)
        hd.align_to([-width / 2 + 0.3, 0, 0], LEFT)
        for r in rr:
            r[0].align_to([-width / 2 + 0.3, 0, 0], LEFT)
            r[1].align_to([width / 2 - 0.3, 0, 0], RIGHT)
        tt[0].align_to([-width / 2 + 0.3, 0, 0], LEFT)
        tt[1].align_to([width / 2 - 0.3, 0, 0], RIGHT)
        box = RoundedRectangle(width=width, height=body.height + 0.45, corner_radius=0.15, stroke_color=color,
                               stroke_width=2.5, fill_color=PANEL, fill_opacity=0.95).move_to(body)
        c = VGroup(box, hd, rr, tl, tt)
        c.box, c.head, c.rows, c.line, c.total = box, hd, rr, tl, tt
        return c
    left = col("Bonds broken", "energy absorbed (in)", broken, broken_total, SC)
    right = col("Bonds formed", "energy released (out)", formed, formed_total, USEFUL)
    g = VGroup(left, right).arrange(RIGHT, buff=0.4, aligned_edge=UP)
    g.left, g.right = left, right
    return g


# ------------------------------------------------------------------ energy profiles
def profile_fn(R: float, TS: float, P: float, x0: float = 2.0, xp: float = 5.0, x1: float = 8.0):
    """Smooth (C1) enthalpy curve: flat at R until x0, cosine rise to TS at xp, cosine fall to P at x1, then flat."""
    def f(x):
        if x <= x0:
            return R
        if x <= xp:
            t = (x - x0) / (xp - x0)
            return R + (TS - R) * (1 - np.cos(np.pi * t)) / 2
        if x <= x1:
            t = (x - xp) / (x1 - xp)
            return TS + (P - TS) * (1 - np.cos(np.pi * t)) / 2
        return P
    return f


def profile_axes(y_max: float = 175, y_step: float = 25, width: float = 7.0, height: float = 4.6,
                 numbers: bool = True, y_label: str = "Enthalpy (kJ mol⁻¹)") -> VGroup:
    """Axes for an energy profile. x: reaction coordinate 0..10 (not time). Returns VGroup(axes, xlab, ylab)."""
    from manim import Axes
    height = min(height, 4.20)
    ax = Axes(x_range=[0, 10, 1], y_range=[0, y_max, y_step], x_length=width, y_length=height,
              axis_config=dict(color=MUTED, stroke_width=1.3, include_ticks=False, tip_length=0.12,
                               label_constructor=Text),
              y_axis_config=dict(include_ticks=numbers, include_numbers=numbers,
                                 numbers_to_include=np.arange(0, y_max + 1, y_step) if numbers else [],
                                 font_size=24, decimal_number_config=dict(num_decimal_places=0, color=MUTED)))
    xl = T("Reaction coordinate (not time)", size=SMALL, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.18)
    yl = T(y_label, size=SMALL, color=MUTED).rotate(np.pi / 2).next_to(ax.y_axis, LEFT, buff=0.55 if numbers else 0.2)
    g = VGroup(ax, xl, yl)
    g.ax, g.xlab, g.ylab = ax, xl, yl
    return g


def profile_curve(ax, R: float, TS: float, P: float, color: str = TEXT, dashed: bool = False, width: float = 4,
                  x0: float = 2.0, xp: float = 5.0, x1: float = 8.0):
    c = ax.plot(profile_fn(R, TS, P, x0, xp, x1), x_range=[0.4, 9.6, 0.02], color=color, stroke_width=width,
                use_smoothing=False)
    return DashedVMobject(c, num_dashes=60) if dashed else c


def v_arrow(ax, x: float, y_from: float, y_to: float, text: str, color: str, side=RIGHT, size: int = SMALL + 2,
            double: bool = False, at: str = "mid") -> VGroup:
    """Vertical arrow between two enthalpy values (data coordinates) with a label.
    at="mid" centres the label on the arrow; "top"/"bottom" puts it beside the upper/lower end."""
    from manim import DoubleArrow
    p, q = ax.c2p(x, y_from), ax.c2p(x, y_to)
    cls = DoubleArrow if double else Arrow
    a = cls(p, q, buff=0, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.12, tip_length=0.18)
    t = T(text, size=size, color=color).next_to(a, side, buff=0.1)
    if at == "top":
        t.align_to(a, UP).shift(0.12 * DOWN)
    elif at == "bottom":
        t.align_to(a, DOWN).shift(0.12 * UP)
    return VGroup(a, t)


def h_guide(ax, y: float, x_from: float, x_to: float, color: str = FAINT) -> DashedLine:
    return DashedLine(ax.c2p(x_from, y), ax.c2p(x_to, y), color=color, stroke_width=1.5, dash_length=0.08)


# ------------------------------------------------------------------ reaction budget (initial / used / remaining)
class Budget(VGroup):
    """Grid with species rows and stage columns (e.g. initial, used, remaining, formed).
    Use .cell(r, c, text, color) to create a value mobject positioned in a cell (not added automatically)."""

    def __init__(self, species: list[str], cols: list[str], col_w: float = 2.2, label_w: float = 1.8,
                 row_h: float = 0.62, size: int = LABEL, col_colors: list[str] | None = None, **kw):
        super().__init__(**kw)
        self.col_w, self.label_w, self.row_h, self.size = col_w, label_w, row_h, size
        n_r, n_c = len(species), len(cols)
        W = label_w + n_c * col_w
        H = (n_r + 1) * row_h
        col_colors = col_colors or [MUTED] * n_c
        self.heads = VGroup(*[TB(c, size=size, color=col_colors[i]).move_to([label_w + (i + 0.5) * col_w, -0.5 * row_h, 0])
                              for i, c in enumerate(cols)])
        self.labels = VGroup(*[T(s, size=size + 2).move_to([label_w / 2, -(r + 1.5) * row_h, 0])
                               for r, s in enumerate(species)])
        lines = VGroup(Line([0, -row_h, 0], [W, -row_h, 0], color=SYSTEM, stroke_width=2.5))
        for r in range(2, n_r + 1):
            lines.add(Line([0, -r * row_h, 0], [W, -r * row_h, 0], color=FAINT, stroke_width=1.2))
        for c in range(n_c):
            x = label_w + c * col_w
            lines.add(Line([x, 0, 0], [x, -H, 0], color=FAINT, stroke_width=1.2))
        self.lines = lines
        self.add(lines, self.heads, self.labels)
        self._origin = self.get_center().copy()

    def pos(self, r: int, c: int):
        shift = self.get_center() - self._origin
        return np.array([self.label_w + (c + 0.5) * self.col_w, -(r + 1.5) * self.row_h, 0]) + shift

    def cell(self, r: int, c: int, text: str, color: str = TEXT, bold: bool = False):
        t = (TB if bold else T)(text, size=self.size, color=color)
        if t.width > self.col_w - 0.15:
            t.scale((self.col_w - 0.15) / t.width)
        return t.move_to(self.pos(r, c))

    def move_to(self, point, **kw):
        super().move_to(point, **kw)
        return self


# ------------------------------------------------------------------ temperature-time plots (real data only)
def temp_axes(x_max: float = 400, x_step: float = 60, y_min: float = 20, y_max: float = 27, y_step: float = 1,
              width: float = 8.0, height: float = 4.4, x_label: str = "Time (s)", y_label: str = "Temperature (°C)"):
    """Axes for temperature-time data. Returns VGroup(ax, xlab, ylab) with .ax set."""
    from manim import Axes
    height = min(height, 4.0)
    ax = Axes(x_range=[0, x_max, x_step], y_range=[y_min, y_max, y_step], x_length=width, y_length=height,
              axis_config=dict(color=MUTED, stroke_width=1.3, include_tip=False, font_size=22,
                               label_constructor=Text,
                               decimal_number_config=dict(num_decimal_places=0, color=MUTED)),
              x_axis_config=dict(numbers_to_include=np.arange(0, x_max + 1, x_step)),
              y_axis_config=dict(numbers_to_include=np.arange(y_min, y_max + 0.01, y_step)))
    grid = VGroup(*[DashedLine(ax.c2p(0, y), ax.c2p(x_max, y), color=FAINT, stroke_width=1, dash_length=0.06)
                    for y in np.arange(y_min + y_step, y_max + 0.01, y_step)])
    xl = T(x_label, size=SMALL + 1, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.45)
    yl = T(y_label, size=SMALL + 1, color=MUTED).rotate(np.pi / 2).next_to(ax.y_axis, LEFT, buff=0.55)
    g = VGroup(grid, ax, xl, yl)
    g.ax, g.grid = ax, grid
    return g


def data_points(ax, pts, color: str = TEXT, radius: float = 0.07) -> VGroup:
    return VGroup(*[Dot(ax.c2p(x, y), radius=radius, color=color) for x, y in pts])


def linfit(pts):
    xs = np.array([p[0] for p in pts], dtype=float)
    ys = np.array([p[1] for p in pts], dtype=float)
    b, a = np.polyfit(xs, ys, 1)
    return b, a          # slope, intercept
