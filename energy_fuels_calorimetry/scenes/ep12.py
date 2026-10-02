"""
Episode 12 - Fair fuel comparisons and sustainability.
Narration: scripts/ep12.md (beat names must match).
Q23 and Fuel T data are hypothetical teaching values (labelled on screen).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (bullets, mark_tally, question_card, result_box, right_panel, table,  # noqa: E402
                               title_card, wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, ENERGY_C, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, LOSS, MASS_C,  # noqa: E402
                          MOL_C, MUTED, PANEL, SMALL, SURR, SYSTEM, TEXT, UNKNOWN, USEFUL, M, T, TB, chip, header,
                          panel)

FOSSIL, BIO = "#A1887F", "#7BE495"
CO2E = "#AEB6BF"


def requested(text: str) -> VGroup:
    c = chip("Asked", UNKNOWN)
    t = T(text, size=SMALL + 2, color=UNKNOWN)
    return VGroup(c, t).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.4)


def hbars(rows, scale, x_left=-2.4, y0=0.0, gap=0.6, h=0.42, fmt="{:.0f}", unit=""):
    """rows: [(label, value, colour)] -> labelled horizontal bars."""
    g = VGroup()
    for i, (lab, v, col) in enumerate(rows):
        y = y0 - i * gap
        t = T(lab, size=LABEL).move_to([0, y, 0]).align_to([x_left - 0.25, 0, 0], RIGHT)
        r = Rectangle(width=max(0.02, v * scale), height=h, fill_color=col, fill_opacity=0.85, stroke_width=0)
        r.move_to([0, y, 0]).align_to([x_left, 0, 0], LEFT)
        vt = T(fmt.format(v) + unit, size=LABEL, color=col).next_to(r, RIGHT, buff=0.15)
        g.add(VGroup(t, r, vt))
    return g


def card(title, lines, color, width=3.6, size=SMALL + 1):
    t = TB(title, size=LABEL, color=color)
    body = VGroup(*[wrapped(l, size=size, width=width - 0.4) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    g = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    r = RoundedRectangle(width=width, height=g.height + 0.35, corner_radius=0.12, stroke_color=color, stroke_width=2.5,
                         fill_color=PANEL, fill_opacity=0.95).move_to(g)
    g.move_to(r)
    return VGroup(r, g)


# =====================================================================================
class E12S01_Retrieval(NarratedScene):
    def construct(self):
        tc = title_card(12, "Fair fuel comparisons and sustainability")
        with self.beat("b01"):
            self.play(FadeIn(tc, shift=0.2 * UP), run_time=1.5)
        with self.beat("b02") as b:
            self.play(FadeOut(tc), run_time=0.5)
            h = header("Retrieval check")
            q1 = T("1.  Do yeast enzymes change ΔH for fermentation?", size=BODY)
            q2 = T("2.  25% efficient; 10.0 MJ useful heat needed. Fuel energy?", size=BODY)
            qs = VGroup(q1, q2).arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to([0, 0.9, 0])
            self.play(FadeIn(h), FadeIn(q1), run_time=0.7)
            b.until(0.4)
            self.play(FadeIn(q2), run_time=0.6)
            self.qs = qs
        with self.beat("b03") as b:
            a1 = T("No: they lower Ea only", size=BODY, color=GOOD).next_to(self.qs[0], DOWN, buff=0.15).align_to(self.qs[0], LEFT).shift(0.6 * RIGHT)
            a2 = M(r"10.0 \div 0.25 = 40.0\ \text{MJ}", size=EQ_SMALL, color=GOOD).next_to(self.qs[1], DOWN, buff=0.15).align_to(self.qs[1], LEFT).shift(0.6 * RIGHT)
            self.play(FadeIn(a1), run_time=0.6)
            b.until(0.35)
            self.play(Write(a2), run_time=0.8)


# =====================================================================================
class E12S02_Bases(NarratedScene):
    def construct(self):
        h = header("Per mole, per gram, per useful output")
        data = VGroup(M(r"\ce{CH4}: \Delta H_c = -890\ \text{kJ mol}^{-1},\ M = 16.0", size=EQ_SMALL - 8),
                      M(r"\ce{C8H18}: \Delta H_c \approx -5460\ \text{kJ mol}^{-1},\ M = 114.0", size=EQ_SMALL - 8)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        data.move_to([0, 2.2, 0])
        b1 = hbars([("methane", 890, SURR), ("octane", 5460, SYSTEM)], 1 / 1000, x_left=-2.2, y0=0.75)
        t1 = TB("per mole (kJ mol⁻¹)", size=LABEL + 2).next_to(b1, UP, buff=0.15).align_to([-4.6, 0, 0], LEFT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(data), run_time=0.9)
            b.until(0.4)
            self.play(FadeIn(t1), FadeIn(b1), run_time=1.0)
        b2 = hbars([("methane", 55.6, SURR), ("octane", 47.9, SYSTEM)], 1 / 14, x_left=-2.2, y0=-1.05, fmt="{:.1f}")
        t2 = TB("per gram (kJ g⁻¹)", size=LABEL + 2).next_to(b2, UP, buff=0.15).align_to([-4.6, 0, 0], LEFT)
        with self.beat("b02") as b:
            self.play(FadeIn(t2), FadeIn(b2), run_time=1.0)
            c = VGroup(M(r"890 \div 16.0 = 55.6", size=EQ_SMALL - 10, color=SURR), M(r"5460 \div 114.0 = 47.9", size=EQ_SMALL - 10, color=SYSTEM)).arrange(DOWN, buff=0.18)
            c.move_to([4.9, -1.35, 0])
            b.until(0.4)
            self.play(Write(c), run_time=1.0)
        with self.beat("b03") as b:
            third = T("third basis: per useful MJ delivered (needs efficiency)", size=LABEL + 2, color=UNKNOWN).move_to([0, -2.35, 0])
            self.play(FadeIn(third), run_time=0.8)


# =====================================================================================
class E12S03_PerLitre(NarratedScene):
    def construct(self):
        h = header("Per litre: another basis for gases")
        data = VGroup(M(r"\ce{H2}: \Delta H_c = -286\ \text{kJ mol}^{-1},\ M = 2.0", size=EQ_SMALL - 8),
                      M(r"\ce{CH4}: \Delta H_c = -890\ \text{kJ mol}^{-1},\ M = 16.0", size=EQ_SMALL - 8)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        data.move_to([0, 2.2, 0])
        H2C = "#F7DC6F"
        b1 = hbars([("hydrogen", 143, H2C), ("methane", 55.6, SURR)], 1 / 30, x_left=-2.2, y0=0.75, fmt="{:.1f}")
        b1[0][2].become(T("143", size=LABEL, color=H2C).next_to(b1[0][1], RIGHT, buff=0.15))
        t1 = TB("per gram (kJ g⁻¹)", size=LABEL + 2).next_to(b1, UP, buff=0.15).align_to([-4.6, 0, 0], LEFT)
        q = T("per gram? per litre at SLC?", size=LABEL + 1, color=UNKNOWN).move_to([0, 0.5, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(data), run_time=0.9)
            b.until(0.7)
            self.play(FadeIn(q), run_time=0.5)
            self.q = q
        with self.beat("b02") as b:
            self.play(FadeOut(self.q), FadeIn(t1), FadeIn(b1), run_time=1.0)
            c1 = VGroup(M(r"286 \div 2.0 = 143", size=EQ_SMALL - 10, color=H2C),
                        M(r"890 \div 16.0 = 55.6", size=EQ_SMALL - 10, color=SURR)).arrange(DOWN, buff=0.18)
            c1.move_to([4.9, 0.45, 0])
            b.until(0.4)
            self.play(Write(c1), run_time=1.0)
        b2 = hbars([("hydrogen", 11.5, H2C), ("methane", 35.9, SURR)], 1 / 9, x_left=-2.2, y0=-1.05, fmt="{:.1f}")
        t2 = TB("per litre of gas at SLC (kJ L⁻¹)", size=LABEL + 2).next_to(b2, UP, buff=0.15).align_to([-4.6, 0, 0], LEFT)
        with self.beat("b03") as b:
            v = T("1 mol of gas at SLC = 24.8 L", size=SMALL, color=MUTED).move_to([4.6, -0.45, 0])
            self.play(FadeIn(v), run_time=0.5)
            b.until(0.2)
            self.play(FadeIn(t2), FadeIn(b2), run_time=1.0)
            c2 = VGroup(M(r"286 \div 24.8 = 11.5", size=EQ_SMALL - 10, color=H2C),
                        M(r"890 \div 24.8 = 35.9", size=EQ_SMALL - 10, color=SURR)).arrange(DOWN, buff=0.18)
            c2.move_to([4.9, -1.35, 0])
            self.play(Write(c2), run_time=1.0)
            st = T("the ranking flips again: state the basis", size=LABEL + 1, color=UNKNOWN).move_to([0, -2.4, 0])
            b.until(0.6)
            self.play(FadeIn(st), run_time=0.5)


# =====================================================================================
class E12S04_Oxygenated(NarratedScene):
    def construct(self):
        h = header("Why oxygen-containing fuels release less energy")
        data = VGroup(M(r"\ce{C2H5OH}: \Delta H_c = -1370\ \text{kJ mol}^{-1},\ M = 46.0", size=EQ_SMALL - 8),
                      M(r"\ce{C3H8}: \Delta H_c = -2220\ \text{kJ mol}^{-1},\ M = 44.0", size=EQ_SMALL - 8)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        data.move_to([0, 2.2, 0])
        PROP = "#85C1E9"
        bars = hbars([("ethanol", 29.8, SYSTEM), ("propane", 50.5, PROP)], 1 / 12, x_left=-2.2, y0=0.75, fmt="{:.1f}")
        tb = TB("per gram (kJ g⁻¹)", size=LABEL + 2).next_to(bars, UP, buff=0.15).align_to([-4.6, 0, 0], LEFT)
        calc = VGroup(M(r"1370 \div 46.0 = 29.8", size=EQ_SMALL - 10, color=SYSTEM),
                      M(r"2220 \div 44.0 = 50.5", size=EQ_SMALL - 10, color=PROP)).arrange(DOWN, buff=0.18).move_to([5.1, 0.45, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(data), run_time=0.9)
            b.until(0.55)
            self.play(FadeIn(tb), FadeIn(bars), run_time=1.0)
            b.until(0.75)
            self.play(Write(calc), run_time=0.9)
        with self.beat("b02") as b:
            eth = M(r"\ce{CH3CH2}", r"\ce{OH}", size=EQ_SMALL - 2).move_to([-2.6, -0.85, 0])
            eth[1].set_color(LOSS)
            pro = M(r"\ce{CH3CH2CH3}", size=EQ_SMALL - 2, color=PROP).move_to([2.6, -0.85, 0])
            self.play(FadeIn(eth), FadeIn(pro), run_time=0.7)
            ring = SurroundingRectangle(eth[1], color=LOSS, buff=0.03)
            lab = T("already partly oxidised", size=SMALL + 2, color=LOSS).next_to(ring, DOWN, buff=0.15)
            b.until(0.3)
            self.play(Create(ring), FadeIn(lab), run_time=0.7)
            lt = T("less left to oxidise → less energy released", size=LABEL, color=UNKNOWN).move_to([0, -1.85, 0])
            b.until(0.65)
            self.play(FadeIn(lt), run_time=0.5)
        with self.beat("b03") as b:
            note = T("explain with partial oxidation; “different bond enthalpies” alone isn't enough", size=SMALL + 2,
                     color=GOOD).move_to([0, -2.45, 0])
            self.play(FadeIn(note), run_time=0.6)


# =====================================================================================
class E12S05_Normalise(NarratedScene):
    def construct(self):
        h = header("Normalise to the same useful output")
        boxes = [("1.00 MJ useful heat", USEFUL), ("fuel energy input (MJ)", SYSTEM), ("mass of fuel (kg)", MASS_C), ("emissions (g)", CO2E)]
        nodes = VGroup()
        for t, c in boxes:
            tx = T(t, size=LABEL, color=c)
            r = RoundedRectangle(width=tx.width + 0.5, height=0.8, corner_radius=0.12, stroke_color=c, stroke_width=2.5,
                                 fill_color=PANEL, fill_opacity=1)
            nodes.add(VGroup(r, tx.move_to(r)))
        nodes[0].move_to([-4.95, 1.3, 0])
        nodes[1].move_to([-0.2, 1.3, 0])
        nodes[2].move_to([4.85, 1.3, 0])
        nodes[3].move_to([-0.2, -1.0, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(nodes[0]), run_time=0.8)
            fix = T("fix the task first", size=SMALL + 1, color=MUTED).next_to(nodes[0], UP, buff=0.15)
            self.play(FadeIn(fix), run_time=0.4)
        a1 = Arrow(nodes[0].get_right(), nodes[1].get_left(), buff=0.1, color=TEXT, stroke_width=4)
        l1 = M(r"\div\ \text{efficiency}", size=EQ_SMALL - 10, color=SYSTEM).next_to(a1, DOWN, buff=0.52)
        a2 = Arrow(nodes[1].get_right(), nodes[2].get_left(), buff=0.1, color=TEXT, stroke_width=4)
        l2 = M(r"\div\ \text{MJ kg}^{-1}", size=EQ_SMALL - 10, color=MASS_C).next_to(a2, UP, buff=0.08)
        a3 = Arrow(nodes[1].get_bottom(), nodes[3].get_top(), buff=0.1, color=TEXT, stroke_width=4)
        l3 = M(r"\times\ \text{g CO}_2\text{-e per MJ input}", size=EQ_SMALL - 10, color=CO2E).next_to(a3, RIGHT, buff=0.15)
        with self.beat("b02") as b:
            self.play(GrowArrow(a1), FadeIn(l1), FadeIn(nodes[1]), run_time=0.9)
            b.until(0.35)
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(nodes[2]), run_time=0.9)
            b.until(0.7)
            self.play(GrowArrow(a3), FadeIn(l3), FadeIn(nodes[3]), run_time=0.9)
        with self.beat("b03") as b:
            u = VGroup(M(r"\text{MJ} \div \text{MJ kg}^{-1} = \text{kg}", size=EQ_SMALL - 6, color=MASS_C),
                       M(r"\text{MJ} \times \text{g MJ}^{-1} = \text{g}", size=EQ_SMALL - 6, color=CO2E)).arrange(RIGHT, buff=1.2).move_to([0, -2.3, 0])
            self.play(Write(u), run_time=1.2)


# =====================================================================================
class E12S06_Q23(NarratedScene):
    def construct(self):
        h = header("Practice Q23")
        qc = question_card("Q23").move_to([0, 0.3, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        req = requested("per 1.00 MJ useful heat")
        hyp = T("hypothetical data", size=SMALL, color=MUTED).next_to(req, DOWN, buff=0.1).align_to(req, RIGHT)
        xR, xS = -3.3, 3.3
        hR = TB("Fossil Fuel R", size=LABEL + 2, color=FOSSIL).move_to([xR, 2.25, 0])
        hS = TB("Biofuel S", size=LABEL + 2, color=BIO).move_to([xS, 2.25, 0])

        def row(x, tex, y, col):
            return M(tex, size=EQ_SMALL - 8, color=col).move_to([x, y, 0])
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(req), FadeIn(hyp), FadeIn(hR), FadeIn(hS), run_time=0.7)
            r1 = row(xR, r"\text{input} = \frac{1.00}{0.350} = 2.857\ \text{MJ}", 1.5, SYSTEM)
            s1 = row(xS, r"\text{input} = \frac{1.00}{0.280} = 3.571\ \text{MJ}", 1.5, SYSTEM)
            self.play(Write(r1), run_time=1.0)
            b.until(0.5)
            self.play(Write(s1), run_time=1.0)
        with self.beat("b03") as b:
            r2 = row(xR, r"m = \frac{2.857}{43.0} = 0.0664\ \text{kg}", 0.6, MASS_C)
            s2 = row(xS, r"m = \frac{3.571}{29.0} = 0.123\ \text{kg}", 0.6, MASS_C)
            self.play(Write(r2), run_time=1.0)
            b.until(0.45)
            self.play(Write(s2), run_time=1.0)
            less = T("R: less mass", size=SMALL + 1, color=FOSSIL).next_to(r2, DOWN, buff=0.1)
            self.play(FadeIn(less), run_time=0.4)
        with self.beat("b04") as b:
            r3 = row(xR, r"2.857 \times 80.0 = 229\ \text{g CO}_2\text{-e}", -0.35, CO2E)
            s3 = row(xS, r"3.571 \times 45.0 = 161\ \text{g CO}_2\text{-e}", -0.35, CO2E)
            self.play(Write(r3), run_time=1.0)
            b.until(0.45)
            self.play(Write(s3), run_time=1.0)
            lower = T("S: lower lifecycle emissions", size=SMALL + 1, color=BIO).next_to(s3, DOWN, buff=0.1)
            self.play(FadeIn(lower), run_time=0.4)
        with self.beat("b05") as b:
            ev = right_panel("Evaluation", ["False here: R needs less mass, but S emits less for the same useful heat. "
                                            "Mass and emissions measure different things."], width=10.5, size=LABEL)
            ev.move_to([0, -1.88, 0])
            self.play(FadeIn(ev), run_time=0.9)
            mk = T("marks: 2 inputs · 2 masses · 2 emissions · 1 evaluation", size=SMALL + 1, color=GOOD).to_corner(UL, buff=0.4).shift(0.8 * DOWN)
            b.until(0.75)
            self.play(FadeIn(mk), run_time=0.5)


# =====================================================================================
class E12S07_Checkpoint(NarratedScene):
    def construct(self):
        h = header("Checkpoint: per input vs per useful output")
        hyp = T("hypothetical data", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
        d = VGroup(T("R: 80 g CO₂-e per MJ input, 35% efficient", size=LABEL + 2, color=FOSSIL),
                   T("T: 70 g CO₂-e per MJ input, 20% efficient", size=LABEL + 2, color=SURR)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        d.move_to([0, 2.0, 0])
        b1 = hbars([("R", 80, FOSSIL), ("T", 70, SURR)], 1 / 95, x_left=-3.0, y0=0.55, unit=" g per MJ input")
        t1 = T("per MJ of fuel energy input: T looks better", size=LABEL, color=MUTED).next_to(b1, UP, buff=0.12).align_to(b1, LEFT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(hyp), FadeIn(d), run_time=0.9)
            self.play(FadeIn(t1), FadeIn(b1), run_time=0.9)
            q = T("Which is lower per MJ of useful heat?", size=LABEL + 2, color=UNKNOWN).move_to([0, -0.85, 0])
            self.play(FadeIn(q), run_time=0.5)
            self.q = q
        with self.beat("b02") as b:
            self.play(FadeOut(self.q), run_time=0.3)
            b2 = hbars([("R", 228.6, FOSSIL), ("T", 350, SURR)], 1 / 95, x_left=-3.0, y0=-1.4, unit=" g per useful MJ")
            t2 = T("per MJ of useful heat (÷ efficiency): R is better", size=LABEL, color=UNKNOWN).next_to(b2, UP, buff=0.12).align_to(b2, LEFT)
            c = VGroup(M(r"80 \div 0.35 = 229", size=EQ_SMALL - 10, color=FOSSIL), M(r"70 \div 0.20 = 350", size=EQ_SMALL - 10, color=SURR)).arrange(DOWN, buff=0.2)
            c.move_to([5.4, -1.7, 0])
            self.play(FadeIn(t2), FadeIn(b2), run_time=1.0)
            self.play(Write(c), run_time=0.8)


# =====================================================================================
class E12S08_Boundary(NarratedScene):
    def construct(self):
        h = header("Drawing the system boundary")
        stages = ["grow\nfeedstock", "fertiliser,\nmachines", "processing\nenergy", "transport", "COMBUSTION"]
        cols = [BIO, BIO, SYSTEM, MUTED, SYSTEM]
        nodes = VGroup()
        for s_, c in zip(stages, cols):
            tx = VGroup(*[T(l, size=SMALL, color=c) for l in s_.split("\n")]).arrange(DOWN, buff=0.05)
            r = RoundedRectangle(width=2.15, height=0.95, corner_radius=0.12, stroke_color=c, stroke_width=2.5,
                                 fill_color=PANEL, fill_opacity=1)
            nodes.add(VGroup(r, tx.move_to(r)))
        nodes.arrange(RIGHT, buff=0.32).move_to([0, 0.2, 0])
        arrows = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.03, color=FAINT, stroke_width=3,
                                max_tip_length_to_length_ratio=0.4) for i in range(4)])
        inner = DashedVMobject(SurroundingRectangle(nodes[4], color=UNKNOWN, buff=0.2, corner_radius=0.1), num_dashes=30)
        it = T("operational (direct) emissions", size=LABEL, color=UNKNOWN).next_to(inner, UP, buff=0.15).align_to(inner, RIGHT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(nodes[4]), run_time=0.7)
            self.play(Create(inner), FadeIn(it), run_time=0.8)
        outer = DashedVMobject(SurroundingRectangle(nodes, color=GOOD, buff=0.18, corner_radius=0.15), num_dashes=80)
        ot = T("lifecycle emissions", size=LABEL + 2, color=GOOD).next_to(outer, DOWN, buff=0.15)
        with self.beat("b02") as b:
            self.play(FadeIn(nodes[:4]), Create(arrows), run_time=1.2)
            b.until(0.5)
            self.play(it.animate.shift(0.0 * UP), Create(outer), FadeIn(ot), run_time=1.2)
        with self.beat("b03") as b:
            tip = nodes[2].get_top() + 1.3 * UP + 0.9 * LEFT
            leak = DashedVMobject(Arrow(nodes[2].get_top(), tip, buff=0.05, color=LOSS, stroke_width=5), num_dashes=8)
            lt = T("CH₄ leakage: a potent greenhouse gas", size=LABEL, color=LOSS).next_to(tip, LEFT, buff=0.1)
            self.play(Create(leak), FadeIn(lt), run_time=0.9)
            say = T("Every emission claim should state its boundary", size=LABEL + 2, color=UNKNOWN).move_to([0, -2.3, 0])
            b.until(0.6)
            self.play(FadeIn(say), run_time=0.6)


# =====================================================================================
class E12S09_Neutral(NarratedScene):
    def construct(self):
        h = header("Is a biofuel carbon neutral?")
        claim = T("“Our biofuel is carbon neutral: the crop absorbed the CO₂ it releases.”", size=LABEL + 1)
        claim.move_to([0, 2.15, 0])

        def node(text, color, pos):
            t = T(text, size=SMALL + 2, color=color)
            r = RoundedRectangle(width=t.width + 0.4, height=0.62, corner_radius=0.12, stroke_color=color,
                                 stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
            return VGroup(r, t.move_to(r)).move_to(pos)
        air = node("CO₂ in the air", CO2E, [-3.45, 1.1, 0])
        crop = node("growing crop", BIO, [-5.45, -0.45, 0])
        fuel = node("biofuel", SYSTEM, [-3.45, -2.0, 0])
        burn = node("combustion", LOSS, [-1.45, -0.45, 0])
        cyc = VGroup(
            CurvedArrow(air.get_left() + 0.05 * DOWN, crop.get_top(), angle=0.6, color=BIO, stroke_width=3),
            CurvedArrow(crop.get_bottom(), fuel.get_left(), angle=0.6, color=BIO, stroke_width=3),
            CurvedArrow(fuel.get_right(), burn.get_bottom(), angle=0.6, color=LOSS, stroke_width=3),
            CurvedArrow(burn.get_top(), air.get_right() + 0.05 * DOWN, angle=0.6, color=LOSS, stroke_width=3))
        ph = T("photosynthesis", size=SMALL, color=BIO).move_to([-5.55, 0.6, 0])
        x0 = 0.9
        extras = VGroup(*[T(t, size=SMALL + 1, color=c) for t, c in (
            ("+ fertiliser production", SYSTEM), ("+ farm machinery", SYSTEM), ("+ processing heat", SYSTEM),
            ("+ transport", SYSTEM), ("+ methane leakage (some systems)", LOSS))]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        extras.move_to([0, 0.0, 0]).align_to([x0, 0, 0], LEFT)
        eh = TB("extra lifecycle emissions", size=LABEL, color=SYSTEM).next_to(extras, UP, buff=0.2).align_to(extras, LEFT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(claim), run_time=0.9)
            q = chip("fully justified?", UNKNOWN, size=SMALL + 2).next_to(claim, DOWN, buff=0.2)
            b.until(0.6)
            self.play(FadeIn(q), run_time=0.4)
            self.qc = q
        with self.beat("b02") as b:
            self.play(FadeOut(self.qc), FadeIn(air), run_time=0.5)
            self.play(Create(cyc[0]), FadeIn(ph), FadeIn(crop), run_time=0.8)
            self.play(Create(cyc[1]), FadeIn(fuel), run_time=0.6)
            b.until(0.5)
            self.play(Create(cyc[2]), FadeIn(burn), run_time=0.6)
            self.play(Create(cyc[3]), run_time=0.6)
            sc = VGroup(T("short-term", size=SMALL, color=BIO), T("carbon cycle", size=SMALL, color=BIO)).arrange(DOWN, buff=0.06)
            sc.move_to([-3.45, -0.45, 0])
            b.until(0.75)
            self.play(FadeIn(sc), run_time=0.5)
        with self.beat("b03") as b:
            self.play(FadeIn(eh), run_time=0.4)
            for i, fr in enumerate((0.05, 0.13, 0.2, 0.27, 0.36)):
                b.until(fr)
                self.play(FadeIn(extras[i], shift=0.1 * LEFT), run_time=0.4)
            v = right_panel("Verdict", [wrapped("lower-carbon is possible; “carbon neutral” needs lifecycle evidence",
                                                size=SMALL + 1, width=4.8)], size=SMALL + 1, width=4.8, color=UNKNOWN)
            v.move_to([0, -1.85, 0]).align_to([x0, 0, 0], LEFT)
            b.until(0.6)
            self.play(FadeIn(v), run_time=0.7)


# =====================================================================================
class E12S10_Sustainable(NarratedScene):
    def construct(self):
        h = header("Renewable is not the same as sustainable")
        tr = VGroup(card("Land", ["fuel crops can displace food crops"], BAD, 3.0),
                    card("Water", ["irrigation can use a lot of fresh water"], SURR, 3.0),
                    card("Habitat", ["clearing land reduces biodiversity"], BIO, 3.0)).arrange(RIGHT, buff=0.35).move_to([0, 1.5, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for i, c in enumerate(tr):
                b.until(0.15 + 0.22 * i)
                self.play(FadeIn(c, shift=0.1 * UP), run_time=0.5)
        names = ["food waste", "digester", "biogas → heat", "digestate → fertiliser", "crops → food"]
        cols = [MUTED, SYSTEM, USEFUL, BIO, GOOD]
        R = 1.8
        cx, cy = -2.7, -0.75
        nodes = VGroup()
        for k, (n, c) in enumerate(zip(names, cols)):
            ang = PI / 2 - k * 2 * PI / 5
            t = T(n, size=SMALL + 1, color=c)
            r = RoundedRectangle(width=t.width + 0.3, height=0.55, corner_radius=0.12, stroke_color=c, stroke_width=2,
                                 fill_color=PANEL, fill_opacity=1)
            nodes.add(VGroup(r, t.move_to(r)).move_to([cx + R * 1.35 * np.cos(ang), cy + R * 0.62 * np.sin(ang), 0]))
        loop = VGroup(*[CurvedArrow(nodes[k].get_center(), nodes[(k + 1) % 5].get_center(), angle=-PI / 5, color=FAINT,
                                    stroke_width=3) for k in range(5)])
        for a in loop:
            a.set_z_index(-1)
        with self.beat("b02") as b:
            tsum = T("trade-offs: land · water · habitat", size=LABEL, color=MUTED).move_to([0, 2.45, 0])
            self.play(FadeOut(tr), FadeIn(tsum), run_time=0.6)
            for k in range(5):
                self.play(FadeIn(nodes[k]), Create(loop[k]), run_time=0.45)
            circ = T("waste becomes an input: materials stay in use", size=SMALL + 1, color=GOOD).move_to([cx, cy - 1.55, 0])
            self.play(FadeIn(circ), run_time=0.5)
        gc = VGroup(TB("Green chemistry principles", size=LABEL, color=GOOD),
                    T("• use renewable feedstocks", size=SMALL + 1), T("• prevent waste", size=SMALL + 1),
                    T("• design for energy efficiency", size=SMALL + 1), T("• use catalysts (e.g. enzymes)", size=SMALL + 1),
                    T("• high atom economy", size=SMALL + 1)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        gc.move_to([4.2, 0.65, 0])
        with self.beat("b03") as b:
            self.play(FadeIn(gc[0]), run_time=0.4)
            for i in range(1, 6):
                b.until(0.06 + 0.16 * i)
                self.play(FadeIn(gc[i]), run_time=0.4)
        with self.beat("b04") as b:
            sdg = VGroup(*[chip(s, c, size=SMALL) for s, c in [("SDG 7 energy", UNKNOWN), ("SDG 12 production", SURR),
                                                                 ("SDG 13 climate", GOOD), ("SDG 2 hunger", BAD)]])
            sdg.arrange_in_grid(2, 2, buff=0.15).move_to([4.2, -1.4, 0])
            self.play(LaggedStart(*[FadeIn(s_) for s_ in sdg], lag_ratio=0.25), run_time=1.4)


# =====================================================================================
class E12S11_Q24(NarratedScene):
    def construct(self):
        h = header("Practice Q24")
        qc = question_card("Q24", size=SMALL + 1, width=13.0, cols=2).move_to([0, 0.2, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        rows = [["per kg ethanol", "Process A", "Process B"],
                ["feedstock", "edible crop", "food-processing waste"],
                ["energy", "8 MJ natural-gas heat", "10 MJ electricity (60% renewable)"],
                ["fresh water", "12 L", "20 L"],
                ["fermentation CO₂", "vented", "captured and used"]]
        tb = table(rows, [3.0, 3.6, 4.6], size=SMALL + 1, row_h=0.5).move_to([0, 1.5, 0])
        sent_y = [-0.75, -1.5, -2.15]
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(tb), run_time=0.9)
            s1 = wrapped("1. Feedstock: B uses waste, not an edible crop, so it avoids competing with food and keeps materials in use "
                         "(renewable feedstocks; circular economy).", size=SMALL + 1, width=12.6, color=GOOD)
            s1.move_to([0, sent_y[0], 0]).align_to([-6.0, 0, 0], LEFT)
            hl = SurroundingRectangle(VGroup(*tb[1][3:6]), color=GOOD, buff=0.05)
            b.until(0.3)
            self.play(Create(hl), FadeIn(s1), run_time=1.0)
            self.hl = hl
        with self.beat("b03") as b:
            s2 = wrapped("2. Resources: A uses less listed energy (8 vs 10 MJ) and less fresh water (12 vs 20 L) per kg.",
                         size=SMALL + 1, width=12.6, color=SURR)
            s2.move_to([0, sent_y[1], 0]).align_to([-6.0, 0, 0], LEFT)
            hl2 = SurroundingRectangle(VGroup(*tb[1][6:12]), color=SURR, buff=0.05)
            self.play(ReplacementTransform(self.hl, hl2), FadeIn(s2), run_time=1.0)
            self.hl = hl2
        with self.beat("b04") as b:
            s3 = wrapped("3. Trade-off: B wins on feedstock and CO₂ use; A wins on energy and water. Using CO₂ is not permanent storage.",
                         size=SMALL + 1, width=12.6, color=UNKNOWN)
            s3.move_to([0, sent_y[2], 0]).align_to([-6.0, 0, 0], LEFT)
            self.play(FadeOut(self.hl), FadeIn(s3), run_time=1.0)
            self.sents = VGroup(s3)
        with self.beat("b05") as b:
            lim = wrong_panel("Can't conclude total lifecycle emissions", ["no emission factors for the gas heat or the 40% non-renewable "
                                                                            "electricity; no transport or feedstock data"],
                              width=11.6, size=SMALL + 1)
            lim.move_to([0, 0.9, 0])
            self.play(*[FadeOut(m) for m in self.mobjects if m is not h], run_time=0.5)
            self.play(FadeIn(lim), run_time=0.9)
            self.lim = lim
        with self.beat("b06") as b:
            rec = right_panel("Conditional recommendation", ["If avoiding food competition is the priority, choose B, accepting its higher energy and water use. "
                                                              "Either choice is defensible if it follows the stated priorities."], width=11.6, size=SMALL + 1)
            rec.move_to([0, -0.8, 0])
            self.play(FadeIn(rec), run_time=0.9)
            mk = T("marks: 2 + 2 comparisons · 1 trade-off or limit · 1 consistent conditional conclusion", size=SMALL + 1, color=GOOD).move_to([0, -2.3, 0])
            b.until(0.7)
            self.play(FadeIn(mk), run_time=0.5)


# =====================================================================================
class E12S12_Recap(NarratedScene):
    def construct(self):
        h = header("Recap")
        items = bullets(["State the basis: per mole, per gram, or per useful energy",
                         "Same task → same useful output → divide by efficiency",
                         "Say which boundary an emission claim uses (operational vs lifecycle)",
                         "Renewable ≠ sustainable: land, food, water, leakage, processing energy"], size=LABEL + 2, width=12.0, buff=0.35)
        items.move_to([0, 0.3, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for i, it in enumerate(items):
                b.until(0.05 + 0.2 * i)
                self.play(FadeIn(it, shift=0.1 * RIGHT), run_time=0.6)
        with self.beat("b02") as b:
            self.play(FadeOut(items), run_time=0.4)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN),
                       T("Name two reasons a renewable biofuel might not be sustainable.", size=BODY)).arrange(DOWN, buff=0.35).move_to([0, 1.0, 0])
            self.play(FadeIn(q), run_time=0.8)
            self.q = q
        with self.beat("b03") as b:
            a = bullets(["crop competes with food for land, or uses a lot of water",
                         "methane leaks during production",
                         "processing relies on fossil energy"], size=LABEL + 2, width=10.0, color=GOOD, buff=0.2)
            a.next_to(self.q, DOWN, buff=0.45)
            self.play(FadeIn(a), run_time=0.9)
            b.until(0.6)
            nxt = T("Next: Episode 13 · Exam workshop A on fuels and combustion", size=LABEL, color=MUTED).move_to([0, -2.35, 0])
            self.play(FadeIn(nxt), run_time=0.5)


EPISODE_SCENES = ["E12S01_Retrieval", "E12S02_Bases", "E12S03_PerLitre", "E12S04_Oxygenated",
                  "E12S05_Normalise", "E12S06_Q23", "E12S07_Checkpoint", "E12S08_Boundary", "E12S09_Neutral",
                  "E12S10_Sustainable", "E12S11_Q24", "E12S12_Recap"]
