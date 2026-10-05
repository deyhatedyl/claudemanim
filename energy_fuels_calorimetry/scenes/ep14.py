"""
Episode 14 - Exam workshop B: calorimetry and data evaluation (Q27, Q28).
Narration: scripts/ep14.md (beat names must match).
Q27 and Q28 are original practice questions written for this series (labelled on screen; not VCAA questions);
X in Q28 is hypothetical. Plotted points are the Q27 data exactly; the cooling fit is recomputed (np.polyfit).
Every value shown is recomputed in checks/verify_anchors.py (q27, q28, ep14_workshop_values).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (bullets, calorimeter, data_points, linfit, mark_tally, question_card,  # noqa: E402
                               result_box, right_panel, table, temp_axes, title_card, wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, ENERGY_C, EQ_SMALL, FAINT, GOOD, LABEL, LOSS, MASS_C, MOL_C,  # noqa: E402
                          MUTED, PANEL, SMALL, SURR, SYSTEM, TEMP_C, TEXT, UNKNOWN, USEFUL, M, T, TB, chip, header,
                          panel)
from shared.workshop import (WK, X0, XM, attempt_card, blank, boxes_for, mbox, node, number, part_tag,  # noqa: E402
                             requested, tally_text, tick, work)

COOL = [(120, 24.7), (180, 24.6), (240, 24.5), (300, 24.4)]
SLOPE, ICPT = linfit(COOL)
T_MIX = SLOPE * 60 + ICPT
assert abs(T_MIX - 24.8) < 1e-9
BASE = 20.0


def annotated_rows(rows, size=LABEL, y0=2.2, dy=0.82, x_left=-6.2):
    """[(given, annotation, colour, trap)] -> rows of 'given -> annotation' with trap chips."""
    built = VGroup()
    x_arrow = max(T(d, size=size).width for d, *_ in rows) + x_left + 0.3
    for i, (d, a, c, trap) in enumerate(rows):
        y = y0 - i * dy
        dt = T(d, size=size).move_to([0, y, 0]).align_to([x_left, 0, 0], LEFT)
        ar = Arrow([x_arrow, y, 0], [x_arrow + 0.7, y, 0], buff=0, stroke_width=3, color=FAINT,
                   max_tip_length_to_length_ratio=0.35)
        at = T(a, size=size, color=c).move_to([0, y, 0]).align_to([x_arrow + 0.9, 0, 0], LEFT)
        g = VGroup(dt, ar, at)
        if trap:
            g.add(chip("trap", LOSS, size=SMALL - 2).next_to(at, RIGHT, buff=0.25))
        built.add(g)
    return built


def show_row(scene, r, run=0.8):
    anims = [FadeIn(r[0]), GrowArrow(r[1]), FadeIn(r[2], shift=0.1 * RIGHT)]
    if len(r) > 3:
        anims.append(FadeIn(r[3], scale=1.2))
    scene.play(*anims, run_time=run)


def hbar(value, scale, color, y, x_left, label, val_text, h=0.36, lab_size=SMALL + 1):
    r = Rectangle(width=max(0.02, value * scale), height=h, fill_color=color, fill_opacity=0.85, stroke_width=0)
    r.move_to([0, y, 0]).align_to([x_left, 0, 0], LEFT)
    lt = T(label, size=lab_size).next_to(r, LEFT, buff=0.2)
    vt = T(val_text, size=lab_size, color=color).next_to(r, RIGHT, buff=0.15)
    return VGroup(r, lt, vt)


# =====================================================================================
class E14S01_Retrieval(NarratedScene):
    def construct(self):
        tc = title_card(14, "Exam workshop B: calorimetry and data evaluation")
        note = T("Q27 and Q28 are original practice questions written for this series, not VCAA questions.",
                 size=SMALL, color=MUTED).next_to(tc, DOWN, buff=0.45)
        with self.beat("b01") as b:
            self.play(FadeIn(tc, shift=0.2 * UP), run_time=1.5)
            b.until(0.75)
            self.play(FadeIn(note), run_time=0.6)
        with self.beat("b02") as b:
            self.play(FadeOut(tc), FadeOut(note), run_time=0.5)
            h = header("Retrieval check")
            q1 = wrapped("1.  How many moles of HCl are in 25.0 mL of 0.200 mol L⁻¹ HCl(aq)?", size=LABEL + 4, width=12.2)
            q2 = wrapped("2.  A heater runs at 6.00 V and 1.50 A for 2.00 min. How much energy does it supply?",
                         size=LABEL + 4, width=12.2)
            qs = VGroup(q1, q2).arrange(DOWN, buff=1.1, aligned_edge=LEFT).move_to([0, 0.75, 0])
            self.play(FadeIn(h), FadeIn(q1), run_time=0.7)
            b.until(0.4)
            self.play(FadeIn(q2), run_time=0.6)
            self.qs = qs
        with self.beat("b03") as b:
            a1 = M(r"n = 0.200 \times 0.0250\ \text{L} = 0.00500\ \text{mol}", size=EQ_SMALL - 4, color=GOOD)
            a1.next_to(self.qs[0], DOWN, buff=0.25).align_to(self.qs[0], LEFT).shift(0.6 * RIGHT)
            a2 = M(r"E = 6.00 \times 1.50 \times 120\ \text{s} = 1080\ \text{J}", size=EQ_SMALL - 4, color=GOOD)
            a2.next_to(self.qs[1], DOWN, buff=0.25).align_to(self.qs[1], LEFT).shift(0.6 * RIGHT)
            self.play(Write(a1), run_time=0.9)
            b.until(0.5)
            self.play(Write(a2), run_time=0.9)
            u = T("units first, then multiply", size=LABEL, color=UNKNOWN).move_to([0, -2.3, 0])
            b.until(0.85)
            self.play(FadeIn(u), run_time=0.4)


# =====================================================================================
class E14S02_Q27Attempt(NarratedScene):
    PAUSE_LABELS = {"b02": "Pause the video now and attempt every part"}
    TIMER_CORNER = DR

    def construct(self):
        qc = attempt_card("Q27")
        with self.beat("b01"):
            self.play(FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        with self.beat("b02") as b:
            self.play(Indicate(qc[1][0][0], color=UNKNOWN), run_time=0.8)


# =====================================================================================
class E14S03_Annotate(NarratedScene):
    def construct(self):
        h = header("Q27: read and annotate")
        rows = annotated_rows([
            ("5.00 V, 1.20 A, 300 s; 3.00 °C rise", "E = VIt (t in s); CF = E ÷ ΔT", ENERGY_C, False),
            ("125.0 g water in the calibration", "check: CF > 125.0 × 4.18", MUTED, False),
            ("CF applies to the reaction mixture", "q = CF × ΔT, not m c ΔT", UNKNOWN, True),
            ("50.0 mL 1.00 M HCl, 75.0 mL 0.800 M NaOH", "n = cV, V in L; limiting?", UNKNOWN, True),
            ("baseline 20.0 °C; mixing at t = 60 s", "extrapolate back to 60 s", UNKNOWN, True),
            ("cooling readings from 120 s", "linear trend: best line", SURR, False),
        ])
        given = T("given", size=SMALL, color=MUTED).next_to(rows[0][0], UP, buff=0.06).align_to(rows[0][0], LEFT)
        note = T("annotation", size=SMALL, color=MUTED).next_to(rows[0][2], UP, buff=0.06).align_to(rows[0][2], LEFT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(given), FadeIn(note), run_time=0.6)
            show_row(self, rows[0])
            b.until(0.6)
            show_row(self, rows[1])
        with self.beat("b02") as b:
            show_row(self, rows[2])
        with self.beat("b03") as b:
            show_row(self, rows[3])
        with self.beat("b04") as b:
            show_row(self, rows[4])
            b.until(0.5)
            show_row(self, rows[5])
            traps = VGroup(*[SurroundingRectangle(rows[i], color=LOSS, buff=0.08, stroke_width=2) for i in (2, 3, 4)])
            self.play(LaggedStart(*[Create(t) for t in traps], lag_ratio=0.25), run_time=1.0)


# =====================================================================================
class E14S04_Plan(NarratedScene):
    def construct(self):
        h = header("Q27: plan the methods")
        a = node("a", ["E = V × I × t", "CF = E ÷ ΔT", "compare with water alone"], ENERGY_C)
        bb = node("b", ["n = c × V (V in L)", "find the limiting reactant"], MOL_C)
        c = node("c", ["graph: extrapolate", "→ corrected ΔT"], TEMP_C)
        d = node("d", ["q = CF × ΔT", "ΔH = −q ÷ n(limiting)"], UNKNOWN)
        e = node("e", ["precision vs", "accuracy"], SURR)
        f = node("f", ["which reactant", "limits the heat?"], SURR)
        a.move_to([-4.5, 1.75, 0])
        bb.move_to([-4.5, 0.2, 0])
        c.move_to([-4.5, -1.3, 0])
        d.move_to([0.6, 0.2, 0])
        e.move_to([4.7, 0.95, 0])
        f.move_to([4.7, -0.55, 0])
        rl = T("reasoning parts", size=SMALL + 1, color=MUTED).next_to(e, UP, buff=0.2)
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for n_, fr in zip((a, bb, c, d), (0.03, 0.28, 0.5, 0.66)):
                b.until(fr)
                self.play(FadeIn(n_, shift=0.1 * UP), run_time=0.5)
        with self.beat("b02") as b:
            arr = VGroup(*[Arrow(src.get_right(), d.get_left(), buff=0.1, stroke_width=4, color=UNKNOWN,
                                 max_tip_length_to_length_ratio=0.12) for src in (a, bb, c)])
            self.play(LaggedStart(*[GrowArrow(x) for x in arr], lag_ratio=0.25), run_time=1.2)
            b.until(0.5)
            self.play(FadeIn(e), FadeIn(f), FadeIn(rl), run_time=0.7)


# =====================================================================================
class E14S05_PartA(NarratedScene):
    def construct(self):
        h = header("Q27 part a: calibration")
        tl = tally_text("Q27", 0, 14)
        cal = calorimeter(width=2.3, height=2.1, heater=True).move_to([-4.7, 1.2, 0])
        x0 = -2.6
        l1 = work(r"E = 5.00 \times 1.20 \times 300 = 1800\ \text{J}", 1.75, ENERGY_C, x=x0)
        l2 = work(r"\text{CF} = 1800 \div 3.00 = 600\ \text{J}\,{}^{\circ}\text{C}^{-1}", 0.95, UNKNOWN, x=x0)
        b1, b2 = boxes_for(l1), boxes_for(l2)
        with self.beat("b01") as b:
            self.tl = tl
            self.play(FadeIn(h), FadeIn(tl), FadeIn(cal), run_time=0.8)
            self.play(Write(l1), FadeIn(b1), run_time=1.0)
            self.play(tick(b1), Transform(self.tl, tally_text("Q27", 1, 14)), run_time=0.4)
            b.until(0.55)
            self.play(Write(l2), FadeIn(b2), run_time=1.0)
            self.play(tick(b2), Transform(self.tl, tally_text("Q27", 2, 14)), run_time=0.4)
        with self.beat("b02") as b:
            sc = 0.0075
            r1 = hbar(600, sc, UNKNOWN, -0.55, -1.4, "CF (whole calorimeter)", "600 J °C⁻¹")
            r2 = hbar(522.5, sc, SURR, -1.15, -1.4, "water only: 125.0 × 4.18", "522.5 J °C⁻¹")
            self.play(FadeIn(r2), run_time=0.8)
            b.until(0.35)
            self.play(FadeIn(r1), run_time=0.8)
            ok = T("CF > water alone ✓  the cup, thermometer and stirrer absorb energy too", size=SMALL + 1, color=GOOD)
            ok.move_to([0, -1.85, 0])
            b3 = mbox().move_to([XM, -1.85, 0])
            b.until(0.55)
            self.play(FadeIn(ok), FadeIn(b3), run_time=0.6)
            warn = T("CF smaller than the water alone would signal an error", size=SMALL + 1, color=MUTED).move_to([0, -2.42, 0])
            b.until(0.75)
            self.play(FadeIn(warn), tick(b3), Transform(self.tl, tally_text("Q27", 3, 14)), run_time=0.6)


# =====================================================================================
class E14S06_PartB(NarratedScene):
    def construct(self):
        h = header("Q27 part b: the limiting reactant")
        tl = tally_text("Q27", 3, 14)
        eq = M(r"\ce{HCl(aq) + NaOH(aq) -> NaCl(aq) + H2O(l)}", size=EQ_SMALL - 4).move_to([0, 2.15, 0])
        l1 = work(r"n(\ce{HCl}) = 1.00 \times 0.0500\ \text{L} = 0.0500\ \text{mol}", 1.3, MOL_C)
        l2 = work(r"n(\ce{NaOH}) = 0.800 \times 0.0750\ \text{L} = 0.0600\ \text{mol}", 0.6, MOL_C)
        bx = boxes_for(l2)
        with self.beat("b01") as b:
            self.tl = tl
            self.play(FadeIn(h), FadeIn(tl), Write(eq), run_time=1.0)
            b.until(0.1)
            self.play(Write(l1), run_time=1.0)
            b.until(0.55)
            self.play(Write(l2), FadeIn(bx), run_time=1.0)
            self.play(tick(bx), Transform(self.tl, tally_text("Q27", 4, 14)), run_time=0.4)
        with self.beat("b02") as b:
            sc = 55
            r1 = hbar(0.0500, sc, MOL_C, -0.35, -2.2, "HCl", "0.0500 mol")
            r2 = hbar(0.0600, sc, FAINT, -0.95, -2.2, "NaOH", "0.0600 mol")
            self.play(FadeIn(r1), FadeIn(r2), run_time=0.8)
            ratio = T("1 : 1 ratio", size=SMALL + 1, color=MUTED).move_to([4.2, -0.65, 0])
            self.play(FadeIn(ratio), run_time=0.4)
            lim = chip("HCl is limiting", LOSS, size=SMALL + 2)
            left = T("NaOH left over: 0.0100 mol", size=SMALL + 1, color=MUTED)
            water = T("n(H₂O formed) = 0.0500 mol", size=SMALL + 2, color=UNKNOWN)
            VGroup(lim, left, water).arrange(RIGHT, buff=0.5).move_to([0, -1.75, 0])
            b.until(0.2)
            self.play(FadeIn(lim, scale=1.1), run_time=0.5)
            self.play(FadeIn(left), run_time=0.4)
            b.until(0.55)
            self.play(FadeIn(water), run_time=0.5)
            b2 = mbox().move_to([XM, -2.35, 0])
            b.until(0.8)
            self.play(FadeIn(b2), run_time=0.3)
            self.play(tick(b2), Transform(self.tl, tally_text("Q27", 5, 14)), run_time=0.4)


# =====================================================================================
class E14S07_Graph(NarratedScene):
    def construct(self):
        h = header("Q27 part c: correcting the temperature rise")
        pg = temp_axes(x_max=300, x_step=60, y_min=19, y_max=26, width=6.8, height=4.2).move_to([-2.3, 0.0, 0])
        ax = pg.ax
        col = 4.45
        base = Line(ax.c2p(0, BASE), ax.c2p(60, BASE), color=SURR, stroke_width=4)
        bt = T("baseline 20.0 °C (given)", size=SMALL + 1, color=SURR).move_to([4.45, -1.85, 0])
        mix = DashedLine(ax.c2p(60, 19), ax.c2p(60, 26), color=UNKNOWN, stroke_width=2.5)
        mixt = T("mixing, t = 60 s", size=SMALL + 1, color=UNKNOWN).move_to([col, 1.9, 0])
        pts = data_points(ax, COOL)
        src = T("data: practice question Q27", size=SMALL, color=MUTED).move_to([col, -2.35, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), Create(ax), FadeIn(pg.grid), FadeIn(pg[2]), FadeIn(pg[3]), FadeIn(src), run_time=1.2)
            self.play(Create(base), FadeIn(bt), run_time=0.7)
            b.until(0.3)
            self.play(Create(mix), FadeIn(mixt), run_time=0.6)
            b.until(0.45)
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.3), run_time=1.4)
        with self.beat("b02") as b:
            mx = Circle(radius=0.15, color=SYSTEM, stroke_width=3).move_to(pts[0])
            mxt = T("highest reading 24.7 °C", size=SMALL + 1, color=SYSTEM).move_to([col, 1.35, 0])
            self.play(Create(mx), FadeIn(mxt), run_time=0.7)
            fit = Line(ax.c2p(120, SLOPE * 120 + ICPT), ax.c2p(300, SLOPE * 300 + ICPT), color=SURR, stroke_width=4)
            b.until(0.45)
            self.play(Create(fit), run_time=1.0)
            ext = DashedLine(ax.c2p(120, SLOPE * 120 + ICPT), ax.c2p(60, T_MIX), color=SURR, stroke_width=4, dash_length=0.1)
            b.until(0.7)
            self.play(Create(ext), run_time=0.9)
        with self.beat("b03") as b:
            sl = M(r"\text{slope} = -0.1\ {}^{\circ}\text{C per } 60\ \text{s}", size=WK - 6, color=SURR).move_to([col, 0.75, 0])
            self.play(Write(sl), run_time=0.9)
            dia = Square(side_length=0.2, color=UNKNOWN, fill_color=UNKNOWN, fill_opacity=1).rotate(PI / 4).move_to(ax.c2p(60, T_MIX))
            ct = M(r"T(60\ \text{s}) = 24.7 + 0.1 = 24.8\ {}^{\circ}\text{C}", size=WK - 6, color=UNKNOWN).move_to([col, 0.15, 0])
            b.until(0.3)
            self.play(FadeIn(dia, scale=1.6), Write(ct), run_time=1.0)
            cor = DashedVMobject(DoubleArrow(ax.c2p(45, BASE), ax.c2p(45, T_MIX), buff=0, color=UNKNOWN, stroke_width=3,
                                             tip_length=0.15), num_dashes=16)
            rise = M(r"\Delta T = 24.8 - 20.0 = 4.8\ {}^{\circ}\text{C}", size=WK - 4, color=UNKNOWN).move_to([col, -0.55, 0])
            b.until(0.6)
            self.play(Create(cor), Write(rise), run_time=1.0)
            rb = result_box(rise, UNKNOWN)
            mk = T("c: 1 extrapolation · 1 corrected rise", size=SMALL, color=GOOD).move_to([col, -1.3, 0])
            b.until(0.85)
            self.play(Create(rb), FadeIn(mk), run_time=0.6)


# =====================================================================================
class E14S08_PartD(NarratedScene):
    def construct(self):
        h = header("Q27 part d: molar enthalpy")
        tl = tally_text("Q27", 7, 14)
        l1 = work(r"q = \text{CF} \times \Delta T = 600 \times 4.8 = 2880\ \text{J} = 2.880\ \text{kJ}", 1.9, ENERGY_C)
        l2 = work(r"\Delta H = -\frac{2.880\ \text{kJ}}{0.0500\ \text{mol}} = -57.6\ \text{kJ mol}^{-1}", 0.5, UNKNOWN)
        l3 = work(r"\approx -58\ \text{kJ per mol of water formed}", -0.5, UNKNOWN)
        tg = part_tag("d", l1)
        b1, b2 = boxes_for(l1), boxes_for(l2, 2)
        with self.beat("b01") as b:
            self.tl = tl
            self.play(FadeIn(h), FadeIn(tl), FadeIn(tg), run_time=0.5)
            self.play(Write(l1), FadeIn(b1), run_time=1.2)
            b.until(0.75)
            self.play(tick(b1), Transform(self.tl, tally_text("Q27", 8, 14)), run_time=0.4)
        with self.beat("b02") as b:
            nl = T("n(limiting) = n(H₂O) = 0.0500 mol", size=SMALL + 1, color=MOL_C).move_to([0, 1.3, 0]).align_to([X0, 0, 0], LEFT)
            self.play(FadeIn(nl), run_time=0.5)
            self.play(Write(l2), FadeIn(b2), run_time=1.2)
            sign = chip("temperature rose → heat released → ΔH negative", LOSS, size=SMALL + 1).move_to([0, -1.3, 0])
            b.until(0.5)
            self.play(FadeIn(sign), run_time=0.5)
            b.until(0.72)
            self.play(Write(l3), run_time=0.8)
            sf = T("2 significant figures: the corrected rise (4.8 °C) has two", size=SMALL + 1, color=MUTED).move_to([0, -2.0, 0])
            self.play(FadeIn(sf), Create(result_box(l3, UNKNOWN)), run_time=0.6)
        with self.beat("b03") as b:
            self.play(tick(b2), Transform(self.tl, tally_text("Q27", 10, 14)), run_time=0.5)
            mk = T("d: 1 heat · 1 ÷ limiting amount · 1 sign and units", size=SMALL + 1, color=GOOD).move_to([0, -2.5, 0])
            self.play(FadeIn(mk), run_time=0.5)


# =====================================================================================
class E14S09_Wrong(NarratedScene):
    def construct(self):
        h = header("Wrong solutions for Q27")
        sz = EQ_SMALL - 12
        p1 = wrong_panel("÷ n(NaOH)", [M(r"-2.880 \div 0.0600 = -48.0", size=sz)],
                         note="NaOH in excess: not all of it reacted", size=SMALL + 1, width=3.5)
        p2 = wrong_panel("highest reading", [M(r"600 \times 4.7 \div 0.0500 \to -56.4", size=sz)],
                         note="cooling had already begun", size=SMALL + 1, width=3.5)
        p3 = wrong_panel("m c ΔT, no CF", [M(r"125.0 \times 4.18 \times 4.8 = 2508\ \text{J}", size=sz),
                                            M(r"\to -50.2", size=sz)],
                         note="ignores the calorimeter itself", size=SMALL + 1, width=3.5)
        ps = VGroup(p1, p2, p3).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to([0, 1.1, 0])
        nl = NumberLine(x_range=[-60, -45, 5], length=9.0, include_numbers=True, color=TEXT, font_size=22,
                        decimal_number_config=dict(num_decimal_places=0, color=MUTED)).move_to([0, -1.75, 0])
        unit = T("ΔH (kJ mol⁻¹)", size=SMALL, color=MUTED).next_to(nl, RIGHT, buff=0.3)
        good = VGroup(Dot(nl.n2p(-57.6), radius=0.11, color=GOOD),
                      T("−57.6 correct", size=SMALL, color=GOOD)).arrange(DOWN, buff=0.08)
        good[0].move_to(nl.n2p(-57.6) + 0.35 * UP)
        good[1].move_to(nl.n2p(-57.6) + 0.62 * DOWN)

        def wrong_pt(v, n):
            d = Dot(nl.n2p(v) + 0.35 * UP, radius=0.1, color=BAD)
            t = T(f"{n}", size=SMALL, color=BAD).next_to(d, UP, buff=0.08)
            return VGroup(d, t)
        w1, w2, w3 = wrong_pt(-48.0, "1"), wrong_pt(-56.4, "2"), wrong_pt(-50.16, "3")
        for i, p in enumerate(ps):
            p.add(T(str(i + 1), size=SMALL + 2, color=BAD).next_to(p, UP, buff=0.08).align_to(p, LEFT))
        with self.beat("b01") as b:
            self.play(FadeIn(h), Create(nl), FadeIn(unit), FadeIn(good), run_time=0.9)
            b.until(0.2)
            self.play(FadeIn(p1), FadeIn(w1), run_time=0.8)
        with self.beat("b02") as b:
            b.until(0.15)
            self.play(FadeIn(p2), FadeIn(w2), run_time=0.8)
        with self.beat("b03") as b:
            b.until(0.15)
            self.play(FadeIn(p3), FadeIn(w3), run_time=0.8)


# =====================================================================================
class E14S10_PartsEF(NarratedScene):
    def construct(self):
        h = header("Q27 parts e and f")
        tl = tally_text("Q27", 10, 14)
        with self.beat("b01") as b:
            self.tl = tl
            self.play(FadeIn(h), FadeIn(tl), run_time=0.5)
            nl = NumberLine(x_range=[-62, -50, 2], length=6.0, include_numbers=True, color=TEXT, font_size=20,
                            decimal_number_config=dict(num_decimal_places=0, color=MUTED)).move_to([-2.6, 1.0, 0])
            tv = DashedLine(nl.n2p(-60.0) + 0.9 * UP, nl.n2p(-60.0) + 0.15 * DOWN, color=GOOD, stroke_width=3)
            tvt = T("true value (hypothetical)", size=SMALL, color=GOOD).next_to(tv, UP, buff=0.08)
            reps = VGroup(*[Dot(nl.n2p(v) + 0.35 * UP, radius=0.08, color=SYSTEM) for v in (-57.4, -57.7, -57.6, -57.8)])
            self.play(Create(nl), Create(tv), FadeIn(tvt), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in reps], lag_ratio=0.2), run_time=0.8)
            e1 = T("close repeats → precise (repeatable)", size=SMALL + 2, color=SYSTEM)
            e2 = T("not necessarily accurate: a systematic error shifts every repeat", size=SMALL + 2, color=LOSS)
            ee = VGroup(e1, e2).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([0, -0.25, 0]).align_to([X0 - 0.6, 0, 0], LEFT)
            b.until(0.3)
            self.play(FadeIn(e1), run_time=0.5)
            b.until(0.55)
            self.play(FadeIn(e2), run_time=0.5)
            be = VGroup(mbox(), mbox()).arrange(RIGHT, buff=0.1).move_to([XM - 0.28, -0.25, 0])
            b.until(0.85)
            self.play(FadeIn(be), run_time=0.3)
            self.play(tick(be), Transform(self.tl, tally_text("Q27", 12, 14)), run_time=0.4)
        with self.beat("b02") as b:
            f1 = work(r"\text{f: } n(\ce{NaOH}) = 1.60 \times 0.0750 = 0.120\ \text{mol}", -1.15, MOL_C, size=WK - 2, x=X0 - 0.6)
            f2 = work(r"n(\ce{HCl}) = 0.0500\ \text{mol: still limiting} \Rightarrow \text{same } n(\ce{H2O}),\ \text{same heat}",
                      -1.85, UNKNOWN, size=WK - 2, x=X0 - 0.6)
            self.play(Write(f1), run_time=1.0)
            b.until(0.4)
            self.play(Write(f2), run_time=1.2)
            bf = VGroup(mbox(), mbox()).arrange(RIGHT, buff=0.1).move_to([XM - 0.28, -1.85, 0])
            b.until(0.8)
            self.play(FadeIn(bf), run_time=0.3)
            self.play(tick(bf), Transform(self.tl, tally_text("Q27", 14, 14)), run_time=0.4)
        with self.beat("b03") as b:
            self.clear()
            tally = mark_tally([(3, "a: energy, CF, plausibility check"), (2, "b: amounts; limiting reactant"),
                                (2, "c: extrapolation; corrected rise"), (3, "d: heat; ÷ limiting amount; sign and units"),
                                (2, "e: precise, not necessarily accurate"), (2, "f: acid still limiting; same heat")],
                               size=SMALL + 1, width=9.0, title="Q27 indicative marks").move_to([0, 0.15, 0])
            self.play(FadeIn(tally), run_time=1.0)


# =====================================================================================
class E14S11_SpotError(NarratedScene):
    def construct(self):
        h = header("Checkpoint: spot the error")
        sub = T("three lines from different students' answers to Q27 and Q28 · one mistake in each", size=SMALL + 1, color=MUTED)
        sub.next_to(h, DOWN, buff=0.25).align_to(h, LEFT)
        ys = [1.45, 0.05, -1.35]
        lines = [work(r"n(\ce{HCl}) = 1.00 \times 50.0 = 50.0\ \text{mol}", ys[0], x=-4.9),
                 work(r"\Delta H = +57.6\ \text{kJ mol}^{-1}", ys[1], x=-4.9),
                 work(r"n(\text{X}) = 960 \div 24.0 = 40.0\ \text{mol}", ys[2], x=-4.9)]
        nums = VGroup(*[number(i + 1, l) for i, l in enumerate(lines)])
        fixes = [work(r"1.00 \times 0.0500\ \text{L} = 0.0500\ \text{mol}\quad(\text{mL} \to \text{L})", ys[0] - 0.62,
                      GOOD, size=WK - 4, x=-4.9),
                 work(r"\text{heat released} \Rightarrow \Delta H = -57.6\ \text{kJ mol}^{-1}", ys[1] - 0.62,
                      GOOD, size=WK - 4, x=-4.9),
                 work(r"0.960\ \text{kJ} \div 24.0\ \text{kJ mol}^{-1} = 0.0400\ \text{mol}\quad(\text{J} \to \text{kJ})",
                      ys[2] - 0.62, GOOD, size=WK - 4, x=-4.9)]
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(sub), run_time=0.5)
            for i in range(3):
                self.play(FadeIn(nums[i]), Write(lines[i]), run_time=0.8)
        with self.beat("b02") as b:
            self.play(Create(SurroundingRectangle(lines[0][0][12:16], color=BAD, buff=0.06)), run_time=0.5)
            b.until(0.3)
            self.play(FadeIn(fixes[0], shift=0.1 * DOWN), run_time=0.8)
        with self.beat("b03") as b:
            self.play(Create(SurroundingRectangle(lines[1][0][3:4], color=BAD, buff=0.06)), run_time=0.5)
            b.until(0.3)
            self.play(FadeIn(fixes[1], shift=0.1 * DOWN), run_time=0.8)
        with self.beat("b04") as b:
            self.play(Create(SurroundingRectangle(lines[2][0][5:8], color=BAD, buff=0.06)), run_time=0.5)
            b.until(0.25)
            self.play(FadeIn(fixes[2], shift=0.1 * DOWN), run_time=0.9)
            b.until(0.55)
            warn = M(r"\text{uncorrected: } 40.0\ \text{mol} \times 80.0 = 3200\ \text{g of X in a } 4.00\ \text{g sample (impossible)}",
                     size=WK - 4, color=BAD).move_to([0, -2.45, 0])
            self.play(FadeIn(warn), run_time=0.7)


# =====================================================================================
class E14S12_Q28Attempt(NarratedScene):
    PAUSE_LABELS = {"b02": "Pause the video now and attempt every part"}
    TIMER_CORNER = DR

    def construct(self):
        qc = attempt_card("Q28")
        with self.beat("b01"):
            self.play(FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        with self.beat("b02") as b:
            self.play(Indicate(qc[1][0][0], color=UNKNOWN), run_time=0.8)


# =====================================================================================
def chain(items, colors, y, x_left=-6.1, gap=0.95, size=LABEL):
    """Values in boxes joined by arrows carrying the operation on each step."""
    boxes = VGroup()
    for (val, op), c in zip(items, colors):
        t = TB(val, size=size, color=c)
        r = RoundedRectangle(width=t.width + 0.36, height=0.6, corner_radius=0.1, stroke_color=c, stroke_width=2.5,
                             fill_color=PANEL, fill_opacity=1)
        boxes.add(VGroup(r, t.move_to(r)))
    boxes.arrange(RIGHT, buff=gap).move_to([0, y, 0]).align_to([x_left, 0, 0], LEFT)
    arrows = VGroup()
    for i in range(len(items) - 1):
        a = Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.06, stroke_width=3, color=FAINT,
                  max_tip_length_to_length_ratio=0.25)
        op = T(items[i + 1][1], size=SMALL - 2, color=MUTED).move_to([a.get_center()[0], boxes.get_top()[1] + 0.2, 0])
        arrows.add(VGroup(a, op))
    return boxes, arrows


class E14S13_PartsAC(NarratedScene):
    def construct(self):
        h = header("Q28 parts a to c")
        tl = tally_text("Q28", 0, 12)
        items = [("3.20 °C", ""), ("960 J", "× 300"), ("0.960 kJ", "÷ 1000"), ("0.0400 mol", "÷ 24.0"),
                 ("3.20 g X", "× 80.0"), ("80.0%", "÷ 4.00")]
        cols = [TEMP_C, ENERGY_C, ENERGY_C, MOL_C, MASS_C, UNKNOWN]
        boxes, arrows = chain(items, cols, 1.75, x_left=-6.35, gap=0.85, size=SMALL + 1)
        tags = VGroup(T("a", size=SMALL, color=SYSTEM).next_to(boxes[1], DOWN, buff=0.15),
                      T("b", size=SMALL, color=SYSTEM).next_to(boxes[3], DOWN, buff=0.15),
                      T("b", size=SMALL, color=SYSTEM).next_to(boxes[5], DOWN, buff=0.15))
        with self.beat("b01") as b:
            self.tl = tl
            self.play(FadeIn(h), FadeIn(tl), FadeIn(boxes[0]), run_time=0.6)
            self.play(GrowArrow(arrows[0][0]), FadeIn(arrows[0][1]), FadeIn(boxes[1]), FadeIn(tags[0]), run_time=0.8)
            l1 = work(r"\text{a: } q = 300 \times 3.20 = 960\ \text{J}", 0.75, ENERGY_C, x=X0 - 0.6)
            self.play(Write(l1), run_time=0.8)
            b.until(0.8)
            self.play(Transform(self.tl, tally_text("Q28", 2, 12)), run_time=0.4)
        with self.beat("b02") as b:
            for i in (1, 2):
                self.play(GrowArrow(arrows[i][0]), FadeIn(arrows[i][1]), FadeIn(boxes[i + 1]), run_time=0.7)
                b.until(0.3 if i == 1 else 0.5)
            self.play(FadeIn(tags[1]), run_time=0.3)
            l2 = work(r"\text{b: } n(\text{X}) = 0.960\ \text{kJ} \div 24.0\ \text{kJ mol}^{-1} = 0.0400\ \text{mol}", 0.1,
                      MOL_C, x=X0 - 0.6)
            self.play(Write(l2), run_time=1.0)
        with self.beat("b03") as b:
            for i in (3, 4):
                self.play(GrowArrow(arrows[i][0]), FadeIn(arrows[i][1]), FadeIn(boxes[i + 1]), run_time=0.7)
                b.until(0.35 if i == 3 else 0.6)
            l3 = work(r"m(\text{X}) = 0.0400 \times 80.0 = 3.20\ \text{g};\quad \frac{3.20}{4.00} \times 100\% = 80.0\%",
                      -0.7, MASS_C, x=X0 - 0.6)
            self.play(Write(l3), FadeIn(tags[2]), run_time=1.0)
            b.until(0.85)
            self.play(Transform(self.tl, tally_text("Q28", 6, 12)), run_time=0.4)
        with self.beat("b04") as b:
            g = NumberLine(x_range=[70, 100, 5], length=7.0, include_numbers=True, color=TEXT, font_size=20,
                           decimal_number_config=dict(num_decimal_places=0, color=MUTED)).move_to([-0.6, -2.15, 0])
            pct = T("% X", size=SMALL, color=MUTED).next_to(g, RIGHT, buff=0.25)
            meas = VGroup(Dot(g.n2p(80.0) + 0.3 * UP, radius=0.1, color=GOOD))
            meas.add(T("measured 80.0%", size=SMALL, color=GOOD).next_to(meas[0], UP, buff=0.06))
            claim = DashedLine(g.n2p(95.0) + 0.75 * UP, g.n2p(95.0) + 0.1 * DOWN, color=UNKNOWN, stroke_width=3)
            ct = T("claim 95.0%", size=SMALL, color=UNKNOWN).next_to(claim, UP, buff=0.05)
            self.play(Create(g), FadeIn(pct), FadeIn(meas), Create(claim), FadeIn(ct), run_time=1.0)
            v = T("c: not supported", size=SMALL + 2, color=LOSS).move_to([5.0, -1.45, 0])
            b.until(0.5)
            self.play(FadeIn(v), Transform(self.tl, tally_text("Q28", 7, 12)), run_time=0.5)


# =====================================================================================
class E14S14_PartsDE(NarratedScene):
    def construct(self):
        h = header("Q28 parts d and e: a calibration error")
        tl = tally_text("Q28", 7, 12)
        rows = [[blank(), "CF (J °C⁻¹)", "q (J)", "n(X) (mol)", "m(X) (g)", "% X"],
                ["correct", "300", "960", "0.0400", "3.20", "80.0"],
                ["wrong CF", "360", "1152", "0.0480", "3.84", "96.0"]]
        tb = table(rows, [1.9, 2.0, 1.6, 2.0, 1.8, 1.5], size=SMALL + 2, row_h=0.6).move_to([0, 1.45, 0])
        grid, cells = tb[0], tb[1]
        wrong_cells = VGroup(*cells[13:18])
        for c in wrong_cells:
            c.set_color(BAD)
        cells[12].set_color(BAD)
        with self.beat("b01") as b:
            self.tl = tl
            self.play(FadeIn(h), FadeIn(tl), Create(grid), FadeIn(VGroup(*cells[:12])), run_time=1.0)
            self.play(FadeIn(cells[12]), FadeIn(cells[13]), run_time=0.5)
            for i, fr in zip(range(14, 18), (0.3, 0.5, 0.68, 0.85)):
                b.until(fr)
                self.play(FadeIn(cells[i], shift=0.05 * DOWN), run_time=0.4)
        with self.beat("b02") as b:
            ups = VGroup(*[Arrow(cells[i].get_bottom() + 0.05 * DOWN + 0.25 * DOWN, cells[i].get_bottom() + 0.05 * DOWN,
                                 buff=0, color=BAD, stroke_width=4, max_tip_length_to_length_ratio=0.45).next_to(cells[i], RIGHT, buff=0.08)
                         for i in range(14, 18)])
            msg = T("CF too large → every quantity calculated from it too large", size=SMALL + 2, color=BAD).move_to([0, 0.05, 0])
            self.play(LaggedStart(*[GrowArrow(u) for u in ups], lag_ratio=0.15), FadeIn(msg), run_time=1.0)
            g = NumberLine(x_range=[70, 100, 5], length=7.0, include_numbers=True, color=TEXT, font_size=20,
                           decimal_number_config=dict(num_decimal_places=0, color=MUTED)).move_to([-0.6, -1.4, 0])
            claim = DashedLine(g.n2p(95.0) + 0.75 * UP, g.n2p(95.0) + 0.1 * DOWN, color=UNKNOWN, stroke_width=3)
            ct = T("claim 95.0%", size=SMALL, color=UNKNOWN).next_to(claim, UP, buff=0.05).shift(0.45 * LEFT)
            m1 = Dot(g.n2p(80.0) + 0.3 * UP, radius=0.1, color=GOOD)
            m2 = Dot(g.n2p(96.0) + 0.3 * UP, radius=0.1, color=BAD)
            l2 = T("96.0%: appears to meet the claim", size=SMALL, color=BAD).next_to(g, DOWN, buff=0.15).align_to(g.n2p(96.0), RIGHT).shift(0.6 * RIGHT)
            b.until(0.4)
            self.play(Create(g), Create(claim), FadeIn(ct), FadeIn(m1), run_time=0.8)
            biased = m1.copy().set_color(BAD)
            self.add(biased)
            self.play(biased.animate.move_to(m2), FadeIn(l2), run_time=1.6)
            self.remove(biased)
            self.add(m2)
            bd = VGroup(mbox(), mbox()).arrange(RIGHT, buff=0.1).move_to([XM - 0.28, 0.05, 0])
            b.until(0.85)
            self.play(FadeIn(bd), run_time=0.3)
            self.play(tick(bd), Transform(self.tl, tally_text("Q28", 9, 12)), run_time=0.4)
            self.g, self.m2 = g, m2
        with self.beat("b03") as b:
            reps = VGroup(*[Dot(self.g.n2p(v) + 0.3 * UP, radius=0.07, color=BAD) for v in (95.8, 96.2, 95.9, 96.1)])
            self.play(LaggedStart(*[FadeIn(r, scale=1.5) for r in reps], lag_ratio=0.2), run_time=0.8)
            e = T("e: repeating with the same wrong CF repeats the bias: precise, still wrong", size=SMALL + 2, color=LOSS)
            e.move_to([0, -2.45, 0])
            b.until(0.5)
            self.play(FadeIn(e), Transform(self.tl, tally_text("Q28", 10, 12)), run_time=0.6)


# =====================================================================================
class E14S15_PartF(NarratedScene):
    def construct(self):
        h = header("Q28 part f: moisture")
        tl = tally_text("Q28", 10, 12)
        sc = 2.0
        x_left = -2.8

        def bar(parts, y, label):
            g = VGroup()
            x = x_left
            for w, c, t in parts:
                r = Rectangle(width=w * sc, height=0.55, fill_color=c, fill_opacity=0.85, stroke_color=BG, stroke_width=2)
                r.move_to([x + w * sc / 2, y, 0])
                g.add(VGroup(r, T(t, size=SMALL, color=BG, weight="BOLD").move_to(r)))
                x += w * sc
            lab = T(label, size=SMALL + 1).next_to(g, LEFT, buff=0.25)
            return VGroup(g, lab)
        dry = bar([(3.20, SYSTEM, "X"), (0.80, FAINT, "filler")], 1.5, "dry 4.00 g sample")
        wet = bar([(2.85, SYSTEM, "less X"), (0.70, FAINT, "filler"), (0.45, SURR, "water")], 0.6, "moist 4.00 g sample")
        ill = T("schematic proportions", size=SMALL - 2, color=MUTED).next_to(wet, DOWN, buff=0.12).align_to(wet[0], RIGHT)
        with self.beat("b01") as b:
            self.tl = tl
            self.play(FadeIn(h), FadeIn(tl), FadeIn(dry), run_time=0.7)
            b.until(0.45)
            self.play(FadeIn(wet), FadeIn(ill), run_time=0.9)
        with self.beat("b02") as b:
            steps = ["less X", "less heat", "smaller ΔT", "lower % X"]
            chips = VGroup(*[chip(s, c, size=SMALL + 2) for s, c in zip(steps, (SYSTEM, ENERGY_C, TEMP_C, LOSS))])
            chips.arrange(RIGHT, buff=0.7).move_to([0, -0.85, 0])
            arr = VGroup(*[Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.08, stroke_width=3, color=FAINT,
                                 max_tip_length_to_length_ratio=0.3) for i in range(3)])
            self.play(FadeIn(chips[0]), run_time=0.4)
            for i, fr in enumerate((0.2, 0.35, 0.5)):
                b.until(fr)
                self.play(GrowArrow(arr[i]), FadeIn(chips[i + 1]), run_time=0.5)
            bf = VGroup(mbox(), mbox()).arrange(RIGHT, buff=0.1).move_to([XM - 0.28, -0.85, 0])
            b.until(0.75)
            self.play(FadeIn(bf), run_time=0.3)
            self.play(tick(bf), Transform(self.tl, tally_text("Q28", 12, 12)), run_time=0.4)
        with self.beat("b03") as b:
            self.clear()
            tally = mark_tally([(2, "a: q = CF × ΔT = 960 J"), (4, "b: kJ conversion; n(X); m(X); % X"),
                                (1, "c: 80.0% does not support 95.0%"), (2, "d: 96.0% with CF = 360; bias direction"),
                                (1, "e: repeating keeps the bias"), (2, "f: less active mass; lower result")],
                               size=SMALL + 1, width=9.0, title="Q28 indicative marks").move_to([0, 0.15, 0])
            self.play(FadeIn(tally), run_time=1.0)


# =====================================================================================
class E14S16_WhichWay(NarratedScene):
    def construct(self):
        h = header("Checkpoint: which way does the result move?")
        sub = T("for the Q28 test: is the calculated % X too high or too low?", size=SMALL + 1, color=MUTED)
        sub.next_to(h, DOWN, buff=0.25).align_to(h, LEFT)
        ys = [1.35, 0.15, -1.05]
        changes = [T("1.  heat lost to the surroundings during the test", size=LABEL + 1),
                   T("2.  sample mass recorded as 3.80 g (really 4.00 g)", size=LABEL + 1),
                   T("3.  calibration factor used is too small", size=LABEL + 1)]
        for c, y in zip(changes, ys):
            c.move_to([0, y, 0]).align_to([-6.2, 0, 0], LEFT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(sub), run_time=0.5)
            for i, fr in enumerate((0.2, 0.45, 0.72)):
                b.until(fr)
                self.play(FadeIn(changes[i]), run_time=0.5)
        with self.beat("b02") as b:
            res = [("↓ too low", "smaller ΔT → less q → less X", LOSS),
                   ("↑ too high", "3.20 ÷ 3.80 × 100% = 84.2%", BAD),
                   ("↓ too low", "q = CF × ΔT too small", LOSS)]
            for i, ((a, why, c), fr) in enumerate(zip(res, (0.0, 0.3, 0.62))):
                b.until(fr)
                g = VGroup(TB(a, size=LABEL + 1, color=c), T(why, size=SMALL + 1, color=MUTED)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
                g.move_to([0, ys[i], 0]).align_to([2.4, 0, 0], LEFT)
                self.play(FadeIn(g, shift=0.1 * LEFT), run_time=0.6)
            tip = T("follow each change through q → n → m → %", size=LABEL, color=UNKNOWN).move_to([0, -2.2, 0])
            b.until(0.85)
            self.play(FadeIn(tip), run_time=0.5)


# =====================================================================================
class E14S17_Methods(NarratedScene):
    def construct(self):
        h = header("Choosing a method")
        left = [["Given or asked", "Relationship"],
                ["mass of a substance", "n = m ÷ M"],
                ["gas volume at SLC", "n = V ÷ 24.8 L mol⁻¹"],
                ["solution", "n = c × V  (V in L)"],
                ["energy released by a fuel", "E = n × |ΔH|"],
                ["heating water", "q = m c ΔT"],
                ["electrical calibration", "E = V × I × t;  CF = E ÷ ΔT"],
                ["calibrated calorimeter", "q = CF × ΔT"]]
        right = [["Asked", "Relationship"],
                 ["molar enthalpy", "ΔH = −q ÷ n(limiting); negative if heat is released"],
                 ["efficiency", "useful output ÷ energy input × 100%"],
                 ["input needed for a target output", "useful output ÷ efficiency"],
                 ["comparing fuels", "state the basis: per mol, per g or per useful kJ"]]
        tl = table(left, [2.75, 3.45], size=SMALL, pad=0.11)
        tr = table(right, [2.45, 3.75], size=SMALL, pad=0.11)
        tl.move_to([-3.25, 0, 0]).align_to([0, 2.35, 0], UP)
        tr.move_to([3.3, 0, 0]).align_to([0, 2.35, 0], UP)
        lg, lc = tl[0], tl[1]
        rg, rc = tr[0], tr[1]

        def rows_of(cells, rr):
            return VGroup(*[cells[i] for r in rr for i in (2 * r, 2 * r + 1)])

        def hl(cells, rr):
            return SurroundingRectangle(rows_of(cells, rr), color=UNKNOWN, buff=0.08, stroke_width=2.5)
        with self.beat("b01") as b:
            self.play(FadeIn(h), Create(lg), FadeIn(lc[0]), FadeIn(lc[1]), run_time=0.8)
            self.play(FadeIn(rows_of(lc, range(1, 4)), lag_ratio=0.2), run_time=1.0)
            self.box = hl(lc, range(1, 4))
            self.play(Create(self.box), run_time=0.5)
        with self.beat("b02") as b:
            self.play(FadeIn(rows_of(lc, range(4, 8)), lag_ratio=0.2), run_time=1.2)
            self.play(Transform(self.box, hl(lc, range(4, 8))), run_time=0.5)
        with self.beat("b03") as b:
            self.play(Create(rg), FadeIn(rc[0]), FadeIn(rc[1]), run_time=0.6)
            self.play(FadeIn(rows_of(rc, range(1, 5)), lag_ratio=0.2), run_time=1.2)
            self.play(Transform(self.box, hl(rc, range(1, 5))), run_time=0.5)


# =====================================================================================
class E14S18_Diagnostic(NarratedScene):
    ROUND1 = [("n(NaOH) = 0.800 × 75.0 = 60.0 mol", "✗  mL → L: 0.0600 mol"),
              ("A 90% CH₄ mixture: use its total amount as n(CH₄)", "✗  mixture vs component"),
              ("60.0 L of air contains 60.0 L of O₂", "✗  air is 21.0% O₂"),
              ("ΔH: divide q by the amount of the excess reactant", "✗  use the limiting reactant"),
              ("q = 600 J °C⁻¹ × 4.8 °C = 2880 kJ", "✗  J, not kJ"),
              ("ΔH for an exothermic reaction is negative", "✓  correct")]
    ROUND2 = [("The highest reading is the corrected temperature", "✗  extrapolate the cooling line"),
              ("Repeats that agree closely must be accurate", "✗  precision ≠ accuracy"),
              ("A catalyst increases the energy released per mole", "✗  same ΔH, lower Ea"),
              ("Efficiency = useful output ÷ energy input × 100%", "✓  correct"),
              ("Less CO₂ per mol of fuel → less per useful kJ", "✗  basis; efficiency matters"),
              ("A renewable fuel is always sustainable", "✗  renewable ≠ sustainable")]

    def items(self, data, start):
        st, an = VGroup(), VGroup()
        for i, (s, a) in enumerate(data):
            y = 2.1 - i * 0.78
            t = T(f"{start + i}.  {s}", size=LABEL).move_to([0, y, 0]).align_to([-6.3, 0, 0], LEFT)
            c = GOOD if a.startswith("✓") else BAD
            r = T(a, size=SMALL + 1, color=c).move_to([0, y, 0]).align_to([2.05, 0, 0], LEFT)
            st.add(t)
            an.add(r)
        return st, an

    def construct(self):
        h = header("Diagnostic: the central traps")
        s1, a1 = self.items(self.ROUND1, 1)
        s2, a2 = self.items(self.ROUND2, 7)
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(s) for s in s1], lag_ratio=0.2), run_time=1.6)
        with self.beat("b02") as b:
            for i, fr in enumerate((0.0, 0.2, 0.36, 0.5, 0.7, 0.88)):
                b.until(fr)
                self.play(FadeIn(a1[i], shift=0.1 * LEFT), run_time=0.4)
        with self.beat("b03") as b:
            self.play(FadeOut(s1), FadeOut(a1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(s) for s in s2], lag_ratio=0.2), run_time=1.6)
        with self.beat("b04") as b:
            for i, fr in enumerate((0.0, 0.17, 0.33, 0.47, 0.6, 0.76)):
                b.until(fr)
                self.play(FadeIn(a2[i], shift=0.1 * LEFT), run_time=0.4)
            log = T("add any you missed to your error log", size=LABEL, color=UNKNOWN).move_to([0, -2.45, 0])
            b.until(0.92)
            self.play(FadeIn(log), run_time=0.4)


# =====================================================================================
class E14S19_Close(NarratedScene):
    def construct(self):
        h = header("Your toolkit")
        cards = [("Moles and units", "n = m/M, V/24.8, cV; convert first", MOL_C),
                 ("Energy from reactions", "ΔH sign; E = n|ΔH|; bonds; profiles", ENERGY_C),
                 ("Calorimetry", "calibration, q = CF × ΔT, graph correction", TEMP_C),
                 ("Fair comparisons", "state the basis; lifecycle; sustainability", USEFUL)]
        built = VGroup()
        for t, s, c in cards:
            tt = TB(t, size=LABEL + 2, color=c)
            ss = wrapped(s, size=SMALL + 1, width=5.0, color=TEXT)
            g = VGroup(tt, ss).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            r = RoundedRectangle(width=5.8, height=g.height + 0.45, corner_radius=0.14, stroke_color=c, stroke_width=2.5,
                                 fill_color=PANEL, fill_opacity=1)
            g.move_to(r).align_to(r, LEFT).shift(0.3 * RIGHT)
            built.add(VGroup(r, g))
        built.arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.3)).move_to([0, 1.08, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for i, fr in enumerate((0.25, 0.42, 0.6, 0.78)):
                b.until(fr)
                self.play(FadeIn(built[i], shift=0.1 * UP), run_time=0.5)
        with self.beat("b02") as b:
            res = VGroup(*[T(s, size=LABEL, color=c) for s, c in
                           (("worksheet: attempt every practice question again", TEXT),
                            ("worked solutions: steps, indicative marks, traps", TEXT),
                            ("formula and method sheet", TEXT),
                            ("your error log", UNKNOWN))]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            res.move_to([0, -1.5, 0]).align_to([-5.9, 0, 0], LEFT)
            self.play(FadeIn(res, lag_ratio=0.2), run_time=1.2)
            end = T("End of series · good luck", size=LABEL, color=MUTED).move_to([4.3, -2.35, 0])
            b.until(0.85)
            self.play(FadeIn(end), run_time=0.5)


EPISODE_SCENES = ["E14S01_Retrieval", "E14S02_Q27Attempt", "E14S03_Annotate", "E14S04_Plan", "E14S05_PartA",
                  "E14S06_PartB", "E14S07_Graph", "E14S08_PartD", "E14S09_Wrong", "E14S10_PartsEF",
                  "E14S11_SpotError", "E14S12_Q28Attempt", "E14S13_PartsAC", "E14S14_PartsDE", "E14S15_PartF",
                  "E14S16_WhichWay", "E14S17_Methods", "E14S18_Diagnostic", "E14S19_Close"]
