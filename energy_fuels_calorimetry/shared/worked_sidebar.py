"""Persistent question and data provenance panel for narrated worked examples.

Questions stay in view while the derivation runs. Each quantity is explicitly
labelled as supplied by the question, taken from the 2026 data book, or carried
forward from a previous calculation. The panel is deliberately passive so it
does not alter narration beat durations. Scenes can animate rows with
`Indicate(sidebar.focus("key"))` at the narrated word or calculation.
"""
from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, RoundedRectangle, VGroup

from .components import wrapped
from .style import (
    BG, FAINT, GOOD, LABEL, MUTED, PANEL, SMALL, SURR, SYSTEM, TEXT,
    UNKNOWN, T, TB, fit_content,
)


SOURCE_COLOURS = {
    "question": SURR,
    "2026 data book": UNKNOWN,
    "earlier result": GOOD,
}


class WorkedQuestionSidebar(VGroup):
    """Compact, reusable left/right panel pinned beside working.

    `givens` entries are (key, label, value, provenance). Do not label a
    question-supplied rounded enthalpy as a current data-book value.
    """

    def __init__(self, qid: str, question: str, givens: list[tuple[str, str, str, str]],
                 asked: str, *, left: bool = True, width: float = 3.80,
                 max_height: float = 5.12):
        heading = TB(f"{qid}  •  QUESTION", size=SMALL, color=SYSTEM)
        short_question = wrapped(question, size=SMALL - 3, width=width - 0.45, buff=0.045)
        given_heading = TB("GIVEN / SOURCE", size=SMALL - 2, color=TEXT)
        body_rows = VGroup()
        keyed_rows = {}
        for key, label, value, provenance in givens:
            col = SOURCE_COLOURS.get(provenance, MUTED)
            title = T(label, size=SMALL - 4, color=TEXT)
            datum = TB(value, size=SMALL - 2, color=col)
            top = VGroup(title, datum).arrange(RIGHT, buff=0.13)
            src = T(f"from: {provenance}", size=SMALL - 7, color=col)
            entry = VGroup(top, src).arrange(DOWN, aligned_edge=LEFT, buff=0.018)
            body_rows.add(entry)
            keyed_rows[key] = entry
        body_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.115)
        ask_head = TB("FIND / CALCULATE", size=SMALL - 2, color=UNKNOWN)
        ask_text = wrapped(asked, size=SMALL - 3, width=width - 0.45, buff=0.045)

        contents = VGroup(
            heading, short_question, given_heading, body_rows, ask_head, ask_text
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fit_content(contents, max_width=width - 0.42, max_height=max_height - 0.38)
        back = RoundedRectangle(
            width=width, height=contents.height + 0.40,
            corner_radius=0.14, stroke_color=FAINT, stroke_width=1.5,
            fill_color=PANEL, fill_opacity=0.98,
        )
        contents.move_to(back)
        super().__init__(back, contents)
        self._keyed_rows = keyed_rows
        x_center = (-6.48 + width / 2) if left else (6.48 - width / 2)
        self.move_to([x_center, -0.06, 0])

    def focus(self, key: str):
        """Return the live row mobject so a scene can highlight it during speech."""
        return self._keyed_rows[key]

    def show_calculated(self, label: str, value: str):
        """Use this label on worked lines for new results (green / calculated)."""
        return VGroup(T(label, size=SMALL - 4, color=GOOD),
                      TB(value, size=SMALL - 2, color=GOOD)).arrange(RIGHT, buff=0.14)
