"""
Shared helpers for the exam-workshop episodes (E13, E14): working lines with indicative-mark boxes,
running mark tallies, question-card pause banners and method-map nodes.
"""
from manim import *  # noqa: F403

from .components import question_card, wrapped
from .style import (BG, EQ_SMALL, FAINT, GOOD, LABEL, MUTED, PANEL, SMALL, SYSTEM, TEXT, UNKNOWN, M, T, TB, chip)

BIO = "#7BE495"
CO2E = "#AEB6BF"
WK = EQ_SMALL - 8          # working-line size
X0 = -5.55                 # left edge of working lines
XM = 6.0                   # mark-box column


def requested(text: str) -> VGroup:
    from shared.style import asked_pill
    return asked_pill(text)


def mbox(n: int = 1) -> VGroup:
    """An indicative-mark box; tick() fills it once the step is visible."""
    r = RoundedRectangle(width=0.46, height=0.42, corner_radius=0.08, stroke_color=GOOD, stroke_width=2,
                         fill_color=GOOD, fill_opacity=0)
    return VGroup(r, T(str(n), size=SMALL, color=GOOD).move_to(r))


def tick(box: VGroup) -> Animation:
    """Fill one mark box (or every box in a row of them) solid green with a dark number."""
    boxes = [box] if isinstance(box[0], RoundedRectangle) else list(box)
    return AnimationGroup(*[a for x in boxes for a in (x[0].animate.set_fill(GOOD, opacity=0.95),
                                                       x[1].animate.set_color(BG))])


def work(tex: str, y: float, color: str = TEXT, size: int = WK, x: float = X0) -> MathTex:
    m = M(tex, size=size, color=color)
    return m.move_to([0, y, 0]).align_to([x, 0, 0], LEFT)


def part_tag(letter: str, line: Mobject) -> Text:
    return TB(f"{letter}.", size=LABEL + 2, color=SYSTEM).next_to(line, LEFT, buff=0.3).align_to([X0 - 0.75, 0, 0], LEFT)


def boxes_for(line: Mobject, n: int = 1, marks: int = 1) -> VGroup:
    g = VGroup(*[mbox(marks) for _ in range(n)]).arrange(LEFT, buff=0.1)
    return g.move_to([XM - (g.width - 0.46) / 2, line.get_y(), 0])


def tally_text(qid: str, got: int, total: int) -> Text:
    return T(f"{qid} marks shown: {got} / {total}", size=SMALL + 1, color=GOOD).to_corner(UR, buff=0.4)


def blank() -> Dot:
    return Dot(radius=0.001, fill_opacity=0, stroke_width=0)


def node(letter: str, lines: list[str], color: str, width: float = 3.4, size: int = SMALL + 1) -> VGroup:
    lab = chip(letter, color, size=SMALL + 2)
    body = VGroup(*[T(l, size=size) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    body.next_to(lab, RIGHT, buff=0.18, aligned_edge=UP)
    g = VGroup(lab, body)
    r = RoundedRectangle(width=max(width, g.width + 0.4), height=max(0.72, g.height + 0.32), corner_radius=0.12,
                         stroke_color=color, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
    g.move_to(r)
    return VGroup(r, g)


def number(n: int, line: Mobject) -> VGroup:
    c = Circle(radius=0.24, stroke_color=SYSTEM, stroke_width=2.5)
    t = TB(str(n), size=LABEL, color=SYSTEM).move_to(c)
    return VGroup(c, t).next_to(line, LEFT, buff=0.35)


def attempt_card(qid: str, size: int = SMALL + 1) -> VGroup:
    """Full question for the quiet attempt period. No header (the card carries the title); the scene's timer sits
    in the bottom strip (TIMER_CORNER = DR), which carries no captions during the silent pause."""
    qc = question_card(qid, size=size, width=13.3, cols=2, inline_marks=True, tight=True, balance=True)
    return qc.move_to([0, 0, 0]).align_to([0, 3.62, 0], UP)
