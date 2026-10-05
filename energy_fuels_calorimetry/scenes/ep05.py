"""
Episode 05 - Food as a chemical energy source.
Narration: scripts/ep05.md (beat names must match).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (bullets, mark_tally, question_card, result_box, right_panel, table,  # noqa: E402
                               title_card, wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, ENERGY_C, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, MASS_C, MUTED,  # noqa: E402
                          PANEL, SMALL, SURR, SYSTEM, TEXT, UNKNOWN, USEFUL, M, T, TB, chip, header, panel)

CARB, PROT, FAT = "#F7DC6F", "#85C1E9", "#F1948A"
SCALE = 1 / 330      # bar length (units) per kJ


def requested(text: str) -> VGroup:
    from shared.style import asked_pill
    return asked_pill(text)


def seg(kj: float, color: str, label: str, h: float = 0.7) -> VGroup:
    r = Rectangle(width=max(kj * SCALE, 0.02), height=h, fill_color=color, fill_opacity=0.9, stroke_color=BG, stroke_width=2)
    t = T(label, size=SMALL, color=BG, weight="BOLD").move_to(r)
    if t.width > r.width - 0.1:
        t.scale((r.width - 0.1) / t.width)
    return VGroup(r, t)


def food_bar(c_kj, p_kj, f_kj, x_left=-5.6, y=0.0, labels=True):
    parts = [seg(c_kj, CARB, "carb" if labels else ""), seg(p_kj, PROT, "prot" if labels else ""), seg(f_kj, FAT, "fat" if labels else "")]
    g = VGroup(*parts).arrange(RIGHT, buff=0)
    g.move_to([0, y, 0]).align_to([x_left, 0, 0], LEFT)
    return g


# =====================================================================================
class E05S01_Retrieval(NarratedScene):
    def construct(self):
        tc = title_card(5, "Food as a chemical energy source")
        with self.beat("b01"):
            self.play(FadeIn(tc, shift=0.2 * UP), run_time=1.5)
        with self.beat("b02") as b:
            self.play(FadeOut(tc), run_time=0.5)
            h = header("Retrieval check")
            q1 = T("1.  Is cellular respiration exothermic or endothermic?", size=BODY)
            q2 = T("2.  Where does the energy for photosynthesis come from?", size=BODY)
            qs = VGroup(q1, q2).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([0, 0.9, 0])
            self.play(FadeIn(h), FadeIn(q1), run_time=0.7)
            b.until(0.4)
            self.play(FadeIn(q2), run_time=0.7)
            self.qs = qs
        with self.beat("b03") as b:
            a1 = T("exothermic", size=BODY, color=GOOD).next_to(self.qs[0], DOWN, buff=0.15).align_to(self.qs[0], LEFT).shift(0.6 * RIGHT)
            a2 = T("absorbed from sunlight (endothermic)", size=BODY, color=GOOD).next_to(self.qs[1], DOWN, buff=0.15).align_to(self.qs[1], LEFT).shift(0.6 * RIGHT)
            self.play(FadeIn(a1), run_time=0.5)
            b.until(0.35)
            self.play(FadeIn(a2), run_time=0.6)


# =====================================================================================
class E05S02_Respiration(NarratedScene):
    def construct(self):
        h = header("Respiration: food as a fuel")
        eq = M(r"\ce{C6H12O6}", "+", r"6\,\ce{O2}", r"\ce{->}", r"6\,\ce{CO2}", "+", r"6\,\ce{H2O}", size=EQ).move_to([0, 1.6, 0])
        same = T("same overall equation and energy change as burning glucose; many enzyme-controlled steps",
                 size=LABEL, color=MUTED).next_to(eq, DOWN, buff=0.3)
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(eq), run_time=1.4)
            b.until(0.5)
            self.play(FadeIn(same), run_time=0.8)
        o0 = T("O: 0", size=LABEL, color=UNKNOWN).next_to(eq[2], UP, buff=0.25)
        o1 = T("O: −2", size=LABEL, color=UNKNOWN).next_to(eq[4], UP, buff=0.25)
        o2 = T("O: −2", size=LABEL, color=UNKNOWN).next_to(eq[6], UP, buff=0.25)
        with self.beat("b02") as b:
            self.play(FadeOut(same), FadeIn(o0), run_time=0.6)
            b.until(0.25)
            self.play(FadeIn(o1), FadeIn(o2), run_time=0.7)
            red = VGroup(T("oxidation number of O decreases: oxygen is reduced", size=LABEL + 2, color=UNKNOWN),
                         T("glucose is oxidised: a redox reaction", size=LABEL + 2)).arrange(DOWN, buff=0.2).move_to([0, 0.2, 0])
            b.until(0.45)
            self.play(FadeIn(red[0]), run_time=0.7)
            b.until(0.75)
            self.play(FadeIn(red[1]), run_time=0.6)
            self.red = red
        with self.beat("b03") as b:
            self.play(FadeOut(self.red), run_time=0.4)
            total = Rectangle(width=9.0, height=0.7, stroke_color=TEXT, stroke_width=2).move_to([0, -0.6, 0])
            tl = T("energy released by respiration (conserved)", size=LABEL).next_to(total, UP, buff=0.12)
            work = Rectangle(width=3.6, height=0.7, fill_color=USEFUL, fill_opacity=0.85, stroke_width=0).align_to(total, LEFT).set_y(-0.6)
            heat = Rectangle(width=5.4, height=0.7, fill_color=SYSTEM, fill_opacity=0.6, stroke_width=0).next_to(work, RIGHT, buff=0)
            wl = T("useful work (muscles, cells)", size=SMALL + 1, color=USEFUL).next_to(work, DOWN, buff=0.12)
            hl = T("heat (keeps the body warm)", size=SMALL + 1, color=SYSTEM).next_to(heat, DOWN, buff=0.12)
            sch = T("schematic split, not to scale", size=SMALL, color=MUTED).move_to([0, -2.2, 0])
            self.play(Create(total), FadeIn(tl), run_time=0.8)
            b.until(0.35)
            self.play(GrowFromEdge(work, LEFT), FadeIn(wl), run_time=1.0)
            b.until(0.6)
            self.play(GrowFromEdge(heat, LEFT), FadeIn(hl), FadeIn(sch), run_time=1.0)


# =====================================================================================
class E05S03_Factors(NarratedScene):
    def construct(self):
        h = header("Energy factors")
        rows = [["Nutrient", "Energy factor"], ["carbohydrate", "16 kJ g⁻¹"], ["protein", "17 kJ g⁻¹"], ["fat", "37 kJ g⁻¹"]]
        tb = table(rows, [3.4, 3.0], size=LABEL + 2, row_h=0.65).move_to([-3.6, 1.15, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(tb), run_time=1.0)
            note = T("fat: more than twice the others", size=LABEL, color=FAT).next_to(tb, RIGHT, buff=0.5).shift(0.6 * DOWN)
            b.until(0.6)
            self.play(FadeIn(note), run_time=0.6)
            self.note = note
        lab = VGroup(TB("Muesli bar, per 100 g", size=LABEL + 2), T("illustrative label values", size=SMALL, color=MUTED),
                     T("carbohydrate 60 g", size=LABEL, color=CARB), T("protein 8 g", size=LABEL, color=PROT),
                     T("fat 15 g", size=LABEL, color=FAT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lb = panel(lab)
        lg = VGroup(lb, lab).move_to([3.6, 1.2, 0])
        with self.beat("b02") as b:
            self.play(FadeOut(self.note), FadeIn(lg), run_time=0.9)
        calcs = VGroup(M(r"60\ \text{g} \times 16\ \text{kJ g}^{-1} = 960\ \text{kJ}", size=EQ_SMALL - 6, color=CARB),
                       M(r"8\ \text{g} \times 17\ \text{kJ g}^{-1} = 136\ \text{kJ}", size=EQ_SMALL - 6, color=PROT),
                       M(r"15\ \text{g} \times 37\ \text{kJ g}^{-1} = 555\ \text{kJ}", size=EQ_SMALL - 6, color=FAT)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        calcs.move_to([-3.0, -0.95, 0])
        bar = food_bar(960, 136, 555, x_left=0.6, y=-1.0)
        with self.beat("b03") as b:
            for i in range(3):
                b.until(0.1 + 0.25 * i)
                self.play(Write(calcs[i]), FadeIn(bar[i], shift=0.1 * RIGHT), run_time=0.9)
            gc = T("grams cancel → kJ", size=SMALL, color=MUTED).next_to(calcs, DOWN, buff=0.12)
            self.play(FadeIn(gc), run_time=0.4)
        with self.beat("b04") as b:
            tot = M(r"\text{total} = 1651\ \text{kJ per 100 g}", size=EQ_SMALL - 2, color=ENERGY_C).next_to(bar, DOWN, buff=0.3).align_to(bar, LEFT)
            brace = Brace(bar, UP, color=ENERGY_C)
            self.play(GrowFromCenter(brace), Write(tot), run_time=1.0)
            third = T("fat: 15 g gives about a third of the energy", size=SMALL + 1, color=FAT).next_to(tot, DOWN, buff=0.15).align_to(tot, LEFT)
            b.until(0.6)
            self.play(Indicate(bar[2]), FadeIn(third), run_time=1.0)


# =====================================================================================
class E05S04_Scaling(NarratedScene):
    def construct(self):
        h = header("Per 100 g, per serving, per packet")
        base = M(r"1651\ \text{kJ per 100 g}", size=EQ, color=ENERGY_C).move_to([0, 2.1, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(base), run_time=1.0)
            sv = T("serving: 45 g = 45/100 of 100 g", size=LABEL + 2).move_to([0, 1.2, 0])
            b.until(0.5)
            self.play(FadeIn(sv), run_time=0.7)
        line = M(r"E_{\text{serving}} = ", r"\frac{1651\ \text{kJ}}{100\ \text{g}}", r"\times 45\ \text{g}", r"= 742.95\ \text{kJ} \approx 743\ \text{kJ}", size=EQ_SMALL)
        line.move_to([0, 0.1, 0])
        with self.beat("b02") as b:
            self.play(Write(line[:3]), run_time=1.4)
            g1, g2 = line[1][-1], line[2][-1]
            st = VGroup(Line(g1.get_corner(DL) + 0.04 * DL, g1.get_corner(UR) + 0.04 * UR, color=BAD, stroke_width=4),
                        Line(g2.get_corner(DL) + 0.04 * DL, g2.get_corner(UR) + 0.04 * UR, color=BAD, stroke_width=4))
            b.until(0.45)
            self.play(Create(st), run_time=0.6)
            self.play(Write(line[3]), run_time=1.0)
        pg = VGroup(T("per gram:", size=LABEL + 2), M(r"\frac{1651\ \text{kJ}}{100\ \text{g}} = 16.5\ \text{kJ g}^{-1}", size=EQ_SMALL - 4)).arrange(RIGHT, buff=0.3)
        pg.move_to([0, -1.2, 0])
        with self.beat("b03") as b:
            self.play(FadeIn(pg), run_time=0.9)
            prop = T("per gram: a property of the food   ·   per serving: depends on how much you eat", size=LABEL, color=MUTED).move_to([0, -2.0, 0])
            b.until(0.5)
            self.play(FadeIn(prop), run_time=0.7)
            self.prop = prop
        with self.beat("b04") as b:
            self.play(FadeOut(self.prop), run_time=0.3)
            ck = T("Checkpoint: two servings instead of one?", size=LABEL + 2, color=UNKNOWN).move_to([0, -2.0, 0])
            self.play(FadeIn(ck), run_time=0.6)
            self.ck = ck
        with self.beat("b05") as b:
            a = VGroup(T("energy taken in doubles: ≈ 1486 kJ", size=LABEL + 2, color=GOOD),
                       T("energy per gram unchanged: 16.5 kJ g⁻¹", size=LABEL + 2, color=GOOD)).arrange(RIGHT, buff=0.6)
            a.move_to([0, -2.50, 0])
            self.play(FadeIn(a[0]), run_time=0.7)
            b.until(0.45)
            self.play(FadeIn(a[1]), run_time=0.6)


# =====================================================================================
class E05S05_Basis(NarratedScene):
    def construct(self):
        h = header("Nutrition factors are a different basis")
        c1 = VGroup(TB("Nutrition factor", size=LABEL + 2, color=CARB), M(r"16\ \text{kJ g}^{-1}", size=EQ),
                    wrapped("rounded average: energy the body can obtain from carbohydrate in typical foods", size=LABEL, width=5.0))
        c1.arrange(DOWN, buff=0.25)
        p1 = panel(c1, color=CARB)
        g1 = VGroup(p1, c1).move_to([-3.4, 0.6, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(g1), run_time=1.0)
        c2 = VGroup(TB("Heat of combustion (pure glucose)", size=LABEL + 2, color=SYSTEM),
                    M(r"\approx 2.8\times10^{3}\ \text{kJ mol}^{-1}", size=EQ_SMALL),
                    M(r"\frac{2.8\times10^{3}\ \text{kJ mol}^{-1}}{180\ \text{g mol}^{-1}} \approx 15.6\ \text{kJ g}^{-1}", size=EQ_SMALL - 6))
        c2.arrange(DOWN, buff=0.25)
        p2 = panel(c2, color=SYSTEM)
        g2 = VGroup(p2, c2).move_to([3.3, 0.6, 0])
        with self.beat("b02") as b:
            self.play(FadeIn(p2), FadeIn(c2[:2]), run_time=0.9)
            b.until(0.5)
            self.play(Write(c2[2]), run_time=1.2)
        with self.beat("b03") as b:
            caut = wrapped("Close, but different questions on different bases: use the data and basis you are given.",
                           size=LABEL + 2, width=11.0, color=UNKNOWN)
            cp = panel(caut, color=UNKNOWN)
            VGroup(cp, caut).move_to([0, -2.1, 0])
            b.until(0.4)
            self.play(FadeIn(cp), FadeIn(caut), run_time=0.9)


# =====================================================================================
class E05S06_Q09(NarratedScene):
    def construct(self):
        h = header("Practice Q09")
        qc = question_card("Q09").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        req = requested("one serving, in kJ and J")
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(req), run_time=0.6)
            plan = VGroup(T("per 100 g label", size=LABEL + 2), Arrow(LEFT * 0.5, RIGHT * 0.5, buff=0, color=TEXT),
                          T("energy per 100 g", size=LABEL + 2), Arrow(LEFT * 0.5, RIGHT * 0.5, buff=0, color=TEXT),
                          T("× 30.0/100", size=LABEL + 2, color=UNKNOWN), Arrow(LEFT * 0.5, RIGHT * 0.5, buff=0, color=TEXT),
                          T("one serving", size=LABEL + 2)).arrange(RIGHT, buff=0.2).move_to([0, 1.9, 0])
            b.until(0.4)
            self.play(FadeIn(plan), run_time=1.0)
            self.plan = plan
        with self.beat("b03") as b:
            pred = T("Predict: 30 g is a bit under a third of 100 g, so a bit under a third of the per-100 g energy",
                     size=LABEL, color=UNKNOWN).move_to([0, 1.1, 0])
            self.play(FadeIn(pred), run_time=0.8)
            self.pred = pred
        calcs = VGroup(M(r"48.0 \times 16 = 768\ \text{kJ}", size=EQ_SMALL - 6, color=CARB),
                       M(r"12.0 \times 17 = 204\ \text{kJ}", size=EQ_SMALL - 6, color=PROT),
                       M(r"18.0 \times 37 = 666\ \text{kJ}", size=EQ_SMALL - 6, color=FAT)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        calcs.move_to([-4.0, -0.4, 0])
        bar = food_bar(768, 204, 666, x_left=-1.4, y=-0.4)
        with self.beat("b04") as b:
            for i in range(3):
                b.until(0.08 + 0.22 * i)
                self.play(Write(calcs[i]), FadeIn(bar[i]), run_time=0.8)
            tot = M(r"1638\ \text{kJ per 100 g}", size=EQ_SMALL - 2, color=ENERGY_C).next_to(bar, RIGHT, buff=0.3)
            b.until(0.8)
            self.play(Write(tot), run_time=0.7)
            self.tot = tot
        with self.beat("b05") as b:
            s1 = M(r"1638\ \text{kJ} \times \frac{30.0\ \text{g}}{100\ \text{g}} = 491.4\ \text{kJ} \approx 491\ \text{kJ}", size=EQ_SMALL - 2)
            s1.move_to([0, -1.6, 0])
            self.play(Write(s1), run_time=1.4)
            ok = T("✓ just under a third", size=SMALL + 1, color=GOOD).next_to(s1, RIGHT, buff=0.3)
            b.until(0.7)
            self.play(FadeIn(ok), run_time=0.4)
        with self.beat("b06") as b:
            s2 = M(r"491.4\ \text{kJ} \times 1000\ \text{J kJ}^{-1} = 4.91\times10^{5}\ \text{J}", size=EQ_SMALL - 2, color=GOOD)
            s2.move_to([0, -2.35, 0])
            self.play(Write(s2), run_time=1.2)
        with self.beat("b07") as b:
            self.clear(h, req)
            tally = mark_tally([(2, "weighted sum: 1638 kJ per 100 g"), (1, "serving factor: 491 kJ"),
                                (1, "conversion: 4.91 × 10⁵ J")], width=5.8).move_to([-3.3, 0.4, 0])
            ws = VGroup(wrong_panel("Whole 90 g packet", [M(r"1638 \times 0.90 = 1474\ \text{kJ}", size=EQ_SMALL - 8, color=TEXT)], width=4.6),
                        wrong_panel("kJ written as J", [T("“491 J”: 1000 × too small", size=LABEL)], width=4.6))
            ws.arrange(DOWN, buff=0.3).move_to([3.4, 0.4, 0])
            self.play(FadeIn(tally), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(ws[0]), run_time=0.6)
            b.until(0.75)
            self.play(FadeIn(ws[1]), run_time=0.6)


# =====================================================================================
class E05S07_WhichFood(NarratedScene):
    def construct(self):
        h = header("More energy per what?")
        y_axis_x = -5.4
        foods = [("nuts", 2500, 25, "#C8A165"), ("cooked pasta", 650, 250, "#F4D03F")]
        sc = 1 / 450

        def bars(values, y0, title):
            t = TB(title, size=LABEL + 2).move_to([0, y0 + 0.75, 0]).align_to([y_axis_x, 0, 0], LEFT)
            g = VGroup(t)
            for i, ((name, _, _, col), v) in enumerate(zip(foods, values)):
                y = y0 - 0.55 * i
                lab = T(name, size=LABEL).move_to([0, y, 0]).align_to([y_axis_x, 0, 0], LEFT)
                r = Rectangle(width=v * sc, height=0.4, fill_color=col, fill_opacity=0.9, stroke_width=0)
                r.move_to([0, y, 0]).align_to([-2.9, 0, 0], LEFT)
                val = T(f"{v:,.0f} kJ".replace(",", " "), size=LABEL).next_to(r, RIGHT, buff=0.15)
                g.add(VGroup(lab, r, val))
            return g
        b1 = bars([2500, 650], 1.6, "per 100 g")
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(b1[0]), run_time=0.6)
            ill = T("illustrative label values", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
            self.play(FadeIn(b1[1]), FadeIn(ill), run_time=0.7)
            b.until(0.6)
            self.play(FadeIn(b1[2]), run_time=0.7)
        with self.beat("b02") as b:
            w1 = T("nuts higher: fat-rich, little water", size=LABEL, color=GOOD).next_to(b1[0], RIGHT, buff=0.6)
            self.play(Indicate(b1[1][1]), FadeIn(w1), run_time=1.0)
            self.w1 = w1
        b2 = bars([625, 1625], -0.75, "per serving (nuts 25 g, pasta 250 g)")
        with self.beat("b03") as b:
            self.play(FadeOut(self.w1), FadeIn(b2[0]), run_time=0.6)
            c1 = M(r"2500 \times \tfrac{25}{100} = 625", size=EQ_SMALL - 8, color=MUTED)
            c2 = M(r"650 \times \tfrac{250}{100} = 1625", size=EQ_SMALL - 8, color=MUTED)
            self.play(FadeIn(b2[1]), run_time=0.7)
            c1.next_to(b2[1], RIGHT, buff=0.4)
            self.play(FadeIn(c1), run_time=0.4)
            b.until(0.55)
            self.play(FadeIn(b2[2]), run_time=0.7)
            c2.next_to(b2[2], RIGHT, buff=0.4)
            self.play(FadeIn(c2), Indicate(b2[2][1]), run_time=0.8)
        with self.beat("b04") as b:
            rule = T("State the basis → show both foods on that basis → then compare", size=LABEL + 2, color=UNKNOWN)
            rp = panel(rule, color=UNKNOWN)
            VGroup(rp, rule).move_to([0, -2.2, 0])
            self.play(FadeIn(rp), FadeIn(rule), run_time=0.9)


# =====================================================================================
class E05S08_Q10(NarratedScene):
    def construct(self):
        h = header("Practice Q10")
        qc = question_card("Q10").scale(0.95).move_to([0, 0.12, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
            bases = T("First: which two comparison bases?", size=LABEL + 2, color=UNKNOWN).next_to(qc, DOWN, buff=0.15)
            self.play(FadeIn(bases), run_time=0.6)
            self.qc, self.bases = qc, bases
        colA, colB = -3.4, 3.4
        hA = TB("Food A", size=BODY, color=SYSTEM).move_to([colA, 2.3, 0])
        hB = TB("Food B", size=BODY, color=SURR).move_to([colB, 2.3, 0])
        with self.beat("b02") as b:
            self.play(FadeOut(self.qc), FadeOut(self.bases), FadeIn(hA), FadeIn(hB), run_time=0.7)
            bt = T("per 100 g", size=LABEL + 2, color=UNKNOWN).move_to([0, 1.65, 0])
            a1 = M(r"50(16) + 10(17) + 12(37)", size=EQ_SMALL - 8).move_to([colA, 1.15, 0])
            a2 = M(r"= 1414\ \text{kJ}", size=EQ_SMALL - 4, color=SYSTEM).next_to(a1, DOWN, buff=0.15)
            b1 = M(r"35(16) + 20(17) + 15(37)", size=EQ_SMALL - 8).move_to([colB, 1.15, 0])
            b2 = M(r"= 1455\ \text{kJ}", size=EQ_SMALL - 4, color=SURR).next_to(b1, DOWN, buff=0.15)
            self.play(FadeIn(bt), Write(a1), run_time=1.0)
            self.play(Write(a2), run_time=0.6)
            b.until(0.55)
            self.play(Write(b1), run_time=1.0)
            self.play(Write(b2), run_time=0.6)
            self.b2 = b2
        with self.beat("b03") as b:
            hi = SurroundingRectangle(self.b2, color=GOOD, buff=0.1)
            hiT = T("higher per 100 g", size=SMALL + 1, color=GOOD).next_to(hi, RIGHT, buff=0.15)
            self.play(Create(hi), FadeIn(hiT), run_time=0.7)
            st = T("per serving", size=LABEL + 2, color=UNKNOWN).move_to([0, -0.45, 0])
            a3 = M(r"1414 \times 0.80 = 1131.2\ \text{kJ}", size=EQ_SMALL - 6, color=SYSTEM).move_to([colA, -1.0, 0])
            b3 = M(r"1455 \times 0.50 = 727.5\ \text{kJ}", size=EQ_SMALL - 6, color=SURR).move_to([colB, -1.0, 0])
            b.until(0.3)
            self.play(FadeIn(st), Write(a3), run_time=1.0)
            b.until(0.65)
            self.play(Write(b3), run_time=1.0)
            hi2 = SurroundingRectangle(a3, color=GOOD, buff=0.1)
            hi2T = T("larger serving energy", size=SMALL + 1, color=GOOD).next_to(hi2, DOWN, buff=0.1)
            self.play(Create(hi2), FadeIn(hi2T), run_time=0.6)
        with self.beat("b04") as b:
            concl = T("B: more energy per 100 g.   A serving: more energy per serving.", size=LABEL + 2, color=UNKNOWN).move_to([0, -2.0, 0])
            self.play(FadeIn(concl), run_time=0.8)
            marks = T("Marks: 2 per-100 g values · 2 serving values · 1 both comparisons with bases", size=SMALL + 1, color=GOOD)
            marks.move_to([0, -2.5, 0])
            b.until(0.4)
            self.play(FadeIn(marks), run_time=0.6)


# =====================================================================================
class E05S09_Recap(NarratedScene):
    def construct(self):
        h = header("Recap")
        items = bullets(["Respiration oxidises food like combustion; oxygen is reduced (0 → −2); energy is conserved: work and heat",
                         "Food energy factors: carbohydrate 16, protein 17, fat 37 kJ per gram",
                         "Scale with units attached: kJ per 100 g × serving mass",
                         "Always state the basis before comparing foods"], size=LABEL + 2, width=12.0, buff=0.35)
        items.move_to([0, 0.3, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for i, it in enumerate(items):
                b.until(0.05 + 0.22 * i)
                self.play(FadeIn(it, shift=0.1 * RIGHT), run_time=0.6)
        with self.beat("b02") as b:
            self.play(FadeOut(items), run_time=0.4)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN),
                       T("How much energy do 20 g of fat provide (food factor)?", size=BODY)).arrange(DOWN, buff=0.35).move_to([0, 1.0, 0])
            self.play(FadeIn(q), run_time=0.7)
            self.q = q
        with self.beat("b03") as b:
            a = M(r"20\ \text{g} \times 37\ \text{kJ g}^{-1} = 740\ \text{kJ}", size=EQ, color=GOOD).next_to(self.q, DOWN, buff=0.5)
            self.play(Write(a), run_time=1.0)
            b.until(0.45)
            nxt = T("Next: Episode 06 · Combustion equations and gaseous products", size=LABEL, color=MUTED).move_to([0, -2.35, 0])
            self.play(FadeIn(nxt), run_time=0.5)


EPISODE_SCENES = ["E05S01_Retrieval", "E05S02_Respiration", "E05S03_Factors", "E05S04_Scaling", "E05S05_Basis",
                  "E05S06_Q09", "E05S07_WhichFood", "E05S08_Q10", "E05S09_Recap"]
