"""
Episode 07 - Limiting reactants, excess fuel and gas mixtures.
Narration: scripts/ep07.md (beat names must match).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (Budget, bullets, mark_tally, mol_CH4, mol_O2, question_card, result_box,  # noqa: E402
                               right_panel, title_card, wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, ENERGY_C, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, MASS_C, MOL_C,  # noqa: E402
                          MUTED, PANEL, SMALL, SURR, SYSTEM, TEXT, UNKNOWN, USEFUL, VOL_C, M, T, TB, chip,
                          header, panel)

O2C, CH4C, INERT, CO2C = "#E74C3C", "#F5B041", "#7F8C8D", "#AEB6BF"


def requested(text: str) -> VGroup:
    from shared.style import asked_pill
    return asked_pill(text)


def stream_bar(parts, width=8.0, h=0.6, y=0.0, x_left=-4.0):
    """parts: [(fraction, label, colour, reactive)] -> VGroup of segments with labels."""
    g = VGroup()
    x = x_left
    for frac, lab, col, reactive in parts:
        w = width * frac
        r = Rectangle(width=w, height=h, fill_color=col, fill_opacity=0.9 if reactive else 0.45,
                      stroke_color=TEXT, stroke_width=1.5).move_to([x + w / 2, y, 0])
        t = T(lab, size=SMALL, color=BG if reactive else TEXT, weight="BOLD").move_to(r)
        if t.width > w - 0.1:
            t.scale((w - 0.1) / t.width)
        seg = VGroup(r, t)
        seg.reactive = reactive
        g.add(seg)
        x += w
    return g


# =====================================================================================
class E07S01_Retrieval(NarratedScene):
    def construct(self):
        tc = title_card(7, "Limiting reactants, excess fuel and gas mixtures")
        with self.beat("b01"):
            self.play(FadeIn(tc, shift=0.2 * UP), run_time=1.5)
        with self.beat("b02") as b:
            self.play(FadeOut(tc), run_time=0.5)
            h = header("Retrieval check")
            q1 = T("1.  Balance the complete combustion of methane.", size=BODY)
            q2 = T("2.  Volume of 0.100 mol CO₂ at SLC?", size=BODY)
            qs = VGroup(q1, q2).arrange(DOWN, buff=0.75, aligned_edge=LEFT).move_to([0, 0.9, 0])
            self.play(FadeIn(h), FadeIn(q1), run_time=0.7)
            b.until(0.4)
            self.play(FadeIn(q2), run_time=0.6)
            self.qs = qs
        with self.beat("b03") as b:
            a1 = M(r"\ce{CH4 + 2O2 -> CO2 + 2H2O}", size=EQ_SMALL, color=GOOD).next_to(self.qs[0], DOWN, buff=0.15).align_to(self.qs[0], LEFT).shift(0.6 * RIGHT)
            a2 = M(r"0.100\ \text{mol} \times 24.8\ \text{L mol}^{-1} = 2.48\ \text{L}", size=EQ_SMALL, color=GOOD)
            a2.next_to(self.qs[1], DOWN, buff=0.15).align_to(self.qs[1], LEFT).shift(0.6 * RIGHT)
            self.play(Write(a1), run_time=0.9)
            b.until(0.4)
            self.play(Write(a2), run_time=0.9)


# =====================================================================================
class E07S02_Batches(NarratedScene):
    def construct(self):
        h = header("Which reactant runs out?")
        recipe = VGroup(TB("Recipe for one batch:", size=LABEL), mol_CH4(0.6), T("+", size=LABEL), mol_O2(0.6), mol_O2(0.6),
                        T("→ CO₂ + 2H₂O", size=LABEL)).arrange(RIGHT, buff=0.25).move_to([0, 2.15, 0])
        ch4s = VGroup(*[mol_CH4(0.7) for _ in range(3)]).arrange(DOWN, buff=0.35).move_to([-5.2, 0.2, 0])
        o2s = VGroup(*[mol_O2(0.7) for _ in range(4)]).arrange(DOWN, buff=0.3).move_to([-3.4, 0.2, 0])
        lab1 = T("3 CH₄", size=LABEL, color=CH4C).next_to(ch4s, DOWN, buff=0.2)
        lab2 = T("4 O₂", size=LABEL, color=O2C).next_to(o2s, DOWN, buff=0.2)
        sch = T("schematic", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(sch), FadeIn(recipe), run_time=0.8)
            self.play(FadeIn(ch4s), FadeIn(o2s), FadeIn(lab1), FadeIn(lab2), run_time=0.8)
            q = T("Methane is the smaller number. Does it run out?", size=LABEL + 2, color=UNKNOWN).move_to([2.6, 1.3, 0])
            b.until(0.6)
            self.play(FadeIn(q), run_time=0.6)
            self.q = q
        boxes = VGroup(*[RoundedRectangle(width=2.6, height=1.3, corner_radius=0.12, color=GOOD, stroke_width=2.5) for _ in range(2)])
        boxes.arrange(RIGHT, buff=0.4).move_to([2.2, -0.2, 0])
        bl = VGroup(*[T(f"batch {i+1}", size=SMALL, color=GOOD).next_to(bx, UP, buff=0.08) for i, bx in enumerate(boxes)])
        with self.beat("b02") as b:
            self.play(FadeOut(self.q), Create(boxes), FadeIn(bl), run_time=0.7)
            for i in range(2):
                c = boxes[i].get_center()
                self.play(ch4s[i].animate(path_arc=PI / 8).move_to(c + LEFT * 0.75),
                          o2s[2 * i].animate(path_arc=-PI / 8).move_to(c + RIGHT * 0.55 + UP * 0.3),
                          o2s[2 * i + 1].animate(path_arc=-PI / 8).move_to(c + RIGHT * 0.55 + DOWN * 0.3), run_time=1.3)
            left = SurroundingRectangle(ch4s[2], color=UNKNOWN, buff=0.12)
            lt = T("1 CH₄ left over", size=LABEL, color=UNKNOWN).next_to(left, RIGHT, buff=0.2)
            out = T("O₂ ran out: O₂ limits the reaction", size=LABEL + 2, color=O2C).move_to([2.2, -1.5, 0])
            b.until(0.6)
            self.play(Create(left), FadeIn(lt), FadeIn(out), FadeOut(lab1), FadeOut(lab2), run_time=0.8)
            self.left = VGroup(left, lt)
        with self.beat("b03") as b:
            rule = VGroup(T("each batch needs 2 O₂ for every 1 CH₄", size=LABEL + 2),
                          T("compare how many batches each reactant could make:", size=LABEL + 2),
                          M(r"\frac{\text{amount}}{\text{coefficient}}", size=EQ, color=UNKNOWN)).arrange(DOWN, buff=0.25)
            rule.move_to([0, -0.2, 0])
            self.clear(h, sch, recipe)
            self.play(FadeIn(rule[0]), run_time=0.6)
            b.until(0.45)
            self.play(FadeIn(rule[1]), Write(rule[2]), run_time=1.2)
            self.rule = rule
        with self.beat("b04") as b:
            self.play(FadeOut(recipe), self.rule.animate.scale(0.86).move_to([0, 1.55, 0]), run_time=0.6)
            rows = VGroup(M(r"\ce{CH4}:\ \frac{1.00\ \text{mol}}{1} = 1.00", size=EQ_SMALL, color=CH4C),
                          M(r"\ce{O2}:\ \frac{1.50\ \text{mol}}{2} = 0.75", size=EQ_SMALL, color=O2C)).arrange(RIGHT, buff=1.2).move_to([0, -0.4, 0])
            self.play(Write(rows[0]), run_time=1.0)
            b.until(0.45)
            self.play(Write(rows[1]), run_time=1.0)
            box = SurroundingRectangle(rows[1], color=UNKNOWN, buff=0.12)
            lim = T("smaller value → O₂ is limiting", size=LABEL + 2, color=UNKNOWN).next_to(rows, DOWN, buff=0.5)
            b.until(0.75)
            self.play(Create(box), FadeIn(lim), run_time=0.7)


# =====================================================================================
class E07S03_Trays(NarratedScene):
    def construct(self):
        h = header("Initial, used, remaining")
        eq = M(r"\ce{CH4 + 2O2 -> CO2 + 2H2O}", size=EQ_SMALL).move_to([-2.0, 2.45, 0])
        ext = VGroup(T("extent =", size=LABEL + 2), M(r"0.75\ \text{mol}", size=EQ_SMALL, color=UNKNOWN)).arrange(RIGHT, buff=0.2)
        ext.move_to([4.2, 2.45, 0])
        bud = Budget(["CH₄", "O₂", "CO₂", "H₂O"], ["initial", "used / formed", "remaining"], col_w=2.6, label_w=1.6,
                     col_colors=[MUTED, SYSTEM, GOOD]).move_to([-0.6, 0.0, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(eq), run_time=1.0)
            self.play(FadeIn(bud), run_time=0.8)
            init = VGroup(bud.cell(0, 0, "1.00"), bud.cell(1, 0, "1.50"), bud.cell(2, 0, "0"), bud.cell(3, 0, "0"))
            self.play(FadeIn(init), run_time=0.6)
            b.until(0.5)
            self.play(FadeIn(ext), run_time=0.6)
        with self.beat("b02") as b:
            u0 = bud.cell(0, 1, "1 × 0.75 = 0.75", SYSTEM)
            u1 = bud.cell(1, 1, "2 × 0.75 = 1.50", SYSTEM)
            self.play(FadeIn(u0), run_time=0.7)
            b.until(0.45)
            self.play(FadeIn(u1), run_time=0.7)
            allx = T("all of it", size=SMALL, color=O2C).next_to(u1, RIGHT, buff=0.1).shift(0.0 * UP)
        with self.beat("b03") as b:
            f0 = bud.cell(2, 1, "+1 × 0.75 = 0.75", GOOD)
            f1 = bud.cell(3, 1, "+2 × 0.75 = 1.50", GOOD)
            self.play(FadeIn(f0), run_time=0.7)
            b.until(0.5)
            self.play(FadeIn(f1), run_time=0.7)
        with self.beat("b04") as b:
            inv = M(r"\text{remaining} = \text{initial} - \text{used} \;\ge 0", size=EQ_SMALL - 4, color=UNKNOWN).move_to([0, -2.35, 0])
            self.play(Write(inv), run_time=1.0)
            r0 = bud.cell(0, 2, "0.25 (excess)", GOOD)
            r1 = bud.cell(1, 2, "0", GOOD)
            r2 = bud.cell(2, 2, "0.75", GOOD)
            r3 = bud.cell(3, 2, "1.50", GOOD)
            self.play(FadeIn(r0), run_time=0.6)
            b.until(0.45)
            self.play(FadeIn(r1), FadeIn(r2), FadeIn(r3), run_time=0.6)
            ticks = T("✓ none negative", size=LABEL, color=GOOD).next_to(bud, RIGHT, buff=0.3)
            b.until(0.7)
            self.play(FadeIn(ticks), run_time=0.5)
        with self.beat("b05") as b:
            self.clear(h, eq)
            p = VGroup(TB("Quick prediction", size=BODY, color=UNKNOWN),
                       T("0.20 mol CH₄ with 0.50 mol O₂", size=BODY),
                       T("Which is limiting? How much of the other is left?", size=LABEL + 2)).arrange(DOWN, buff=0.3)
            p.move_to([0, 0.9, 0])
            self.play(FadeIn(p), run_time=0.8)
            self.p = p
        with self.beat("b06") as b:
            r = VGroup(M(r"\ce{CH4}: \tfrac{0.20}{1} = 0.20", size=EQ_SMALL, color=CH4C),
                       M(r"\ce{O2}: \tfrac{0.50}{2} = 0.25", size=EQ_SMALL, color=O2C)).arrange(RIGHT, buff=1.0)
            r.next_to(self.p, DOWN, buff=0.45)
            self.play(Write(r), run_time=1.2)
            box = SurroundingRectangle(r[0], color=UNKNOWN, buff=0.1)
            a = T("CH₄ limiting · O₂ used 0.40 mol · 0.10 mol O₂ left", size=LABEL + 2, color=GOOD).next_to(r, DOWN, buff=0.4)
            b.until(0.4)
            self.play(Create(box), FadeIn(a), run_time=0.8)
            sw = T("the same reactants can swap roles when the amounts change", size=LABEL, color=MUTED).next_to(a, DOWN, buff=0.25)
            b.until(0.8)
            self.play(FadeIn(sw), run_time=0.5)


# =====================================================================================
class E07S04_MassCheck(NarratedScene):
    def construct(self):
        h = header("Checkpoint: more grams, still limiting")
        eq = M(r"\ce{CH4 + 2O2 -> CO2 + 2H2O}", size=EQ_SMALL).move_to([0, 2.3, 0])
        data = T("3.20 g CH₄ with 9.60 g O₂, ignited", size=BODY).move_to([0, 1.5, 0])
        x0 = -5.6

        def L(tex, y, col=TEXT, s=EQ_SMALL - 6):
            return M(tex, size=s, color=col).move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(eq), run_time=0.9)
            self.play(FadeIn(data), run_time=0.6)
            q = T("Which is limiting? How much of the other is left?", size=LABEL + 2, color=UNKNOWN).move_to([0, 0.75, 0])
            b.until(0.6)
            self.play(FadeIn(q), run_time=0.5)
            self.q = q
        with self.beat("b02") as b:
            self.play(FadeOut(self.q), run_time=0.3)
            l1 = L(r"n(\ce{CH4}) = 3.20 \div 16.0 = 0.200\ \text{mol}", 0.75, CH4C)
            l2 = L(r"n(\ce{O2}) = 9.60 \div 32.0 = 0.300\ \text{mol}", 0.1, O2C)
            self.play(Write(l1), run_time=0.9)
            b.until(0.5)
            self.play(Write(l2), run_time=0.9)
        with self.beat("b03") as b:
            r1 = M(r"\ce{CH4}: \tfrac{0.200}{1} = 0.200", size=EQ_SMALL - 4, color=CH4C).move_to([3.2, 0.75, 0])
            r2 = M(r"\ce{O2}: \tfrac{0.300}{2} = 0.150", size=EQ_SMALL - 4, color=O2C).move_to([3.2, 0.1, 0])
            self.play(Write(r1), run_time=0.8)
            b.until(0.35)
            self.play(Write(r2), run_time=0.8)
            box = SurroundingRectangle(r2, color=UNKNOWN, buff=0.1)
            lim = chip("O₂ limiting, despite more grams and more moles", BAD, size=SMALL + 2).move_to([0, -0.7, 0])
            b.until(0.65)
            self.play(Create(box), FadeIn(lim), run_time=0.7)
        with self.beat("b04") as b:
            l3 = L(r"\text{extent} = 0.150\ \text{mol};\ \ \ce{CH4}\ \text{left} = 0.200 - 0.150 = 0.0500\ \text{mol} = 0.800\ \text{g}",
                   -1.5, GOOD, s=EQ_SMALL - 8)
            l4 = L(r"\ce{CO2}\ \text{formed} = 0.150\ \text{mol}", -2.2, GOOD, s=EQ_SMALL - 8)
            self.play(Write(l3), run_time=1.2)
            b.until(0.7)
            self.play(Write(l4), run_time=0.8)


# =====================================================================================
class E07S05_Q13(NarratedScene):
    def construct(self):
        h = header("Practice Q13")
        qc = question_card("Q13").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        model = T("idealised: reacting ethanol burns completely; excess ethanol left unreacted", size=LABEL, color=MUTED).move_to([0, 2.5, 0])
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(model), run_time=0.6)
            a = VGroup(M(r"n(\text{ethanol}) = 0.400\ \text{mol}", size=EQ_SMALL - 2, color=MOL_C),
                       M(r"n(\ce{O2}) = \frac{32.0\ \text{g}}{32.0\ \text{g mol}^{-1}} = 1.00\ \text{mol}", size=EQ_SMALL - 2, color=MOL_C)).arrange(RIGHT, buff=0.8)
            a.move_to([0, 1.5, 0])
            b.until(0.3)
            self.play(Write(a[0]), run_time=0.7)
            b.until(0.6)
            self.play(Write(a[1]), run_time=1.0)
            self.amts = a
        eq = M(r"\ce{C2H5OH + 3O2 -> 2CO2 + 3H2O}", size=EQ_SMALL).move_to([0, 0.55, 0])
        with self.beat("b03") as b:
            self.play(Write(eq), run_time=0.9)
            cmp_ = VGroup(M(r"\text{ethanol}: \tfrac{0.400}{1} = 0.400", size=EQ_SMALL - 4),
                          M(r"\ce{O2}: \tfrac{1.00}{3} = 0.333", size=EQ_SMALL - 4, color=O2C)).arrange(RIGHT, buff=1.0).move_to([0, -0.4, 0])
            b.until(0.4)
            self.play(Write(cmp_), run_time=1.2)
            box = SurroundingRectangle(cmp_[1], color=UNKNOWN, buff=0.1)
            lim = T("O₂ limiting", size=LABEL + 2, color=UNKNOWN).next_to(box, DOWN, buff=0.15)
            b.until(0.8)
            self.play(Create(box), FadeIn(lim), run_time=0.6)
            self.cmp = VGroup(cmp_, box, lim)
        with self.beat("b04") as b:
            just = right_panel("Exam sentence", ["0.400 mol ethanol would need 3 × 0.400 = 1.20 mol O₂, but only 1.00 mol O₂ is available, "
                                                 "so O₂ is limiting."], width=11.0, size=LABEL)
            just.move_to([0, -1.75, 0])
            self.play(FadeOut(self.cmp[2]), FadeIn(just), run_time=1.0)
            self.just = just
        with self.beat("b05") as b:
            self.play(FadeOut(self.just), FadeOut(self.cmp), FadeOut(self.amts), FadeOut(model), run_time=0.5)
            self.play(eq.animate.move_to([0, 2.45, 0]), run_time=0.5)
            bud = Budget(["ethanol", "O₂", "CO₂"], ["initial (mol)", "used / formed", "remaining"], col_w=2.9, label_w=1.7,
                         col_colors=[MUTED, SYSTEM, GOOD]).move_to([0, 0.75, 0])
            self.play(FadeIn(bud), FadeIn(VGroup(bud.cell(0, 0, "0.400"), bud.cell(1, 0, "1.00"), bud.cell(2, 0, "0"))), run_time=0.8)
            ext = T("extent = 1.00 ÷ 3 = 0.3333 mol", size=LABEL, color=UNKNOWN).next_to(bud, DOWN, buff=0.15)
            self.play(FadeIn(ext), run_time=0.5)
            self.play(FadeIn(bud.cell(0, 1, "0.3333", SYSTEM)), FadeIn(bud.cell(1, 1, "1.00 (all)", SYSTEM)), run_time=0.6)
            b.until(0.5)
            self.play(FadeIn(bud.cell(0, 2, "0.0667", GOOD)), FadeIn(bud.cell(1, 2, "0", GOOD)), run_time=0.6)
            m = M(r"m(\text{ethanol left}) = 0.0667 \times 46.0 = 3.07\ \text{g}", size=EQ_SMALL - 4, color=MASS_C).move_to([0, -1.35, 0])
            b.until(0.75)
            self.play(Write(m), run_time=1.0)
            self.bud, self.ext, self.m = bud, ext, m
        with self.beat("b06") as b:
            self.play(FadeIn(self.bud.cell(2, 1, "+0.6667", GOOD)), FadeIn(self.bud.cell(2, 2, "0.6667", GOOD)), run_time=0.6)
            c = M(r"m(\ce{CO2}) = 0.6667 \times 44.0 = 29.3\ \text{g}", size=EQ_SMALL - 4, color=MASS_C).move_to([0, -1.95, 0])
            e = M(r"E = 0.3333 \times 1370 = 456.7 \approx 457\ \text{kJ released}", size=EQ_SMALL - 4, color=ENERGY_C).move_to([0, -2.5, 0])
            self.play(Write(c), run_time=1.0)
            b.until(0.55)
            self.play(Write(e), run_time=1.0)
        with self.beat("b07") as b:
            self.clear(h)
            tally = mark_tally([(2, "amounts and limiting justification"), (2, "ethanol used; 3.07 g remaining"),
                                (1, "CO₂: 29.3 g"), (1, "energy: 457 kJ")], width=5.6).move_to([-3.4, 0.4, 0])
            ws = VGroup(wrong_panel("Smaller raw amount = limiting", [T("0.400 < 1.00, so ethanol? ✗", size=LABEL)],
                                    note="coefficients ignored", width=4.6),
                        wrong_panel("Starting amount reported as left", [T("0.400 mol (18.4 g) ✗", size=LABEL)], width=4.6))
            ws.arrange(DOWN, buff=0.3).move_to([3.4, 0.4, 0])
            self.play(FadeIn(tally), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(ws[0]), run_time=0.6)
            b.until(0.75)
            self.play(FadeIn(ws[1]), run_time=0.6)


# =====================================================================================
class E07S06_Mixtures(NarratedScene):
    def construct(self):
        h = header("Gas mixtures: only the reactive part reacts")
        air = stream_bar([(0.79, "N₂ and others 79% (inert here)", INERT, False), (0.21, "O₂ 21%", O2C, True)], y=1.4, x_left=-5.6, width=7.0)
        fuel = stream_bar([(0.20, "CO₂ 20%", CO2C, False), (0.80, "CH₄ 80%", CH4C, True)], y=-0.1, x_left=-5.6, width=7.0)
        al = T("air", size=LABEL + 2).next_to(air, LEFT, buff=0.2)
        fl = T("fuel", size=LABEL + 2).next_to(fuel, LEFT, buff=0.2)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(air), FadeIn(al), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(fuel), FadeIn(fl), run_time=0.8)
        with self.beat("b02") as b:
            ass = VGroup(TB("Assumption", size=LABEL + 2, color=UNKNOWN),
                         wrapped("ideal gases at the same temperature and pressure: equal volumes contain equal amounts, "
                                 "so volume fraction = mole fraction", size=LABEL, width=11.0)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            ap = panel(ass, color=UNKNOWN)
            VGroup(ap, ass).move_to([0, -1.85, 0])
            self.play(FadeIn(ap), FadeIn(ass), run_time=1.0)
            self.ass = VGroup(ap, ass)
        box = RoundedRectangle(width=2.2, height=2.0, corner_radius=0.2, color=SYSTEM, stroke_width=3).move_to([4.6, 0.65, 0])
        bt = T("reaction", size=LABEL, color=SYSTEM).move_to(box)
        with self.beat("b03") as b:
            self.play(FadeOut(self.ass), Create(box), FadeIn(bt), run_time=0.7)
            a1 = Arrow(air[1].get_right(), box.get_left() + 0.4 * UP, buff=0.1, color=O2C, stroke_width=4)
            a2 = Arrow(fuel[1].get_right(), box.get_left() + 0.4 * DOWN, buff=0.1, color=CH4C, stroke_width=4)
            self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.8)
            by1 = DashedLine(air[0].get_bottom() + 0.05 * DOWN, air[0].get_bottom() + 0.45 * DOWN, color=INERT)
            by2 = DashedLine(fuel[0].get_bottom() + 0.05 * DOWN, fuel[0].get_bottom() + 0.6 * DOWN, color=CO2C)
            pt = T("pass through unchanged", size=SMALL + 1, color=MUTED).next_to(by2, DOWN, buff=0.1)
            b.until(0.6)
            self.play(Create(by1), Create(by2), FadeIn(pt), run_time=0.8)
            rule = T("split each stream before any stoichiometry", size=LABEL + 2, color=UNKNOWN).move_to([0, -2.1, 0])
            self.play(FadeIn(rule), run_time=0.5)


# =====================================================================================
class E07S07_GasVolumes(NarratedScene):
    def construct(self):
        h = header("Gas volumes react in the same ratio")
        rule = chip("same temperature and pressure: volume ratio = mole ratio", UNKNOWN, size=SMALL + 2).move_to([0, 2.3, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            b.until(0.3)
            self.play(FadeIn(rule), run_time=0.7)
        eq = M(r"\ce{C3H8(g) + 5O2(g) -> 3CO2(g) + 4H2O(l)}", size=EQ_SMALL).move_to([0, 1.5, 0])
        sc, xl = 0.42, -2.0

        def vbar(v, y, col, lab, val):
            r = Rectangle(width=v * sc, height=0.38, fill_color=col, fill_opacity=0.85, stroke_width=0)
            r.move_to([0, y, 0]).align_to([xl, 0, 0], LEFT)
            return VGroup(r, T(lab, size=SMALL + 1).next_to(r, LEFT, buff=0.2).align_to([xl - 0.2, 0, 0], RIGHT),
                          T(val, size=SMALL + 1, color=col).next_to(r, RIGHT, buff=0.15))
        bars = [vbar(2.00, 0.6, SYSTEM, "propane", "2.00 L"), vbar(10.0, 0.0, O2C, "oxygen (× 5)", "10.0 L"),
                vbar(6.00, -0.6, "#AEB6BF", "carbon dioxide (× 3)", "6.00 L")]
        with self.beat("b02") as b:
            self.play(Write(eq), run_time=1.0)
            self.play(FadeIn(bars[0]), run_time=0.5)
            b.until(0.35)
            self.play(GrowFromEdge(bars[1][0], LEFT), FadeIn(bars[1][1:]), run_time=0.8)
            b.until(0.55)
            self.play(GrowFromEdge(bars[2][0], LEFT), FadeIn(bars[2][1:]), run_time=0.8)
            wl = T("water: liquid at SLC, no gas volume", size=SMALL + 1, color=MUTED).move_to([0, -1.15, 0])
            b.until(0.82)
            self.play(FadeIn(wl), run_time=0.5)
        with self.beat("b03") as b:
            air = M(r"V(\text{air}) = \frac{10.0\ \text{L}}{0.210} = 47.6\ \text{L}", size=EQ_SMALL - 6, color=SURR).move_to([0, -1.85, 0])
            self.play(Write(air), run_time=1.1)
            note = T("gases only, all volumes at the same temperature and pressure", size=SMALL + 1, color=UNKNOWN)
            note.move_to([0, -2.5, 0])
            b.until(0.6)
            self.play(FadeIn(note), run_time=0.5)


# =====================================================================================
def syringe(reading: float, label: str, max_ml: float = 60.0, length: float = 4.2) -> VGroup:
    """Schematic gas syringe: barrel with graduations every 10 mL, plunger drawn out to the reading."""
    barrel = Rectangle(width=length, height=0.55, stroke_color=TEXT, stroke_width=2.5)
    marks = VGroup()
    for v in range(0, int(max_ml) + 1, 10):
        x = barrel.get_left()[0] + length * v / max_ml
        marks.add(Line([x, barrel.get_top()[1], 0], [x, barrel.get_top()[1] - 0.15, 0], color=MUTED, stroke_width=1.5))
        marks.add(T(str(v), size=SMALL - 4, color=MUTED).move_to([x, barrel.get_top()[1] + 0.18, 0]))
    xg = barrel.get_left()[0] + length * reading / max_ml
    gas = Rectangle(width=max(0.02, xg - barrel.get_left()[0]), height=0.5, stroke_width=0, fill_color=CO2C,
                    fill_opacity=0.5).move_to(barrel).align_to(barrel, LEFT)
    plunger = VGroup(Line([xg, barrel.get_bottom()[1] + 0.03, 0], [xg, barrel.get_top()[1] - 0.03, 0], color=TEXT,
                          stroke_width=5),
                     Line([xg, barrel.get_center()[1], 0], [barrel.get_right()[0] + 0.6, barrel.get_center()[1], 0],
                          color=TEXT, stroke_width=3))
    nozzle = Line(barrel.get_left(), barrel.get_left() + 0.4 * LEFT, color=TEXT, stroke_width=4)
    lab = T(label, size=SMALL + 1, color=MUTED).next_to(barrel, DOWN, buff=0.15).align_to(barrel, LEFT)
    rd = T(f"{reading:.1f} mL", size=LABEL + 1, color=UNKNOWN).next_to(plunger[1], RIGHT, buff=0.2)
    return VGroup(barrel, marks, gas, plunger, nozzle, lab, rd)


class E07S08_GasMeasure(NarratedScene):
    def construct(self):
        h = header("Measuring a gas volume")
        hyp = T("hypothetical readings", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
        s1 = syringe(2.0, "before the reaction").move_to([-2.7, 1.9, 0])
        s2 = syringe(52.5, "after the reaction").move_to([-2.7, 0.55, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(hyp), run_time=0.5)
            b.until(0.4)
            self.play(FadeIn(s1), run_time=0.7)
            b.until(0.7)
            self.play(FadeIn(s2), run_time=0.7)
        x0 = -6.2

        def L(tex, y, col=TEXT, s=EQ_SMALL - 8):
            return M(tex, size=s, color=col).move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
        with self.beat("b02") as b:
            l1 = L(r"V = 52.5 - 2.0 = 50.5\ \text{mL} = 0.0505\ \text{L}", -0.5, VOL_C)
            l2 = L(r"n = 0.0505 \div 24.8 = 0.00204\ \text{mol}", -1.15, MOL_C)
            l3 = L(r"\%\ \text{yield} = \frac{0.00204}{0.00250} \times 100\% = 81.5\%", -1.95, GOOD)
            self.play(Write(l1), run_time=1.0)
            b.until(0.4)
            self.play(Write(l2), run_time=0.9)
            b.until(0.72)
            self.play(Write(l3), run_time=1.0)
            tr = T("final − initial reading; mL → L", size=SMALL + 1, color=MUTED).next_to(l1, RIGHT, buff=0.4)
            self.play(FadeIn(tr), run_time=0.4)
            self.work = VGroup(l1, l2, l3, tr)
        with self.beat("b03") as b:
            ttl = TB("assumptions behind 24.8 L mol⁻¹", size=LABEL, color=UNKNOWN)
            ass = VGroup(*[T("• " + t, size=SMALL + 1) for t in (
                "gas at 25 °C and 100 kPa", "behaves as an ideal gas", "only this gas is collected",
                "none dissolves or escapes")]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            grp = VGroup(ttl, ass).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.9, 1.35, 0])
            self.play(FadeIn(ttl), LaggedStart(*[FadeIn(a) for a in ass], lag_ratio=0.25), run_time=1.6)
            lim = wrapped("limitation: CO₂ collected over water partly dissolves, so the measured volume is too small",
                          size=SMALL + 1, width=5.2, color=BAD).move_to([3.6, -1.2, 0])
            b.until(0.65)
            self.play(FadeIn(lim), run_time=0.6)


# =====================================================================================
class E07S09_NewVsInlet(NarratedScene):
    def construct(self):
        h = header("New CO₂ versus inlet CO₂")
        box = RoundedRectangle(width=2.6, height=1.6, corner_radius=0.2, color=SYSTEM, stroke_width=3).move_to([0, 0.9, 0])
        bt = T("CH₄ burns", size=LABEL, color=SYSTEM).move_to(box)
        fin = Arrow([-5.6, 0.9, 0], box.get_left(), buff=0.05, color=CH4C, stroke_width=4)
        fin_t = T("fuel: CH₄ + CO₂", size=LABEL).next_to(fin, UP, buff=0.1)
        byp = VGroup(Line([-3.6, 0.9, 0], [-3.6, -0.6, 0], color=CO2C, stroke_width=4),
                     Line([-3.6, -0.6, 0], [3.0, -0.6, 0], color=CO2C, stroke_width=4),
                     Arrow([3.0, -0.6, 0], [3.0, 0.75, 0], buff=0, color=CO2C, stroke_width=4))
        byp_t = T("inlet CO₂ passes through", size=LABEL, color=CO2C).next_to(byp[1], DOWN, buff=0.12)
        out = Arrow(box.get_right(), [5.6, 0.9, 0], buff=0.05, color=GOOD, stroke_width=4)
        new_t = T("new CO₂ (formed)", size=LABEL, color=GOOD).next_to(out, UP, buff=0.12).shift(0.4 * LEFT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), Create(box), FadeIn(bt), GrowArrow(fin), FadeIn(fin_t), run_time=0.9)
            b.until(0.3)
            self.play(Create(byp), FadeIn(byp_t), run_time=1.2)
            b.until(0.55)
            self.play(GrowArrow(out), FadeIn(new_t), run_time=0.8)
        with self.beat("b02") as b:
            cards = VGroup(VGroup(TB("“CO₂ formed / produced”", size=LABEL, color=GOOD), T("new part only", size=LABEL)).arrange(DOWN, buff=0.1),
                           VGroup(TB("“total CO₂ in the exhaust”", size=LABEL, color=TEXT), T("new + inlet", size=LABEL)).arrange(DOWN, buff=0.1))
            cards.arrange(RIGHT, buff=1.4).move_to([0, -2.0, 0])
            self.play(FadeIn(cards[0]), run_time=0.7)
            b.until(0.45)
            self.play(FadeIn(cards[1]), run_time=0.7)


# =====================================================================================
class E07S10_Q14a(NarratedScene):
    def construct(self):
        h = header("Practice Q14 (part 1)")
        qc = question_card("Q14", size=SMALL + 1, width=13.2, cols=2).move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        req = requested("limiting reactant; CH₄ left (g)")
        fuel = stream_bar([(0.80, "CH₄ 0.400 mol", CH4C, True), (0.20, "CO₂ 0.100", CO2C, False)], y=2.0, x_left=-5.0, width=6.0)
        fl = T("12.4 L ÷ 24.8 = 0.500 mol", size=SMALL + 1).next_to(fuel, RIGHT, buff=0.3)
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(req), run_time=0.5)
            self.play(FadeIn(fuel), FadeIn(fl), run_time=0.9)
        air = stream_bar([(0.21, "O₂", O2C, True), (0.79, "inert 79%", INERT, False)], y=1.1, x_left=-5.0, width=6.0)
        al = VGroup(M(r"0.210 \times 90.0 = 18.9\ \text{L}", size=EQ_SMALL - 8),
                    M(r"\tfrac{18.9}{24.8} = 0.7621\ \text{mol}", size=EQ_SMALL - 8, color=O2C)).arrange(RIGHT, buff=0.3).scale(0.88).next_to(air, RIGHT, buff=0.3)
        with self.beat("b03") as b:
            self.play(FadeIn(air), run_time=0.7)
            b.until(0.35)
            self.play(Write(al), run_time=1.2)
        cmp_ = VGroup(M(r"\ce{CH4}: \tfrac{0.400}{1} = 0.400", size=EQ_SMALL - 6, color=CH4C),
                      M(r"\ce{O2}: \tfrac{0.7621}{2} = 0.3810", size=EQ_SMALL - 6, color=O2C)).arrange(RIGHT, buff=0.9).move_to([0, 0.2, 0])
        with self.beat("b04") as b:
            eq = T("CH₄ + 2O₂ → CO₂ + 2H₂O", size=LABEL).next_to(cmp_, LEFT, buff=0.4)
            VGroup(eq, cmp_).move_to([0, 0.2, 0])
            self.play(FadeIn(eq), Write(cmp_), run_time=1.2)
            box = SurroundingRectangle(cmp_[1], color=UNKNOWN, buff=0.1)
            lt = T("O₂ limiting · extent = 0.3810 mol", size=LABEL, color=UNKNOWN).next_to(box, DOWN, buff=0.12)
            b.until(0.6)
            self.play(Create(box), FadeIn(lt), run_time=0.6)
        bud = Budget(["O₂", "CH₄"], ["initial", "used", "remaining"], col_w=2.3, label_w=1.3, row_h=0.55,
                     col_colors=[MUTED, SYSTEM, GOOD]).move_to([-1.5, -1.65, 0])
        with self.beat("b05") as b:
            self.play(FadeIn(bud), run_time=0.5)
            self.play(FadeIn(bud.cell(0, 0, "0.7621")), FadeIn(bud.cell(0, 1, "0.7621", SYSTEM)), FadeIn(bud.cell(0, 2, "0", GOOD)), run_time=0.8)
            b.until(0.35)
            self.play(FadeIn(bud.cell(1, 0, "0.400")), FadeIn(bud.cell(1, 1, "0.3810", SYSTEM)), FadeIn(bud.cell(1, 2, "0.01895", GOOD)), run_time=0.8)
            m = M(r"0.01895 \times 16.0 = 0.303\ \text{g}", size=EQ_SMALL - 6, color=MASS_C).next_to(bud, RIGHT, buff=0.35)
            b.until(0.7)
            self.play(Write(m), run_time=0.9)


# =====================================================================================
class E07S11_Q14b(NarratedScene):
    def construct(self):
        h = header("Practice Q14 (part 2)")
        sc = 0.55
        newb = Rectangle(width=9.45 * sc, height=0.6, fill_color=GOOD, fill_opacity=0.85, stroke_width=0)
        inb = Rectangle(width=2.48 * sc, height=0.6, fill_color=CO2C, fill_opacity=0.85, stroke_width=0)
        VGroup(newb, inb).arrange(RIGHT, buff=0).move_to([-0.6, 1.4, 0])
        nl = M(r"\text{new: } 0.3810 \times 24.8 = 9.45\ \text{L}", size=EQ_SMALL - 6, color=GOOD).next_to(newb, UP, buff=0.15)
        il = T("inlet: 2.48 L", size=SMALL + 1, color=CO2C).next_to(inb, DOWN, buff=0.12)
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            self.play(GrowFromEdge(newb, LEFT), Write(nl), run_time=1.2)
        tot = M(r"\text{total} = 9.45 + 2.48 = 11.93 \approx 11.9\ \text{L}", size=EQ_SMALL - 4).move_to([0, 0.15, 0])
        with self.beat("b02") as b:
            self.play(GrowFromEdge(inb, LEFT), FadeIn(il), run_time=0.8)
            b.until(0.4)
            self.play(Write(tot), run_time=1.2)
        with self.beat("b03") as b:
            e = M(r"E = 0.3810\ \text{mol} \times 890\ \text{kJ mol}^{-1} = 339\ \text{kJ released}", size=EQ_SMALL - 4, color=ENERGY_C).move_to([0, -0.85, 0])
            self.play(Write(e), run_time=1.2)
            n = T("(ΔH data for water formed as a liquid)", size=SMALL + 1, color=MUTED).next_to(e, DOWN, buff=0.15)
            b.until(0.6)
            self.play(FadeIn(n), run_time=0.5)
        with self.beat("b04") as b:
            self.clear(h)
            tally = mark_tally([(2, "reactive fuel amount and O₂ amount"), (1, "O₂ limiting"), (2, "CH₄ remaining: 0.303 g"),
                                (1, "new CO₂: 9.45 L"), (1, "total CO₂: 11.9 L"), (1, "energy: 339 kJ")], width=6.6).move_to([0, 0.2, 0])
            self.play(FadeIn(tally), run_time=1.0)
            self.tally = tally
        with self.beat("b05") as b:
            self.play(FadeOut(self.tally), run_time=0.4)
            ws = VGroup(wrong_panel("All fuel gas as methane", [T("12.4 L → 0.500 mol CH₄ (should be 0.400)", size=LABEL)], width=7.5),
                        wrong_panel("All air as oxygen", [T("90.0 L → 3.63 mol O₂ → wrong limiting reactant", size=LABEL)], width=7.5),
                        wrong_panel("New and inlet CO₂ mixed up", [T("formed = 9.45 L; total = 11.93 L", size=LABEL)], width=7.5))
            ws.arrange(DOWN, buff=0.25).move_to([0, 0.2, 0])
            for i, w in enumerate(ws):
                b.until(0.1 + 0.28 * i)
                self.play(FadeIn(w), run_time=0.6)


# =====================================================================================
class E07S12_Recap(NarratedScene):
    def construct(self):
        h = header("The limiting-reactant routine")
        steps = ["Convert to moles (reactive part of any mixture only)",
                 "Divide by coefficients: smallest → limiting, gives the extent",
                 "Used = coefficient × extent",
                 "Remaining = initial − used (never negative)",
                 "Formed = coefficient × extent (+ anything passing through)"]
        rows = VGroup()
        from shared.components import number_badge
        for i, s in enumerate(steps, 1):
            rows.add(VGroup(number_badge(i), T(s, size=LABEL + 2)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.2, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for i, r in enumerate(rows):
                b.until(0.05 + 0.18 * i)
                self.play(FadeIn(r, shift=0.1 * RIGHT), run_time=0.5)
        with self.beat("b02") as b:
            self.play(FadeOut(rows), run_time=0.4)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN), M(r"2\ce{H2} + \ce{O2} \ce{->} 2\ce{H2O}", size=EQ),
                       T("3.0 mol H₂ with 2.0 mol O₂: limiting? left over?", size=BODY)).arrange(DOWN, buff=0.3).move_to([0, 1.0, 0])
            self.play(FadeIn(q), run_time=0.8)
            self.q = q
        with self.beat("b03") as b:
            a = VGroup(M(r"\ce{H2}: \tfrac{3.0}{2} = 1.5 \qquad \ce{O2}: \tfrac{2.0}{1} = 2.0", size=EQ_SMALL, color=GOOD),
                       T("H₂ limiting · O₂ used 1.5 mol · 0.50 mol O₂ left", size=LABEL + 2, color=GOOD)).arrange(DOWN, buff=0.25)
            a.next_to(self.q, DOWN, buff=0.45)
            self.play(Write(a[0]), run_time=1.0)
            b.until(0.4)
            self.play(FadeIn(a[1]), run_time=0.6)
            nxt = T("Next: Episode 08 · Measuring combustion energy and efficiency", size=LABEL, color=MUTED).move_to([0, -2.35, 0])
            b.until(0.7)
            self.play(FadeIn(nxt), run_time=0.5)


EPISODE_SCENES = ["E07S01_Retrieval", "E07S02_Batches", "E07S03_Trays", "E07S04_MassCheck", "E07S05_Q13",
                  "E07S06_Mixtures", "E07S07_GasVolumes", "E07S08_GasMeasure", "E07S09_NewVsInlet",
                  "E07S10_Q14a", "E07S11_Q14b", "E07S12_Recap"]
