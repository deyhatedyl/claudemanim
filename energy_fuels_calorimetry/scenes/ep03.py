"""
Episode 03 - Energy profiles and thermochemical equations.
Narration: scripts/ep03.md (beat names must match).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (bullets, dH_arrow, enthalpy_axis, h_guide, level, mark_tally, profile_axes,  # noqa: E402
                               profile_curve, question_card, result_box, right_panel, title_card, v_arrow,
                               wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, MUTED, PANEL, SMALL,  # noqa: E402
                          SURR, SYSTEM, TEXT, UNKNOWN, USEFUL, M, T, TB, chip, header, panel)

CAT = "#5DD39E"   # catalysed path (always dashed + labelled)


def requested(text: str) -> VGroup:
    from shared.style import asked_pill
    return asked_pill(text)


def flat(ax, y, x_from, x_to, color=TEXT, width=5):
    return Line(ax.c2p(x_from, y), ax.c2p(x_to, y), color=color, stroke_width=width)


# =====================================================================================
class E03S01_Retrieval(NarratedScene):
    def construct(self):
        card = title_card(3, "Energy profiles and thermochemical equations")
        with self.beat("b01"):
            self.play(FadeIn(card, shift=0.2 * UP), run_time=1.5)
        with self.beat("b02") as b:
            self.play(FadeOut(card), run_time=0.5)
            h = header("Retrieval check")
            q1 = T("1.  Does breaking a bond absorb or release energy?", size=BODY)
            q2 = T("2.  Products lower in enthalpy than reactants: is ΔH positive or negative?", size=BODY)
            qs = VGroup(q1, q2).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([0, 1.0, 0])
            self.play(FadeIn(h), FadeIn(q1), run_time=0.8)
            b.until(0.4)
            self.play(FadeIn(q2), run_time=0.8)
            self.qs = qs
        with self.beat("b03") as b:
            a1 = T("absorbs", size=BODY, color=SYSTEM).next_to(self.qs[0], DOWN, buff=0.15).align_to(self.qs[0], LEFT).shift(0.6 * RIGHT)
            a2 = T("negative: ΔH = H(products) − H(reactants) < 0, exothermic", size=BODY, color=GOOD)
            a2.next_to(self.qs[1], DOWN, buff=0.15).align_to(self.qs[1], LEFT).shift(0.6 * RIGHT)
            self.play(FadeIn(a1), run_time=0.6)
            b.until(0.3)
            self.play(FadeIn(a2), run_time=0.8)


# =====================================================================================
class E03S02_Axes(NarratedScene):
    def construct(self):
        h = header("Energy profiles: axes and endpoints")
        pa = profile_axes(numbers=False, y_label="Enthalpy, H", width=7.2, height=4.6).move_to([-2.4, -0.15, 0])
        ax = pa.ax
        R, P = 120, 50
        note = VGroup(TB("Reaction coordinate", size=LABEL + 2, color=UNKNOWN),
                      wrapped("how far the atoms have got in rearranging from reactants to products", size=LABEL, width=4.3),
                      wrapped("not time: a profile says nothing about speed", size=LABEL, width=4.3, color=BAD))
        note.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.3, 1.2, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), Create(ax), run_time=1.2)
            self.play(FadeIn(pa.ylab), run_time=0.5)
            b.until(0.3)
            self.play(FadeIn(pa.xlab), FadeIn(note[0]), FadeIn(note[1]), run_time=1.0)
            b.until(0.65)
            self.play(FadeIn(note[2]), Indicate(pa.xlab, color=BAD), run_time=1.0)

        rl = flat(ax, R, 0.4, 2.0)
        pl = flat(ax, P, 8.0, 9.6)
        rt = T("reactants", size=LABEL).next_to(rl, UP, buff=0.12)
        pt = T("products", size=LABEL).next_to(pl, DOWN, buff=0.12)
        with self.beat("b02") as b:
            self.play(FadeOut(note), run_time=0.4)
            self.play(Create(rl), FadeIn(rt), run_time=0.8)
            b.until(0.45)
            self.play(Create(pl), FadeIn(pt), run_time=0.8)
            lower = T("exothermic: products lower", size=LABEL, color=SYSTEM).move_to([4.3, 0.4, 0])
            self.play(FadeIn(lower), run_time=0.5)
            self.lower = lower

        with self.beat("b03") as b:
            g1 = h_guide(ax, R, 2.0, 9.3)
            arr = v_arrow(ax, 9.1, R, P, "ΔH < 0", UNKNOWN, side=RIGHT, size=LABEL)
            self.play(Create(g1), run_time=0.5)
            self.play(GrowArrow(arr[0]), FadeIn(arr[1]), run_time=0.8)
            dep = wrapped("ΔH depends only on where the two endpoints sit", size=LABEL, width=4.3, color=UNKNOWN)
            dep.move_to([4.3, -0.6, 0])
            b.until(0.55)
            self.play(FadeIn(dep), run_time=0.7)


# =====================================================================================
class E03S03_Activation(NarratedScene):
    def construct(self):
        h = header("Activation energy, forward and reverse")
        pa = profile_axes(numbers=False, y_label="Enthalpy, H", width=7.2, height=4.6).move_to([-2.4, -0.15, 0])
        ax = pa.ax
        R, TS, P = 105, 160, 45
        curve = profile_curve(ax, R, TS, P)
        ts_dot = Dot(ax.c2p(5, TS), color=UNKNOWN, radius=0.07)
        ts_lab = T("transition state", size=SMALL, color=UNKNOWN).next_to(ts_dot, UP, buff=0.1)
        rt = T("reactants", size=SMALL + 2).next_to(ax.c2p(1.2, R), DOWN, buff=0.12)
        pt = T("products", size=SMALL + 2).next_to(ax.c2p(8.8, P), DOWN, buff=0.12)
        with self.beat("b01") as b:
            self.add(h, pa)
            self.play(FadeIn(rt), FadeIn(pt), run_time=0.5)
            self.play(Create(curve), run_time=2.5)
            b.until(0.6)
            self.play(FadeIn(ts_dot), FadeIn(ts_lab), run_time=0.6)

        gR = h_guide(ax, R, 2.0, 9.8)
        gT = h_guide(ax, TS, 1.0, 8.2)
        gP = h_guide(ax, P, 5.0, 8.0)
        eaf = v_arrow(ax, 1.5, R, TS, "forward Ea", SYSTEM, side=RIGHT, at="top")
        ear = v_arrow(ax, 7.9, P, TS, "reverse Ea", SURR, side=RIGHT, at="top")
        dh = v_arrow(ax, 9.7, R, P, "ΔH", UNKNOWN, side=RIGHT)
        with self.beat("b02") as b:
            self.play(Create(gR), Create(gT), run_time=0.6)
            self.play(GrowArrow(eaf[0]), FadeIn(eaf[1]), run_time=0.9)
        with self.beat("b03") as b:
            self.play(Create(gP), run_time=0.4)
            self.play(GrowArrow(ear[0]), FadeIn(ear[1]), run_time=0.9)

        rules = VGroup(T("forward Ea = peak − reactants", size=LABEL, color=SYSTEM),
                       T("reverse Ea = peak − products", size=LABEL, color=SURR),
                       T("ΔH = products − reactants", size=LABEL, color=UNKNOWN),
                       T("every one is a difference", size=LABEL, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        for r_ in rules:
            r_.scale(0.9)
        rules.move_to([4.6, 0.9, 0]).align_to([3.0, 0, 0], LEFT)
        with self.beat("b04") as b:
            self.play(GrowArrow(dh[0]), FadeIn(dh[1]), run_time=0.8)
            for i in range(3):
                b.until(0.25 + 0.18 * i)
                self.play(FadeIn(rules[i]), run_time=0.5)
            b.until(0.85)
            self.play(FadeIn(rules[3]), run_time=0.5)

        with self.beat("b05") as b:
            R2, TS2, P2 = 45, 160, 105
            curve2 = profile_curve(ax, R2, TS2, P2)
            self.play(FadeOut(VGroup(gR, gT, gP, eaf, ear, dh, ts_dot, ts_lab, rt, pt)), run_time=0.5)
            self.play(Transform(curve, curve2), run_time=1.5)
            rt2 = T("reactants", size=SMALL + 2).next_to(ax.c2p(1.2, R2), DOWN, buff=0.12)
            pt2 = T("products", size=SMALL + 2).next_to(ax.c2p(8.8, P2), UP, buff=0.12)
            gR2 = h_guide(ax, R2, 2.0, 9.8)
            dh2 = v_arrow(ax, 9.7, R2, P2, "ΔH > 0", UNKNOWN, side=RIGHT)
            eaf2 = v_arrow(ax, 1.5, R2, TS2, "forward Ea", SYSTEM, side=RIGHT, at="top")
            gT2 = h_guide(ax, TS2, 1.0, 6.6)
            self.play(FadeIn(rt2), FadeIn(pt2), Create(gR2), Create(gT2), run_time=0.6)
            self.play(GrowArrow(dh2[0]), FadeIn(dh2[1]), GrowArrow(eaf2[0]), FadeIn(eaf2[1]), run_time=1.0)
            endo = VGroup(wrapped("endothermic: products higher", size=SMALL + 1, width=3.4, color=SURR),
                          wrapped("forward Ea is now the larger one", size=SMALL + 1, width=3.4, color=SYSTEM)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            endo.move_to([4.6, -1.3, 0]).align_to(rules, LEFT)
            self.play(FadeIn(endo), run_time=0.5)


# =====================================================================================
class E03S04_Catalyst(NarratedScene):
    def construct(self):
        h = header("What a catalyst changes")
        pa = profile_axes(numbers=False, y_label="Enthalpy, H", width=7.2, height=4.6).move_to([-2.4, -0.15, 0])
        ax = pa.ax
        R, TS, TSc, P = 105, 165, 130, 45
        kw = dict(x0=3.0, xp=5.6, x1=8.0)
        c1 = profile_curve(ax, R, TS, P, **kw)
        c2 = profile_curve(ax, R, TSc, P, color=CAT, dashed=True, **kw)
        leg1 = VGroup(Line(LEFT * 0.4, RIGHT * 0.4, color=TEXT, stroke_width=4), T("uncatalysed", size=LABEL)).arrange(RIGHT, buff=0.2)
        leg2 = VGroup(DashedLine(LEFT * 0.4, RIGHT * 0.4, color=CAT, stroke_width=4, dash_length=0.1),
                      T("catalysed", size=LABEL, color=CAT)).arrange(RIGHT, buff=0.2)
        l1 = leg1.move_to([3.2, 2.45, 0]).align_to([2.3, 0, 0], LEFT)
        l2 = leg2.next_to(leg1, DOWN, buff=0.15).align_to(leg1, LEFT)
        with self.beat("b01") as b:
            self.add(h, pa, c1, l1)
            b.until(0.35)
            self.play(Create(c2), run_time=2.0)
            self.play(FadeIn(l2), run_time=0.5)

        e1 = Circle(radius=0.28, color=UNKNOWN, stroke_width=3).move_to(ax.c2p(2.2, R))
        e2 = Circle(radius=0.28, color=UNKNOWN, stroke_width=3).move_to(ax.c2p(8.8, P))
        same = T("same endpoints", size=LABEL, color=UNKNOWN).move_to([4.4, 1.2, 0]).align_to([2.3, 0, 0], LEFT)
        with self.beat("b02") as b:
            self.play(Create(e1), Create(e2), FadeIn(same), run_time=1.0)
            nc = wrapped("not consumed; same reactants and products, so the same enthalpies", size=LABEL, width=4.2)
            nc.next_to(same, DOWN, buff=0.2).align_to(same, LEFT)
            b.until(0.5)
            self.play(FadeIn(nc), run_time=0.8)
            self.side = VGroup(same, nc)

        gR = h_guide(ax, R, 3.0, 9.8)
        gT = h_guide(ax, TS, 0.6, 5.6)
        gTc = h_guide(ax, TSc, 0.6, 5.6, color=CAT)
        ea1 = v_arrow(ax, 0.9, R, TS, "Ea", TEXT, side=RIGHT, at="top")
        ea2 = v_arrow(ax, 2.0, R, TSc, "Ea (cat.)", CAT, side=RIGHT, at="top")
        dh = v_arrow(ax, 9.7, R, P, "ΔH", UNKNOWN, side=RIGHT)
        with self.beat("b03") as b:
            self.play(FadeOut(e1), FadeOut(e2), Create(gR), Create(gT), Create(gTc), run_time=0.6)
            self.play(GrowArrow(ea1[0]), FadeIn(ea1[1]), run_time=0.6)
            self.play(GrowArrow(ea2[0]), FadeIn(ea2[1]), run_time=0.6)
            b.until(0.6)
            self.play(GrowArrow(dh[0]), FadeIn(dh[1]), run_time=0.8)
            unch = T("ΔH unchanged", size=LABEL, color=UNKNOWN).next_to(self.side, DOWN, buff=0.35).align_to(self.side, LEFT)
            self.play(FadeIn(unch), run_time=0.5)
            self.side.add(unch)

        with self.beat("b04") as b:
            self.play(FadeOut(self.side), run_time=0.4)
            ck = VGroup(TB("Checkpoint", size=LABEL + 2, color=UNKNOWN),
                        wrapped("“Adding a catalyst makes an exothermic reaction release more heat.”", size=LABEL, width=4.3),
                        T("Right or wrong? Why?", size=LABEL, color=UNKNOWN)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            ck.move_to([4.4, 0.6, 0]).align_to([2.3, 0, 0], LEFT).align_to([0, 1.75, 0], UP)
            self.play(FadeIn(ck), run_time=0.8)
            self.ck = ck

        with self.beat("b05") as b:
            ans = VGroup(TB("Wrong.", size=LABEL + 2, color=BAD),
                         wrapped("For the same amount reacting, heat released = |ΔH|, and the catalyst does not change ΔH.",
                                 size=LABEL, width=4.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            ans.next_to(self.ck, DOWN, buff=0.35).align_to(self.ck, LEFT)
            self.play(FadeIn(ans[0]), run_time=0.4)
            self.play(FadeIn(ans[1]), run_time=0.8)


# =====================================================================================
class E03S05_Q06(NarratedScene):
    def construct(self):
        h = header("Practice Q06")
        card = question_card("Q06").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(card, shift=0.1 * UP), run_time=1.0)

        pa = profile_axes(y_max=175, y_step=25, numbers=True, width=6.2, height=4.1).move_to([-2.85, -0.15, 0])
        ax = pa.ax
        R, P, TS, TSc = 80, 25, 150, 110
        c1 = profile_curve(ax, R, TS, P)
        c2 = profile_curve(ax, R, TSc, P, color=CAT, dashed=True)
        guides = VGroup(h_guide(ax, R, 0, 9.4), h_guide(ax, P, 0, 9.4), h_guide(ax, TS, 0, 5.0),
                        h_guide(ax, TSc, 0, 5.0, color=CAT))
        vals = VGroup(*[T(str(v), size=SMALL, color=c).next_to(ax.c2p(0, v), RIGHT, buff=0.08).shift(0.16 * UP)
                        for v, c in [(R, TEXT), (P, TEXT), (TS, TEXT), (TSc, CAT)]])
        req = requested("differences between levels")
        with self.beat("b02") as b:
            self.play(FadeOut(card), run_time=0.5)
            self.play(FadeIn(pa), FadeIn(req), run_time=0.8)
            self.play(Create(c1), run_time=1.6)
            self.play(Create(guides[:3]), FadeIn(vals[:3]), run_time=0.8)
            b.until(0.7)
            self.play(Create(c2), Create(guides[3]), FadeIn(vals[3]), run_time=1.2)

        col_x = 1.7
        lines = []

        def work(label, tex, y, color=TEXT):
            l = TB(label, size=LABEL + 2, color=SYSTEM).move_to([col_x, y, 0])
            m = M(tex, size=EQ_SMALL - 8, color=color).next_to(l, RIGHT, buff=0.2)
            return VGroup(l, m)

        wa = work("a.", r"E_a = 150 - 80 = 70\ \text{kJ mol}^{-1}", 2.2)
        ea = v_arrow(ax, 3.5, R, TS, "70", SYSTEM, side=LEFT)
        with self.beat("b03") as b:
            self.play(GrowArrow(ea[0]), FadeIn(ea[1]), run_time=0.8)
            self.play(Write(wa), run_time=1.0)
        wb = work("b.", r"E_a(\text{rev}) = 150 - 25 = 125", 1.35)
        er = v_arrow(ax, 6.6, P, TS, "125", SURR, side=RIGHT)
        with self.beat("b04") as b:
            self.play(Create(h_guide(ax, TS, 5.0, 7.0)), run_time=0.3)
            self.play(GrowArrow(er[0]), FadeIn(er[1]), run_time=0.8)
            self.play(Write(wb), run_time=1.0)
        wc = work("c.", r"\Delta H = 25 - 80 = -55\ \text{kJ mol}^{-1}", 0.5)
        dh = v_arrow(ax, 9.0, R, P, "−55", UNKNOWN, side=RIGHT)
        with self.beat("b05") as b:
            self.play(GrowArrow(dh[0]), FadeIn(dh[1]), run_time=0.8)
            self.play(Write(wc), run_time=1.0)
            ok = T("products lower: exothermic ✓", size=SMALL, color=GOOD).next_to(wc, DOWN, buff=0.1).align_to(wc[1], LEFT)
            b.until(0.6)
            self.play(FadeIn(ok), run_time=0.5)
        wd = work("d.", r"E_a(\text{cat}) = 110 - 80 = 30", -0.55, color=CAT)
        ec = v_arrow(ax, 4.3, R, TSc, "30", CAT, side=RIGHT)
        with self.beat("b06") as b:
            self.play(GrowArrow(ec[0]), FadeIn(ec[1]), run_time=0.8)
            self.play(Write(wd), run_time=1.0)
        with self.beat("b07") as b:
            le = TB("e.", size=LABEL + 2, color=SYSTEM).move_to([col_x, -1.45, 0])
            te = wrapped("No change: same reactant and product levels, so the same ΔH and heat released.",
                         size=SMALL + 1, width=4.0).next_to(le, RIGHT, buff=0.2, aligned_edge=UP)
            self.play(FadeIn(le), FadeIn(te), run_time=1.0)
            self.work = VGroup(wa, wb, wc, ok, wd, le, te)

        with self.beat("b08") as b:
            self.play(FadeOut(self.work), run_time=0.5)
            tally = mark_tally([(1, "a. 70"), (1, "b. 125"), (1, "c. −55"), (1, "d. 30"), (1, "e. ΔH unchanged")],
                               width=3.6, size=SMALL + 1)
            tally.move_to([4.2, 0.2, 0])
            self.play(FadeIn(tally), run_time=0.8)
            w = wrong_panel("Peak read as Ea", [T("Ea = 150 ✗", size=LABEL)],
                            note="First wrong step: not subtracting the reactant level", width=4.0, size=SMALL + 1)
            w.move_to([4.2, 0.2, 0])
            b.until(0.42)
            self.play(FadeOut(tally), run_time=0.4)
            self.play(FadeIn(w), run_time=0.8)
            self.tw = w

        with self.beat("b09") as b:
            self.play(FadeOut(self.tw), run_time=0.5)
            p = VGroup(TB("Predict", size=LABEL + 2, color=UNKNOWN),
                       T("catalysed reverse Ea = ?", size=LABEL + 2)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            p.move_to([4.3, 1.5, 0])
            self.play(FadeIn(p), run_time=0.6)
            self.p = p
        with self.beat("b10") as b:
            ecr = v_arrow(ax, 7.4, P, TSc, "85", CAT, side=RIGHT)
            self.play(Create(h_guide(ax, TSc, 5.0, 7.8, color=CAT)), run_time=0.3)
            self.play(GrowArrow(ecr[0]), FadeIn(ecr[1]), run_time=0.8)
            m = M(r"110 - 25 = 85\ \text{kJ mol}^{-1}", size=EQ_SMALL - 4, color=CAT).next_to(self.p, DOWN, buff=0.3).align_to(self.p, LEFT)
            n = wrapped("40 less than 125: the same 40 the catalyst took off the forward barrier (70 → 30)",
                        size=SMALL + 1, width=4.2).next_to(m, DOWN, buff=0.25).align_to(m, LEFT)
            self.play(Write(m), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(n), run_time=0.8)


# =====================================================================================
class E03S06_Thermo(NarratedScene):
    def construct(self):
        h = header("Thermochemical equations")
        rows = [
            (r"2\ce{H2(g)} + \ce{O2(g)} \ce{->} 2\ce{H2O(l)}", r"\Delta H = -572\ \text{kJ}", "as written", TEXT),
            (r"4\ce{H2(g)} + 2\ce{O2(g)} \ce{->} 4\ce{H2O(l)}", r"\Delta H = -1144\ \text{kJ}", "× 2: both double", GOOD),
            (r"2\ce{H2O(l)} \ce{->} 2\ce{H2(g)} + \ce{O2(g)}", r"\Delta H = +572\ \text{kJ}", "reversed: flip sign", SURR),
            (r"\ce{H2(g)} + \tfrac{1}{2}\ce{O2(g)} \ce{->} \ce{H2O(l)}", r"\Delta H = -286\ \text{kJ}", "÷ 2: both halve", SYSTEM),
        ]
        ys = [2.15, 0.95, -0.25, -1.45]
        built = []
        for (eq, dh, tag_, col), y in zip(rows, ys):
            e = M(eq, size=EQ_SMALL - 2).move_to([0, y, 0]).align_to([-6.4, 0, 0], LEFT)
            d = M(dh, size=EQ_SMALL - 2, color=col).move_to([0, y, 0]).align_to([0.9, 0, 0], LEFT)
            t = T(tag_, size=SMALL + 1, color=col).move_to([0, y, 0]).align_to([4.35, 0, 0], LEFT)
            built.append(VGroup(e, d, t))
        note0 = T("refers to 2 mol H₂ + 1 mol O₂ → 2 mol H₂O(l)", size=SMALL + 1, color=MUTED).next_to(built[0][0], DOWN, buff=0.08).align_to(built[0][0], LEFT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(built[0][0]), run_time=1.2)
            self.play(Write(built[0][1]), FadeIn(built[0][2]), run_time=0.8)
            b.until(0.55)
            self.play(FadeIn(note0), run_time=0.6)
        with self.beat("b02") as b:
            self.play(TransformFromCopy(built[0][0], built[1][0]), run_time=1.0)
            b.until(0.4)
            self.play(TransformFromCopy(built[0][1], built[1][1]), FadeIn(built[1][2]), run_time=1.0)
        with self.beat("b03") as b:
            self.play(TransformFromCopy(built[0][0], built[2][0]), run_time=1.0)
            b.until(0.35)
            self.play(TransformFromCopy(built[0][1], built[2][1]), FadeIn(built[2][2]), run_time=1.0)
        with self.beat("b04") as b:
            self.play(TransformFromCopy(built[0][0], built[3][0]), run_time=1.0)
            self.play(TransformFromCopy(built[0][1], built[3][1]), FadeIn(built[3][2]), run_time=1.0)
            molar = VGroup(T("Molar enthalpy of combustion of H₂:", size=LABEL),
                           M(r"-286\ \text{kJ per mol of } \ce{H2}", size=EQ_SMALL - 4, color=SYSTEM)).arrange(RIGHT, buff=0.25)
            molar.move_to([0, -2.35, 0])
            b.until(0.55)
            self.play(FadeIn(molar), run_time=0.8)


# =====================================================================================
class E03S07_States(NarratedScene):
    def construct(self):
        h = header("States matter: liquid or gaseous water")
        ax = enthalpy_axis(4.6).move_to([-6.0, -0.1, 0])
        top, liq = 1.9, -1.9
        gas = top - (top - liq) * 484 / 572
        Lr = level(3.0, "2H₂(g) + O₂(g)").move_to([-3.4, top, 0])
        Ll = level(3.0, "2H₂O(l)").move_to([-3.4, liq, 0])
        Lg = level(3.0, "2H₂O(g)", color=SURR).move_to([-3.4, gas, 0])
        Lr.label.next_to(Lr.line, UP, buff=0.1)
        for L_ in (Ll, Lg):
            L_.label.next_to(L_.line, RIGHT, buff=0.2)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(ax), run_time=0.6)
            self.play(Create(Lr.line), FadeIn(Lr.label), Create(Ll.line), FadeIn(Ll.label), run_time=1.0)
            a1 = dH_arrow(top, liq, -4.2, "−572 kJ", color=UNKNOWN, side=LEFT, size=LABEL)
            self.play(GrowArrow(a1[0]), FadeIn(a1[1]), run_time=0.8)
            q = T("What if the water formed were a gas?", size=LABEL + 2, color=UNKNOWN).move_to([3.6, 1.7, 0])
            b.until(0.5)
            self.play(FadeIn(q), run_time=0.6)
        with self.beat("b02") as b:
            self.play(Create(Lg.line), FadeIn(Lg.label), run_time=0.8)
            ext = VGroup(DashedLine([-1.9, liq, 0], [0.75, liq, 0], color=FAINT, stroke_width=1.5),
                         DashedLine([-1.9, gas, 0], [0.75, gas, 0], color=FAINT, stroke_width=1.5))
            self.play(Create(ext), run_time=0.4)
            vap = Arrow([0.6, liq, 0], [0.6, gas, 0], buff=0, color=SURR, stroke_width=5, max_tip_length_to_length_ratio=0.35)
            vt = T("vaporisation absorbs ≈ 44 kJ per mol (25 °C)", size=SMALL + 1, color=SURR).move_to([3.9, 0.6, 0])
            vt2 = T("2 mol: ≈ 88 kJ", size=SMALL + 1, color=SURR).next_to(vt, DOWN, buff=0.1)
            self.play(GrowArrow(vap), run_time=0.6)
            b.until(0.4)
            self.play(FadeIn(vt), FadeIn(vt2), run_time=0.8)
        with self.beat("b03") as b:
            a2 = dH_arrow(top, gas, -2.75, "≈ −484 kJ", color=SURR, side=RIGHT, size=LABEL)
            self.play(GrowArrow(a2[0]), FadeIn(a2[1]), run_time=0.8)
            calc = M(r"-572 + 88 \approx -484\ \text{kJ}", size=EQ_SMALL - 4).move_to([3.6, -0.3, 0])
            self.play(Write(calc), run_time=0.8)
            msg = wrapped("Different product state → different ΔH. Use data for the states actually involved.",
                          size=LABEL, width=5.5, color=UNKNOWN).move_to([3.9, -1.15, 0])
            b.until(0.6)
            self.play(FadeIn(msg), run_time=0.8)
        with self.beat("b04") as b:
            ex = VGroup(T("hot exhaust: water vapour", size=SMALL + 1, color=SURR),
                        T("room-temperature calorimeter: mostly liquid", size=SMALL + 1)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            ex.move_to([3.6, -2.3, 0])
            self.play(FadeIn(ex), run_time=0.8)


# =====================================================================================
class E03S08_Q05(NarratedScene):
    def construct(self):
        h = header("Practice Q05")
        card = question_card("Q05").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(card, shift=0.1 * UP), run_time=1.0)
        given = M(r"2\ce{H2(g)} + \ce{O2(g)} \ce{->} 2\ce{H2O(l)} \qquad \Delta H = -572\ \text{kJ}", size=EQ_SMALL - 2).move_to([0, 2.3, 0])
        with self.beat("b02") as b:
            self.play(FadeOut(card), FadeIn(given), run_time=0.8)
            la = TB("a.", size=LABEL + 2, color=SYSTEM).move_to([-6.2, 1.25, 0])
            st = T("reverse (flip sign), then halve (halve value)", size=LABEL, color=MUTED).next_to(la, RIGHT, buff=0.25)
            ans = M(r"\ce{H2O(l)} \ce{->} \ce{H2(g)} + \tfrac{1}{2}\ce{O2(g)} \qquad \Delta H = +286\ \text{kJ}", size=EQ_SMALL - 2, color=GOOD)
            ans.next_to(st, DOWN, buff=0.2).align_to(st, LEFT)
            self.play(FadeIn(la), FadeIn(st), run_time=0.8)
            b.until(0.5)
            self.play(Write(ans), run_time=1.4)
        with self.beat("b03") as b:
            lb = TB("b.", size=LABEL + 2, color=SYSTEM).move_to([-6.2, -0.4, 0])
            s1 = M(r"572\ \text{kJ per 2 mol }\ce{H2} \;\Rightarrow\; 286\ \text{kJ per mol }\ce{H2}", size=EQ_SMALL - 4)
            s2 = M(r"0.750\ \text{mol} \times 286\ \text{kJ mol}^{-1} = 214.5\ \text{kJ} \approx 215\ \text{kJ released}", size=EQ_SMALL - 4, color=GOOD)
            VGroup(s1, s2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(lb, RIGHT, buff=0.25, aligned_edge=UP)
            self.play(FadeIn(lb), Write(s1), run_time=1.2)
            b.until(0.55)
            self.play(Write(s2), run_time=1.4)
        with self.beat("b04") as b:
            lc = TB("c.", size=LABEL + 2, color=SYSTEM).move_to([-6.2, -1.9, 0])
            tc = wrapped("No. H₂O(g) sits higher in enthalpy than H₂O(l) (vaporisation absorbs energy), so less energy "
                         "is released and a different ΔH is needed.", size=LABEL, width=11.6)
            tc.next_to(lc, RIGHT, buff=0.25, aligned_edge=UP)
            self.play(FadeIn(lc), FadeIn(tc), run_time=1.0)
        with self.beat("b05") as b:
            self.clear(h)
            tally = mark_tally([(2, "a. reversed, halved equation with ΔH = +286 kJ"), (2, "b. 215 kJ released"),
                                (1, "c. state changes ΔH")], width=5.8).move_to([-3.3, 0.4, 0])
            w = wrong_panel("Equation value used per mol H₂", [M(r"0.750 \times 572 = 429\ \text{kJ}", size=EQ_SMALL - 6, color=TEXT)],
                            note="First wrong step: not asking what amount ΔH refers to (2 mol H₂).", width=5.2).move_to([3.4, 0.4, 0])
            self.play(FadeIn(tally), run_time=0.8)
            b.until(0.4)
            self.play(FadeIn(w), run_time=0.8)


# =====================================================================================
class E03S09_Recap(NarratedScene):
    def construct(self):
        h = header("Recap")
        pa = profile_axes(numbers=False, y_label="Enthalpy, H", width=5.6, height=3.8).move_to([-3.4, 0.0, 0])
        ax = pa.ax
        R, TS, TSc, P = 105, 165, 130, 45
        c1 = profile_curve(ax, R, TS, P)
        c2 = profile_curve(ax, R, TSc, P, color=CAT, dashed=True)
        arrs = VGroup(v_arrow(ax, 3.6, R, TS, "Ea", SYSTEM, side=LEFT), v_arrow(ax, 6.4, P, TS, "Ea rev", SURR),
                      v_arrow(ax, 9.2, R, P, "ΔH", UNKNOWN))
        rules = VGroup(T("every quantity is a vertical difference", size=LABEL),
                       T("catalyst: lower peak, same endpoints, same ΔH", size=LABEL, color=CAT),
                       T("× n: ΔH × n", size=LABEL), T("reverse: change the sign", size=LABEL),
                       T("states change ΔH", size=LABEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rules.scale(0.9).move_to([3.3, 0.2, 0]).align_to([0.7, 0, 0], LEFT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(pa), Create(c1), run_time=1.0)
            self.play(FadeIn(arrs), FadeIn(rules[0]), run_time=0.8)
            b.until(0.35)
            self.play(Create(c2), FadeIn(rules[1]), run_time=1.0)
            b.until(0.6)
            self.play(FadeIn(rules[2]), FadeIn(rules[3]), run_time=0.8)
            b.until(0.85)
            self.play(FadeIn(rules[4]), run_time=0.5)
        with self.beat("b02") as b:
            self.clear(h)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN),
                       M(r"\Delta H = -100\ \text{kJ}", size=EQ),
                       T("ΔH for the reverse equation with every coefficient tripled?", size=BODY)).arrange(DOWN, buff=0.35)
            q.move_to([0, 0.9, 0])
            self.play(FadeIn(q), run_time=0.8)
            self.q = q
        with self.beat("b03") as b:
            a = M(r"\text{reverse: } +100\ \text{kJ} \;\;\rightarrow\;\; \times 3: +300\ \text{kJ}", size=EQ_SMALL, color=GOOD)
            a.next_to(self.q, DOWN, buff=0.5)
            self.play(Write(a), run_time=1.2)
            b.until(0.5)
            nxt = T("Next: Episode 04 · Fuels, biofuels and the carbon cycle", size=LABEL, color=MUTED).move_to([0, -2.35, 0])
            self.play(FadeIn(nxt), run_time=0.6)


EPISODE_SCENES = ["E03S01_Retrieval", "E03S02_Axes", "E03S03_Activation", "E03S04_Catalyst", "E03S05_Q06",
                  "E03S06_Thermo", "E03S07_States", "E03S08_Q05", "E03S09_Recap"]
