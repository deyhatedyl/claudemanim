"""
Episode 08 - Measuring combustion energy and efficiency.
Narration: scripts/ep08.md (beat names must match).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (Thermometer, bullets, mark_tally, question_card, result_box, right_panel,  # noqa: E402
                               title_card, wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, ENERGY_C, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, LOSS, MASS_C,  # noqa: E402
                          MOL_C, MUTED, PANEL, SMALL, SURR, SYSTEM, TEMP_C, TEXT, UNKNOWN, USEFUL, M, T, TB,
                          chip, header, panel)


def requested(text: str) -> VGroup:
    from shared.style import asked_pill
    return asked_pill(text)


def burner_rig(center=ORIGIN, scale=1.0):
    """Schematic spirit burner under a metal can of water with a thermometer."""
    bottle = RoundedRectangle(width=1.2, height=0.9, corner_radius=0.15, color=TEXT, stroke_width=2.5)
    fuel = Rectangle(width=1.1, height=0.45, stroke_width=0, fill_color=SYSTEM, fill_opacity=0.5).align_to(bottle, DOWN).shift(0.05 * UP)
    wick = Line(bottle.get_top(), bottle.get_top() + 0.25 * UP, color=MUTED, stroke_width=4)
    flame = VGroup(Ellipse(width=0.45, height=0.9, fill_color=SYSTEM, fill_opacity=0.85, stroke_width=0),
                   Ellipse(width=0.22, height=0.5, fill_color=UNKNOWN, fill_opacity=0.9, stroke_width=0))
    flame.next_to(wick, UP, buff=-0.05)
    flame[1].align_to(flame[0], DOWN).shift(0.05 * UP)
    can = Rectangle(width=2.2, height=1.7, color="#BDC3C7", stroke_width=3).next_to(flame, UP, buff=0.35)
    water = Rectangle(width=2.1, height=1.15, stroke_width=0, fill_color=SURR, fill_opacity=0.45).align_to(can, DOWN).shift(0.04 * UP)
    th = Thermometer(height=2.3, level=0.3).move_to(can.get_center() + 0.55 * RIGHT + 0.5 * UP)
    stand = VGroup(Line(can.get_corner(DL) + 0.1 * RIGHT, can.get_corner(DL) + 0.1 * RIGHT + 2.0 * DOWN, color=FAINT, stroke_width=3),
                   Line(can.get_corner(DR) + 0.1 * LEFT, can.get_corner(DR) + 0.1 * LEFT + 2.0 * DOWN, color=FAINT, stroke_width=3))
    g = VGroup(stand, bottle, fuel, wick, flame, can, water, th)
    g.bottle, g.fuel, g.flame, g.can, g.water, g.th = bottle, fuel, flame, can, water, th
    g.scale(scale).move_to(center)
    return g


def readout(value: str, color=TEXT, label="balance"):
    box = RoundedRectangle(width=2.6, height=0.8, corner_radius=0.1, color=MUTED, stroke_width=2, fill_color="#0B1A12", fill_opacity=1)
    t = T(value, size=BODY, color=GOOD, font="DejaVu Sans Mono") if False else T(value, size=BODY, color=GOOD)
    t.move_to(box)
    lab = T(label, size=SMALL, color=MUTED).next_to(box, UP, buff=0.08)
    return VGroup(box, t, lab)


# =====================================================================================
class E08S01_Retrieval(NarratedScene):
    def construct(self):
        tc = title_card(8, "Measuring combustion energy and efficiency")
        with self.beat("b01"):
            self.play(FadeIn(tc, shift=0.2 * UP), run_time=1.5)
        with self.beat("b02") as b:
            self.play(FadeOut(tc), run_time=0.5)
            h = header("Retrieval check")
            q1 = VGroup(T("1.", size=BODY), M(r"\Delta H_c(\text{ethanol}) = -1370\ \text{kJ mol}^{-1}", size=EQ_SMALL),
                        T(": energy from 0.0200 mol?", size=BODY)).arrange(RIGHT, buff=0.2)
            q2 = T("2.  17 974 J in kJ?", size=BODY)
            qs = VGroup(q1, q2).arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to([0, 0.9, 0])
            self.play(FadeIn(h), FadeIn(q1), run_time=0.8)
            b.until(0.55)
            self.play(FadeIn(q2), run_time=0.6)
            self.qs = qs
        with self.beat("b03") as b:
            a1 = M(r"0.0200 \times 1370 = 27.4\ \text{kJ released}", size=EQ_SMALL, color=GOOD).next_to(self.qs[0], DOWN, buff=0.15).align_to(self.qs[0], LEFT).shift(0.6 * RIGHT)
            a2 = M(r"17\,974\ \text{J} \div 1000 = 17.974\ \text{kJ}", size=EQ_SMALL, color=GOOD).next_to(self.qs[1], DOWN, buff=0.15).align_to(self.qs[1], LEFT).shift(0.6 * RIGHT)
            self.play(Write(a1), run_time=0.9)
            b.until(0.35)
            self.play(Write(a2), run_time=0.9)


# =====================================================================================
class E08S02_EnergyFlow(NarratedScene):
    def construct(self):
        from shared.motion import flow
        h = header("Where the energy goes")
        sch = T("schematic", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
        rig = burner_rig([-2.7, -0.2, 0], 0.95)
        labs = VGroup(T("spirit burner (fuel)", size=SMALL + 1, color=SYSTEM).next_to(rig.bottle, LEFT, buff=0.25),
                      T("metal can + water", size=SMALL + 1, color=SURR).next_to(rig.can, LEFT, buff=0.25),
                      T("thermometer", size=SMALL + 1, color=TEMP_C).next_to(rig.th, RIGHT, buff=0.15).shift(0.8 * UP))
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(sch), FadeIn(rig), run_time=1.0)
            self.play(FadeIn(labs), run_time=0.8)
        fpos = rig.flame.get_top()
        a_w = Arrow(fpos, rig.water.get_center(), buff=0.05, color=USEFUL, stroke_width=6)
        a_can = Arrow(fpos + 0.1 * RIGHT, rig.can.get_corner(DR) + 0.2 * UP, buff=0.05, color="#BDC3C7", stroke_width=4)
        a_air1 = DashedVMobject(Arrow(fpos + 0.2 * RIGHT, fpos + np.array([2.4, 1.4, 0]), buff=0, color=LOSS, stroke_width=5), num_dashes=10)
        a_air2 = DashedVMobject(Arrow(fpos + 0.2 * LEFT, fpos + np.array([-1.8, 1.6, 0]), buff=0, color=LOSS, stroke_width=5), num_dashes=10)
        legend = VGroup(VGroup(Line(LEFT * 0.35, RIGHT * 0.35, color=USEFUL, stroke_width=6), T("heats the water (useful, measured)", size=LABEL, color=USEFUL)).arrange(RIGHT, buff=0.2),
                        VGroup(Line(LEFT * 0.35, RIGHT * 0.35, color="#BDC3C7", stroke_width=4), T("heats the can and thermometer", size=LABEL)).arrange(RIGHT, buff=0.2),
                        VGroup(DashedLine(LEFT * 0.35, RIGHT * 0.35, color=LOSS, stroke_width=5), T("heats the air (lost)", size=LABEL, color=LOSS)).arrange(RIGHT, buff=0.2))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.2, 1.0, 0])
        with self.beat("b02") as b:
            self.play(FadeOut(labs[0]), FadeOut(labs[1]), GrowArrow(a_w), FadeIn(legend[0]), run_time=0.9)
            flow(self, a_w.get_start(), a_w.get_end(), USEFUL)
            self.play(rig.th.level.animate.set_value(0.65), run_time=1.0)
            b.until(0.4)
            self.play(GrowArrow(a_can), FadeIn(legend[1]), run_time=0.8)
            b.until(0.65)
            self.play(Create(a_air1), Create(a_air2), FadeIn(legend[2]), run_time=0.9)
            flow(self, fpos, fpos + np.array([2.4, 1.4, 0]), LOSS, run_time=1.4)
        with self.beat("b03") as b:
            soot = VGroup(*[Dot(rig.can.get_bottom() + RIGHT * x + 0.03 * UP, radius=0.05, color="#333333") for x in np.linspace(-0.6, 0.6, 9)])
            st = VGroup(T("incomplete combustion", size=LABEL, color=UNKNOWN), T("soot; less energy released", size=LABEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            st.move_to([3.2, -0.45, 0]).align_to(legend, LEFT)
            self.play(FadeIn(soot), FadeIn(st), run_time=1.0)
        with self.beat("b04") as b:
            key = VGroup(T("energy gained by water", size=LABEL + 2, color=USEFUL), M(r"<", size=EQ),
                         T("energy the fuel could release", size=LABEL + 2, color=SYSTEM)).arrange(DOWN, buff=0.1)
            kp = panel(key, color=UNKNOWN)
            VGroup(kp, key).move_to([3.6, -1.85, 0])
            self.play(FadeIn(kp), FadeIn(key), run_time=0.9)


# =====================================================================================
class E08S03_qmcT(NarratedScene):
    def construct(self):
        h = header("Building q = mcΔT")
        block = Square(side_length=0.7, fill_color=SURR, fill_opacity=0.6, stroke_color=TEXT, stroke_width=2).move_to([-4.8, 1.4, 0])
        bl = T("1 g water", size=SMALL + 1).next_to(block, DOWN, buff=0.1)
        one = VGroup(T("+1 °C needs", size=LABEL + 2), M(r"4.18\ \text{J}", size=EQ_SMALL, color=ENERGY_C)).arrange(RIGHT, buff=0.2).next_to(block, RIGHT, buff=0.5)
        cdef = VGroup(M(r"c = 4.18\ \text{J g}^{-1}\,{}^{\circ}\text{C}^{-1}", size=EQ_SMALL, color=ENERGY_C), T("specific heat capacity of water", size=SMALL + 1, color=MUTED)).arrange(DOWN, buff=0.1)
        cdef.move_to([3.6, 1.4, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(block), FadeIn(bl), run_time=0.7)
            self.play(FadeIn(one), run_time=0.7)
            b.until(0.55)
            self.play(FadeIn(cdef), run_time=0.8)
        grid = VGroup(*[Square(side_length=0.28, fill_color=SURR, fill_opacity=0.6, stroke_color=TEXT, stroke_width=1) for _ in range(50)])
        grid.arrange_in_grid(5, 10, buff=0.04).move_to([-3.6, -0.4, 0])
        gl = T("× 250 g → 250 × the energy", size=LABEL + 2, color=MASS_C).next_to(grid, RIGHT, buff=0.4)
        with self.beat("b02") as b:
            self.play(TransformFromCopy(block, grid), run_time=1.2)
            b.until(0.45)
            self.play(FadeIn(gl), run_time=0.7)
        with self.beat("b03") as b:
            th = Thermometer(height=1.9, level=0.15).move_to([5.6, -0.6, 0])
            tl = T("× 10 °C → 10 × the energy", size=LABEL + 2, color=TEMP_C).next_to(gl, DOWN, buff=0.3).align_to(gl, LEFT)
            self.play(FadeIn(th), run_time=0.4)
            self.play(th.level.animate.set_value(0.8), FadeIn(tl), run_time=1.4)
            self.th = th
        with self.beat("b04") as b:
            self.clear(h)
            f = M(r"q", "=", r"m", r"\,c\,", r"\Delta T", size=EQ + 8).move_to([0, 1.5, 0])
            f[2].set_color(MASS_C)
            f[3].set_color(ENERGY_C)
            f[4].set_color(TEMP_C)
            u = M(r"\text{J} = \text{g} \times \text{J g}^{-1}\,{}^{\circ}\text{C}^{-1} \times {}^{\circ}\text{C}", size=EQ_SMALL).next_to(f, DOWN, buff=0.45)
            self.play(Write(f), run_time=1.2)
            b.until(0.35)
            self.play(Write(u), run_time=1.2)
            self.f, self.u = f, u
        with self.beat("b05") as b:
            chk = VGroup(VGroup(TB("m:", size=LABEL + 2, color=MASS_C), T("mass of the WATER (not the fuel)", size=LABEL + 2)).arrange(RIGHT, buff=0.2),
                         VGroup(TB("ΔT:", size=LABEL + 2, color=TEMP_C), T("temperature RISE = final − initial (not the final temperature)", size=LABEL + 2)).arrange(RIGHT, buff=0.2))
            chk.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.4, 0])
            self.play(FadeIn(chk[0]), run_time=0.7)
            b.until(0.45)
            self.play(FadeIn(chk[1]), run_time=0.7)


# =====================================================================================
class E08S04_MassEnergy(NarratedScene):
    def construct(self):
        h = header("What changes the temperature rise?")
        f = M(r"\Delta T = \frac{q}{m\,c}", size=EQ).move_to([0, 2.15, 0]).to_edge(RIGHT, buff=0.8)
        specs = [("4180 J", "100 g", 10, "+10 °C"), ("4180 J", "200 g", 5, "+5 °C"), ("8360 J", "100 g", 20, "+20 °C")]
        panels = VGroup()
        for e, m, dt, lab in specs:
            beaker = Rectangle(width=1.2 if m == "100 g" else 1.8, height=0.9 if m == "100 g" else 1.4, color=TEXT, stroke_width=2)
            water = Rectangle(width=beaker.width - 0.08, height=beaker.height - 0.15, stroke_width=0, fill_color=SURR, fill_opacity=0.5).align_to(beaker, DOWN).shift(0.04 * UP)
            th = Thermometer(height=1.9, level=0.1)
            top = VGroup(T(e, size=LABEL + 2, color=ENERGY_C), T(f"into {m} of water", size=LABEL, color=MASS_C)).arrange(DOWN, buff=0.08)
            body = VGroup(VGroup(beaker, water), th).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
            res = T(lab, size=BODY, color=TEMP_C)
            p = VGroup(top, body, res).arrange(DOWN, buff=0.3)
            p.dt, p.th = dt, th
            panels.add(p)
        panels.arrange(RIGHT, buff=1.0).move_to([0, 0.15, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(f), run_time=1.0)
            p = panels[0]
            self.play(FadeIn(p[0]), FadeIn(p[1]), run_time=0.7)
            self.play(p.th.level.animate.set_value(0.1 + 0.03 * p.dt), FadeIn(p[2]), run_time=1.0)
        with self.beat("b02") as b:
            p = panels[1]
            self.play(FadeIn(p[0]), FadeIn(p[1]), run_time=0.7)
            self.play(p.th.level.animate.set_value(0.1 + 0.03 * p.dt), FadeIn(p[2]), run_time=1.0)
            n = wrapped("twice the water: half the rise", size=SMALL + 1, width=2.6, color=MUTED).next_to(p, DOWN, buff=0.2)
            self.play(FadeIn(n), run_time=0.5)
        with self.beat("b03") as b:
            p = panels[2]
            self.play(FadeIn(p[0]), FadeIn(p[1]), run_time=0.7)
            self.play(p.th.level.animate.set_value(0.1 + 0.03 * p.dt), FadeIn(p[2]), run_time=1.0)
            n = wrapped("twice the energy: twice the rise", size=SMALL + 1, width=2.6, color=MUTED).next_to(p, DOWN, buff=0.2)
            self.play(FadeIn(n), run_time=0.5)


# =====================================================================================
class E08S05_MassLoss(NarratedScene):
    def construct(self):
        h = header("How much fuel burned?")
        r1 = readout("102.640 g", label="burner before").move_to([-4.0, 1.8, 0])
        r2 = readout("101.720 g", label="burner after").move_to([-1.0, 1.8, 0])
        chain = VGroup(M(r"\Delta m = \text{fuel burned}", size=EQ_SMALL - 4, color=MASS_C),
                       M(r"\xrightarrow{\ \div M\ }\ n", size=EQ_SMALL - 4, color=MOL_C),
                       M(r"\xrightarrow{\ \times |\Delta H_c|\ }\ E_{\text{released}}", size=EQ_SMALL - 4, color=ENERGY_C)).arrange(RIGHT, buff=0.25)
        chain.move_to([0, 0.55, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(r1), run_time=0.7)
            self.play(FadeIn(r2), run_time=0.7)
            b.until(0.3)
            self.play(Write(chain[0]), run_time=0.8)
            b.until(0.55)
            self.play(Write(chain[1]), run_time=0.7)
            b.until(0.75)
            self.play(Write(chain[2]), run_time=0.8)
            self.top = VGroup(r1, r2, chain)
        food = VGroup(TB("Food calorimetry", size=LABEL + 2, color=SYSTEM),
                      T("1.50 g dry food burned · 100.0 g water · rise 8.0 °C", size=LABEL)).arrange(DOWN, buff=0.12)
        food.move_to([0, 2.2, 0])
        with self.beat("b02") as b:
            self.play(FadeOut(self.top), run_time=0.5)
            self.play(FadeIn(food), run_time=0.8)
            q = M(r"q = 100.0 \times 4.18 \times 8.0 = 3344\ \text{J}", size=EQ_SMALL, color=ENERGY_C).move_to([0, 1.45, 0])
            b.until(0.5)
            self.play(Write(q), run_time=1.2)
        with self.beat("b03") as b:
            per = M(r"\frac{3344\ \text{J}}{1.50\ \text{g}} = 2229\ \text{J g}^{-1} \approx 2.2\ \text{kJ g}^{-1}", size=EQ_SMALL, color=UNKNOWN).move_to([0, 0.5, 0])
            self.play(Write(per), run_time=1.2)
            lab = T("typical label: 15 or more kJ per gram for a dry, carbohydrate-rich food", size=LABEL, color=MUTED).move_to([0, -0.3, 0])
            b.until(0.6)
            self.play(FadeIn(lab), run_time=0.7)
        with self.beat("b04") as b:
            why = VGroup(T("1. losses to the can and air; incomplete burning", size=LABEL),
                         T("2. a label gives energy the body can obtain: a different basis", size=LABEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            name = T("call it an experimental water-heat yield, not the label energy", size=LABEL, color=UNKNOWN)
            g = VGroup(why, name).arrange(DOWN, buff=0.2)
            gp = panel(g)
            VGroup(gp, g).move_to([0, -1.6, 0])
            self.play(FadeIn(gp), FadeIn(why[0]), run_time=0.7)
            b.until(0.4)
            self.play(FadeIn(why[1]), run_time=0.6)
            b.until(0.75)
            self.play(FadeIn(name), run_time=0.6)


# =====================================================================================
class E08S06_Q15(NarratedScene):
    def construct(self):
        h = header("Practice Q15")
        qc = question_card("Q15").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        req = requested("efficiency (%)")
        colL = -6.2

        def L(tex, y, col=TEXT, s=EQ_SMALL - 6):
            return M(tex, size=s, color=col).move_to([0, y, 0]).align_to([colL, 0, 0], LEFT)
        l1 = L(r"m = 102.640 - 101.720 = 0.920\ \text{g}", 2.2, MASS_C)
        l2 = L(r"n = \frac{0.920\ \text{g}}{46.0\ \text{g mol}^{-1}} = 0.0200\ \text{mol}", 1.45, MOL_C)
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(req), run_time=0.5)
            self.play(Write(l1), run_time=1.0)
            b.until(0.45)
            self.play(Write(l2), run_time=1.1)
        l3 = L(r"E_{\text{fuel}} = 0.0200 \times 1370 = 27.4\ \text{kJ}", 0.7, ENERGY_C)
        with self.beat("b03") as b:
            self.play(Write(l3), run_time=1.0)
        l4 = L(r"\Delta T = 37.0 - 19.8 = 17.2\ {}^{\circ}\text{C}", 0.0, TEMP_C)
        l5 = L(r"q = 250.0 \times 4.18 \times 17.2 = 17\,974\ \text{J} = 17.974\ \text{kJ}", -0.7, USEFUL)
        with self.beat("b04") as b:
            self.play(Write(l4), run_time=0.9)
            b.until(0.35)
            self.play(Write(l5), run_time=1.2)
            nw = T("water's mass, not the fuel's", size=SMALL + 1, color=MUTED).next_to(l5, RIGHT, buff=0.3)
            self.play(FadeIn(nw), run_time=0.4)
        with self.beat("b05") as b:
            pred = T("predict: water gained less than the fuel released → below 100%", size=LABEL, color=UNKNOWN).move_to([0, -1.4, 0])
            self.play(FadeIn(pred), run_time=0.6)
            l6 = M(r"\text{efficiency} = \frac{17.974\ \text{kJ}}{27.4\ \text{kJ}} \times 100\% = 65.6\%", size=EQ_SMALL - 4, color=GOOD).move_to([0, -2.2, 0])
            b.until(0.35)
            self.play(Write(l6), run_time=1.3)
        with self.beat("b06") as b:
            self.clear(h, req)
            tally = mark_tally([(2, "mass and amount of ethanol"), (1, "fuel energy: 27.4 kJ"), (2, "water heat: 18.0 kJ"),
                                (1, "efficiency: 65.6%")], width=5.4).move_to([-3.5, 0.4, 0])
            ws = VGroup(wrong_panel("Whole burner mass", [T("102.640 g → 2.23 mol ✗", size=LABEL)], width=4.8, size=SMALL + 2),
                        wrong_panel("Fuel mass in mcΔT", [T("0.920 × 4.18 × 17.2 = 66 J ✗", size=LABEL)], width=4.8, size=SMALL + 2),
                        wrong_panel("J divided by kJ", [T("17 974 ÷ 27.4 → 656% ✗", size=LABEL)], width=4.8, size=SMALL + 2))
            ws.arrange(DOWN, buff=0.2).move_to([3.4, 0.4, 0])
            self.play(FadeIn(tally), run_time=0.8)
            for i, w in enumerate(ws):
                b.until(0.3 + 0.2 * i)
                self.play(FadeIn(w), run_time=0.5)


# =====================================================================================
class E08S07_Efficiency(NarratedScene):
    def construct(self):
        h = header("Efficiency, forwards and backwards")
        f = M(r"\text{efficiency}", "=", r"\frac{\text{useful energy output}}{\text{total energy input}}", r"\times 100\%", size=EQ).move_to([0, 1.8, 0])
        f[2].set_color(USEFUL)
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(f), run_time=1.4)
            n = T("say what counts as useful; use the same unit top and bottom", size=LABEL, color=MUTED).next_to(f, DOWN, buff=0.3)
            b.until(0.6)
            self.play(FadeIn(n), run_time=0.6)
            self.n = n
        with self.beat("b02") as b:
            self.play(FadeOut(self.n), run_time=0.3)
            g = M(r"\text{total input}", "=", r"\frac{\text{useful output}}{\text{efficiency (as a fraction)}}", size=EQ).move_to([0, 0.35, 0])
            g[2].set_color(UNKNOWN)
            self.play(TransformFromCopy(f, g), run_time=1.4)
            ex = T("e.g. 45.0% → divide by 0.450", size=LABEL + 2, color=UNKNOWN).next_to(g, DOWN, buff=0.25)
            b.until(0.65)
            self.play(FadeIn(ex), run_time=0.6)
            self.g, self.ex = g, ex
        with self.beat("b03") as b:
            self.play(FadeOut(f), FadeOut(self.ex), self.g.animate.scale(0.8).move_to([0, 2.2, 0]), run_time=0.7)
            sc = 0.06
            useful = 45.1
            bars = VGroup()
            for eff, lab in [(1.0, "100% efficient"), (0.45, "45% efficient")]:
                inp = useful / eff
                ib = Rectangle(width=inp * sc, height=0.5, fill_color=SYSTEM, fill_opacity=0.35, stroke_color=SYSTEM, stroke_width=2)
                ub = Rectangle(width=useful * sc, height=0.5, fill_color=USEFUL, fill_opacity=0.85, stroke_width=0)
                ub.align_to(ib, LEFT)
                tl = T(lab, size=LABEL).next_to(ib, LEFT, buff=0.3)
                vt = T(f"input {inp:.1f} kJ", size=LABEL, color=SYSTEM).next_to(ib, RIGHT, buff=0.2)
                bars.add(VGroup(ib, ub, tl, vt))
            bars.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([0.3, 0.2, 0])
            ul = T("useful output 45.1 kJ (same task)", size=SMALL + 1, color=USEFUL).next_to(bars, UP, buff=0.2).align_to(bars, LEFT)
            self.play(FadeIn(ul), FadeIn(bars[0]), run_time=0.9)
            b.until(0.35)
            self.play(FadeIn(bars[1]), run_time=0.9)
            msg = T("less efficient → more fuel for the same useful energy", size=LABEL + 2, color=UNKNOWN).move_to([0, -1.6, 0])
            b.until(0.6)
            self.play(FadeIn(msg), run_time=0.6)
            self.stuff = VGroup(bars, ul, msg)
        with self.beat("b04") as b:
            self.play(FadeOut(self.stuff), run_time=0.4)
            ck = VGroup(TB("Checkpoint", size=BODY, color=UNKNOWN),
                        T("Input found by multiplying useful energy × efficiency: too big or too small?", size=LABEL + 2)).arrange(DOWN, buff=0.3)
            ck.move_to([0, 0.4, 0])
            self.play(FadeIn(ck), run_time=0.8)
            self.ck = ck
        with self.beat("b05") as b:
            a = VGroup(TB("Too small.", size=BODY, color=BAD),
                       T("× 0.450 gives less than the useful output: more energy out than in, impossible", size=LABEL + 2)).arrange(DOWN, buff=0.2)
            a.next_to(self.ck, DOWN, buff=0.45)
            self.play(FadeIn(a), run_time=0.8)


# =====================================================================================
class E08S08_Q16(NarratedScene):
    def construct(self):
        h = header("Practice Q16")
        qc = question_card("Q16").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        req = requested("minimum fuel mass (g)")
        colL = -6.2

        def L(tex, y, col=TEXT, s=EQ_SMALL - 6):
            return M(tex, size=s, color=col).move_to([0, y, 0]).align_to([colL, 0, 0], LEFT)
        l1 = L(r"q = 180.0 \times 4.18 \times 60.0 = 45\,144\ \text{J} = 45.144\ \text{kJ}", 2.2, USEFUL)
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(req), run_time=0.5)
            dt = T("ΔT = 78.0 − 18.0 = 60.0 °C", size=LABEL, color=TEMP_C).move_to([0, 2.75, 0]).align_to([colL, 0, 0], LEFT)
            self.play(FadeIn(dt), run_time=0.6)
            b.until(0.35)
            self.play(Write(l1), run_time=1.3)
        l2 = L(r"E_{\text{input}} = \frac{45.144\ \text{kJ}}{0.450} = 100.32\ \text{kJ}", 1.35, SYSTEM)
        with self.beat("b03") as b:
            self.play(Write(l2), run_time=1.2)
            bigger = T("larger than the useful heat ✓", size=SMALL + 1, color=GOOD).next_to(l2, RIGHT, buff=0.3)
            self.play(FadeIn(bigger), run_time=0.4)
        l3 = L(r"m = \frac{100.32\ \text{kJ}}{29.8\ \text{kJ g}^{-1}} = 3.366\ \text{g} \approx 3.37\ \text{g}", 0.35, MASS_C)
        with self.beat("b04") as b:
            self.play(Write(l3), run_time=1.3)
        with self.beat("b05") as b:
            w = wrong_panel("Efficiency used the wrong way", [M(r"\frac{45.144 \times 0.450}{29.8} = 0.682\ \text{g}", size=EQ_SMALL - 8, color=TEXT)], width=5.4)
            w.move_to([-3.2, -1.55, 0])
            minb = right_panel("100% efficient minimum", [M(r"\frac{45.144}{29.8} = 1.515\ \text{g}", size=EQ_SMALL - 8, color=TEXT),
                                                          T("0.682 g < 1.515 g: impossible", size=LABEL, color=BAD)], width=5.0)
            minb.move_to([3.3, -1.55, 0])
            self.play(FadeIn(w), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(minb), run_time=0.8)
        with self.beat("b06") as b:
            self.clear(h, req)
            tally = mark_tally([(2, "useful heat: 45.144 kJ"), (1, "divide by efficiency: 100.32 kJ"), (1, "fuel mass: 3.37 g"),
                                (1, "explanation with the 100% sanity check")], width=7.0).move_to([0, 0.2, 0])
            self.play(FadeIn(tally), run_time=0.9)


# =====================================================================================
class E08S09_TooLow(NarratedScene):
    def construct(self):
        h = header("Why measured values come out low")
        sch = T("schematic", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
        rig = burner_rig([-4.2, -0.35, 0], 0.85)
        x0 = -1.2
        q = wrapped("Measured |ΔH| for ethanol is much smaller than the data book value. Why?", size=LABEL + 1, width=7.4,
                    color=UNKNOWN).move_to([0, 1.9, 0]).align_to([x0, 0, 0], LEFT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(sch), FadeIn(rig), run_time=1.0)
            b.until(0.3)
            self.play(FadeIn(q), run_time=0.7)
        causes = [("hot gases escape around the can", LOSS), ("the can and clamp warm up", MUTED),
                  ("sooty yellow flame: incomplete combustion", UNKNOWN),
                  ("fuel evaporates from the wick before reweighing", SYSTEM)]
        rows = VGroup(*[VGroup(Dot(radius=0.06, color=c), T(t, size=SMALL + 2, color=c)).arrange(RIGHT, buff=0.18)
                        for t, c in causes]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        rows.move_to([0, 0.35, 0]).align_to([x0, 0, 0], LEFT)
        fpos = rig.flame.get_top()
        gas = VGroup(DashedVMobject(Arrow(fpos + 0.15 * RIGHT, fpos + np.array([1.6, 1.2, 0]), buff=0, color=LOSS,
                                          stroke_width=4), num_dashes=8),
                     DashedVMobject(Arrow(fpos + 0.15 * LEFT, fpos + np.array([-1.4, 1.3, 0]), buff=0, color=LOSS,
                                          stroke_width=4), num_dashes=8))
        soot = VGroup(*[Dot(rig.can.get_bottom() + RIGHT * x + 0.03 * UP, radius=0.045, color="#333333")
                        for x in np.linspace(-0.55, 0.55, 8)])
        vap = VGroup(*[DashedVMobject(Arc(radius=0.18, start_angle=-PI / 2, angle=PI, color=SYSTEM, stroke_width=2.5),
                                      num_dashes=5).move_to(rig.bottle.get_right() + np.array([0.3, 0.15 + 0.32 * i, 0]))
                       for i in range(2)])
        with self.beat("b02") as b:
            self.play(Create(gas), FadeIn(rows[0]), run_time=0.8)
            b.until(0.25)
            self.play(Indicate(rig.can, color=MUTED), FadeIn(rows[1]), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(soot), FadeIn(rows[2]), run_time=0.8)
            b.until(0.68)
            self.play(Create(vap), FadeIn(rows[3]), run_time=0.8)
            self.rows = rows
        with self.beat("b03") as b:
            dirn = chip("each makes the calculated |ΔH| too small", LOSS, size=SMALL + 2)
            dirn.move_to([0, -1.17, 0]).align_to([x0, 0, 0], LEFT)
            self.play(FadeIn(dirn), run_time=0.5)
            fixes = VGroup(*[T(t, size=SMALL + 1, color=GOOD) for t in (
                "draught shield and lid; flame close to a thin copper can; stir",
                "enough air for a clean blue flame; cap and reweigh at once")]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            fixes.scale_to_fit_width(7.55).move_to([0, -1.87, 0]).align_to([x0, 0, 0], LEFT)
            b.until(0.3)
            self.play(FadeIn(fixes, lag_ratio=0.3), run_time=0.9)
            note = T("a result above the data book value points to an error", size=SMALL,
                     color=MUTED).move_to([0, -2.55, 0]).align_to([x0, 0, 0], LEFT)
            b.until(0.82)
            self.play(FadeIn(note), run_time=0.5)


# =====================================================================================
class E08S10_Recap(NarratedScene):
    def construct(self):
        h = header("Recap")
        steps = VGroup(T("mass lost", size=LABEL + 2, color=MASS_C), T("→ ÷ M → mol", size=LABEL + 2, color=MOL_C),
                       T("→ × |ΔHc| → energy released", size=LABEL + 2, color=ENERGY_C)).arrange(RIGHT, buff=0.25).move_to([0, 1.8, 0])
        w = M(r"q_{\text{water}} = m_{\text{water}}\, c\, \Delta T", size=EQ_SMALL, color=USEFUL).move_to([0, 0.8, 0])
        e = M(r"\text{efficiency} = \frac{\text{useful}}{\text{total}} \times 100\% \qquad \text{input} = \frac{\text{useful}}{\text{efficiency}}", size=EQ_SMALL).move_to([0, -0.4, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(steps), run_time=1.0)
            b.until(0.35)
            self.play(Write(w), run_time=0.9)
            b.until(0.6)
            self.play(Write(e), run_time=1.2)
        with self.beat("b02") as b:
            self.clear(h)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN),
                       T("Efficiency halves. How does the fuel mass needed change (same heating task)?", size=LABEL + 2)).arrange(DOWN, buff=0.35).move_to([0, 1.0, 0])
            self.play(FadeIn(q), run_time=0.8)
            self.q = q
        with self.beat("b03") as b:
            a = T("It doubles: input = useful output ÷ efficiency", size=BODY, color=GOOD).next_to(self.q, DOWN, buff=0.5)
            self.play(FadeIn(a), run_time=0.8)
            b.until(0.5)
            nxt = T("Next: Episode 09 · Why calorimeters need calibration", size=LABEL, color=MUTED).move_to([0, -2.35, 0])
            self.play(FadeIn(nxt), run_time=0.5)


EPISODE_SCENES = ["E08S01_Retrieval", "E08S02_EnergyFlow", "E08S03_qmcT", "E08S04_MassEnergy",
                  "E08S05_MassLoss", "E08S06_Q15", "E08S07_Efficiency", "E08S08_Q16", "E08S09_TooLow",
                  "E08S10_Recap"]
