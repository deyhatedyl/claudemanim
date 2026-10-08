"""
Episode 11 - Temperature graphs, correction and experimental reasoning.
Narration: scripts/ep11.md (beat names must match).
All plotted points are the Q21 data exactly; the fit is recomputed from the data (np.polyfit).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (bullets, data_points, linfit, mark_tally, question_card, result_box,  # noqa: E402
                               right_panel, table, temp_axes, title_card, wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, ENERGY_C, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, LOSS, MUTED,  # noqa: E402
                          PANEL, SMALL, SURR, SYSTEM, TEMP_C, TEXT, UNKNOWN, USEFUL, M, T, TB, chip, header,
                          panel)

PRE = [(0, 21.0), (60, 21.0), (120, 21.0)]
POST = [(135, 23.0), (150, 25.0), (165, 26.0), (180, 26.1), (240, 25.9), (300, 25.7), (360, 25.5)]
COOL = [(180, 26.1), (240, 25.9), (300, 25.7), (360, 25.5)]
SLOPE, ICPT = linfit(COOL)
T_MIX = SLOPE * 120 + ICPT
assert abs(T_MIX - 26.3) < 1e-9


def requested(text: str) -> VGroup:
    from shared.style import asked_pill
    return asked_pill(text)


def q21_plot(center=(-2.0, -0.15, 0), width=7.2, height=3.8):
    g = temp_axes(x_max=420, x_step=60, y_min=20, y_max=27, width=width, height=height)
    g.move_to(center)
    return g


# =====================================================================================
class E11S01_Retrieval(NarratedScene):
    def construct(self):
        tc = title_card(11, "Temperature graphs, correction and experimental reasoning")
        with self.beat("b01"):
            self.play(FadeIn(tc, shift=0.2 * UP), run_time=1.5)
        with self.beat("b02") as b:
            self.play(FadeOut(tc), run_time=0.5)
            h = header("Retrieval check")
            q1 = T("1.  Heat escapes during electrical calibration: CF too large or too small?", size=LABEL + 4)
            q2 = T("2.  A reaction warms the calorimeter: is ΔH positive or negative?", size=LABEL + 4)
            qs = VGroup(q1, q2).arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to([0, 0.9, 0])
            self.play(FadeIn(h), FadeIn(q1), run_time=0.7)
            b.until(0.5)
            self.play(FadeIn(q2), run_time=0.6)
            self.qs = qs
        with self.beat("b03") as b:
            a1 = T("too large: ΔT smaller, CF = E ÷ ΔT", size=BODY, color=GOOD).next_to(self.qs[0], DOWN, buff=0.15).align_to(self.qs[0], LEFT).shift(0.6 * RIGHT)
            a2 = T("negative: energy transferred to the calorimeter", size=BODY, color=GOOD).next_to(self.qs[1], DOWN, buff=0.15).align_to(self.qs[1], LEFT).shift(0.6 * RIGHT)
            self.play(FadeIn(a1), run_time=0.6)
            b.until(0.5)
            self.play(FadeIn(a2), run_time=0.6)


# =====================================================================================
class E11S02_ReadGraph(NarratedScene):
    def construct(self):
        h = header("Reading a temperature-time graph")
        pg = q21_plot()
        ax = pg.ax
        pre = data_points(ax, PRE)
        post = data_points(ax, POST)
        src = wrapped("data: practice question Q21 (measured points only)", size=SMALL, width=3.6, color=MUTED).move_to([4.6, -1.6, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(src), Create(pg.ax), FadeIn(pg.grid), run_time=1.2)
            self.play(FadeIn(pg[2]), FadeIn(pg[3]), run_time=0.6)
        notes_x = 4.6
        with self.beat("b02") as b:
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pre], lag_ratio=0.3), run_time=1.0)
            base = T("baseline 21.0 °C", size=LABEL, color=SURR).move_to([notes_x, 1.6, 0])
            mix = DashedLine(ax.c2p(120, 20), ax.c2p(120, 27), color=UNKNOWN, stroke_width=2.5)
            mixt = T("mixing, t = 120 s", size=LABEL, color=UNKNOWN).move_to([notes_x, 1.0, 0])
            self.play(FadeIn(base), run_time=0.5)
            b.until(0.5)
            self.play(Create(mix), FadeIn(mixt), run_time=0.8)
        with self.beat("b03") as b:
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in post[:4]], lag_ratio=0.3), run_time=1.6)
            mx = Circle(radius=0.16, color=SYSTEM, stroke_width=3).move_to(post[3])
            mxt = T("highest reading 26.1 °C", size=LABEL, color=SYSTEM).move_to([notes_x, 0.4, 0])
            b.until(0.6)
            self.play(Create(mx), FadeIn(mxt), run_time=0.7)
        with self.beat("b04") as b:
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in post[4:]], lag_ratio=0.3), run_time=1.2)
            cr = Brace(VGroup(post[3], post[6]), DOWN, color=SURR, buff=0.4)
            crt = T("cooling region: steady fall", size=LABEL, color=SURR).move_to([notes_x, -0.2, 0])
            b.until(0.55)
            self.play(GrowFromCenter(cr), FadeIn(crt), run_time=0.8)


# =====================================================================================
class E11S03_PeakTooLow(NarratedScene):
    def construct(self):
        h = header("Why the highest reading is too low")
        pg = q21_plot()
        ax = pg.ax
        pts = data_points(ax, PRE + POST)
        self.add(h, pg, pts)
        with self.beat("b01") as b:
            arrows = VGroup(*[DashedVMobject(Arrow(ax.c2p(x, y) + 0.1 * UP, ax.c2p(x, y) + 0.9 * UP + 0.4 * RIGHT, buff=0,
                                                   color=LOSS, stroke_width=4), num_dashes=6)
                              for x, y in [(135, 23.0), (150, 25.0), (165, 26.0)]])
            lab = wrapped("heat already escaping while the reaction is still going", size=LABEL, width=3.8, color=LOSS).move_to([4.6, 1.2, 0])
            self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.3), run_time=1.4)
            self.play(FadeIn(lab), run_time=0.6)
        with self.beat("b02") as b:
            mx = Circle(radius=0.16, color=SYSTEM, stroke_width=3).move_to(pts[6])
            t = wrapped("so the highest reading underestimates the rise, and the heat released", size=LABEL, width=3.8, color=SYSTEM)
            t.move_to([4.6, -0.3, 0])
            self.play(Create(mx), FadeIn(t), run_time=0.9)


# =====================================================================================
class E11S04_Extrapolate(NarratedScene):
    def construct(self):
        from shared.motion import trace
        h = header("Extrapolating the cooling line")
        pg = q21_plot()
        ax = pg.ax
        pts = data_points(ax, PRE + POST)
        self.add(h, pg, pts)
        fit = Line(ax.c2p(180, SLOPE * 180 + ICPT), ax.c2p(360, SLOPE * 360 + ICPT), color=SURR, stroke_width=4)
        col = 4.75
        with self.beat("b01") as b:
            self.play(Create(fit), run_time=1.2)
            ft = T("best straight line (exact here)", size=LABEL, color=SURR).move_to([col, 1.9, 0])
            self.play(FadeIn(ft), run_time=0.5)
            self.ft = ft
        with self.beat("b02") as b:
            tri = VGroup(DashedLine(ax.c2p(180, 26.1), ax.c2p(360, 26.1), color=MUTED, stroke_width=2),
                         DashedLine(ax.c2p(360, 26.1), ax.c2p(360, 25.5), color=MUTED, stroke_width=2))
            run = T("180 s", size=SMALL, color=MUTED).next_to(tri[0], UP, buff=0.05)
            rise = T("−0.6 °C", size=SMALL, color=MUTED).next_to(tri[1], LEFT, buff=0.08)
            self.play(Create(tri), FadeIn(run), FadeIn(rise), run_time=1.0)
            sl = M(r"\text{slope} = \frac{-0.6}{180} = -0.00333\ {}^{\circ}\text{C s}^{-1}", size=EQ_SMALL - 10, color=SURR).move_to([col, 1.25, 0])
            b.until(0.4)
            self.play(Write(sl), run_time=1.2)
            self.tri = VGroup(tri, run, rise)
        with self.beat("b03") as b:
            self.play(FadeOut(self.tri), run_time=0.3)
            ext = DashedLine(ax.c2p(180, 26.1), ax.c2p(120, T_MIX), color=SURR, stroke_width=4, dash_length=0.1)
            trace(self, ext, SURR, run_time=1.4)
            corr = Square(side_length=0.2, color=UNKNOWN, fill_color=UNKNOWN, fill_opacity=1).rotate(PI / 4).move_to(ax.c2p(120, T_MIX))
            ct = M(r"26.1 + 60 \times 0.00333 = 26.3\ {}^{\circ}\text{C}", size=EQ_SMALL - 10, color=UNKNOWN).move_to([col, 0.6, 0])
            b.until(0.5)
            self.play(FadeIn(corr, scale=1.6), Write(ct), run_time=1.0)
            mk = VGroup(VGroup(Dot(radius=0.07, color=TEXT), T("measured", size=SMALL, color=MUTED)).arrange(RIGHT, buff=0.12),
                        VGroup(Square(side_length=0.16, color=UNKNOWN, fill_opacity=1).rotate(PI / 4), T("extrapolated estimate", size=SMALL, color=MUTED)).arrange(RIGHT, buff=0.12))
            mk.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([col, -2.25, 0])
            self.play(FadeIn(mk), run_time=0.4)
        with self.beat("b04") as b:
            obs = DoubleArrow(ax.c2p(200, 21.0), ax.c2p(200, 26.1), buff=0, color=SYSTEM, stroke_width=3, tip_length=0.15)
            cor = DashedVMobject(DoubleArrow(ax.c2p(105, 21.0), ax.c2p(105, T_MIX), buff=0, color=UNKNOWN, stroke_width=3, tip_length=0.15), num_dashes=16)
            ob_t = M(r"\text{observed: } 26.1 - 21.0 = 5.1\ {}^{\circ}\text{C}", size=EQ_SMALL - 10, color=SYSTEM).move_to([col, -0.05, 0])
            co_t = M(r"\text{corrected: } 26.3 - 21.0 = 5.3\ {}^{\circ}\text{C}", size=EQ_SMALL - 10, color=UNKNOWN).move_to([col, -0.65, 0])
            self.play(GrowFromCenter(obs), Write(ob_t), run_time=1.0)
            b.until(0.45)
            self.play(Create(cor), Write(co_t), run_time=1.0)
            lg = T("solid: observed · dashed: corrected", size=SMALL, color=MUTED).move_to([col - 0.2, -1.2, 0])
            self.play(FadeIn(lg), run_time=0.4)
            self.side = VGroup(sl, ct, ob_t, co_t, lg)
        with self.beat("b05") as b:
            caut = wrapped("26.3 °C is a model-based estimate: it assumes a constant cooling rate and that the reaction "
                           "happened at the moment of mixing. Better than the raw maximum, not a perfect recovery.",
                           size=SMALL + 1, width=3.7, color=UNKNOWN)
            cp = panel(caut, color=UNKNOWN, buff=0.15)
            VGroup(cp, caut).move_to([col, 0.6, 0])
            self.play(FadeOut(self.ft), FadeOut(self.side), run_time=0.5)
            self.play(FadeIn(cp), FadeIn(caut), run_time=0.9)


# =====================================================================================
class E11S05_Q21(NarratedScene):
    def construct(self):
        h = header("Practice Q21")
        qc = question_card("Q21", size=SMALL + 2).move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        req = requested("corrected heat; comparison")
        colL = -6.3

        def L(tex, y, col=TEXT, s=EQ_SMALL - 6):
            return M(tex, size=s, color=col).move_to([0, y, 0]).align_to([colL, 0, 0], LEFT)
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(req), run_time=0.5)
            a = L(r"\text{a. slope} = -0.00333\ {}^{\circ}\text{C s}^{-1};\ T(120\ \text{s}) = 26.1 + 0.2 = 26.3\ {}^{\circ}\text{C}", 2.2, SURR)
            bb = L(r"\text{b. corrected rise} = 26.3 - 21.0 = 5.3\ {}^{\circ}\text{C}", 1.45, UNKNOWN)
            self.play(Write(a), run_time=1.4)
            b.until(0.55)
            self.play(Write(bb), run_time=1.0)
        with self.beat("b03") as b:
            c = L(r"\text{c. } q = 650 \times 5.3 = 3445\ \text{J} \approx 3.4\ \text{kJ}", 0.65, GOOD)
            self.play(Write(c), run_time=1.2)
            sf = T("2 significant figures: the rise is a graph estimate", size=SMALL + 1, color=MUTED).next_to(c, RIGHT, buff=0.3)
            b.until(0.6)
            self.play(FadeIn(sf), run_time=0.5)
        with self.beat("b04") as b:
            d = L(r"\text{d. observed max: } 650 \times 5.1 = 3315\ \text{J} \approx 3.3\ \text{kJ}", -0.15, SYSTEM)
            self.play(Write(d), run_time=1.2)
            u = T("underestimate: cooling had already begun before the peak", size=LABEL, color=SYSTEM).next_to(d, DOWN, buff=0.2).align_to(d, LEFT)
            b.until(0.6)
            self.play(FadeIn(u), run_time=0.6)
        with self.beat("b05") as b:
            self.clear(h, req)
            tally = mark_tally([(2, "cooling region and extrapolation to 26.3 °C"), (1, "corrected rise 5.3 °C"),
                                (1, "corrected heat ≈ 3.4 kJ"), (1, "comparison: observed max underestimates")], width=6.2).move_to([-3.2, 0.3, 0])
            ws = VGroup(wrong_panel("Observed max used as corrected", [T("5.1 °C → 3.3 kJ", size=LABEL)], width=4.8),
                        wrong_panel("Temperature read as ΔT", [T("26.3 °C used as the rise", size=LABEL)], width=4.8))
            ws.arrange(DOWN, buff=0.3).move_to([3.5, 0.3, 0])
            self.play(FadeIn(tally), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(ws), run_time=0.8)


# =====================================================================================
DRAW_PRE = [(0, 21.0), (60, 21.0), (120, 21.0)]
DRAW_RISE = [(135, 23.4), (150, 25.2), (165, 25.95)]
DRAW_COOL = [(195, 26.08), (225, 25.93), (255, 25.86), (285, 25.70), (315, 25.62), (345, 25.47), (375, 25.42),
             (405, 25.27)]


class E11S06_Drawing(NarratedScene):
    def construct(self):
        h = header("Drawing the extrapolation well")
        pg = q21_plot()
        ax = pg.ax
        pts = data_points(ax, DRAW_PRE + DRAW_RISE + DRAW_COOL)
        hyp = T("hypothetical readings", size=SMALL, color=MUTED).move_to([4.75, -2.35, 0])
        col = 4.75
        m_g, c_g = linfit(DRAW_COOL)
        m_p, c_p = linfit(DRAW_RISE[1:] + DRAW_COOL)
        mix = DashedLine(ax.c2p(120, 20), ax.c2p(120, 27), color=UNKNOWN, stroke_width=2.5)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(pg), FadeIn(hyp), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in pts], lag_ratio=0.12), run_time=1.6)
            self.play(Create(mix), run_time=0.5)
        with self.beat("b02") as b:
            poor = DashedLine(ax.c2p(120, m_p * 120 + c_p), ax.c2p(405, m_p * 405 + c_p), color=BAD, stroke_width=3)
            pd = Dot(ax.c2p(120, m_p * 120 + c_p), radius=0.08, color=BAD)
            pt = T("includes rising points ✗", size=SMALL + 1, color=BAD).move_to([col, 1.9, 0])
            ring = VGroup(*[Circle(radius=0.14, color=BAD, stroke_width=2.5).move_to(ax.c2p(*p)) for p in DRAW_RISE[1:]])
            b.until(0.2)
            self.play(Create(ring), run_time=0.6)
            b.until(0.4)
            self.play(Create(poor), FadeIn(pd), FadeIn(pt), run_time=1.0)
            pk = wrapped("don't force the line through the highest point", size=SMALL + 1, width=3.6, color=MUTED).move_to([col, 1.3, 0])
            b.until(0.8)
            self.play(FadeIn(pk), run_time=0.5)
            self.poor = VGroup(poor, pd, ring)
        with self.beat("b03") as b:
            self.play(self.poor.animate.set_opacity(0.3), run_time=0.4)
            good = Line(ax.c2p(195, m_g * 195 + c_g), ax.c2p(405, m_g * 405 + c_g), color=SURR, stroke_width=4)
            ext = DashedLine(ax.c2p(195, m_g * 195 + c_g), ax.c2p(120, m_g * 120 + c_g), color=SURR, stroke_width=4,
                             dash_length=0.1)
            dia = Square(side_length=0.2, color=UNKNOWN, fill_color=UNKNOWN, fill_opacity=1).rotate(PI / 4)
            dia.move_to(ax.c2p(120, m_g * 120 + c_g))
            self.play(Create(good), run_time=1.0)
            gt = wrapped("best line: steady cooling region only", size=SMALL + 1, width=3.6, color=SURR).move_to([col, 0.5, 0])
            self.play(FadeIn(gt), run_time=0.4)
            b.until(0.45)
            self.play(Create(ext), run_time=0.8)
            self.play(FadeIn(dia, scale=1.5), run_time=0.4)
            rd = T(f"read at mixing: ≈ {m_g * 120 + c_g:.1f} °C", size=SMALL + 2, color=UNKNOWN).move_to([col, -0.2, 0])
            b.until(0.75)
            self.play(FadeIn(rd), run_time=0.5)
        with self.beat("b04") as b:
            cv = wrapped("curved trend? use the part nearest the mixing time, and call the result an estimate",
                         size=SMALL + 1, width=3.6, color=MUTED).move_to([col, -1.15, 0])
            self.play(FadeIn(cv), run_time=0.7)


# =====================================================================================
ENDO_PTS = [(90, 19.4), (120, 18.9), (180, 19.1), (240, 19.3), (300, 19.5)]
E_SLOPE, E_ICPT = linfit(ENDO_PTS[1:])
E_MIX = E_SLOPE * 60 + E_ICPT
assert abs(E_MIX - 18.7) < 1e-9


class E11S07_Endo(NarratedScene):
    def construct(self):
        h = header("When the temperature falls")
        pg = temp_axes(x_max=300, x_step=60, y_min=17, y_max=23, width=6.8, height=4.2).move_to([-2.3, 0.0, 0])
        ax = pg.ax
        col = 4.45
        base = Line(ax.c2p(0, 22.0), ax.c2p(60, 22.0), color=SURR, stroke_width=4)
        mix = DashedLine(ax.c2p(60, 17), ax.c2p(60, 23), color=UNKNOWN, stroke_width=2.5)
        pts = data_points(ax, ENDO_PTS)
        hyp = T("hypothetical data", size=SMALL, color=MUTED).move_to([col, -2.35, 0])
        notes = VGroup(T("baseline 22.0 °C", size=SMALL + 1, color=SURR),
                       T("mixing at t = 60 s", size=SMALL + 1, color=UNKNOWN),
                       T("lowest reading 18.9 °C", size=SMALL + 1, color=SYSTEM)).arrange(DOWN, buff=0.12)
        notes.move_to([col, 1.75, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(pg), FadeIn(hyp), run_time=0.9)
            self.play(Create(base), FadeIn(notes[0]), run_time=0.6)
            b.until(0.25)
            self.play(Create(mix), FadeIn(notes[1]), run_time=0.5)
            b.until(0.45)
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.25), run_time=1.3)
            lo = Circle(radius=0.15, color=SYSTEM, stroke_width=3).move_to(pts[1])
            self.play(Create(lo), FadeIn(notes[2]), run_time=0.5)
            why = chip("why does it rise again?", UNKNOWN, size=SMALL + 1).move_to([col, 0.65, 0])
            b.until(0.85)
            self.play(FadeIn(why), run_time=0.4)
            self.why = why
        with self.beat("b02") as b:
            arrows = VGroup(*[Arrow(ax.c2p(x, 21.6), ax.c2p(x, y + 0.35), buff=0, color=SURR, stroke_width=3,
                                    max_tip_length_to_length_ratio=0.2) for x, y in ENDO_PTS[2:]])
            lab = T("heat flows in from the room", size=SMALL + 1, color=SURR).move_to([col, 0.65, 0])
            self.play(FadeOut(self.why), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=1.0)
            self.play(FadeIn(lab), run_time=0.4)
            self.arrows, self.lab = arrows, lab
        with self.beat("b03") as b:
            self.play(FadeOut(self.arrows), FadeOut(self.lab), run_time=0.4)
            fit = Line(ax.c2p(120, E_SLOPE * 120 + E_ICPT), ax.c2p(300, E_SLOPE * 300 + E_ICPT), color=SURR,
                       stroke_width=4)
            ext = DashedLine(ax.c2p(120, E_SLOPE * 120 + E_ICPT), ax.c2p(60, E_MIX), color=SURR, stroke_width=4,
                             dash_length=0.1)
            dia = Square(side_length=0.2, color=UNKNOWN, fill_color=UNKNOWN, fill_opacity=1).rotate(PI / 4)
            dia.move_to(ax.c2p(60, E_MIX))
            self.play(Create(fit), run_time=0.8)
            w1 = M(r"\text{warming: } +0.2\ {}^{\circ}\text{C per } 60\ \text{s}", size=EQ_SMALL - 14,
                   color=SURR).move_to([col, 0.65, 0])
            self.play(Write(w1), run_time=0.7)
            b.until(0.35)
            self.play(Create(ext), FadeIn(dia, scale=1.5), run_time=0.9)
            w2 = M(r"T(60\ \text{s}) = 18.9 - 0.2 = 18.7\ {}^{\circ}\text{C}", size=EQ_SMALL - 14,
                   color=UNKNOWN).move_to([col, 0.05, 0])
            self.play(Write(w2), run_time=0.8)
            w3 = M(r"\Delta T = 18.7 - 22.0 = -3.3\ {}^{\circ}\text{C}", size=EQ_SMALL - 12,
                   color=UNKNOWN).move_to([col, -0.6, 0])
            w4 = T("(lowest reading gives −3.1 °C)", size=SMALL, color=MUTED).move_to([col, -1.05, 0])
            b.until(0.65)
            self.play(Write(w3), FadeIn(w4), run_time=0.9)
        with self.beat("b04") as b:
            sg = VGroup(T("ΔT < 0 → q(cal) < 0", size=SMALL + 1, color=SURR),
                        T("→ ΔH > 0 (endothermic)", size=SMALL + 1, color=UNKNOWN)).arrange(DOWN, buff=0.08)
            sg.move_to([col, -1.7, 0])
            self.play(FadeIn(sg), run_time=0.7)


# =====================================================================================
def updown(mob, up: bool, color, label=""):
    a = Arrow(mob.get_right() + 0.15 * RIGHT + (0.3 * DOWN if up else 0.3 * UP),
              mob.get_right() + 0.15 * RIGHT + (0.3 * UP if up else 0.3 * DOWN), buff=0, color=color, stroke_width=6,
              max_tip_length_to_length_ratio=0.4)
    g = VGroup(a)
    if label:
        g.add(T(label, size=SMALL + 1, color=color).next_to(a, RIGHT, buff=0.1))
    return g


class E11S08_TwoLosses(NarratedScene):
    def construct(self):
        h = header("Heat loss: calibration vs reaction")
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            t = T("Same cause, different effects: follow the formula", size=BODY, color=UNKNOWN).move_to([0, 2.3, 0])
            self.play(FadeIn(t), run_time=0.7)
        lp = VGroup(TB("During calibration", size=LABEL + 2, color=SURR), T("E known correctly", size=SMALL + 1, color=MUTED))
        lp.arrange(DOWN, buff=0.1).move_to([-3.4, 1.2, 0])
        lf = M(r"CF = \frac{E}{\Delta T}", size=EQ + 6).move_to([-3.6, -0.2, 0])
        with self.beat("b02") as b:
            self.play(FadeIn(lp), Write(lf), run_time=1.0)
            d1 = updown(lf[0][-2:], False, BAD, "ΔT ↓").shift(0.0 * RIGHT)
            d1.next_to(lf, RIGHT, buff=0.2).shift(0.35 * DOWN)
            u1 = Arrow(lf.get_left() + 0.3 * LEFT + 0.35 * DOWN, lf.get_left() + 0.3 * LEFT + 0.35 * UP, buff=0, color=UNKNOWN, stroke_width=7)
            u1t = T("CF ↑", size=LABEL + 2, color=UNKNOWN).next_to(u1, LEFT, buff=0.1)
            b.until(0.4)
            self.play(FadeIn(d1), run_time=0.6)
            self.play(GrowArrow(u1), FadeIn(u1t), run_time=0.6)
        rp = VGroup(TB("During the reaction", size=LABEL + 2, color=SYSTEM), T("valid CF, no correction", size=SMALL + 1, color=MUTED))
        rp.arrange(DOWN, buff=0.1).move_to([3.4, 1.2, 0])
        rf = M(r"q = CF \times \Delta T", size=EQ).move_to([3.4, -0.2, 0])
        with self.beat("b03") as b:
            self.play(FadeIn(rp), Write(rf), run_time=1.0)
            d2 = T("ΔT ↓  →  q ↓  →  |ΔH| ↓", size=LABEL + 2, color=BAD).next_to(rf, DOWN, buff=0.35)
            b.until(0.4)
            self.play(FadeIn(d2), run_time=0.8)
        with self.beat("b04") as b:
            msg = wrapped("ΔT is in the denominator of one formula and the numerator of the other, so the same heat loss moves "
                          "the results in opposite directions.", size=LABEL, width=11.0, color=UNKNOWN)
            mp = panel(msg, color=UNKNOWN)
            VGroup(mp, msg).move_to([0, -2.05, 0])
            self.play(FadeIn(mp), FadeIn(msg), run_time=0.9)


# =====================================================================================
class E11S09_Errors(NarratedScene):
    def construct(self):
        h = header("Systematic and random errors")
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            c1 = VGroup(TB("Random error", size=LABEL + 2, color=SURR), wrapped("results scatter unpredictably, high and low", size=LABEL, width=5.4)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            c2 = VGroup(TB("Systematic error", size=LABEL + 2, color=SYSTEM), wrapped("every result pushed the same way, by a consistent amount or proportion", size=LABEL, width=5.4)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            VGroup(c1, c2).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 2.0, 0])
            self.play(FadeIn(c1), run_time=0.7)
            b.until(0.45)
            self.play(FadeIn(c2), run_time=0.7)
            self.cards = VGroup(c1, c2)
        nl = NumberLine(x_range=[-60, -40, 5], length=9.0, include_numbers=True, color=TEXT, font_size=22,
                        decimal_number_config=dict(num_decimal_places=0, color=MUTED)).move_to([0, -0.4, 0])
        nlt = T("ΔH (kJ mol⁻¹)", size=SMALL, color=MUTED).next_to(nl, RIGHT, buff=0.2)
        true = DashedLine(nl.n2p(-50) + 1.2 * UP, nl.n2p(-50) + 0.12 * UP, color=GOOD, stroke_width=3)
        truet = T("true value", size=SMALL + 1, color=GOOD).next_to(true, UP, buff=0.05)
        tight = VGroup(*[Dot(nl.n2p(v) + 0.45 * UP, radius=0.08, color=SYSTEM) for v in (-45.4, -45.1, -44.9, -45.2, -44.8)])
        loose = VGroup(*[Dot(nl.n2p(v) + 0.85 * UP, radius=0.08, color=SURR) for v in (-55.5, -47.0, -52.5, -44.5, -50.5)])
        with self.beat("b02") as b:
            self.play(Create(nl), FadeIn(nlt), Create(true), FadeIn(truet), run_time=1.0)
            accuracy = VGroup(TB("accuracy:", size=SMALL + 1, color=GOOD),
                              T("close to the true value", size=SMALL + 1)).arrange(RIGHT, buff=0.12)
            precision = VGroup(TB("precision:", size=SMALL + 1, color=SYSTEM),
                               T("repeats agree with each other", size=SMALL + 1)).arrange(RIGHT, buff=0.12)
            d = VGroup(accuracy, precision).arrange(RIGHT, buff=0.5)
            d.move_to([0, -1.45, 0])
            self.play(FadeIn(d), run_time=0.6)
            b.until(0.5)
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in tight], lag_ratio=0.2), run_time=1.0)
            tl = wrapped("precise, not accurate: systematic error", size=SMALL + 1, width=3.2, color=SYSTEM).next_to(tight, RIGHT, buff=0.3)
            self.play(FadeIn(tl), run_time=0.5)
            self.extra = VGroup(tl)
        with self.beat("b03") as b:
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in loose], lag_ratio=0.2), run_time=1.0)
            ll = T("scattered: random error", size=SMALL + 1, color=SURR).next_to(loose, LEFT, buff=0.3)
            self.play(FadeIn(ll), run_time=0.4)
            rv = VGroup(T("repeatability: same person, method, equipment → close agreement (precision, not accuracy)", size=SMALL + 1),
                        T("validity: does the experiment measure what it claims, under controlled conditions?", size=SMALL + 1)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            rv.move_to([0, -2.15, 0])
            b.until(0.45)
            self.play(FadeIn(rv), run_time=0.8)
            self.rv = rv
        with self.beat("b04") as b:
            av = T("more repeats → smaller random error; systematic error unchanged", size=LABEL + 2, color=UNKNOWN)
            ap = panel(av, color=UNKNOWN, buff=0.15)
            VGroup(ap, av).move_to([0, -2.1, 0])
            self.play(FadeOut(self.rv), FadeIn(ap), FadeIn(av), run_time=0.8)


# =====================================================================================
def display(value: str, label: str, color=TEXT) -> VGroup:
    """A digital readout box with a caption."""
    box = RoundedRectangle(width=2.5, height=0.85, corner_radius=0.1, stroke_color=MUTED, stroke_width=2,
                           fill_color="#0B1A12", fill_opacity=1)
    t = T(value, size=BODY, color=GOOD).move_to(box)
    lab = T(label, size=SMALL, color=MUTED).next_to(box, UP, buff=0.1)
    return VGroup(box, t, lab)


class E11S10_Resolution(NarratedScene):
    def construct(self):
        from shared.components import Thermometer
        h = header("Resolution, mistakes and outliers")
        th = Thermometer(height=2.6, level=0.5).move_to([-4.6, 0.75, 0])
        ticks = VGroup(*[T(f"{v}", size=SMALL - 2, color=MUTED) for v in (20, 21, 22, 23)])
        for i, tk in enumerate(ticks):
            tk.next_to(th.tube, LEFT, buff=0.12).set_y(th.tube.get_bottom()[1] + 0.45 + i * 0.62)
        thl = T("marked every 1 °C", size=SMALL, color=MUTED).next_to(th, DOWN, buff=0.2)
        probe = display("23.4 °C", "digital probe").move_to([-0.6, 1.0, 0])
        bal = display("12.37 g", "digital balance").move_to([3.6, 1.0, 0])
        q = T("higher resolution: the thermometer or the probe?", size=LABEL + 1, color=UNKNOWN).move_to([0, -1.75, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(th), FadeIn(ticks), FadeIn(thl), run_time=0.9)
            self.play(FadeIn(probe), run_time=0.6)
            b.until(0.7)
            self.play(FadeIn(q), run_time=0.5)
            self.q = q
        with self.beat("b02") as b:
            self.play(FadeOut(self.q), run_time=0.3)
            d = T("resolution: the smallest change an instrument can show, with a unit", size=LABEL + 1).move_to([0, 2.3, 0])
            self.play(FadeIn(d), run_time=0.7)
            c1 = chip("1 °C", SURR, size=SMALL + 2).next_to(thl, DOWN, buff=0.15)
            c2 = chip("0.1 °C", GOOD, size=SMALL + 2).next_to(probe, DOWN, buff=0.2)
            c3 = chip("0.01 g", GOOD, size=SMALL + 2).next_to(bal, DOWN, buff=0.2)
            b.until(0.3)
            self.play(FadeIn(c1, scale=1.1), run_time=0.5)
            b.until(0.48)
            self.play(FadeIn(c2, scale=1.1), run_time=0.5)
            b.until(0.62)
            self.play(FadeIn(bal), FadeIn(c3, scale=1.1), run_time=0.6)
            hi = T("higher resolution = finer increments", size=LABEL, color=GOOD).move_to([0, -1.55, 0])
            b.until(0.85)
            self.play(FadeIn(hi), Indicate(probe, color=GOOD), run_time=0.7)
            self.hi = hi
        with self.beat("b03") as b:
            n1 = T("not automatically more accurate: a fine display can still be badly calibrated", size=SMALL + 2,
                   color=LOSS).move_to([0, -2.15, 0])
            self.play(FadeIn(n1), run_time=0.6)
            n2 = T("coarse thermometer → ΔT supports fewer significant figures", size=SMALL + 2, color=MUTED)
            n2.move_to([0, -2.6, 0])
            b.until(0.6)
            self.play(FadeIn(n2), run_time=0.5)
        with self.beat("b04") as b:
            self.clear(h)
            m = right_panel("Mistake (not an error)", [wrapped("e.g. misreading a scale or spilling solution: identify it, "
                                                                "leave that result out, and repeat the measurement",
                                                                size=SMALL + 2, width=5.2)],
                            size=SMALL + 2, width=5.2, color=SYSTEM)
            o = right_panel("Outlier", [wrapped("one odd value in an otherwise precise set is not evidence of a "
                                                "systematic error: investigate it and report how it was treated",
                                                size=SMALL + 2, width=5.2)],
                            size=SMALL + 2, width=5.2, color=UNKNOWN)
            VGroup(m, o).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to([0, 0.5, 0])
            self.play(FadeIn(m), run_time=0.7)
            b.until(0.5)
            self.play(FadeIn(o), run_time=0.7)


# =====================================================================================
class E11S11_Q22(NarratedScene):
    def construct(self):
        h = header("Practice Q22")
        qc = question_card("Q22").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        req = requested("reported vs corrected ΔH")
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(req), run_time=0.5)
            r = VGroup(TB("spreadsheet (CF = 450)", size=LABEL, color=BAD),
                       M(r"\Delta H = -\frac{450 \times 4.00}{0.0400} = -45\,000\ \text{J mol}^{-1}", size=EQ_SMALL - 6),
                       M(r"= -45.0\ \text{kJ mol}^{-1}", size=EQ_SMALL - 4, color=BAD)).arrange(DOWN, buff=0.15)
            c = VGroup(TB("valid (CF = 500)", size=LABEL, color=GOOD),
                       M(r"\Delta H = -\frac{500 \times 4.00}{0.0400} = -50\,000\ \text{J mol}^{-1}", size=EQ_SMALL - 6),
                       M(r"= -50.0\ \text{kJ mol}^{-1}", size=EQ_SMALL - 4, color=GOOD)).arrange(DOWN, buff=0.15)
            VGroup(r, c).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 1.3, 0])
            self.play(FadeIn(r), run_time=1.2)
            b.until(0.55)
            self.play(FadeIn(c), run_time=1.2)
        with self.beat("b03") as b:
            nl = NumberLine(x_range=[-55, -40, 5], length=7.0, include_numbers=True, color=TEXT, font_size=22,
                            decimal_number_config=dict(num_decimal_places=0, color=MUTED)).move_to([0, -0.6, 0])
            reps = VGroup(*[Dot(nl.n2p(v) + 0.35 * UP, radius=0.08, color=BAD) for v in (-45.2, -44.9, -45.0, -45.1)])
            tv = DashedLine(nl.n2p(-50) + 0.8 * UP, nl.n2p(-50) + 0.2 * DOWN, color=GOOD, stroke_width=3)
            self.play(Create(nl), Create(tv), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in reps], lag_ratio=0.2), run_time=0.9)
            t = T("repeats agree (repeatable) but share the same bias", size=LABEL, color=BAD).next_to(nl, DOWN, buff=0.4)
            b.until(0.55)
            self.play(FadeIn(t), run_time=0.6)
            self.nl = VGroup(nl, reps, tv, t)
        with self.beat("b04") as b:
            self.play(FadeOut(self.nl), run_time=0.4)
            off = M(r"\Delta T = (T_f + 1.5) - (T_i + 1.5) = T_f - T_i", size=EQ_SMALL, color=GOOD).move_to([0, -0.6, 0])
            self.play(Write(off), run_time=1.4)
            canc = T("an identical additive offset cancels", size=LABEL + 2, color=GOOD).next_to(off, DOWN, buff=0.25)
            b.until(0.7)
            self.play(FadeIn(canc), run_time=0.5)
            self.off = VGroup(off, canc)
        with self.beat("b05") as b:
            w = wrong_panel("Don't over-generalise", [T("a stretched scale (too many degrees per real degree) changes ΔT", size=LABEL)], width=10.0)
            w.move_to([0, -2.1, 0])
            self.play(FadeIn(w), run_time=0.8)
        with self.beat("b06") as b:
            self.clear(h, req)
            tally = mark_tally([(2, "reported −45.0 and corrected −50.0 kJ mol⁻¹"), (1, "repeating keeps the same bias"),
                                (2, "offset cancels in the subtraction")], width=6.8).move_to([-2.6, 0.4, 0])
            ws = VGroup(wrong_panel("Repeatable = accurate", [T("✗", size=LABEL)], width=3.6),
                        wrong_panel("Every offset changes ΔT", [T("✗", size=LABEL)], width=3.6))
            ws.arrange(DOWN, buff=0.3).move_to([4.2, 0.4, 0])
            self.play(FadeIn(tally), run_time=0.8)
            b.until(0.55)
            self.play(FadeIn(ws), run_time=0.7)


# =====================================================================================
class E11S12_Table(NarratedScene):
    def construct(self):
        h = header("Error directions (simple model)")
        rows = [["Situation", "Direction"],
                ["Heat loss in electrical calibration, E known correctly", "measured ΔT ↓; calculated CF ↑"],
                ["Uncorrected heat loss during reaction, valid CF fixed", "measured ΔT ↓; inferred heat magnitude ↓"],
                ["CF used is too small", "calculated heat and |molar ΔH| ↓"],
                ["Same additive thermometer offset on both readings", "temperature difference unchanged"],
                ["More repeat trials with the same systematic fault", "better estimate of a biased mean; fault remains"]]
        tb = table(rows, [6.8, 6.0], size=SMALL + 1, row_h=0.56).scale(0.86).move_to([0, 0.5, 0])
        grid, cells = tb[0], tb[1]
        with self.beat("b01") as b:
            self.play(FadeIn(h), Create(grid), FadeIn(VGroup(*cells[:2])), run_time=1.0)
        with self.beat("b02") as b:
            self.play(FadeIn(VGroup(*cells[2:4])), run_time=0.7)
            b.until(0.5)
            self.play(FadeIn(VGroup(*cells[4:6])), run_time=0.7)
        with self.beat("b03") as b:
            for i in range(3, 6):
                b.until(0.05 + 0.28 * (i - 3))
                self.play(FadeIn(VGroup(*cells[2 * i:2 * i + 2])), run_time=0.6)
        with self.beat("b04") as b:
            caut = T("Several faults at once: the net direction needs a full model", size=LABEL + 2, color=UNKNOWN)
            cp = panel(caut, color=UNKNOWN, buff=0.15)
            VGroup(cp, caut).move_to([0, -2.25, 0])
            self.play(FadeIn(cp), FadeIn(caut), run_time=0.8)
            self.caut = VGroup(cp, caut)
        with self.beat("b05") as b:
            self.play(FadeOut(tb), FadeOut(self.caut), run_time=0.5)
            imp = bullets(["insulate the lid and sides of the calorimeter",
                           "calibrate with the same volume of solution used in the reaction",
                           "record temperature more often, then extrapolate the cooling trend",
                           "repeat with fresh solutions and average"], size=LABEL + 2, width=11.0, buff=0.3)
            ih = TB("Specific improvements", size=BODY, color=GOOD)
            g = VGroup(ih, imp).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.2, 0])
            self.play(FadeIn(ih), run_time=0.4)
            for i, it in enumerate(imp):
                b.until(0.1 + 0.2 * i)
                self.play(FadeIn(it), run_time=0.5)


# =====================================================================================
class E11S13_Improve(NarratedScene):
    def construct(self):
        h = header("Checkpoint: which improvement fixes which error?")

        def card(text, color, w=5.2):
            t = wrapped(text, size=SMALL + 2, width=w - 0.4)
            r = RoundedRectangle(width=w, height=max(0.7, t.height + 0.3), corner_radius=0.12, stroke_color=color,
                                 stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
            return VGroup(r, t.move_to(r))
        imps = [card(f"{i + 1}. {t}", SYSTEM) for i, t in enumerate(
            ["insulate the lid and sides", "calibrate with the same volume of solution",
             "record temperatures more often and extrapolate", "repeat with fresh solutions and average"])]
        probs = {"A": card("heat exchange with the surroundings (systematic)", SURR),
                 "B": card("CF not valid for the actual conditions (systematic)", SURR),
                 "C": card("observed peak underestimates the rise", SURR),
                 "D": card("random scatter between repeats", SURR)}
        ys = [1.65, 0.55, -0.55, -1.65]
        for c, y in zip(imps, ys):
            c.move_to([-3.4, y, 0])
        for k, y in zip("CADB", ys):
            probs[k].move_to([3.4, y, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c) for c in imps], lag_ratio=0.2), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(probs[k]) for k in "CADB"], lag_ratio=0.2), run_time=1.2)
        with self.beat("b02") as b:
            for i, (k, fr) in enumerate(zip("ABCD", (0.0, 0.2, 0.45, 0.62))):
                b.until(fr)
                ln = Line(imps[i].get_right(), probs[k].get_left(), color=GOOD, stroke_width=3)
                self.play(Create(ln), probs[k][0].animate.set_stroke(GOOD), run_time=0.6)
            tag = chip("averaging reduces the effect of random error only", LOSS, size=SMALL + 1).move_to([0, -2.45, 0])
            b.until(0.78)
            self.play(FadeIn(tag), run_time=0.5)


# =====================================================================================
class E11S14_Recap(NarratedScene):
    def construct(self):
        h = header("Recap")
        items = bullets(["Graph: baseline, mixing time, observed maximum, cooling region",
                         "Extend the cooling line back to mixing: a model-based corrected estimate",
                         "Follow each error through the actual formula",
                         "Precise (repeatable) is not the same as accurate"], size=LABEL + 2, width=12.0, buff=0.35)
        items.move_to([0, 0.3, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for i, it in enumerate(items):
                b.until(0.05 + 0.2 * i)
                self.play(FadeIn(it, shift=0.1 * RIGHT), run_time=0.6)
        with self.beat("b02") as b:
            self.play(FadeOut(items), run_time=0.4)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN),
                       T("Cooling slope −0.002 °C s⁻¹; extrapolate back 50 s. Temperature increase?", size=LABEL + 2)).arrange(DOWN, buff=0.35).move_to([0, 1.0, 0])
            self.play(FadeIn(q), run_time=0.8)
            self.q = q
        with self.beat("b03") as b:
            a = M(r"50\ \text{s} \times 0.002\ {}^{\circ}\text{C s}^{-1} = 0.1\ {}^{\circ}\text{C}", size=EQ, color=GOOD).next_to(self.q, DOWN, buff=0.5)
            self.play(Write(a), run_time=1.0)
            b.until(0.5)
            nxt = T("Next: Episode 12 · Fair fuel comparisons and sustainability", size=LABEL, color=MUTED).move_to([0, -2.35, 0])
            self.play(FadeIn(nxt), run_time=0.5)


EPISODE_SCENES = ["E11S01_Retrieval", "E11S02_ReadGraph", "E11S03_PeakTooLow", "E11S04_Extrapolate",
                  "E11S05_Q21", "E11S06_Drawing", "E11S07_Endo", "E11S08_TwoLosses", "E11S09_Errors",
                  "E11S10_Resolution", "E11S11_Q22", "E11S12_Table", "E11S13_Improve", "E11S14_Recap"]
