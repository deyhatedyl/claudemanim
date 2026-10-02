"""
Episode 10 - Reaction calorimetry and molar enthalpy.
Narration: scripts/ep10.md (beat names must match).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (Budget, Thermometer, bullets, calorimeter, mark_tally, question_card,  # noqa: E402
                               result_box, right_panel, title_card, wrapped, wrong_panel, number_badge)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, CONC_C, ENERGY_C, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, MASS_C,  # noqa: E402
                          MOL_C, MUTED, PANEL, SMALL, SURR, SYSTEM, TEMP_C, TEXT, UNKNOWN, USEFUL, VOL_C, M, T,
                          TB, chip, header, panel)

ACID, BASE = "#F5B7B1", "#AED6F1"


def requested(text: str) -> VGroup:
    c = chip("Asked", UNKNOWN)
    t = T(text, size=SMALL + 2, color=UNKNOWN)
    return VGroup(c, t).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.4)


def cylinder(label, vol, conc, color, fill=0.6, h=2.2):
    tube = RoundedRectangle(width=0.8, height=h, corner_radius=0.08, color=TEXT, stroke_width=2.5)
    liq = Rectangle(width=0.72, height=h * fill, stroke_width=0, fill_color=color, fill_opacity=0.6).align_to(tube, DOWN).shift(0.04 * UP)
    base = Line(LEFT * 0.6, RIGHT * 0.6, color=TEXT, stroke_width=3).next_to(tube, DOWN, buff=0)
    t = VGroup(TB(label, size=LABEL, color=color), T(vol, size=SMALL + 1), T(conc, size=SMALL + 1)).arrange(DOWN, buff=0.06)
    t.next_to(base, DOWN, buff=0.15)
    g = VGroup(tube, liq, base, t)
    g.liq, g.tube = liq, tube
    return g


def two_columns(cal_val: str, rxn_val: str):
    cc = VGroup(TB("calorimeter", size=LABEL + 2, color=SURR), M(cal_val, size=EQ_SMALL, color=SURR), T("gains heat: +", size=SMALL + 1, color=SURR)).arrange(DOWN, buff=0.15)
    rc = VGroup(TB("reacting system", size=LABEL + 2, color=SYSTEM), M(rxn_val, size=EQ_SMALL, color=SYSTEM), T("loses heat: −", size=SMALL + 1, color=SYSTEM)).arrange(DOWN, buff=0.15)
    g = VGroup(rc, cc).arrange(RIGHT, buff=2.4)
    arr = Arrow(rc.get_right(), cc.get_left(), buff=0.25, color=ENERGY_C, stroke_width=6)
    lab = T("heat", size=SMALL + 1, color=ENERGY_C).next_to(arr, UP, buff=0.08)
    return VGroup(g, arr, lab)


# =====================================================================================
class E10S01_Retrieval(NarratedScene):
    def construct(self):
        tc = title_card(10, "Reaction calorimetry and molar enthalpy")
        with self.beat("b01"):
            self.play(FadeIn(tc, shift=0.2 * UP), run_time=1.5)
        with self.beat("b02") as b:
            self.play(FadeOut(tc), run_time=0.5)
            h = header("Retrieval check")
            q1 = T("1.  n(NaOH) in 50.0 mL of 0.900 mol L⁻¹?", size=BODY)
            q2 = T("2.  CF = 540 J °C⁻¹, rise 2.00 °C: heat gained?", size=BODY)
            qs = VGroup(q1, q2).arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to([0, 0.9, 0])
            self.play(FadeIn(h), FadeIn(q1), run_time=0.7)
            b.until(0.4)
            self.play(FadeIn(q2), run_time=0.7)
            self.qs = qs
        with self.beat("b03") as b:
            a1 = M(r"0.0500\ \text{L} \times 0.900\ \text{mol L}^{-1} = 0.0450\ \text{mol}", size=EQ_SMALL, color=GOOD).next_to(self.qs[0], DOWN, buff=0.15).align_to(self.qs[0], LEFT).shift(0.6 * RIGHT)
            a2 = M(r"540 \times 2.00 = 1080\ \text{J}", size=EQ_SMALL, color=GOOD).next_to(self.qs[1], DOWN, buff=0.15).align_to(self.qs[1], LEFT).shift(0.6 * RIGHT)
            self.play(Write(a1), run_time=1.0)
            b.until(0.6)
            self.play(Write(a2), run_time=0.8)


# =====================================================================================
class E10S02_Mixing(NarratedScene):
    def construct(self):
        h = header("Mixing the solutions")
        c1 = cylinder("HCl", "75.0 mL", "0.800 mol L⁻¹", ACID, 0.75).move_to([-5.7, 0.6, 0])
        c2 = cylinder("NaOH", "50.0 mL", "0.900 mol L⁻¹", BASE, 0.5).move_to([-3.6, 0.6, 0])
        cal = calorimeter(width=2.4, height=2.0, water_level=0.05, stirrer=True).move_to([-0.9, 0.3, 0])
        cal.thermo.level.set_value(0.3)
        same = wrapped("both start at the same temperature", size=SMALL + 1, width=2.8, color=MUTED).next_to(cal, DOWN, buff=0.25)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(c1), FadeIn(c2), FadeIn(cal), run_time=1.0)
            self.play(FadeIn(same), run_time=0.5)
            b.until(0.55)
            mix = Rectangle(width=1.8, height=1.0, stroke_width=0, fill_color="#D7BDE2", fill_opacity=0.45).move_to(cal.get_center() + 0.35 * DOWN)
            self.play(c1.liq.animate.stretch(0.05, 1, about_edge=DOWN), c2.liq.animate.stretch(0.05, 1, about_edge=DOWN),
                      FadeIn(mix), run_time=1.4)
        eq = M(r"\ce{HCl(aq) + NaOH(aq) -> NaCl(aq) + H2O(l)}", size=EQ_SMALL - 6).move_to([3.3, 2.4, 0])
        ratio = T("all coefficients 1 → ratio 1 : 1", size=SMALL + 1, color=MOL_C).next_to(eq, DOWN, buff=0.12)
        with self.beat("b02") as b:
            self.play(Write(eq), run_time=1.2)
            b.until(0.55)
            self.play(FadeIn(ratio), run_time=0.5)
        a1 = M(r"n(\ce{HCl}) = 0.0750\ \text{L} \times 0.800 = 0.0600\ \text{mol}", size=EQ_SMALL - 8, color=MOL_C).move_to([0, 1.1, 0]).align_to([1.0, 0, 0], LEFT)
        a2 = M(r"n(\ce{NaOH}) = 0.0500\ \text{L} \times 0.900 = 0.0450\ \text{mol}", size=EQ_SMALL - 8, color=MOL_C).move_to([0, 0.4, 0]).align_to([1.0, 0, 0], LEFT)
        with self.beat("b03") as b:
            b.until(0.15)
            self.play(Write(a1), run_time=1.2)
            b.until(0.6)
            self.play(Write(a2), run_time=1.2)
        with self.beat("b04") as b:
            w = wrong_panel("Not like this", [wrapped("adding volumes or concentrations to get an amount", size=SMALL + 2, width=4.6)],
                            note="each amount: its own c × its own V", width=4.6, size=SMALL + 2)
            w.move_to([3.85, -1.35, 0])
            self.play(FadeIn(w), run_time=0.8)


# =====================================================================================
class E10S03_Limiting(NarratedScene):
    def construct(self):
        h = header("Which reagent sets the heat?")
        bud = Budget(["HCl", "NaOH", "H₂O"], ["initial (mol)", "used / formed", "remaining"], col_w=2.9, label_w=1.7,
                     col_colors=[MUTED, SYSTEM, GOOD]).move_to([0, 0.8, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(bud), run_time=0.8)
            self.play(FadeIn(VGroup(bud.cell(0, 0, "0.0600"), bud.cell(1, 0, "0.0450"), bud.cell(2, 0, "0"))), run_time=0.6)
            lim = SurroundingRectangle(bud.labels[1], color=UNKNOWN, buff=0.1)
            lt = T("limiting (1 : 1, smaller amount)", size=SMALL + 1, color=UNKNOWN).next_to(bud, LEFT, buff=0.2).shift(0.0 * UP)
            lt.next_to(lim, DOWN, buff=0.1).align_to(bud, LEFT)
            b.until(0.4)
            self.play(Create(lim), run_time=0.6)
        with self.beat("b02") as b:
            self.play(FadeIn(bud.cell(0, 1, "0.0450", SYSTEM)), FadeIn(bud.cell(1, 1, "0.0450", SYSTEM)), run_time=0.7)
            self.play(FadeIn(bud.cell(2, 1, "+0.0450", GOOD)), run_time=0.6)
            b.until(0.5)
            self.play(FadeIn(bud.cell(0, 2, "0.0150 (excess)", GOOD)), FadeIn(bud.cell(1, 2, "0", GOOD)),
                      FadeIn(bud.cell(2, 2, "0.0450", GOOD)), run_time=0.8)
        with self.beat("b03") as b:
            msg = VGroup(T("heat released is set by the reaction that happens:", size=LABEL + 2),
                         T("0.0450 mol of water formed", size=LABEL + 2, color=UNKNOWN),
                         T("excess acid releases no extra heat (model)", size=LABEL, color=MUTED)).arrange(DOWN, buff=0.15)
            msg.move_to([0, -1.55, 0])
            self.play(FadeIn(msg[:2]), run_time=0.8)
            b.until(0.6)
            self.play(FadeIn(msg[2]), run_time=0.5)


# =====================================================================================
class E10S04_Signs(NarratedScene):
    def construct(self):
        h = header("From calorimeter heat to ΔH")
        f1 = M(r"q_{\text{cal}} = CF \times \Delta T", size=EQ).move_to([0, 2.2, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(f1), run_time=1.0)
            pos = T("positive for an exothermic reaction", size=LABEL, color=SURR).next_to(f1, DOWN, buff=0.15)
            self.play(FadeIn(pos), run_time=0.5)
        cols = two_columns(r"+\,q", r"-\,q").move_to([0, 0.2, 0])
        f2 = M(r"q_{\text{rxn}} = -\,q_{\text{cal}}", size=EQ, color=SYSTEM).move_to([0, -1.2, 0])
        with self.beat("b02") as b:
            self.play(FadeIn(cols[0][0]), run_time=0.6)
            self.play(GrowArrow(cols[1]), FadeIn(cols[2]), run_time=0.7)
            self.play(FadeIn(cols[0][1]), run_time=0.6)
            b.until(0.6)
            self.play(Write(f2), run_time=0.8)
            ass = T("assumes all the heat stays in the calorimeter", size=SMALL + 1, color=MUTED).next_to(f2, DOWN, buff=0.12)
            self.play(FadeIn(ass), run_time=0.4)
            self.ass = ass
        with self.beat("b03") as b:
            self.play(FadeOut(self.ass), run_time=0.3)
            f3 = M(r"\Delta H = \frac{q_{\text{rxn}}}{n}", r"\quad n = \text{amount the } \Delta H \text{ refers to}", size=EQ_SMALL).move_to([0, -1.95, 0])
            f3[1].set_color(UNKNOWN)
            self.play(f2.animate.shift(0.35 * UP), Write(f3), run_time=1.2)
            note = T("e.g. per mole of water formed: the limiting-set amount", size=SMALL + 1, color=UNKNOWN).next_to(f3, DOWN, buff=0.12)
            b.until(0.6)
            self.play(FadeIn(note), run_time=0.5)


# =====================================================================================
class E10S05_Falls(NarratedScene):
    def construct(self):
        h = header("When the temperature falls")
        hyp = T("salt Y is hypothetical", size=SMALL, color=MUTED).to_corner(UR, buff=0.4)
        th = Thermometer(height=3.0, level=0.62).move_to([-5.2, 0.1, 0])
        t0 = T("21.0 °C", size=LABEL).next_to(th, RIGHT, buff=0.2).shift(0.55 * UP)
        t1 = T("18.6 °C", size=LABEL, color=SURR).next_to(th, RIGHT, buff=0.2).shift(0.15 * UP)
        x0 = -3.4

        def L(tex, y, col=TEXT, s=EQ_SMALL - 6):
            return M(tex, size=s, color=col).move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
        with self.beat("b01") as b:
            data = VGroup(T("0.0500 mol of salt Y dissolves", size=LABEL + 1),
                          T("CF = 500 J °C⁻¹", size=LABEL + 1)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            data.move_to([0, 2.05, 0]).align_to([x0, 0, 0], LEFT)
            self.play(FadeIn(h), FadeIn(hyp), FadeIn(data), FadeIn(th), FadeIn(t0), run_time=0.9)
            b.until(0.5)
            self.play(th.level.animate.set_value(0.45), FadeIn(t1), run_time=1.5)
            q = T("sign of ΔH?", size=LABEL + 2, color=UNKNOWN).move_to([0, 0.9, 0]).align_to([x0, 0, 0], LEFT)
            b.until(0.8)
            self.play(FadeIn(q), run_time=0.4)
            self.q = q
        with self.beat("b02") as b:
            self.play(FadeOut(self.q), run_time=0.3)
            l1 = L(r"\Delta T = 18.6 - 21.0 = -2.40\ {}^{\circ}\text{C}", 0.95, TEMP_C)
            l2 = L(r"q_{\text{cal}} = 500 \times (-2.40) = -1200\ \text{J}", 0.25, SURR)
            self.play(Write(l1), run_time=1.0)
            b.until(0.45)
            self.play(Write(l2), run_time=1.0)
            lost = T("the calorimeter lost energy", size=SMALL + 1, color=SURR).next_to(l2, RIGHT, buff=0.35)
            b.until(0.8)
            self.play(FadeIn(lost), run_time=0.4)
        with self.beat("b03") as b:
            l3 = L(r"q_{\text{process}} = +1200\ \text{J}", -0.45, SYSTEM)
            l4 = L(r"\Delta H = \frac{+1.200\ \text{kJ}}{0.0500\ \text{mol}} = +24.0\ \text{kJ mol}^{-1}", -1.25, UNKNOWN)
            self.play(Write(l3), run_time=0.8)
            b.until(0.3)
            self.play(Write(l4), run_time=1.0)
            self.play(Create(result_box(l4, UNKNOWN)), run_time=0.4)
            tab = VGroup(T("temperature rises → q(cal) > 0 → ΔH < 0 (exothermic)", size=SMALL + 1, color=MUTED),
                         T("temperature falls → q(cal) < 0 → ΔH > 0 (endothermic)", size=SMALL + 1, color=UNKNOWN))
            tab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([0, -2.4, 0])
            b.until(0.65)
            self.play(FadeIn(tab), run_time=0.6)


# =====================================================================================
class E10S06_Q19(NarratedScene):
    def construct(self):
        h = header("Practice Q19")
        qc = question_card("Q19").move_to([0, 0.3, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        req = requested("ΔH per mol water")
        colL = -6.3

        def L(tex, y, col=TEXT, s=EQ_SMALL - 6):
            return M(tex, size=s, color=col).move_to([0, y, 0]).align_to([colL, 0, 0], LEFT)
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(req), run_time=0.5)
            ab = VGroup(L(r"\text{a. } n(\ce{HCl}) = 0.0600,\ n(\ce{NaOH}) = 0.0450\ \text{mol}", 2.3, MOL_C),
                        L(r"\text{b. NaOH limiting; HCl left} = 0.0600 - 0.0450 = 0.0150\ \text{mol}", 1.6, MOL_C))
            self.play(Write(ab[0]), run_time=1.0)
            b.until(0.4)
            self.play(Write(ab[1]), run_time=1.2)
        with self.beat("b03") as b:
            c1 = L(r"\text{c. } \Delta T = 24.30 - 20.00 = 4.30\ {}^{\circ}\text{C}", 0.8, TEMP_C)
            c2 = L(r"q_{\text{cal}} = 590 \times 4.30 = 2537\ \text{J}", 0.15, SURR)
            note = T("CF measured for these exact conditions", size=SMALL + 1, color=MUTED).next_to(c2, RIGHT, buff=0.3)
            self.play(Write(c1), run_time=1.0)
            b.until(0.45)
            self.play(Write(c2), FadeIn(note), run_time=1.0)
        with self.beat("b04") as b:
            pred = T("predict: strong acid + strong base → roughly −50 to −60 kJ per mol of water", size=LABEL, color=UNKNOWN)
            pred.move_to([0, -0.55, 0])
            self.play(FadeIn(pred), run_time=0.7)
            self.pred = pred
        with self.beat("b05") as b:
            d = L(r"\text{d. } \Delta H = \frac{-2.537\ \text{kJ}}{0.0450\ \text{mol H}_2\text{O}} = -56.4\ \text{kJ mol}^{-1}", -1.5, GOOD, EQ_SMALL - 2)
            self.play(Write(d), run_time=1.5)
            rb = result_box(d[0][2:])
            ok = T("✓ in range", size=SMALL + 1, color=GOOD).next_to(d, RIGHT, buff=0.3)
            b.until(0.7)
            self.play(FadeIn(ok), run_time=0.4)
            basis = T("per mole of water formed", size=SMALL + 1, color=UNKNOWN).next_to(d, DOWN, buff=0.15).align_to(d, LEFT).shift(1.0 * RIGHT)
            self.play(FadeIn(basis), run_time=0.4)
        with self.beat("b06") as b:
            self.clear(h, req)
            tally = mark_tally([(2, "amounts"), (2, "limiting reagent and excess"), (2, "heat gained: 2537 J"),
                                (2, "denominator, sign and value: −56.4 kJ mol⁻¹")], width=7.4).move_to([0, 0.3, 0])
            self.play(FadeIn(tally), run_time=0.9)
            self.tally = tally
        with self.beat("b07") as b:
            self.play(FadeOut(self.tally), run_time=0.4)
            ws = VGroup(wrong_panel("÷ acid supplied", [M(r"\frac{-2.537}{0.0600} = -42.3", size=EQ_SMALL - 8, color=TEXT)], width=3.8, size=SMALL + 2),
                        wrong_panel("÷ total moles", [M(r"\frac{-2.537}{0.105} = -24.2", size=EQ_SMALL - 8, color=TEXT)], width=3.8, size=SMALL + 2),
                        wrong_panel("÷ total volume", [T("kJ per litre: not molar", size=SMALL + 2)], width=3.8, size=SMALL + 2))
            ws.arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to([0, 0.6, 0])
            for i, w in enumerate(ws):
                b.until(0.1 + 0.2 * i)
                self.play(FadeIn(w), run_time=0.5)
            first = T("First wrong step in each: not asking how much reaction actually happened.", size=LABEL + 2, color=UNKNOWN).move_to([0, -1.5, 0])
            b.until(0.8)
            self.play(FadeIn(first), run_time=0.6)


# =====================================================================================
class E10S07_MassModel(NarratedScene):
    def construct(self):
        h = header("No calibration factor? Use the solution's mass")
        x0 = -6.0

        def L(tex, y, col=TEXT, s=EQ_SMALL - 6):
            return M(tex, size=s, color=col).move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
        with self.beat("b01") as b:
            chips = VGroup(chip("treat the solution as water", SURR, size=SMALL + 1),
                           chip("density 1.00 g mL⁻¹", MASS_C, size=SMALL + 1),
                           chip("c = 4.18 J g⁻¹ °C⁻¹", ENERGY_C, size=SMALL + 1)).arrange(RIGHT, buff=0.3)
            chips.move_to([0, 2.2, 0])
            self.play(FadeIn(h), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.3), run_time=1.2)
            f = M(r"q = m\,c\,\Delta T \quad (m = \text{total mass of the mixed solution})", size=EQ_SMALL - 4).move_to([0, 1.45, 0])
            b.until(0.6)
            self.play(Write(f), run_time=1.0)
        with self.beat("b02") as b:
            l1 = L(r"V = 75.0 + 50.0 = 125.0\ \text{mL} \;\Rightarrow\; m = 125.0\ \text{g}", 0.6, MASS_C)
            l2 = L(r"q = 125.0 \times 4.18 \times 4.30 = 2247\ \text{J}", -0.1, ENERGY_C)
            l3 = L(r"\Delta H = -\frac{2.247\ \text{kJ}}{0.0450\ \text{mol}} = -49.9\ \text{kJ mol}^{-1}", -0.95, UNKNOWN)
            src = T("Q19 mixture: rise 4.30 °C; 0.0450 mol water formed", size=SMALL + 1, color=MUTED).move_to([0, -2.1, 0])
            self.play(Write(l1), FadeIn(src), run_time=1.0)
            b.until(0.4)
            self.play(Write(l2), run_time=1.0)
            b.until(0.7)
            self.play(Write(l3), run_time=1.0)
            self.work, self.src = VGroup(l1, l2, l3), src
        with self.beat("b03") as b:
            tgt = self.work.copy().scale(0.75)
            tgt.move_to([0, -0.05, 0]).align_to([-6.3, 0, 0], LEFT)
            self.play(FadeOut(self.src), Transform(self.work, tgt), run_time=0.7)
            sc = 0.0042
            x_left = 2.2

            def bar(v, y, col, lab, val):
                r = Rectangle(width=v * sc, height=0.32, fill_color=col, fill_opacity=0.85, stroke_width=0)
                r.move_to([0, y, 0]).align_to([x_left, 0, 0], LEFT)
                return VGroup(r, T(lab, size=SMALL, color=col).next_to(r, UP, buff=0.06).align_to(r, LEFT),
                              T(val, size=SMALL, color=col).next_to(r, RIGHT, buff=0.12))
            hd = T("heat capacity counted (J °C⁻¹)", size=SMALL + 1, color=MUTED).move_to([3.6, 1.05, 0])
            b1 = bar(590, 0.3, UNKNOWN, "calibration factor: whole calorimeter", "590")
            b2 = bar(522.5, -0.45, SURR, "solution only: 125.0 × 4.18", "522.5")
            self.play(FadeIn(hd), FadeIn(b1), FadeIn(b2), run_time=0.9)
            cmp = VGroup(T("CF model: ΔH = −56.4 kJ mol⁻¹", size=SMALL + 2, color=UNKNOWN),
                         T("solution-only model: ΔH = −49.9 kJ mol⁻¹", size=SMALL + 2, color=SURR))
            cmp.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.1, -1.45, 0])
            b.until(0.45)
            self.play(FadeIn(cmp), run_time=0.7)
            use = T("use the model the question gives, and say which one you used", size=LABEL, color=GOOD).move_to([0, -2.4, 0])
            b.until(0.8)
            self.play(FadeIn(use), run_time=0.5)


# =====================================================================================
class E10S08_Extent(NarratedScene):
    def construct(self):
        h = header("One mole of reagent ≠ one mole of reaction")
        eq = M(r"2\ce{NaOH(aq)}", "+", r"\ce{H2SO4(aq)}", r"\ce{->}", r"\ce{Na2SO4(aq)}", "+", r"2\ce{H2O(l)}", size=EQ_SMALL).move_to([0, 2.3, 0])
        dh = M(r"\Delta H = -114\ \text{kJ}\ \ (\text{equation as written})", size=EQ_SMALL, color=SYSTEM).next_to(eq, DOWN, buff=0.25)
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(eq), run_time=1.2)
            b.until(0.5)
            self.play(Write(dh), run_time=1.0)
        with self.beat("b02") as b:
            one = VGroup(T("1 mol of reaction =", size=LABEL + 2),
                         T("2 mol NaOH + 1 mol H₂SO₄ → 2 mol H₂O", size=LABEL + 2, color=MOL_C)).arrange(RIGHT, buff=0.3).move_to([0, 0.75, 0])
            per = T("114 kJ released per 2 mol NaOH (per 2 mol H₂O)", size=LABEL + 2, color=SYSTEM).move_to([0, 0.1, 0])
            self.play(FadeIn(one), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(per), run_time=0.7)
        with self.beat("b03") as b:
            f = M(r"\text{extent} = \min\!\left(\frac{n}{\text{coefficient}}\right)", r"\qquad q = \text{extent} \times |\Delta H|", size=EQ_SMALL).move_to([0, -1.0, 0])
            self.play(Write(f), run_time=1.4)
            coef = SurroundingRectangle(eq[0][0], color=UNKNOWN, buff=0.06)
            cl = T("the coefficient sits under n", size=SMALL + 1, color=UNKNOWN).next_to(f, DOWN, buff=0.2).shift(1.8 * LEFT)
            b.until(0.5)
            self.play(Create(coef), FadeIn(cl), run_time=0.7)
            w = T("n(NaOH) × 114 kJ: double counts", size=LABEL, color=BAD).next_to(cl, RIGHT, buff=0.8)
            b.until(0.75)
            self.play(FadeIn(w), run_time=0.5)


# =====================================================================================
class E10S09_Q20(NarratedScene):
    def construct(self):
        h = header("Practice Q20")
        qc = question_card("Q20", size=SMALL + 2, width=13.0, cols=2).move_to([0, 0.2, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        req = requested("final temperature")
        colL = -6.3

        def L(tex, y, col=TEXT, s=EQ_SMALL - 6):
            return M(tex, size=s, color=col).move_to([0, y, 0]).align_to([colL, 0, 0], LEFT)
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(req), run_time=0.5)
            l1 = L(r"\ce{NaOH}: \tfrac{0.0300}{2} = 0.0150 \qquad \ce{H2SO4}: \tfrac{0.0200}{1} = 0.0200", 2.3, MOL_C)
            self.play(Write(l1), run_time=1.3)
            l2 = L(r"\text{NaOH limiting; extent} = 0.0150\ \text{mol}", 1.6, UNKNOWN)
            b.until(0.6)
            self.play(Write(l2), run_time=1.0)
        with self.beat("b03") as b:
            l3 = L(r"q = 0.0150 \times 114 = 1.710\ \text{kJ} = 1710\ \text{J}", 0.9, ENERGY_C)
            self.play(Write(l3), run_time=1.2)
        th = Thermometer(height=3.0, level=0.2).move_to([5.4, -0.2, 0])
        tl0 = T("21.0 °C", size=LABEL).next_to(th, LEFT, buff=0.2).shift(0.6 * DOWN)
        with self.beat("b04") as b:
            l4 = L(r"\Delta T = \frac{1710\ \text{J}}{480\ \text{J}\ {}^{\circ}\text{C}^{-1}} = 3.5625\ {}^{\circ}\text{C}", 0.1, TEMP_C)
            self.play(Write(l4), FadeIn(th), FadeIn(tl0), run_time=1.3)
        with self.beat("b05") as b:
            l5 = L(r"T_{\text{final}} = 21.0 + 3.5625 = 24.5625 \approx 24.6\ {}^{\circ}\text{C}", -0.7, GOOD)
            self.play(Write(l5), th.level.animate.set_value(0.55), run_time=1.4)
            tl1 = T("24.6 °C", size=LABEL, color=GOOD).next_to(th, LEFT, buff=0.2).shift(0.35 * UP)
            self.play(FadeIn(tl1), run_time=0.4)
        with self.beat("b06") as b:
            l6 = L(r"n(\ce{H2SO4})_{\text{left}} = 0.0200 - 0.0150 = 0.00500\ \text{mol}", -1.45, MOL_C)
            self.play(Write(l6), run_time=1.2)
        with self.beat("b07") as b:
            self.clear(h, req)
            tally = mark_tally([(1, "limiting by n/coefficient"), (1, "extent 0.0150 mol"), (1, "heat 1.710 kJ"),
                                (1, "rise 3.56 °C"), (1, "final 24.6 °C"), (1, "acid left 0.00500 mol")], width=5.2, size=SMALL + 2).move_to([-3.5, 0.3, 0])
            ws = VGroup(wrong_panel("0.0300 × 114 kJ", [T("3.42 kJ: twice the heat", size=LABEL)], width=4.6),
                        wrong_panel("Rise reported as final T", [T("“3.56 °C”", size=LABEL)], width=4.6))
            ws.arrange(DOWN, buff=0.3).move_to([3.4, 0.3, 0])
            self.play(FadeIn(tally), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(ws), run_time=0.8)


# =====================================================================================
class E10S10_Coefficients(NarratedScene):
    def construct(self):
        h = header("Coefficients change ΔH, not the heat")
        left = VGroup(TB("as written", size=LABEL + 2, color=SYSTEM),
                      M(r"2\ce{NaOH} + \ce{H2SO4} \ce{->} \ce{Na2SO4} + 2\ce{H2O}", size=EQ_SMALL - 8),
                      M(r"\Delta H = -114\ \text{kJ}", size=EQ_SMALL - 4, color=SYSTEM),
                      M(r"\text{extent} = \tfrac{0.0300}{2} = 0.0150", size=EQ_SMALL - 6),
                      M(r"q = 0.0150 \times 114 = 1.710\ \text{kJ}", size=EQ_SMALL - 4, color=ENERGY_C)).arrange(DOWN, buff=0.25)
        right = VGroup(TB("halved", size=LABEL + 2, color=SURR),
                       M(r"\ce{NaOH} + \tfrac{1}{2}\ce{H2SO4} \ce{->} \tfrac{1}{2}\ce{Na2SO4} + \ce{H2O}", size=EQ_SMALL - 8),
                       M(r"\Delta H = -57\ \text{kJ}", size=EQ_SMALL - 4, color=SURR),
                       M(r"\text{extent} = \tfrac{0.0300}{1} = 0.0300", size=EQ_SMALL - 6),
                       M(r"q = 0.0300 \times 57 = 1.710\ \text{kJ}", size=EQ_SMALL - 4, color=ENERGY_C)).arrange(DOWN, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to([0, 0.4, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(left[:3]), run_time=0.9)
            b.until(0.35)
            self.play(FadeIn(right[:3]), run_time=0.9)
        with self.beat("b02") as b:
            self.play(FadeIn(left[3]), FadeIn(right[3]), run_time=0.8)
            b.until(0.4)
            self.play(Write(left[4]), Write(right[4]), run_time=1.2)
            same = VGroup(SurroundingRectangle(left[4], color=GOOD, buff=0.08), SurroundingRectangle(right[4], color=GOOD, buff=0.08))
            self.play(Create(same), run_time=0.5)
        with self.beat("b03") as b:
            msg = T("Same physical reaction, same calorimeter → same heat, whatever the coefficients", size=LABEL + 2, color=UNKNOWN)
            mp = panel(msg, color=UNKNOWN)
            VGroup(mp, msg).move_to([0, -2.2, 0])
            self.play(FadeIn(mp), FadeIn(msg), run_time=0.9)


# =====================================================================================
class E10S11_Recap(NarratedScene):
    def construct(self):
        h = header("The reaction calorimetry chain")
        steps = ["n = c × V (V in litres) for each reagent",
                 "limiting reagent and reaction extent",
                 "q(cal) = CF × ΔT",
                 "q(rxn) = −q(cal)",
                 "ΔH = q(rxn) ÷ the amount it refers to (say what it is)"]
        rows = VGroup(*[VGroup(number_badge(i), T(s_, size=LABEL + 2)).arrange(RIGHT, buff=0.3) for i, s_ in enumerate(steps, 1)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.3, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for i, r in enumerate(rows):
                b.until(0.05 + 0.18 * i)
                self.play(FadeIn(r, shift=0.1 * RIGHT), run_time=0.5)
        with self.beat("b02") as b:
            self.play(FadeOut(rows), run_time=0.4)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN),
                       T("0.0400 mol of water forms; the calorimeter gains 2.40 kJ. ΔH per mol of water?", size=LABEL + 2)).arrange(DOWN, buff=0.35).move_to([0, 1.0, 0])
            self.play(FadeIn(q), run_time=0.8)
            self.q = q
        with self.beat("b03") as b:
            a = M(r"\Delta H = \frac{-2.40\ \text{kJ}}{0.0400\ \text{mol}} = -60.0\ \text{kJ mol}^{-1}", size=EQ, color=GOOD).next_to(self.q, DOWN, buff=0.5)
            self.play(Write(a), run_time=1.2)
            b.until(0.5)
            nxt = T("Next: Episode 11 · Temperature graphs, correction and experimental reasoning", size=LABEL, color=MUTED).move_to([0, -2.35, 0])
            self.play(FadeIn(nxt), run_time=0.5)


EPISODE_SCENES = ["E10S01_Retrieval", "E10S02_Mixing", "E10S03_Limiting", "E10S04_Signs", "E10S05_Falls",
                  "E10S06_Q19", "E10S07_MassModel", "E10S08_Extent", "E10S09_Q20", "E10S10_Coefficients",
                  "E10S11_Recap"]
