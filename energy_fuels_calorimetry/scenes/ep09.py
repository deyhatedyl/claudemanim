"""
Episode 09 - Why calorimeters need calibration.
Narration: scripts/ep09.md (beat names must match).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (bullets, calorimeter, mark_tally, question_card, result_box, right_panel,  # noqa: E402
                               title_card, wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, ENERGY_C, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, LOSS, MASS_C,  # noqa: E402
                          MOL_C, MUTED, PANEL, SMALL, SURR, SYSTEM, TEMP_C, TEXT, UNKNOWN, USEFUL, M, T, TB,
                          chip, header, panel)

APP = "#95A5A6"


def requested(text: str) -> VGroup:
    c = chip("Asked", UNKNOWN)
    t = T(text, size=SMALL + 2, color=UNKNOWN)
    return VGroup(c, t).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.4)


def meter(letter, color):
    c = Circle(radius=0.32, color=color, stroke_width=3, fill_color=BG, fill_opacity=1)
    return VGroup(c, TB(letter, size=LABEL, color=color).move_to(c))


def cf_stack(water_jc, app_jc, scale=0.0045, width=1.6, x=0.0, y_base=-2.0, show_total=True):
    """Vertical stack: water block (m c) + apparatus block (C_app)."""
    wb = Rectangle(width=width, height=water_jc * scale, fill_color=SURR, fill_opacity=0.7, stroke_color=TEXT, stroke_width=1.5)
    wb.move_to([x, y_base + water_jc * scale / 2, 0])
    ab = Rectangle(width=width, height=max(app_jc * scale, 0.02), fill_color=APP, fill_opacity=0.8, stroke_color=TEXT, stroke_width=1.5)
    ab.next_to(wb, UP, buff=0)
    wl = T(f"water: {water_jc:g}", size=SMALL + 1, color=SURR).next_to(wb, RIGHT, buff=0.2)
    al = T(f"apparatus: {app_jc:g}", size=SMALL + 1, color=APP).next_to(ab, RIGHT, buff=0.2)
    g = VGroup(wb, ab, wl, al)
    if show_total:
        tl = T(f"CF = {water_jc + app_jc:g} J °C⁻¹", size=LABEL, color=UNKNOWN).next_to(ab, UP, buff=0.15)
        g.add(tl)
    return g


# =====================================================================================
class E09S01_Retrieval(NarratedScene):
    def construct(self):
        tc = title_card(9, "Why calorimeters need calibration")
        with self.beat("b01"):
            self.play(FadeIn(tc, shift=0.2 * UP), run_time=1.5)
        with self.beat("b02") as b:
            self.play(FadeOut(tc), run_time=0.5)
            h = header("Retrieval check")
            q = T("Energy to warm 120.0 g of water by 4.00 °C?", size=BODY).move_to([0, 1.2, 0])
            self.play(FadeIn(h), FadeIn(q), run_time=0.8)
            self.q = q
        with self.beat("b03") as b:
            a = M(r"q = m c \Delta T = 120.0 \times 4.18 \times 4.00 = 2006.4\ \text{J}", size=EQ_SMALL, color=GOOD).next_to(self.q, DOWN, buff=0.5)
            self.play(Write(a), run_time=1.4)
            n = T("close to, but not the same as, what a real calorimeter needs", size=LABEL, color=MUTED).next_to(a, DOWN, buff=0.4)
            b.until(0.6)
            self.play(FadeIn(n), run_time=0.6)


# =====================================================================================
class E09S02_MoreThanWater(NarratedScene):
    def construct(self):
        h = header("More than the water gets heated")
        cal = calorimeter(width=3.4, height=2.8, heater=True).move_to([-3.6, -0.1, 0])
        labs = VGroup(T("insulated cup + lid", size=SMALL + 1, color=SURR).next_to(cal.cup, DOWN, buff=0.15),
                      T("heater", size=SMALL + 1, color=SYSTEM).next_to(cal.heater, UP, buff=0.05).shift(0.6 * RIGHT + 0.3 * UP),
                      T("stirrer", size=SMALL + 1, color=MUTED).next_to(cal.stirrer, UP, buff=0.05),
                      T("probe", size=SMALL + 1, color=TEMP_C).next_to(cal.thermo, UP, buff=0.05))
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(cal), run_time=1.0)
            self.play(FadeIn(labs), run_time=0.8)
        src = Dot([0.6, 0.6, 0], radius=0.01)
        a1 = Arrow([0.2, 0.9, 0], [2.4, 1.6, 0], buff=0, color=SURR, stroke_width=6)
        a2 = Arrow([0.2, 0.5, 0], [2.4, -0.2, 0], buff=0, color=APP, stroke_width=6)
        ein = Arrow([-1.6, 0.7, 0], [0.2, 0.7, 0], buff=0, color=ENERGY_C, stroke_width=7)
        eint = T("energy in", size=LABEL, color=ENERGY_C).next_to(ein, UP, buff=0.1)
        t1 = T("warms the water", size=LABEL, color=SURR).next_to(a1, RIGHT, buff=0.15)
        t2 = wrapped("warms the cup, probe, stirrer and heater", size=LABEL, width=3.9, color=APP).next_to(a2, RIGHT, buff=0.15)
        with self.beat("b02") as b:
            self.play(GrowArrow(ein), FadeIn(eint), run_time=0.7)
            self.play(GrowArrow(a1), FadeIn(t1), run_time=0.7)
            b.until(0.4)
            self.play(GrowArrow(a2), FadeIn(t2), run_time=0.8)
            self.split = VGroup(ein, eint, a1, a2, t1, t2)
        with self.beat("b03") as b:
            d = VGroup(TB("Calibration factor, CF", size=BODY, color=UNKNOWN),
                       wrapped("energy needed to raise the temperature of the calorimeter and its contents by 1 °C", size=LABEL, width=6.4),
                       M(r"\text{units: } \text{J}\ {}^{\circ}\text{C}^{-1}", size=EQ_SMALL - 4)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            dp = panel(d, color=UNKNOWN)
            VGroup(dp, d).move_to([3.2, -1.65, 0])
            self.play(FadeIn(dp), FadeIn(d), run_time=1.0)
            self.dg = VGroup(dp, d)
        with self.beat("b04") as b:
            w = T("belongs to this calorimeter with these contents", size=LABEL + 2, color=UNKNOWN).move_to([0, 2.5, 0])
            self.play(FadeIn(w), run_time=0.8)


# =====================================================================================
def bomb_calorimeter(w: float = 3.0, h: float = 3.0) -> VGroup:
    """Schematic bomb calorimeter: insulated jacket, water bath, sealed steel bomb with sample and O2,
    ignition wires, stirrer and thermometer. Parts: .jacket .water .bomb .sample .wires .stirrer .thermo"""
    jacket = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=SURR, stroke_width=3,
                              fill_color=PANEL, fill_opacity=1)
    water = Rectangle(width=w - 0.35, height=h - 0.75, stroke_width=0, fill_color="#2E5C8A", fill_opacity=0.75)
    water.align_to(jacket, DOWN).shift(0.17 * UP)
    bomb = RoundedRectangle(width=1.05, height=1.45, corner_radius=0.14, stroke_color="#BFC9CA", stroke_width=4,
                            fill_color="#3B4652", fill_opacity=1).move_to(water).shift(0.25 * DOWN + 0.2 * LEFT)
    sample = Rectangle(width=0.42, height=0.14, stroke_color=SYSTEM, stroke_width=2, fill_color=SYSTEM,
                       fill_opacity=0.9).move_to(bomb.get_bottom() + 0.32 * UP)
    o2 = T("O₂", size=SMALL, color=TEXT).move_to(bomb).shift(0.25 * UP + 0.3 * LEFT)
    w1 = Line(bomb.get_top() + 0.18 * LEFT + 0.95 * UP, sample.get_top() + 0.12 * LEFT + 0.08 * UP, color=SYSTEM,
              stroke_width=2.5)
    w2 = Line(bomb.get_top() + 0.18 * RIGHT + 0.95 * UP, sample.get_top() + 0.12 * RIGHT + 0.08 * UP, color=SYSTEM,
              stroke_width=2.5)
    stir = VGroup(Line(water.get_top() + 1.0 * RIGHT + 0.6 * UP, water.get_bottom() + 1.0 * RIGHT + 0.35 * UP,
                       color=TEXT, stroke_width=2.5),
                  Line(LEFT * 0.22, RIGHT * 0.22, color=TEXT, stroke_width=3).move_to(water.get_bottom() + 1.0 * RIGHT
                                                                                    + 0.35 * UP))
    thermo = VGroup(RoundedRectangle(width=0.14, height=h * 0.75, corner_radius=0.07, stroke_color=TEXT,
                                     stroke_width=2, fill_color=BG, fill_opacity=1),
                    Circle(radius=0.1, stroke_color=TEXT, stroke_width=2, fill_color=TEMP_C, fill_opacity=1))
    thermo[0].move_to(water.get_center() + 0.78 * LEFT * (w / 3.0) - 0.6 * RIGHT + 0.55 * UP)
    thermo[0].set_x(water.get_left()[0] + 0.32)
    thermo[1].move_to(thermo[0].get_bottom())
    g = VGroup(jacket, water, bomb, sample, o2, w1, w2, stir, thermo)
    g.jacket, g.water, g.bomb, g.sample, g.wires, g.stirrer, g.thermo = jacket, water, bomb, sample, VGroup(w1, w2), stir, thermo
    g.o2 = o2
    return g


class E09S03_Kinds(NarratedScene):
    def construct(self):
        h = header("Two kinds of calorimeter")
        sol = calorimeter(width=2.5, height=2.3).move_to([-4.3, 0.95, 0])
        st = TB("solution calorimeter", size=LABEL + 1, color=SURR).next_to(sol, DOWN, buff=0.3)
        su = T("reactions in solution", size=SMALL, color=MUTED).next_to(st, DOWN, buff=0.1)
        bc = bomb_calorimeter(3.0, 3.0).move_to([1.3, 0.85, 0])
        bt = TB("bomb calorimeter", size=LABEL + 1, color=SYSTEM).next_to(bc, DOWN, buff=0.3)
        bu = T("combustion of fuels and foods", size=SMALL, color=MUTED).next_to(bt, DOWN, buff=0.1)
        lx = 3.35

        def lab(text, target, y):
            t = T(text, size=SMALL + 1, color=TEXT).move_to([0, y, 0]).align_to([lx + 0.15, 0, 0], LEFT)
            a = Line(t.get_left() + 0.08 * LEFT, target, color=MUTED, stroke_width=1.5)
            return VGroup(a, t)
        labels = [lab("sealed steel bomb", bc.bomb.get_right(), 0.65),
                  lab("excess O₂", bc.o2.get_right() + 0.1 * RIGHT, 1.15),
                  lab("ignition wire", bc.wires[1].point_from_proportion(0.3), 1.85),
                  lab("measured water", bc.water.get_right() + 0.6 * DOWN + 0.05 * LEFT, -0.15),
                  lab("insulated jacket", bc.jacket.get_right() + 1.1 * DOWN, -0.65)]
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            self.play(FadeIn(sol), run_time=0.8)
            self.play(FadeIn(st), FadeIn(su), run_time=0.6)
        with self.beat("b02") as b:
            self.play(FadeIn(bc.jacket), FadeIn(bc.water), run_time=0.6)
            self.play(FadeIn(bc.bomb), FadeIn(bc.sample), FadeIn(bc.o2), run_time=0.6)
            self.play(FadeIn(labels[0]), FadeIn(labels[1]), FadeIn(bt), FadeIn(bu), run_time=0.6)
            b.until(0.4)
            self.play(Create(bc.wires), FadeIn(labels[2]), run_time=0.7)
            self.play(bc.sample.animate.set_fill(LOSS), Flash(bc.sample, color=SYSTEM, line_length=0.15), run_time=0.7)
            b.until(0.65)
            self.play(FadeIn(bc.stirrer), FadeIn(bc.thermo), FadeIn(labels[3]), FadeIn(labels[4]), run_time=0.8)
        with self.beat("b03") as b:
            pros = T("sealed and insulated: complete combustion, little heat lost", size=SMALL + 1, color=GOOD)
            pros.move_to([0, -1.95, 0])
            self.play(FadeIn(pros), run_time=0.6)
            both = chip("both need a calibration factor: q = CF × ΔT", UNKNOWN, size=SMALL + 2).move_to([0, -2.5, 0])
            b.until(0.65)
            self.play(FadeIn(both), run_time=0.5)
            self.pros = pros
        with self.beat("b04") as b:
            errs = T("open cup or can: heat escapes; open flame: may burn incompletely", size=SMALL + 1, color=LOSS)
            errs.move_to(self.pros)
            self.play(FadeOut(self.pros), FadeIn(errs), run_time=0.7)


# =====================================================================================
class E09S04_EVIt(NarratedScene):
    def construct(self):
        h = header("Electrical calibration")
        cal = calorimeter(width=2.6, height=2.2, heater=True).move_to([-4.6, -0.3, 0])
        ps = RoundedRectangle(width=1.6, height=0.9, corner_radius=0.1, color=TEXT, stroke_width=2.5).move_to([-1.6, 1.9, 0])
        pst = T("power supply", size=SMALL, color=MUTED).next_to(ps, UP, buff=0.08)
        vm = meter("V", UNKNOWN).move_to([-1.6, 0.4, 0])
        am = meter("A", SURR).move_to([-3.1, 1.9, 0])
        top_l, top_r = cal.heater[1][0].get_end(), cal.heater[1][1].get_end()
        wires = VGroup(Line(ps.get_left(), am.get_right(), color=TEXT, stroke_width=2.5),
                       Line(am.get_left(), [top_l[0], 1.9, 0], color=TEXT, stroke_width=2.5),
                       Line([top_l[0], 1.9, 0], top_l, color=TEXT, stroke_width=2.5),
                       Line(ps.get_bottom(), [-1.6, 1.0, 0], color=TEXT, stroke_width=2.5),
                       Line([-1.6, -0.2, 0], [-1.6, -1.6, 0], color=TEXT, stroke_width=2.5),
                       Line([-1.6, -1.6, 0], [top_r[0] + 0.6, -1.6, 0], color=TEXT, stroke_width=2.5),
                       Line([top_r[0] + 0.6, -1.6, 0], [top_r[0] + 0.6, top_r[1], 0], color=TEXT, stroke_width=2.5),
                       Line([top_r[0] + 0.6, top_r[1], 0], top_r, color=TEXT, stroke_width=2.5))
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(cal), run_time=0.8)
            self.play(FadeIn(ps), FadeIn(pst), Create(wires), FadeIn(am), FadeIn(vm), run_time=1.2)
            sch = T("schematic", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
            self.play(FadeIn(sch), run_time=0.3)
        f = M(r"E", "=", r"V", r"\,I\,", r"t", size=EQ + 8).move_to([3.6, 1.6, 0])
        f[2].set_color(UNKNOWN)
        f[3].set_color(SURR)
        f[4].set_color(TEMP_C)
        u = M(r"\text{J} = \text{V} \times \text{A} \times \text{s}", size=EQ_SMALL).next_to(f, DOWN, buff=0.35)
        u2 = T("V × A = W = J per second", size=SMALL + 1, color=MUTED).next_to(u, DOWN, buff=0.15)
        with self.beat("b02") as b:
            self.play(Write(f), run_time=1.0)
            self.play(Indicate(vm), Indicate(am), run_time=0.8)
            b.until(0.55)
            self.play(Write(u), FadeIn(u2), run_time=1.0)
        with self.beat("b03") as b:
            tbox = VGroup(T("4 min = 4 × 60 = 240 s", size=LABEL + 2, color=TEMP_C),
                          T("using 4 instead of 240: E is 60 × too small", size=LABEL, color=BAD)).arrange(DOWN, buff=0.15)
            tbox.move_to([3.6, -0.75, 0])
            self.play(FadeIn(tbox[0]), run_time=0.7)
            b.until(0.5)
            self.play(FadeIn(tbox[1]), run_time=0.6)
            self.tbox = tbox
        with self.beat("b04") as b:
            cf = M(r"CF = \frac{E}{\Delta T}", r"\quad (\text{J}\ {}^{\circ}\text{C}^{-1})", size=EQ).move_to([3.6, -2.0, 0])
            cf[0].set_color(UNKNOWN)
            self.play(FadeOut(self.tbox[1]), Write(cf), run_time=1.0)


# =====================================================================================
class E09S05_Stack(NarratedScene):
    def construct(self):
        h = header("Stacking heat capacities")
        st = cf_stack(501.6, 38.4, scale=0.0042, width=1.3, x=-5.3, y_base=-2.3, show_total=False)
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            self.play(GrowFromEdge(st[0], DOWN), FadeIn(st[2]), run_time=1.0)
            b.until(0.5)
            self.play(GrowFromEdge(st[1], DOWN), FadeIn(st[3]), run_time=0.8)
        f = M(r"CF", "=", r"m_{\text{water}}\,c_{\text{water}}", "+", r"C_{\text{apparatus}}", size=EQ).move_to([2.4, 2.0, 0])
        f[0].set_color(UNKNOWN)
        f[2].set_color(SURR)
        f[4].set_color(APP)
        with self.beat("b02") as b:
            self.play(Write(f), run_time=1.2)
            ass = wrapped("model: the parts add, and their heat capacities stay constant over a small temperature range",
                          size=LABEL, width=6.6, color=MUTED).next_to(f, DOWN, buff=0.3)
            b.until(0.5)
            self.play(FadeIn(ass), run_time=0.8)
            self.ass = ass
        with self.beat("b03") as b:
            y = st[0].get_top()[1]
            lb = DashedLine([st[0].get_left()[0] - 0.25, y, 0], [st[0].get_right()[0] + 0.25, y, 0], color=UNKNOWN, stroke_width=4)
            lbt = wrapped("dashed: water alone = lower bound", size=SMALL + 1, width=2.6, color=UNKNOWN).next_to(st[2], DOWN, buff=0.25).align_to(st[2], LEFT)
            self.play(Create(lb), FadeIn(lbt), run_time=0.8)
            ineq = M(r"C_{\text{apparatus}} > 0 \;\Rightarrow\; CF > m_{\text{water}}\,c_{\text{water}}", size=EQ_SMALL, color=UNKNOWN)
            ineq.move_to([2.4, 0.1, 0])
            b.until(0.45)
            self.play(FadeOut(self.ass), Write(ineq), run_time=1.2)
        with self.beat("b04") as b:
            w = wrapped("CF below the water's m c means a measurement or calculation went wrong", size=LABEL + 2, width=6.6, color=BAD)
            w.move_to([2.4, -1.3, 0])
            self.play(FadeIn(w), run_time=0.8)


# =====================================================================================
class E09S06_Q17a(NarratedScene):
    def construct(self):
        h = header("Practice Q17")
        qc = question_card("Q17").move_to([0, 0.3, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        req = requested("CF, apparatus share, later heat")
        colL = -6.3

        def L(tex, y, col=TEXT, s=EQ_SMALL - 6):
            return M(tex, size=s, color=col).move_to([0, y, 0]).align_to([colL, 0, 0], LEFT)
        l1 = L(r"E = VIt = 6.00 \times 1.50 \times 240 = 2160\ \text{J}", 2.2, ENERGY_C)
        l2 = L(r"CF = \frac{2160\ \text{J}}{4.00\ {}^{\circ}\text{C}} = 540\ \text{J}\ {}^{\circ}\text{C}^{-1}", 1.35, UNKNOWN)
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(req), run_time=0.5)
            self.play(Write(l1), run_time=1.2)
            b.until(0.5)
            self.play(Write(l2), run_time=1.2)
        st = cf_stack(501.6, 38.4, scale=0.0055, x=3.0, y_base=-2.3)
        with self.beat("b03") as b:
            l3 = L(r"m c = 120.0 \times 4.18 = 501.6\ \text{J}\ {}^{\circ}\text{C}^{-1} < 540 \ \checkmark", 0.45, SURR)
            self.play(Write(l3), run_time=1.2)
            self.play(GrowFromEdge(st[0], DOWN), FadeIn(st[2]), run_time=0.8)
        with self.beat("b04") as b:
            l4 = L(r"C_{\text{app}} = 540 - 501.6 = 38.4\ \text{J}\ {}^{\circ}\text{C}^{-1}", -0.4, APP)
            self.play(Write(l4), run_time=1.0)
            self.play(GrowFromEdge(st[1], DOWN), FadeIn(st[3]), FadeIn(st[4]), run_time=0.8)
        with self.beat("b05") as b:
            l5 = L(r"q = CF \times \Delta T = 540 \times 5.60 = 3024\ \text{J} \approx 3.02\ \text{kJ}", -1.35, GOOD)
            n = T("same calorimeter, same contents (matched)", size=SMALL + 1, color=MUTED).next_to(l5, DOWN, buff=0.15).align_to(l5, LEFT)
            self.play(Write(l5), run_time=1.2)
            b.until(0.55)
            self.play(FadeIn(n), run_time=0.5)


# =====================================================================================
class E09S07_Contents(NarratedScene):
    def construct(self):
        h = header("Changing the contents changes CF")
        q = T("Q17 d: 150.0 g water, same apparatus. Keep CF = 540?", size=LABEL + 2, color=UNKNOWN).move_to([0, 2.45, 0])
        before = cf_stack(501.6, 38.4, scale=0.0034, width=1.0, x=-5.9, y_base=-2.2)
        bl = T("120.0 g water", size=SMALL + 1).next_to(before[0], DOWN, buff=0.1)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(before), FadeIn(bl), run_time=1.0)
            self.play(FadeIn(q), run_time=0.7)
        after = cf_stack(627.0, 38.4, scale=0.0034, width=1.0, x=-2.6, y_base=-2.2)
        al = T("150.0 g water", size=SMALL + 1).next_to(after[0], DOWN, buff=0.1)
        calc = VGroup(M(r"150.0 \times 4.18 = 627.0", size=EQ_SMALL - 6, color=SURR),
                      M(r"627.0 + 38.4 = 665.4 \approx 665\ \text{J}\ {}^{\circ}\text{C}^{-1}", size=EQ_SMALL - 6, color=UNKNOWN)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        calc.move_to([3.6, 1.6, 0])
        with self.beat("b02") as b:
            self.play(TransformFromCopy(before[0], after[0]), FadeIn(al), FadeIn(after[2]), run_time=1.0)
            self.play(Write(calc[0]), run_time=0.8)
            b.until(0.45)
            self.play(TransformFromCopy(before[1], after[1]), FadeIn(after[3]), run_time=0.8)
            b.until(0.7)
            self.play(Write(calc[1]), FadeIn(after[4]), run_time=1.0)
        with self.beat("b03") as b:
            tally = mark_tally([(2, "E and CF"), (1, "apparatus share"), (1, "later heat"), (2, "new CF")], width=3.4,
                               size=SMALL + 1, title="Q17 marks").move_to([2.0, -0.85, 0])
            trap = wrong_panel("Trap", [wrapped("keeping 540 after the contents change", size=SMALL + 1, width=2.4)],
                               width=2.6, size=SMALL + 1).move_to([5.3, -0.85, 0])
            self.play(FadeIn(tally), run_time=0.7)
            b.until(0.5)
            self.play(FadeIn(trap), run_time=0.7)
            self.tt = VGroup(tally, trap)
        with self.beat("b04") as b:
            self.play(FadeOut(self.tt), run_time=0.5)
            w = wrapped("Reuse a CF only for a matched calorimeter and contents", size=LABEL, width=5.6, color=UNKNOWN)
            wp = panel(w, color=UNKNOWN, buff=0.15)
            VGroup(wp, w).move_to([3.5, -0.6, 0])
            self.play(FadeIn(wp), FadeIn(w), run_time=0.8)


# =====================================================================================
class E09S08_Chemical(NarratedScene):
    def construct(self):
        h = header("Calibrating with a reaction of known ΔH")
        x0 = -6.0

        def L(tex, y, col=TEXT, s=EQ_SMALL - 6):
            return M(tex, size=s, color=col).move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
        with self.beat("b01") as b:
            reqs = VGroup(chip("ΔH known accurately", ENERGY_C, size=SMALL + 1),
                          chip("known amount reacts", MOL_C, size=SMALL + 1),
                          chip("same calorimeter and contents", SURR, size=SMALL + 1)).arrange(RIGHT, buff=0.3)
            reqs.move_to([0, 2.2, 0])
            self.play(FadeIn(h), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(r) for r in reqs], lag_ratio=0.3), run_time=1.3)
        with self.beat("b02") as b:
            hyp = T("hypothetical reference reaction: 50.0 kJ released per mol", size=LABEL, color=MUTED)
            hyp.move_to([0, 1.35, 0]).align_to([x0, 0, 0], LEFT)
            l1 = L(r"q = 0.0400\ \text{mol} \times 50.0\ \text{kJ mol}^{-1} = 2.00\ \text{kJ} = 2000\ \text{J}", 0.75, ENERGY_C)
            l2 = L(r"\text{CF} = \frac{2000\ \text{J}}{3.70\ {}^{\circ}\text{C}} = 541\ \text{J}\,{}^{\circ}\text{C}^{-1}", -0.15, UNKNOWN)
            self.play(FadeIn(hyp), run_time=0.5)
            b.until(0.2)
            self.play(Write(l1), run_time=1.2)
            b.until(0.62)
            self.play(Write(l2), run_time=1.1)
            self.play(Create(result_box(l2, UNKNOWN)), run_time=0.4)
        with self.beat("b03") as b:
            el = right_panel("Electrical (usually preferred)", [T("E = VIt measured directly and precisely", size=SMALL)],
                             size=SMALL + 1, width=5.0, color=GOOD)
            ch = right_panel("Chemical", [T("needs a complete reaction and an accurate ΔH", size=SMALL)],
                             size=SMALL + 1, width=5.0, color=SYSTEM)
            VGroup(el, ch).arrange(RIGHT, buff=0.35).move_to([0, -1.65, 0])
            self.play(FadeIn(el), run_time=0.6)
            b.until(0.35)
            self.play(FadeIn(ch), run_time=0.6)
            same = T("either way: calibrate under the same conditions as the experiment", size=SMALL + 1, color=UNKNOWN)
            same.move_to([0, -2.5, 0])
            b.until(0.75)
            self.play(FadeIn(same), run_time=0.5)


# =====================================================================================
def arrow_tag(mob, direction: str, color, label: str = ""):
    if direction == "up":
        a = Arrow(mob.get_top() + 0.1 * UP, mob.get_top() + 0.75 * UP, buff=0, color=color, stroke_width=6)
    elif direction == "down":
        a = Arrow(mob.get_top() + 0.75 * UP, mob.get_top() + 0.1 * UP, buff=0, color=color, stroke_width=6)
    else:
        a = TB("=", size=BODY, color=color).next_to(mob, UP, buff=0.2)
    if label:
        t = T(label, size=SMALL + 1, color=color).next_to(a, UP, buff=0.08)
        return VGroup(a, t)
    return VGroup(a)


class E09S09_HeatLoss(NarratedScene):
    def construct(self):
        h = header("Heat loss during calibration")
        f = M(r"CF", "=", r"\frac{E}{\Delta T}", size=EQ + 16).move_to([0, 0.4, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(f), run_time=1.0)
            q = T("Some heat escapes during calibration. Which way does CF move?", size=LABEL + 2, color=UNKNOWN).move_to([0, 2.4, 0])
            self.play(FadeIn(q), run_time=0.7)
            self.q = q
        E = f[2][0]
        dT = f[2][-2:]
        with self.beat("b02") as b:
            eE = T("E: measured electrically → unchanged", size=LABEL, color=GOOD).move_to([-3.6, 1.2, 0])
            self.play(FadeIn(eE), Indicate(E, color=GOOD), run_time=0.9)
            b.until(0.45)
            dTa = Arrow(dT.get_right() + 0.3 * RIGHT + 0.35 * UP, dT.get_right() + 0.3 * RIGHT + 0.35 * DOWN, buff=0, color=BAD, stroke_width=6)
            dTt = T("ΔT measured smaller", size=LABEL, color=BAD).next_to(dTa, RIGHT, buff=0.15)
            self.play(GrowArrow(dTa), FadeIn(dTt), run_time=0.8)
            self.arrows = VGroup(eE, dTa, dTt)
        with self.beat("b03") as b:
            cfa = Arrow(f[0].get_left() + 0.3 * LEFT + 0.4 * DOWN, f[0].get_left() + 0.3 * LEFT + 0.4 * UP, buff=0, color=UNKNOWN, stroke_width=7)
            cft = T("CF calculated too LARGE", size=LABEL + 2, color=UNKNOWN).next_to(cfa, LEFT, buff=0.15)
            self.play(GrowArrow(cfa), FadeIn(cft), run_time=0.9)
        with self.beat("b04") as b:
            myth = wrong_panel("Memorised rule", [T("“heat loss always makes the answer smaller”", size=LABEL)],
                               note="Trace the affected measurement through the actual formula instead.", width=7.5)
            myth.move_to([0, -1.62, 0])
            self.play(FadeIn(myth), run_time=0.9)
            self.myth = myth
        with self.beat("b05") as b:
            self.clear(h, f)
            ck = VGroup(TB("Checkpoint", size=LABEL + 2, color=UNKNOWN),
                        T("time recorded as 200 s instead of 240 s: CF too big or too small?", size=LABEL + 2)).arrange(DOWN, buff=0.2)
            ck.move_to([0, 2.45, 0])
            self.play(FadeIn(ck), run_time=0.8)
        with self.beat("b06") as b:
            Ea = Arrow(E.get_top() + 0.75 * UP, E.get_top() + 0.1 * UP, buff=0, color=BAD, stroke_width=6)
            Et = T("E = VIt too small", size=LABEL, color=BAD).next_to(Ea, RIGHT, buff=0.15)
            cfa = Arrow(f[0].get_left() + 0.3 * LEFT + 0.4 * UP, f[0].get_left() + 0.3 * LEFT + 0.4 * DOWN, buff=0, color=UNKNOWN, stroke_width=7)
            cft = T("CF too SMALL", size=LABEL + 2, color=UNKNOWN).next_to(cfa, LEFT, buff=0.15)
            same = T("ΔT unchanged", size=LABEL, color=GOOD).next_to(dT, RIGHT, buff=0.4)
            self.play(GrowArrow(Ea), FadeIn(Et), FadeIn(same), run_time=0.9)
            b.until(0.5)
            self.play(GrowArrow(cfa), FadeIn(cft), run_time=0.8)


# =====================================================================================
class E09S10_Q18(NarratedScene):
    def construct(self):
        h = header("Practice Q18")
        qc = question_card("Q18").move_to([0, 0.3, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        nl = NumberLine(x_range=[300, 600, 50], length=10.0, include_numbers=True, color=TEXT,
                        decimal_number_config=dict(num_decimal_places=0, color=MUTED), font_size=24).move_to([0, 1.2, 0])
        unit = T("CF (J °C⁻¹)", size=SMALL + 1, color=MUTED).next_to(nl, RIGHT, buff=0.2).shift(0.0 * UP)
        with self.beat("b02") as b:
            self.play(FadeOut(qc), Create(nl), FadeIn(unit), run_time=1.0)
            lbm = DashedLine(nl.n2p(418) + 0.6 * UP, nl.n2p(418) + 0.6 * DOWN, color=SURR, stroke_width=3)
            lbt = M(r"m c = 100.0 \times 4.18 = 418", size=EQ_SMALL - 8, color=SURR).next_to(lbm, UP, buff=0.1)
            allowed = Line(nl.n2p(418), nl.n2p(600), color=GOOD, stroke_width=10).set_opacity(0.6)
            at = T("allowed: CF > 418", size=SMALL + 1, color=GOOD).next_to(allowed, DOWN, buff=0.75)
            self.play(Create(lbm), Write(lbt), run_time=1.0)
            self.play(Create(allowed), FadeIn(at), run_time=0.7)
            rep = Dot(nl.n2p(360), color=BAD, radius=0.12)
            rt = T("reported 360 ✗", size=LABEL, color=BAD).next_to(rep, DOWN, buff=0.75)
            b.until(0.7)
            self.play(FadeIn(rep), FadeIn(rt), run_time=0.7)
        with self.beat("b03") as b:
            f = M(r"CF = \frac{E}{\Delta T}", size=EQ).move_to([-4.0, -1.4, 0])
            hl = VGroup(T("heat loss: ΔT ↓  →  CF ↑", size=LABEL + 2, color=UNKNOWN),
                        T("so heat loss cannot explain a LOW CF", size=LABEL + 2, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            hl.next_to(f, RIGHT, buff=0.6)
            self.play(Write(f), FadeIn(hl[0]), run_time=1.0)
            b.until(0.55)
            self.play(FadeIn(hl[1]), run_time=0.6)
            self.f, self.hl = f, hl
        with self.beat("b04") as b:
            self.play(FadeOut(self.hl), run_time=0.4)
            ok = right_panel("Errors that make CF too low", ["ΔT overestimated (e.g. thermometer misread)",
                                                             "E underestimated: t, I or V recorded too low"], width=6.6)
            ok.next_to(self.f, RIGHT, buff=0.6)
            self.play(FadeIn(ok), run_time=0.9)
        with self.beat("b05") as b:
            self.clear(h)
            tally = mark_tally([(1, "water-only lower bound: 418 J °C⁻¹"), (1, "360 is inconsistent with the setup"),
                                (1, "heat loss would raise CF, not lower it"), (1, "a valid error that lowers CF")], width=7.2).move_to([0, 0.6, 0])
            pat = T("Full-credit pattern: which measurement → which direction → effect on the result", size=LABEL + 2, color=UNKNOWN).move_to([0, -2.0, 0])
            self.play(FadeIn(tally), run_time=0.9)
            b.until(0.6)
            self.play(FadeIn(pat), run_time=0.6)


# =====================================================================================
class E09S11_Recap(NarratedScene):
    def construct(self):
        h = header("Recap")
        items = bullets(["CF: energy per °C for the whole calorimeter and its contents",
                         "Electrical calibration: E = VIt (t in seconds), CF = E ÷ ΔT",
                         "CF = m c (water) + C (apparatus) > m c (water)",
                         "Reuse CF only for matched contents; trace errors through the formula"], size=LABEL + 2, width=12.0, buff=0.35)
        items.move_to([0, 0.3, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for i, it in enumerate(items):
                b.until(0.05 + 0.2 * i)
                self.play(FadeIn(it, shift=0.1 * RIGHT), run_time=0.6)
        with self.beat("b02") as b:
            self.play(FadeOut(items), run_time=0.4)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN),
                       T("12.0 V, 2.00 A, 5 minutes; temperature rise 6.0 °C. CF = ?", size=BODY)).arrange(DOWN, buff=0.35).move_to([0, 1.0, 0])
            self.play(FadeIn(q), run_time=0.8)
            self.q = q
        with self.beat("b03") as b:
            a = VGroup(M(r"E = 12.0 \times 2.00 \times 300 = 7200\ \text{J}", size=EQ_SMALL, color=GOOD),
                       M(r"CF = \frac{7200}{6.0} = 1200\ \text{J}\ {}^{\circ}\text{C}^{-1}", size=EQ_SMALL, color=GOOD)).arrange(DOWN, buff=0.25)
            a.next_to(self.q, DOWN, buff=0.45)
            self.play(Write(a[0]), run_time=1.0)
            b.until(0.35)
            self.play(Write(a[1]), run_time=1.0)
            nxt = T("Next: Episode 10 · Reaction calorimetry and molar enthalpy", size=LABEL, color=MUTED).move_to([0, -2.4, 0])
            b.until(0.7)
            self.play(FadeIn(nxt), run_time=0.5)


EPISODE_SCENES = ["E09S01_Retrieval", "E09S02_MoreThanWater", "E09S03_Kinds", "E09S04_EVIt", "E09S05_Stack",
                  "E09S06_Q17a", "E09S07_Contents", "E09S08_Chemical", "E09S09_HeatLoss", "E09S10_Q18",
                  "E09S11_Recap"]
