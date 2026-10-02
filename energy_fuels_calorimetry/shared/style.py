"""
Visual conventions for the whole series.

Measured on 1080p frames (see checks/font_metrics.md): Manim Text font_size f gives a cap
height of about 1.34·f px and an em of about 1.875·f px. MathTex font_size f gives a cap height
of about 0.96·f px.

  BODY  (Text 28)   cap ≈ 37 px, em ≈ 52 px      main explanatory text
  LABEL (Text 22)   cap ≈ 29 px, em ≈ 41 px      supporting labels
  SMALL (Text 20)   cap ≈ 27 px, em ≈ 37 px      minimum size used anywhere
  EQ    (MathTex 46) cap ≈ 44 px                  main equations

Layout: content stays inside x ∈ [-6.6, 6.6] and y ∈ [SAFE_BOTTOM, 3.1]. The strip below
SAFE_BOTTOM (bottom ~15% of the frame) is reserved for subtitles.

Colour roles (always reinforced by a label, arrow or line style, never colour alone):
  SYSTEM   reacting chemicals / the system              solid orange outlines
  SURR     calorimeter / surroundings                   solid blue outlines
  USEFUL   useful energy                                solid green arrows
  LOSS     energy lost                                  dashed red arrows
  UNKNOWN  the quantity being found                     yellow, boxed, with a "?" tag
  Quantity chips: amount (mol), mass (g), volume (L), concentration (mol L⁻¹), energy (J/kJ)
"""
from __future__ import annotations

from manim import (DL, DOWN, DR, LEFT, RIGHT, UL, UP, BackgroundRectangle, DashedLine, Line, MarkupText, MathTex,
                   RoundedRectangle, SurroundingRectangle, Tex, TexTemplate, Text, VGroup)

FONT = "Noto Sans"

BG = "#0E1117"
PANEL = "#1A202B"
TEXT = "#ECEFF4"
MUTED = "#AAB2C0"
FAINT = "#5C6573"

SYSTEM = "#FF9F43"
SURR = "#54A0FF"
USEFUL = "#2ECC71"
LOSS = "#FF6B6B"
UNKNOWN = "#FFE066"
GOOD = "#7BE495"
BAD = "#FF7B7B"

MOL_C = "#C39BD3"     # amount, mol
MASS_C = "#48C9B0"    # mass, g
VOL_C = "#7FB3F5"     # volume, L
CONC_C = "#F5A6C8"    # concentration, mol L^-1
ENERGY_C = "#F8C471"  # energy, J / kJ
TEMP_C = "#F1948A"    # temperature, °C

# atoms (CPK-like, but readable on a dark background; every atom also carries its symbol)
ATOM_COLORS = {"C": "#5D6D7E", "H": "#F4F6F7", "O": "#E74C3C", "N": "#3498DB", "Cl": "#2ECC71",
               "Na": "#AF7AC5", "S": "#F4D03F"}

BODY, LABEL, SMALL, HEAD = 28, 22, 20, 34
EQ, EQ_SMALL = 46, 38
SAFE_BOTTOM = -2.75
X_LIMIT = 6.6
TOP_Y = 3.1

TEMPLATE = TexTemplate()
TEMPLATE.add_to_preamble(r"\usepackage{amsmath}\usepackage{amssymb}\usepackage[version=4]{mhchem}"
                         r"\usepackage{siunitx}\sisetup{per-mode=power,inter-unit-product=\,}")


def T(s: str, size: int = BODY, color: str = TEXT, weight: str = "NORMAL", **kw) -> Text:
    """Plain text. size is Manim Text font_size (see module docstring for pixel equivalents).
    'ΔH_c' (as written in the question bank) is drawn with a real subscript c."""
    if "H_c" in s:
        mk = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("H_c", "H<sub>c</sub>")
        return MarkupText(mk, font=FONT, font_size=size, color=color, weight=weight, **kw)
    return Text(s, font=FONT, font_size=size, color=color, weight=weight, **kw)


def TB(s: str, size: int = BODY, color: str = TEXT, **kw) -> Text:
    return T(s, size=size, color=color, weight="BOLD", **kw)


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


def header(title: str, kicker: str | None = None) -> VGroup:
    """Scene title in the top-left with an underline; optional small kicker (e.g. 'Episode 01')."""
    t = TB(title, size=HEAD)
    parts = [t]
    if kicker:
        k = T(kicker, size=SMALL, color=MUTED)
        parts = [k, t]
    g = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    g.to_corner(UL, buff=0.38)
    ul = Line(t.get_corner(DL), t.get_corner(DR), color=SYSTEM, stroke_width=3).shift(0.1 * DOWN)
    g.add(ul)
    return g


def panel(mob, color: str = FAINT, buff: float = 0.25, fill: str = PANEL, opacity: float = 0.92,
          corner: float = 0.18, stroke: float = 2) -> RoundedRectangle:
    r = RoundedRectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff, corner_radius=corner,
                         stroke_color=color, stroke_width=stroke, fill_color=fill, fill_opacity=opacity)
    r.move_to(mob)
    return r


def boxed(mob, color: str = UNKNOWN, buff: float = 0.14) -> SurroundingRectangle:
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08, stroke_width=3)


def chip(label: str, color: str, size: int = SMALL) -> VGroup:
    """Small rounded tag such as [mol] or [g]."""
    t = T(label, size=size, color=BG, weight="BOLD")
    r = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.2, corner_radius=0.12,
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
