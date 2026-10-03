"""
Visual conventions for the whole series.

Inter text and equation letters/numerals are used throughout. Font sizes are Manim units;
the previous Noto Sans/Computer Modern measurements do not describe this font setup.
Render and inspect actual frames before treating the reference match as verified.

Layout: content stays inside x ∈ [-6.6, 6.6] and y ∈ [SAFE_BOTTOM, CONTENT_TOP]. Two rows
above the content hold the section metadata and centered title. The strip below SAFE_BOTTOM
(bottom ~15% of the frame) is reserved for subtitles.

Colour roles (always reinforced by a label, arrow or line style, never colour alone):
  SYSTEM   reacting chemicals / the system              solid orange outlines
  SURR     calorimeter / surroundings                   solid blue outlines
  USEFUL   useful energy                                solid green arrows
  LOSS     energy lost                                  dashed red arrows
  UNKNOWN  the quantity being found                     yellow, boxed, with a "?" tag
  Quantity chips: amount (mol), mass (g), volume (L), concentration (mol L⁻¹), energy (J/kJ)
"""
from __future__ import annotations

import re

from manim import (DL, DOWN, DR, LEFT, RIGHT, UL, UP, UR, BackgroundRectangle, DashedLine, Line, MarkupText, MathTex,
                   RoundedRectangle, SurroundingRectangle, Tex, TexTemplate, Text, VGroup)

FONT = "Inter"
Text.set_default(font=FONT)

BG = "#0C111E"
PANEL = "#141C2C"
TEXT = "#EEF1F8"
MUTED = "#8B98AB"
FAINT = "#566276"

SYSTEM = "#FF9566"
SURR = "#59B6F4"
USEFUL = "#64DA9A"
LOSS = "#FF5578"
UNKNOWN = "#FFCE60"
GOOD = "#64DA9A"
BAD = "#FF5578"

MOL_C = "#B38BFF"     # amount, mol
MASS_C = "#49D4AC"    # mass, g
VOL_C = SURR          # volume, L
CONC_C = "#F173A5"    # concentration, mol L^-1
ENERGY_C = UNKNOWN    # energy, J / kJ
TEMP_C = SYSTEM       # temperature, °C

# atoms (CPK-like, but readable on a dark background; every atom also carries its symbol)
ATOM_COLORS = {"C": "#5D6D7E", "H": "#F4F6F7", "O": "#E74C3C", "N": "#3498DB", "Cl": "#2ECC71",
               "Na": "#AF7AC5", "S": "#F4D03F"}

BODY, LABEL, SMALL, HEAD = 28, 22, 20, 36
EQ, EQ_SMALL = 46, 38
SAFE_BOTTOM = -2.75
X_LIMIT = 6.6
TOP_Y = 3.1
CONTENT_TOP = 2.55
HEADER_GAP = 0.12
_SECTION_ID = ""
_SECTION_TITLE = "VCE Chemistry"


def set_section(scene_id: str, title: str):
    global _SECTION_ID, _SECTION_TITLE
    _SECTION_ID, _SECTION_TITLE = scene_id, title

TEMPLATE = TexTemplate(
    tex_compiler="xelatex", output_format=".xdv",
    preamble=r"\usepackage{amsmath}\usepackage{amssymb}\usepackage[no-math]{fontspec}"
             r"\setmainfont{Inter}\setsansfont{Inter}"
             r"\usepackage{mathastext}\usepackage[version=4]{mhchem}"
             r"\usepackage{siunitx}\sisetup{per-mode=power,inter-unit-product=\,}",
)


def T(s: str, size: int = BODY, color: str = TEXT, weight: str = "NORMAL", **kw) -> Text:
    """Plain text. size is Manim Text font_size.
    'ΔH_c' (as written in the question bank) is drawn with a real subscript c."""
    if weight == "NORMAL" and color not in (TEXT, MUTED, FAINT, BG):
        weight = "SEMIBOLD"
    if "H_c" in s:
        mk = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("H_c", "H<sub>c</sub>")
        return MarkupText(mk, font=FONT, font_size=size, color=color, weight=weight, **kw)
    return Text(s, font=FONT, font_size=size, color=color, weight=weight, **kw)


def TB(s: str, size: int = BODY, color: str = TEXT, **kw) -> Text:
    return T(s, size=size, color=color, weight="SEMIBOLD", **kw)


def M(*s: str, size: int = EQ, color: str = TEXT, **kw) -> MathTex:
    """Display maths (amsmath, mhchem \\ce{}, siunitx \\si{} available)."""
    return MathTex(*s, font_size=size, color=color, tex_template=TEMPLATE, **kw)


def TX(s: str, size: int = EQ, color: str = TEXT, **kw) -> Tex:
    return Tex(s, font_size=size, color=color, tex_template=TEMPLATE, **kw)


def para(lines: list[str] | str, size: int = BODY, color: str = TEXT, buff: float = 0.16,
         align=LEFT) -> VGroup:
    """Several lines of text stacked and left-aligned."""
    if isinstance(lines, str):
        lines = lines.split("\n")
    g = VGroup(*[T(l, size=size, color=color) for l in lines])
    g.arrange(DOWN, buff=buff, aligned_edge=align)
    return g


def header(title: str, kicker: str | None = None, color: str | None = None) -> VGroup:
    """Two fixed rows: the kicker shares the top row with the Asked pill.

    The title has its own full-width row. Its underline is always above the
    content area, including for long titles. This removes the old coupling
    between title height, question-card placement and the top-right reminder.
    """
    color = color or (SYSTEM if title.startswith("Practice") or re.match(r"Q\d+", title)
                      else GOOD if title == "Recap" else TEXT)
    t = TB(title, size=HEAD, color=color)
    if t.width > 12.8:
        t.scale(12.8 / t.width)
    t.move_to([0, 3.03, 0])
    section = re.match(r"E(\d+)S(\d+)", _SECTION_ID)
    num = f"{int(section[1])} · {int(section[2])}" if section else "VCE"
    n = TB(num, size=18, color=SYSTEM).move_to([-6.62, 3.57, 0], aligned_edge=LEFT)
    k = T((kicker or _SECTION_TITLE).upper(), size=15, color=MUTED)
    if k.width > 5.7:
        k.scale(5.7 / k.width)
    k.move_to([-5.87, 3.57, 0], aligned_edge=LEFT)
    ul = Line([-6.62, 3.32, 0], [-6.08, 3.32, 0], color=SYSTEM, stroke_width=1.2)
    g = VGroup(n, k, t, ul)
    g.layout_role = "header"
    return g


def fit_content(mob, max_width: float = 12.9, max_height: float | None = None):
    """Fit a complete component as a unit, preserving its internal layout."""
    max_height = max_height or (CONTENT_TOP - SAFE_BOTTOM - 0.16)
    factor = min(1.0, max_width / max(mob.width, 1e-9), max_height / max(mob.height, 1e-9))
    if factor < 1.0:
        mob.scale(factor)
    return mob


def asked_pill(text: str) -> VGroup:
    """One reserved top-right row, separate from the title and the kicker."""
    c = chip("Asked", UNKNOWN)
    t = T(text, size=SMALL + 2, color=UNKNOWN)
    g = VGroup(c, t).arrange(RIGHT, buff=0.15)
    fit_content(g, max_width=6.3, max_height=0.32)
    g.to_corner(UR, buff=0.25)
    g.layout_role = "header-pill"
    return g


def panel(mob, color: str = FAINT, buff: float = 0.25, fill: str = PANEL, opacity: float = 0.92,
          corner: float = 0.12, stroke: float = 1.2) -> RoundedRectangle:
    r = RoundedRectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff, corner_radius=corner,
                         stroke_color=color, stroke_width=stroke, fill_color=fill, fill_opacity=opacity)
    r.move_to(mob)
    return r


def boxed(mob, color: str = UNKNOWN, buff: float = 0.14) -> SurroundingRectangle:
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08, stroke_width=3)


def chip(label: str, color: str, size: int = SMALL) -> VGroup:
    """Small rounded tag such as [mol] or [g]."""
    t = T(label, size=size, color=BG, weight="BOLD")
    r = RoundedRectangle(width=t.width + 0.30, height=t.height + 0.15, corner_radius=0.13,
                         stroke_width=0, fill_color=color, fill_opacity=1)
    r.move_to(t)
    return VGroup(r, t)


def unknown_tag(mob, text: str = "?") -> VGroup:
    """Mark the current unknown: yellow box plus a '?' tag."""
    b = boxed(mob, UNKNOWN)
    tag = chip(text, UNKNOWN, size=SMALL).next_to(b, UP, buff=0.06).align_to(b, RIGHT)
    return VGroup(b, tag)


def dashed_arrow(start, end, color=LOSS, **kw):
    from manim import Arrow, DashedVMobject
    a = Arrow(start, end, color=color, buff=0.05, **kw)
    return DashedVMobject(a, num_dashes=12)


def safe_check(mob, name: str = "") -> None:
    """Raise if a mobject strays into the subtitle strip or off the sides (layout QA)."""
    if mob.get_bottom()[1] < SAFE_BOTTOM - 1e-3:
        raise ValueError(f"{name or mob}: bottom {mob.get_bottom()[1]:.2f} below caption-safe line")
    if mob.get_left()[0] < -X_LIMIT - 0.3 or mob.get_right()[0] > X_LIMIT + 0.3:
        raise ValueError(f"{name or mob}: outside horizontal margins")
