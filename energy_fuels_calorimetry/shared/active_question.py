"""Exact, part-by-part questions during worked solutions.

Use question_card() to introduce the complete original question. After the
attempt, show one PartPrompt for the CURRENT letter with the exact wording
and marks from questions/bank.py. Only pass inputs relevant to that part.
No data-book value is silently substituted for a value explicitly supplied
by the question (e.g. Q13's -1370 kJ/mol).
"""
from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, RoundedRectangle, VGroup

from .components import wrapped
from .style import FAINT, GOOD, MUTED, PANEL, SMALL, SURR, SYSTEM, TEXT, UNKNOWN, T, TB

from questions.bank import BY_ID

GIVEN_COLOUR = SURR
DATA_BOOK_COLOUR = UNKNOWN
CALCULATED_COLOUR = GOOD


def _source_style(source: str) -> tuple[str, str]:
    lowered = source.casefold().strip()
    if lowered in ("question", "supplied in question", "given in question"):
        return GIVEN_COLOUR, "GIVEN IN QUESTION"
    if "book" in lowered or "vcaa" in lowered:
        return DATA_BOOK_COLOUR, "2026 VCAA DATA BOOK"
    if "final" in lowered:
        return CALCULATED_COLOUR, "FINAL ANSWER"
    return CALCULATED_COLOUR, "CALCULATED EARLIER"


def exact_part(qid: str, letter: str) -> tuple[str, int]:
    """Return the unchanged source question part (wording, indicative marks)."""
    q = BY_ID[qid]
    matches = [(text, marks) for part, text, marks in q["parts"] if part == letter]
    if len(matches) != 1:
        raise KeyError(f"{qid}: original question has no unique part {letter!r}")
    return matches[0]


class PartPrompt(VGroup):
    """A compact card for one active part and its relevant sourced values.

    rows is [(key, label, value, source), ...], where source is 'question',
    '2026 VCAA Data Book', 'earlier result', or 'final answer'.

    The values in this card are informational; visual working stays in the
    main part of the frame. focus(key) returns the actual row for Indicate().
    """

    def __init__(self, qid: str, letter: str, rows: list[tuple[str, str, str, str]],
                 *, left: bool = True, width: float = 4.05,
                 max_height: float = 4.95, y: float = -0.05):
        original, marks = exact_part(qid, letter)
        title = TB(f"{qid}   {letter}.", size=SMALL + 1, color=SYSTEM)
        wording = wrapped(original, size=SMALL - 2, width=width - 0.52, buff=0.06)
        marks_text = T(f"[{marks} mark{'s' if marks != 1 else ''}]", size=SMALL - 5, color=MUTED)
        head = VGroup(title, wording, marks_text).arrange(DOWN, aligned_edge=LEFT, buff=0.10)

        source_header = TB("VALUES FOR THIS PART", size=SMALL - 3, color=TEXT)
        value_rows = VGroup()
        by_key = {}
        for key, label, value, source in rows:
            colour, source_label = _source_style(source)
            name = T(label, size=SMALL - 4, color=TEXT)
            amount = TB(value, size=SMALL - 3, color=colour)
            pair = VGroup(name, amount).arrange(RIGHT, buff=0.12)
            if pair.width > width - 0.51:
                pair.scale((width - 0.51) / pair.width)
            provenance = T(source_label, size=SMALL - 8, color=colour)
            item = VGroup(pair, provenance).arrange(DOWN, aligned_edge=LEFT, buff=0.025)
            by_key[key] = item
            value_rows.add(item)
        if len(value_rows):
            value_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13)

        content = VGroup(head, source_header, value_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        factor = min(1.0, (width - 0.50) / max(content.width, 0.01),
                     (max_height - 0.38) / max(content.height, 0.01))
        if factor < 1.0:
            content.scale(factor)
        border = RoundedRectangle(width=width, height=content.height + 0.40,
                                  corner_radius=0.12, stroke_width=1.4,
                                  stroke_color=FAINT, fill_color=PANEL, fill_opacity=0.97)
        content.move_to(border)
        super().__init__(border, content)
        self._by_key = by_key
        self.question_id, self.part = qid, letter
        self.move_to([(-6.48 + width / 2) if left else (6.48 - width / 2), y, 0])

    def focus(self, key: str):
        return self._by_key[key]


def active_part_ribbon(qid: str, letter: str,
                       rows: list[tuple[str, str, str, str]] | None = None,
                       *, width: float = 12.5, y: float = 2.34,
                       max_height: float = 0.55) -> VGroup:
    """Full-width alternative for scenes whose original diagrams occupy both sides.

    The exact active part wording is shown first; a small selection of inputs
    accompanies it. Scene authors must position diagrams beneath the ribbon.
    """
    original, marks = exact_part(qid, letter)
    heading = TB(f"{qid} {letter}.", size=SMALL - 2, color=SYSTEM)
    wording = T(original, size=SMALL - 3, color=TEXT)
    title = VGroup(heading, wording).arrange(RIGHT, buff=0.20, aligned_edge=DOWN)
    if title.width > width - 0.35:
        title.scale((width - 0.35) / title.width)
    values = VGroup()
    for key, label, value, source in (rows or []):
        colour, source_label = _source_style(source)
        v = T(f"{label}: {value} ({source_label.lower()})", size=SMALL - 7, color=colour)
        values.add(v)
    if len(values):
        values.arrange(RIGHT, buff=0.34)
        if values.width > width - 0.4:
            values.scale((width - 0.4) / values.width)
    elements = [title] + ([values] if len(values) else [])
    body = VGroup(*elements).arrange(DOWN, aligned_edge=LEFT, buff=0.035)
    if body.height > max_height - 0.15:
        body.scale((max_height - 0.15) / body.height)
    background = RoundedRectangle(width=width, height=body.height + 0.14,
                                  corner_radius=0.10, stroke_color=FAINT,
                                  stroke_width=1.1, fill_color=PANEL, fill_opacity=0.97)
    body.move_to(background)
    return VGroup(background, body).move_to([0, y, 0])
