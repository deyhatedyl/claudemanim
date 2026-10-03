"""
Episode 01 - Mole calculations and units that unlock the topic.
Narration: scripts/ep01.md (beat names must match). Render with tools/render.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (bullets, flask, fraction, given_asked, hladder, ladder,  # noqa: E402
                               mark_tally, mol_H2, mol_H2O, mol_O2, molecule, number_badge,
                               question_card, result_box, right_panel, strike, table, tag,
                               title_card, wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, CONC_C, EQ, EQ_SMALL, ENERGY_C, FAINT, GOOD, HEAD, LABEL,  # noqa: E402
                          MASS_C, MOL_C, MUTED, PANEL, SMALL, SYSTEM, TEXT, UNKNOWN, VOL_C, M, T,
                          TB, chip, header, panel)


def requested(text: str) -> VGroup:
    from shared.style import asked_pill
    return asked_pill(text)


# =====================================================================================
class E01S01_Welcome(NarratedScene):
    def construct(self):
        card = title_card(1, "Mole calculations and units that unlock the topic")
        with self.beat("b01"):
            self.play(FadeIn(card, shift=0.2 * UP), run_time=1.5)

        with self.beat("b02") as b:
            self.play(FadeOut(card), run_time=0.6)
            h = header("Quick check")
            gas = flask(liquid=PANEL, level=0.0)
            dots = VGroup(*[Dot(radius=0.06, color=VOL_C).move_to(gas.get_center() + np.array(p))
                            for p in [(-0.5, -0.8, 0), (0.3, -0.5, 0), (0.0, -0.1, 0), (-0.25, 0.35, 0),
                                      (0.55, -0.95, 0), (-0.75, -0.35, 0), (0.15, 0.75, 0)]])
            water = flask(liquid=VOL_C, level=0.4)
            c1 = VGroup(gas, dots)
            c1.move_to([-5.0, 0.6, 0])
            water.move_to([-2.2, 0.6, 0])
            l1 = T("1 mol H₂(g)", size=LABEL).next_to(c1, DOWN, buff=0.25)
            l2 = T("1 mol H₂O(l)", size=LABEL).next_to(water, DOWN, buff=0.25)
            note = T("schematic, not to scale", size=SMALL, color=MUTED).next_to(VGroup(l1, l2), DOWN, buff=0.3)
            q1 = TB("Same amount?", size=BODY, color=UNKNOWN)
            q2 = TB("Same mass?", size=BODY, color=UNKNOWN)
            qs = VGroup(q1, q2).arrange(DOWN, buff=0.9, aligned_edge=LEFT)
            qs.move_to([0, 1.1, 0]).align_to([0.6, 0, 0], LEFT)
            self.play(FadeIn(h), run_time=0.5)
            self.play(FadeIn(c1), FadeIn(water), run_time=0.8)
            self.play(FadeIn(l1), FadeIn(l2), FadeIn(note), run_time=0.6)
            b.until(0.55)
            self.play(Write(q1), run_time=0.6)
            self.play(Write(q2), run_time=0.6)

        with self.beat("b03") as b:
            a1 = T("Yes: equal numbers of molecules", size=LABEL, color=GOOD).next_to(q1, DOWN, aligned_edge=LEFT, buff=0.2)
            self.play(FadeIn(a1), run_time=0.6)
            b.until(0.3)
            m1 = tag("mass", "≈ 2.0 g", MASS_C).next_to(l1, DOWN, buff=0.25)
            m2 = tag("mass", "≈ 18.0 g", MASS_C).next_to(l2, DOWN, buff=0.25)
            self.play(FadeOut(note), FadeIn(m1), FadeIn(m2), run_time=0.8)
            a2 = T("No: 2.0 g versus 18.0 g", size=LABEL, color=BAD).next_to(q2, DOWN, aligned_edge=LEFT, buff=0.2)
            self.play(FadeIn(a2), run_time=0.6)
            b.until(0.8)
            key = TB("Same amount, different mass", size=BODY, color=SYSTEM).move_to([0, -1.5, 0]).align_to(qs, LEFT)
            self.play(Write(key), run_time=0.8)

        with self.beat("b04") as b:
            self.clear(h)
            new_h = header("In this episode")
            items = ["Amount, mass, volume and concentration are different quantities",
                     "Three relationships that give amount in moles",
                     "A unit ladder for conversions",
                     "A balanced equation as a recipe in moles",
                     "Rounding only at the end",
                     "Practice questions Q01 and Q02"]
            rows = VGroup()
            for i, it in enumerate(items, 1):
                rows.add(VGroup(number_badge(i), T(it, size=LABEL + 2)).arrange(RIGHT, buff=0.3))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([0, -0.2, 0])
            self.play(ReplacementTransform(h, new_h), run_time=0.5)
            for r in rows:
                self.play(FadeIn(r, shift=0.1 * RIGHT), run_time=b.rt(0.08, 0.3, 0.8))


# =====================================================================================
class E01S02_Labels(NarratedScene):
    def construct(self):
        h = header("One sample, several labels")
        fl = flask(liquid="#E59866", level=0.5).scale(1.1).move_to([-4.4, 0.5, 0])
        fl_lab = T("ethanol, C₂H₅OH(l)", size=LABEL).next_to(fl, DOWN, buff=0.25)
        t_mass = tag("mass", "46.0 g", MASS_C)
        t_vol = tag("volume", "about 58 mL", VOL_C)
        t_amt = tag("amount", "? mol", MOL_C)
        n_mass = T("what a balance reads", size=SMALL, color=MUTED)
        n_vol = T("the space it takes up", size=SMALL, color=MUTED)
        n_amt = T("a count of particles", size=SMALL, color=MUTED)
        rows = VGroup(*[VGroup(t, n) for t, n in [(t_mass, n_mass), (t_vol, n_vol), (t_amt, n_amt)]])
        for i, (t, n) in enumerate(rows):
            t.move_to([0, 2.2 - 1.0 * i, 0]).align_to([-1.7, 0, 0], LEFT)
            n.move_to(t).align_to([2.35, 0, 0], LEFT)
        links = VGroup(*[Line(fl.get_right() + 0.1 * RIGHT, r[0].get_left(), color=FAINT, stroke_width=2)
                         for r in rows])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(fl), FadeIn(fl_lab), run_time=0.8)
            for i, r in enumerate(rows):
                b.until(0.25 + 0.22 * i)
                self.play(Create(links[i]), FadeIn(r, shift=0.1 * RIGHT), run_time=0.7)

        with self.beat("b02") as b:
            eggs = VGroup(*[Circle(radius=0.12, color="#F5E6CA", fill_opacity=0.9) for _ in range(12)])
            eggs.arrange_in_grid(2, 6, buff=0.08)
            d1 = VGroup(eggs, T("1 dozen = 12 eggs", size=LABEL)).arrange(RIGHT, buff=0.35)
            d2 = M(r"1\ \text{mol} = 6.02\times10^{23}\ \text{particles}", size=EQ_SMALL, color=MOL_C)
            an = VGroup(d1, d2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            box = panel(an)
            grp = VGroup(box, an).move_to([1.9, -1.6, 0])
            self.play(FadeIn(box), FadeIn(d1), run_time=0.8)
            b.until(0.35)
            self.play(Write(d2), run_time=1.2)

        with self.beat("b03") as b:
            mm = M(r"M(\ce{C2H5OH}) = 46.0\ \text{g mol}^{-1}", size=EQ_SMALL)
            eq = M(r"46.0\ \text{g} \;\longrightarrow\; 1.00\ \text{mol}", size=EQ_SMALL, color=MOL_C)
            g2 = VGroup(mm, eq).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            box2 = panel(g2)
            grp2 = VGroup(box2, g2).move_to(grp)
            self.play(FadeOut(grp), FadeIn(box2), Write(mm), run_time=1.0)
            b.until(0.55)
            self.play(Write(eq), run_time=0.8)
            new_amt = tag("amount", "1.00 mol", MOL_C).move_to(t_amt, aligned_edge=LEFT)
            self.play(Transform(t_amt, new_amt), run_time=0.8)

        with self.beat("b04") as b:
            self.clear(h)
            cols = VGroup()
            specs = [("ethanol", "#E59866", "46.0 g", "1.00 mol", r"M = 46.0\ \text{g mol}^{-1}"),
                     ("water", VOL_C, "46.0 g", "2.56 mol", r"M = 18.0\ \text{g mol}^{-1}")]
            for name, col, mass, amt, mtex in specs:
                f = flask(liquid=col, level=0.5).scale(0.85)
                lab = T(name, size=LABEL)
                tm = tag("mass", mass, MASS_C)
                ta = tag("amount", amt, MOL_C)
                mm = M(mtex, size=EQ_SMALL - 4)
                cols.add(VGroup(f, lab, tm, ta, mm).arrange(DOWN, buff=0.22))
            cols.arrange(RIGHT, buff=1.0).move_to([-3.0, -0.1, 0])
            self.play(FadeIn(cols[0]), run_time=0.8)
            b.until(0.15)
            self.play(FadeIn(cols[1][:3]), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(cols[1][4]), run_time=0.6)
            calc = M(r"n = \frac{46.0\ \text{g}}{18.0\ \text{g mol}^{-1}} = 2.56\ \text{mol}", size=EQ_SMALL - 2)
            calc.next_to(cols, RIGHT, buff=0.5).shift(0.4 * DOWN)
            self.play(Write(calc), FadeIn(cols[1][3]), run_time=1.2)
            b.until(0.85)
            key = TB("Same mass, different amount", size=BODY, color=SYSTEM).next_to(calc, UP, buff=0.6)
            self.play(Write(key), run_time=0.8)

        with self.beat("b05") as b:
            self.clear(h)
            ne1 = VGroup(chip("g", MASS_C, size=LABEL), TB("≠", size=HEAD), chip("mol", MOL_C, size=LABEL)).arrange(RIGHT, buff=0.3)
            ne2 = VGroup(chip("mL", VOL_C, size=LABEL), TB("≠", size=HEAD), chip("L", VOL_C, size=LABEL)).arrange(RIGHT, buff=0.3)
            ne = VGroup(ne1, ne2).arrange(RIGHT, buff=1.6).move_to([0, 0.8, 0])
            msg = T("To change one label into another, you need a relationship that connects them.",
                    size=LABEL + 2).next_to(ne, DOWN, buff=0.8)
            self.play(FadeIn(ne1), run_time=0.6)
            self.play(FadeIn(ne2), run_time=0.6)
            b.until(0.5)
            self.play(Write(msg), run_time=1.4)


# =====================================================================================
class E01S03_ThreeRoutes(NarratedScene):
    def construct(self):
        h = header("Three routes to amount in moles")
        ys = [1.93, 0.65, -0.6]

        def row_label(text, color, y):
            return TB(text, size=LABEL + 2, color=color).move_to([-5.2, y, 0])

        # row 1: mass
        l1 = row_label("From a mass", MASS_C, ys[0])
        f1 = M(r"n", "=", r"\frac{m}{M}", size=EQ).move_to([-2.0, ys[0], 0])
        u1 = fraction([r"\text{g}"], [r"\text{g}", r"\ \text{mol}^{-1}"], size=EQ_SMALL)
        r1 = M(r"=\ \text{mol}", size=EQ_SMALL, color=MOL_C)
        unit1 = VGroup(u1, r1).arrange(RIGHT, buff=0.25).move_to([2.6, ys[0], 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(l1), run_time=0.6)
            self.play(Write(f1), run_time=1.0)
            b.until(0.3)
            self.play(FadeIn(u1), run_time=0.8)
            b.until(0.62)
            s1 = VGroup(strike(u1[0][0]), strike(u1[2][0]))
            self.play(Create(s1), run_time=0.8)
            self.play(Write(r1), run_time=0.6)

        # row 2: solution
        l2 = row_label("From a solution", CONC_C, ys[1])
        f2 = M(r"n", "=", r"c\,V", size=EQ).move_to([-2.0, ys[1], 0])
        u2 = M(r"\text{mol}", r"\ \text{L}^{-1}", r"\times", r"\text{L}", size=EQ_SMALL)
        r2 = M(r"=\ \text{mol}", size=EQ_SMALL, color=MOL_C)
        unit2 = VGroup(u2, r2).arrange(RIGHT, buff=0.25).move_to([2.6, ys[1], 0])
        with self.beat("b02") as b:
            self.play(FadeIn(l2), Write(f2), run_time=1.0)
            b.until(0.35)
            self.play(FadeIn(u2), run_time=0.8)
            b.until(0.65)
            self.play(Create(VGroup(strike(u2[1]), strike(u2[3]))), run_time=0.8)
            self.play(Write(r2), run_time=0.6)

        # row 3: gas
        l3 = row_label("From a gas at SLC", VOL_C, ys[2])
        f3 = M(r"n", "=", r"\frac{V}{V_m}", size=EQ).move_to([-2.0, ys[2], 0])
        u3 = fraction([r"\text{L}"], [r"\text{L}", r"\ \text{mol}^{-1}"], size=EQ_SMALL)
        r3 = M(r"=\ \text{mol}", size=EQ_SMALL, color=MOL_C)
        unit3 = VGroup(u3, r3).arrange(RIGHT, buff=0.25).move_to([2.6, ys[2], 0])
        slc = T("SLC: 25 °C and 100 kPa  →  Vₘ = 24.8 L mol⁻¹", size=LABEL, color=VOL_C)
        slc.move_to([-1.0, -1.6, 0])
        with self.beat("b03") as b:
            self.play(FadeIn(l3), run_time=0.5)
            self.play(Write(slc), run_time=1.2)
            b.until(0.6)
            self.play(Write(f3), FadeIn(u3), run_time=1.0)
            self.play(Create(VGroup(strike(u3[0][0]), strike(u3[2][0]))), Write(r3), run_time=0.8)

        with self.beat("b04") as b:
            warn = VGroup(TB("Only for:", size=LABEL, color=UNKNOWN), T("gases,", size=LABEL),
                          T("at 25 °C and 100 kPa.", size=LABEL),
                          T("Hot exhaust at 600 °C ✗", size=LABEL, color=BAD))
            warn.arrange(RIGHT, buff=0.22)
            warn[3].shift(0.3 * RIGHT)
            wb = panel(warn, color=UNKNOWN, buff=0.18)
            wg = VGroup(wb, warn).move_to([0, -2.3, 0])
            self.play(FadeIn(wb), FadeIn(warn[:3]), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(warn[3]), run_time=0.6)

        with self.beat("b05") as b:
            self.clear(h)
            new_h = header("Checkpoint")
            given = VGroup(M(r"c = 0.100\ \text{mol L}^{-1}", size=EQ, color=CONC_C),
                           M(r"V = 250\ \text{mL}", size=EQ, color=VOL_C)).arrange(RIGHT, buff=1.2)
            given.move_to([0, 1.6, 0])
            ask = M(r"n \overset{?}{=} 0.100 \times 250", size=EQ).move_to([0, 0.1, 0])
            why = T("Why can't you do this?", size=BODY, color=UNKNOWN).next_to(ask, DOWN, buff=0.5)
            self.play(ReplacementTransform(h, new_h), FadeIn(given), run_time=0.8)
            b.until(0.5)
            self.play(Write(ask), run_time=1.0)
            self.play(FadeIn(why), run_time=0.5)
            self.ck_given, self.ck_ask, self.ck_why, self.ck_h = given, ask, why, new_h

        with self.beat("b06") as b:
            self.play(FadeOut(self.ck_ask), FadeOut(self.ck_why), run_time=0.4)
            conv = M(r"250\ \text{mL} \div 1000 = 0.250\ \text{L}", size=EQ_SMALL, color=VOL_C)
            ok = M(r"n", "=", r"0.100\ \text{mol}", r"\ \text{L}^{-1}", r"\times 0.250\ ", r"\text{L}",
                   r"= 0.0250\ \text{mol}", size=EQ_SMALL)
            right = VGroup(conv, ok).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            right.move_to([0, 0.35, 0])
            self.play(Write(conv), run_time=1.0)
            self.play(Write(ok), run_time=1.4)
            self.play(Create(VGroup(strike(ok[3]), strike(ok[5]))), run_time=0.6)
            tick = TB("✓", size=HEAD, color=GOOD).next_to(ok, RIGHT, buff=0.3)
            self.play(FadeIn(tick), run_time=0.3)
            b.until(0.45)
            bad = M(r"0.100\ \text{mol L}^{-1} \times 250\ \text{mL} = 25.0\ \ ?", size=EQ_SMALL, color=BAD)
            bad2 = T("mL × mol L⁻¹ does not simplify to mol  →  1000 × too big", size=LABEL, color=BAD)
            badg = VGroup(bad, bad2).arrange(DOWN, buff=0.25).move_to([0, -1.7, 0])
            cross = TB("✗", size=HEAD, color=BAD).next_to(bad, RIGHT, buff=0.3)
            self.play(Write(bad), FadeIn(cross), run_time=1.2)
            b.until(0.75)
            self.play(FadeIn(bad2), run_time=0.6)


# =====================================================================================
class E01S04_Ladder(NarratedScene):
    def construct(self):
        h = header("The unit ladder")
        lad = ladder(["m³", "L", "mL"], ["1000", "1000"], color=VOL_C).move_to([-4.7, 0.3, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.5)
            self.play(FadeIn(lad[0]), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(lad[1]), run_time=1.0)

        rule = VGroup(T("Smaller unit  →  bigger number", size=LABEL + 2, color=GOOD),
                      T("Larger unit  →  smaller number", size=LABEL + 2, color=SYSTEM)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rule.move_to([2.4, 1.6, 0])
        vals = VGroup(T("0.0850 m³", size=LABEL + 2), T("85.0 L", size=LABEL + 2), T("85 000 mL", size=LABEL + 2))
        for v, rung in zip(vals, lad[0]):
            v.next_to(rung, RIGHT, buff=1.15)
        with self.beat("b02") as b:
            self.play(FadeIn(rule[0]), run_time=0.6)
            self.play(FadeIn(rule[1]), run_time=0.6)
            b.until(0.5)
            self.play(FadeIn(vals[0]), run_time=0.5)
            self.play(TransformFromCopy(vals[0], vals[1]), run_time=0.9)
            self.play(TransformFromCopy(vals[1], vals[2]), run_time=0.9)

        mass = hladder(["kg", "g", "mg"], ["1000", "1000"], color=MASS_C)
        energy = hladder(["MJ", "kJ", "J"], ["1000", "1000"], color=ENERGY_C)
        time_ = hladder(["h", "min", "s"], ["60", "60"], color=TEXT)
        for lad_, y in [(mass, 2.10), (energy, 0.95), (time_, -1.05)]:
            lad_.move_to([2.7, y, 0])
        e_ex = T("72 000 J  =  72.0 kJ", size=LABEL, color=ENERGY_C).next_to(energy, DOWN, buff=0.15)
        t_ex = T("0.150 h  =  9.00 min  =  540 s", size=LABEL).next_to(time_, DOWN, buff=0.15)
        with self.beat("b03") as b:
            self.play(FadeOut(rule), run_time=0.4)
            self.play(FadeIn(mass), run_time=0.9)
            b.until(0.4)
            self.play(FadeIn(energy), run_time=0.9)
            b.until(0.75)
            self.play(Write(e_ex), run_time=0.9)

        with self.beat("b04") as b:
            self.play(FadeIn(time_), run_time=0.9)
            b.until(0.55)
            self.play(Write(t_ex), run_time=1.2)

        with self.beat("b05") as b:
            q = T("After every conversion: should the number get bigger or smaller?", size=LABEL + 2, color=UNKNOWN)
            q.move_to([0, -2.38, 0])
            self.play(FadeIn(q, shift=0.1 * UP), run_time=0.8)


# =====================================================================================
class E01S05_Recipe(NarratedScene):
    def construct(self):
        h = header("A balanced equation is a recipe")
        eq = M(r"2\,\ce{H2}", "+", r"\ce{O2}", r"\ce{->}", r"2\,\ce{H2O}", size=EQ + 4).move_to([0, 2.35, 0])
        s = 1.5
        hA, hB, ox = mol_H2(s), mol_H2(s), mol_O2(s)
        hA.move_to([-5.2, 1.0, 0])
        hB.move_to([-5.2, -0.1, 0])
        ox.move_to([-3.2, 0.45, 0])
        arrow = Arrow([-1.9, 0.45, 0], [-0.3, 0.45, 0], buff=0, color=TEXT, stroke_width=4)
        w1, w2 = mol_H2O(s), mol_H2O(s)
        w1.move_to([1.3, 0.45, 0])
        w2.move_to([3.4, 0.45, 0])
        cnt_l = T("before: 4 H atoms, 2 O atoms", size=SMALL, color=MUTED).move_to([-4.2, -0.95, 0])
        cnt_r = T("after: 4 H atoms, 2 O atoms", size=SMALL, color=MUTED).move_to([2.35, -0.95, 0])
        schem = T("schematic", size=SMALL, color=MUTED).move_to([5.6, 1.5, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(eq), run_time=1.2)
            self.play(FadeIn(hA), FadeIn(hB), FadeIn(ox), FadeIn(schem), run_time=0.8)
            self.play(FadeIn(cnt_l), run_time=0.5)
            b.until(0.45)
            # rearrange the same atoms: bonds break, atoms move, new bonds form
            targets = [(hA.atoms[0], w1.atoms[1]), (hA.atoms[1], w1.atoms[2]), (ox.atoms[0], w1.atoms[0]),
                       (hB.atoms[0], w2.atoms[1]), (hB.atoms[1], w2.atoms[2]), (ox.atoms[1], w2.atoms[0])]
            self.play(FadeOut(hA.bonds), FadeOut(hB.bonds), FadeOut(ox.bonds), GrowArrow(arrow), run_time=0.6)
            self.play(*[a.animate.move_to(t.get_center()) for a, t in targets], run_time=1.8)
            self.play(FadeIn(w1.bonds), FadeIn(w2.bonds), FadeIn(cnt_r), run_time=0.6)
            self.picture = VGroup(*[a for a, _ in targets], w1.bonds, w2.bonds, arrow, cnt_l, cnt_r, schem)

        xs = [-4.2, 0.0, 4.2]
        heads = VGroup(*[TB(t, size=BODY, color=c).move_to([x, 1.25, 0])
                         for t, c, x in zip(["H₂", "O₂", "H₂O"], [TEXT, TEXT, TEXT], xs)])
        counts = [["2 molecules", "1 molecule", "2 molecules"], ["20", "10", "20"],
                  ["2 million", "1 million", "2 million"], ["2 mol", "1 mol", "2 mol"]]
        mults = ["the recipe once", "× 10", "× 1 million", "× 6.02 × 10²³  (one mole of recipes)"]

        def count_row(i):
            return VGroup(*[T(c, size=BODY, color=MOL_C).move_to([x, 0.45, 0]) for c, x in zip(counts[i], xs)])

        row = count_row(0)
        mult = T(mults[0], size=LABEL, color=MUTED).move_to([0, -0.35, 0])
        with self.beat("b02") as b:
            self.play(FadeOut(self.picture), run_time=0.5)
            self.play(FadeIn(heads), FadeIn(row), FadeIn(mult), run_time=0.8)
            for i in range(1, 4):
                b.until(0.15 + 0.22 * i)
                self.play(Transform(row, count_row(i)),
                          Transform(mult, T(mults[i], size=LABEL, color=MUTED).move_to([0, -0.35, 0])), run_time=0.8)

        with self.beat("b03") as b:
            self.play(FadeOut(mult), run_time=0.4)
            ex = VGroup(*[TB(c, size=BODY + 2, color=MOL_C).move_to([x, -0.4, 0])
                          for c, x in zip(["0.40 mol", "0.20 mol", "0.40 mol"], xs)])
            self.play(FadeIn(ex[0]), run_time=0.6)
            b.until(0.3)
            self.play(TransformFromCopy(ex[0], ex[1]), run_time=0.8)
            half = T("half as much (2 : 1)", size=SMALL, color=MUTED).next_to(ex[1], DOWN, buff=0.15)
            self.play(FadeIn(half), run_time=0.4)
            b.until(0.55)
            self.play(TransformFromCopy(ex[0], ex[2]), run_time=0.8)
            why = T("Valid because the ratio comes from counting particles, and moles are a count.",
                    size=LABEL, color=GOOD).move_to([0, -1.75, 0])
            b.until(0.75)
            self.play(FadeIn(why), run_time=0.6)
            self.why, self.half = why, half

        with self.beat("b04") as b:
            self.play(FadeOut(self.why), FadeOut(self.half), run_time=0.4)
            masses = VGroup(*[TB(c, size=BODY + 2, color=MASS_C).move_to([x, -1.15, 0])
                              for c, x in zip(["0.80 g", "6.4 g", "7.2 g"], xs)])
            mm = VGroup(*[T(c, size=SMALL, color=MUTED).next_to(m, DOWN, buff=0.1)
                          for c, m in zip(["(× 2.0 g mol⁻¹)", "(× 32.0 g mol⁻¹)", "(× 18.0 g mol⁻¹)"], masses)])
            for i in range(3):
                if i:
                    b.until(0.2 * i)
                self.play(FadeIn(masses[i]), FadeIn(mm[i]), run_time=0.6)
            c1 = T("0.80 g + 6.4 g = 7.2 g:  mass is conserved ✓", size=LABEL, color=GOOD)
            c2 = T("but 0.80 : 6.4 : 7.2 is not 2 : 1 : 2.  Coefficients are mole ratios, not mass ratios ✗",
                   size=LABEL, color=BAD)
            VGroup(c1, c2).arrange(DOWN, buff=0.18).move_to([0, -2.2, 0])
            b.until(0.55)
            self.play(FadeIn(c1), run_time=0.6)
            b.until(0.75)
            self.play(FadeIn(c2), run_time=0.6)


# =====================================================================================
class E01S06_Rounding(NarratedScene):
    def construct(self):
        h = header("Round at the end, not along the way")
        top = M(r"V(\ce{O2}) = 17.765\ \text{L}", size=EQ).move_to([0, 2.35, 0])
        lt = TB("Rounded too early", size=LABEL + 2, color=BAD).move_to([-3.6, 1.4, 0])
        rt_ = TB("Full value carried", size=LABEL + 2, color=GOOD).move_to([3.6, 1.4, 0])
        L = VGroup(M(r"17.765 \rightarrow 17.8\ \text{L}", size=EQ_SMALL),
                   M(r"n = \frac{17.8\ \text{L}}{24.8\ \text{L mol}^{-1}}", size=EQ_SMALL),
                   M(r"= 0.71774\ldots\ \text{mol}", size=EQ_SMALL),
                   M(r"\approx 0.718\ \text{mol}", size=EQ_SMALL, color=BAD)).arrange(DOWN, buff=0.18)
        L.next_to(lt, DOWN, buff=0.3)
        R = VGroup(M(r"n = \frac{17.765\ \text{L}}{24.8\ \text{L mol}^{-1}}", size=EQ_SMALL),
                   M(r"= 0.716330\ldots\ \text{mol}", size=EQ_SMALL),
                   M(r"\approx 0.716\ \text{mol}", size=EQ_SMALL, color=GOOD)).arrange(DOWN, buff=0.18)
        R.next_to(rt_, DOWN, buff=0.3)
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(top), run_time=1.0)
            b.until(0.3)
            self.play(FadeIn(lt), FadeIn(L[0]), run_time=0.8)
            b.until(0.6)
            self.play(Write(L[1]), run_time=0.9)
            self.play(Write(L[2]), run_time=0.7)
            self.play(Write(L[3]), run_time=0.6)
        with self.beat("b02") as b:
            self.play(FadeIn(rt_), Write(R[0]), run_time=1.0)
            self.play(Write(R[1]), run_time=0.7)
            self.play(Write(R[2]), run_time=0.6)
            b.until(0.55)
            d1 = SurroundingRectangle(L[3], color=BAD, buff=0.1)
            d2 = SurroundingRectangle(R[2], color=GOOD, buff=0.1)
            note = VGroup(T("different third", size=LABEL, color=UNKNOWN), T("significant figure", size=LABEL, color=UNKNOWN)).arrange(DOWN, buff=0.1).move_to([0, -0.2, 0])
            self.play(Create(d1), Create(d2), FadeIn(note), run_time=0.8)
        with self.beat("b03") as b:
            keep_l, keep_r = VGroup(L[3], d1), VGroup(R[2], d2)
            self.play(FadeOut(note), FadeOut(L[:3]), FadeOut(R[:2]), run_time=0.5)
            self.play(keep_l.animate.next_to(lt, DOWN, buff=0.3), keep_r.animate.next_to(rt_, DOWN, buff=0.3),
                      run_time=0.6)
            rule = bullets(["Keep the unrounded value in your calculator",
                            "Write intermediate results with a few extra digits",
                            "Round only the final answer, to the significant figures the data supports (here 3)"],
                           size=LABEL, width=12.8)
            box = panel(rule, color=GOOD)
            g = VGroup(box, rule).move_to([0, -1.1, 0])
            self.play(FadeIn(box), run_time=0.4)
            for r in rule:
                self.play(FadeIn(r), run_time=b.rt(0.12, 0.4, 1.0))


# =====================================================================================
class E01S07_Q01(NarratedScene):
    def construct(self):
        h = header("Practice Q01")
        card = question_card("Q01").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(card, shift=0.1 * UP), run_time=1.0)

        with self.beat("b02") as b:
            self.play(FadeOut(card), run_time=0.5)
            ga = given_asked(["m(ethanol) = 0.345 g", "M(ethanol) = 46.0 g mol⁻¹", "V(gas) = 186 mL at SLC"],
                             ["n(ethanol) in mol", "n(gas) in mol", "Do equal amounts mean equal masses?"])
            ga.move_to([0, 0.4, 0])
            self.play(FadeIn(ga[0]), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(ga[1]), run_time=0.8)
            self.ga = ga

        req = requested("amount in mol")
        with self.beat("b03") as b:
            self.play(FadeOut(self.ga), FadeIn(req), run_time=0.6)
            pred = VGroup(TB("Predict first", size=LABEL + 2, color=UNKNOWN),
                          T("1 mol of ethanol = 46.0 g;  we have only 0.345 g", size=LABEL),
                          T("so expect much less than 1 mol: roughly 0.01 mol", size=LABEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            pb = panel(pred, color=UNKNOWN, buff=0.20)
            pg = VGroup(pb, pred).move_to([0, 1.65, 0])
            self.play(FadeIn(pb), FadeIn(pred[0]), run_time=0.6)
            self.play(FadeIn(pred[1]), run_time=0.7)
            b.until(0.6)
            self.play(FadeIn(pred[2]), run_time=0.7)
            self.pg = pg

        with self.beat("b04") as b:
            la = TB("a.", size=LABEL + 2, color=SYSTEM).move_to([-6.2, 0.30, 0])
            w = VGroup(M(r"n(\text{ethanol})", "=", r"\frac{m}{M}", size=EQ_SMALL),
                       M(r"\phantom{n(\text{ethanol})}", "=", r"\frac{0.345\ \text{g}}{46.0\ \text{g mol}^{-1}}", size=EQ_SMALL),
                       M(r"\phantom{n(\text{ethanol})}", "=", r"\quad 0.00750\ \text{mol}", size=EQ_SMALL))
            for i in (1, 2):
                w[i].next_to(w[i - 1], DOWN, buff=0.25)
                w[i].shift((w[0][1].get_center()[0] - w[i][1].get_center()[0]) * RIGHT)
            w.next_to(la, RIGHT, buff=0.3, aligned_edge=UP).shift(0.2 * UP)
            self.play(FadeIn(la), Write(w[0]), run_time=0.9)
            b.until(0.3)
            self.play(Write(w[1]), run_time=1.0)
            b.until(0.55)
            self.play(Write(w[2]), run_time=0.8)
            rb = result_box(w[2][2])
            chk = T("≈ 0.01 ✓ fits", size=SMALL, color=GOOD).next_to(rb, RIGHT, buff=0.2)
            self.play(Create(rb), FadeIn(chk), run_time=0.6)
            self.part_a = VGroup(la, w, rb, chk)

        with self.beat("b05") as b:
            lb = TB("b.", size=LABEL + 2, color=SYSTEM).move_to([0.6, 0.30, 0])
            v = VGroup(M(r"V = 186\ \text{mL} \div 1000 = 0.186\ \text{L}", size=EQ_SMALL - 2, color=VOL_C),
                       M(r"n = \frac{V}{V_m} = \frac{0.186\ \text{L}}{24.8\ \text{L mol}^{-1}}", size=EQ_SMALL - 2),
                       M(r"= 0.00750\ \text{mol}", size=EQ_SMALL - 2)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            v.next_to(lb, RIGHT, buff=0.3, aligned_edge=UP).shift(0.2 * UP)
            self.play(FadeIn(lb), Write(v[0]), run_time=1.0)
            b.until(0.45)
            self.play(Write(v[1]), run_time=1.0)
            b.until(0.8)
            self.play(Write(v[2]), run_time=0.6)
            rb2 = result_box(v[2])
            self.play(Create(rb2), run_time=0.4)
            self.part_b = VGroup(lb, v, rb2)

        with self.beat("b06") as b:
            self.play(FadeOut(self.part_a), FadeOut(self.part_b), FadeOut(self.pg), run_time=0.5)
            lc = TB("c.", size=LABEL + 2, color=SYSTEM)
            good = right_panel("Full-credit style", [
                "No. Equal amounts mean equal numbers of particles, but mass = amount × molar mass.",
                "Molar masses can differ, and the gas's identity and molar mass are not given, so its mass cannot be found."],
                width=11.0)
            VGroup(lc, good).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to([0, 1.2, 0])
            self.play(FadeIn(lc), FadeIn(good[0]), FadeIn(good[1][0]), run_time=0.6)
            self.play(FadeIn(good[1][1][0]), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(good[1][1][1]), run_time=0.8)
            self.good, self.lc = good, lc

        with self.beat("b06b") as b:
            weak = wrong_panel("Misses the causal link", ['"No, because they are different substances."'],
                               note="Why does a different substance matter? Because m = n × M, and M can differ.",
                               width=11.0)
            weak.next_to(self.good, DOWN, buff=0.35).align_to(self.good, LEFT)
            self.play(FadeIn(weak[0]), FadeIn(weak[1]), FadeIn(weak[2][:2]), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(weak[2][2]), run_time=0.8)

        with self.beat("b07") as b:
            self.clear(h, req)
            tally = mark_tally([(1, "a. amount of ethanol, 0.00750 mol"),
                                (2, "b. 186 mL → 0.186 L, then ÷ 24.8 L mol⁻¹ = 0.00750 mol"),
                                (1, "c. equal amounts ≠ equal masses: molar masses differ; gas unknown")],
                               width=9.5).move_to([0, 0.1, 0])
            self.play(FadeIn(tally[0]), FadeIn(tally[1][0]), run_time=0.6)
            for i, row in enumerate(tally[1][1]):
                b.until(0.2 + 0.25 * i)
                self.play(FadeIn(row), run_time=0.5)
            self.play(FadeIn(tally[1][2]), run_time=0.4)
            self.tally = tally

        with self.beat("b08") as b:
            self.play(FadeOut(self.tally), run_time=0.4)
            wp = wrong_panel("Tempting but incorrect", [M(r"n = \frac{186}{24.8} = 7.50\ \text{mol}", size=EQ_SMALL, color=TEXT)],
                             note="First wrong step: 186 mL substituted as if it were litres.", width=6.4)
            wp.move_to([-3.1, 0.4, 0])
            sanity = VGroup(TB("Sanity check", size=LABEL + 2, color=UNKNOWN),
                            M(r"7.50\ \text{mol} \times 24.8\ \text{L mol}^{-1} = 186\ \text{L}", size=EQ_SMALL - 6),
                            T("186 litres, not 186 millilitres", size=LABEL, color=BAD)).arrange(DOWN, buff=0.25)
            sb = panel(sanity, color=UNKNOWN)
            sg = VGroup(sb, sanity).move_to([3.6, 0.4, 0])
            self.play(FadeIn(wp), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(sg), run_time=0.8)

        with self.beat("b09") as b:
            self.clear(h, req)
            p = VGroup(TB("Changed condition", size=BODY, color=UNKNOWN),
                       T("The same gas sample is measured at 50 °C instead.", size=LABEL + 2),
                       T("Can you still divide by 24.8 L mol⁻¹?", size=LABEL + 2)).arrange(DOWN, buff=0.3)
            p.move_to([0, 0.8, 0])
            self.play(FadeIn(p), run_time=0.8)
            self.p = p

        with self.beat("b10") as b:
            ans = VGroup(TB("No.", size=BODY, color=BAD),
                         T("24.8 L mol⁻¹ applies only at 25 °C and 100 kPa.", size=LABEL + 2),
                         T("At 50 °C a mole of gas occupies more volume: use the molar volume for those conditions.",
                           size=LABEL)).arrange(DOWN, buff=0.22)
            ans.next_to(self.p, DOWN, buff=0.6)
            self.play(FadeIn(ans[0]), run_time=0.4)
            self.play(FadeIn(ans[1]), run_time=0.6)
            b.until(0.5)
            self.play(FadeIn(ans[2]), run_time=0.6)


# =====================================================================================
class E01S08_Q02(NarratedScene):
    def construct(self):
        h = header("Practice Q02")
        card = question_card("Q02").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(card, shift=0.1 * UP), run_time=1.0)

        with self.beat("b02") as b:
            self.play(FadeOut(card), run_time=0.5)
            la = TB("a.", size=LABEL + 2, color=SYSTEM).move_to([-6.2, 2.2, 0])
            lines = VGroup(
                M(r"0.0850\ \text{m}^3 \times 1000\ \text{L m}^{-3} = 85.0\ \text{L}", size=EQ_SMALL, color=VOL_C),
                M(r"0.150\ \text{h} \times 3600\ \text{s h}^{-1} = 540\ \text{s}", size=EQ_SMALL),
                M(r"7.20\times10^{4}\ \text{J} \div 1000 = 72.0\ \text{kJ}", size=EQ_SMALL, color=ENERGY_C),
            ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            lines.next_to(la, RIGHT, buff=0.3, aligned_edge=UP).shift(0.15 * UP)
            dirs = VGroup(T("smaller unit, bigger number ✓", size=SMALL, color=GOOD),
                          T("smaller unit, bigger number ✓", size=SMALL, color=GOOD),
                          T("larger unit, smaller number ✓", size=SMALL, color=GOOD))
            for d, l in zip(dirs, lines):
                d.next_to(l, RIGHT, buff=0.4)
            self.play(FadeIn(la), Write(lines[0]), run_time=1.2)
            b.until(0.33)
            self.play(Write(lines[1]), run_time=1.2)
            b.until(0.62)
            self.play(Write(lines[2]), run_time=1.2)
            b.until(0.85)
            self.play(LaggedStart(*[FadeIn(d) for d in dirs], lag_ratio=0.3), run_time=1.0)
            self.part_a = VGroup(la, lines, dirs)

        req = requested("n(O₂) in mol")
        with self.beat("b03") as b:
            self.play(self.part_a.animate.shift(0.2 * UP).set_opacity(0.45), FadeIn(req), run_time=0.6)
            pred = VGroup(TB("Predict first", size=LABEL + 2, color=UNKNOWN),
                          T("all gas: 85 L ÷ about 25 L mol⁻¹ ≈ 3.4 mol", size=LABEL),
                          T("oxygen is about one fifth of air  →  expect ≈ 0.7 mol", size=LABEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            pb = panel(pred, color=UNKNOWN)
            pg = VGroup(pb, pred).move_to([0, -0.85, 0])
            self.play(FadeIn(pb), FadeIn(pred[0]), FadeIn(pred[1]), run_time=0.8)
            b.until(0.55)
            self.play(FadeIn(pred[2]), run_time=0.6)
            self.pg = pg

        with self.beat("b04") as b:
            self.play(FadeOut(self.part_a), self.pg.animate.move_to([0, 1.80, 0]), run_time=0.7)
            lb = TB("b.", size=LABEL + 2, color=SYSTEM).move_to([-6.2, 0.45, 0])
            bar_w = 9.0
            o2w = bar_w * 0.209
            o2 = Rectangle(width=o2w, height=0.7, fill_color=SYSTEM, fill_opacity=0.85, stroke_color=TEXT, stroke_width=2)
            rest = Rectangle(width=bar_w - o2w, height=0.7, fill_color=FAINT, fill_opacity=0.6, stroke_color=TEXT, stroke_width=2)
            bar = VGroup(o2, rest).arrange(RIGHT, buff=0).move_to([0.2, 0.45, 0])
            o2l = T("O₂ 20.9%", size=SMALL, color=BG).move_to(o2)
            restl = T("other gases (inert here) 79.1%", size=SMALL).move_to(rest)
            total = T("85.0 L of air", size=LABEL).next_to(bar, UP, buff=0.1)
            self.play(FadeIn(lb), FadeIn(bar), FadeIn(total), FadeIn(o2l), FadeIn(restl), run_time=0.9)
            calc = M(r"V(\ce{O2}) = 0.209 \times 85.0\ \text{L} = 17.765\ \text{L}", size=EQ_SMALL).move_to([0.2, -0.6, 0])
            b.until(0.3)
            self.play(Write(calc), run_time=1.2)
            note = T("Same temperature and pressure for all the gases, so volume fraction = mole fraction.",
                     size=LABEL, color=MUTED).move_to([0.2, -1.45, 0])
            b.until(0.7)
            self.play(FadeIn(note), run_time=0.7)
            self.bar_grp = VGroup(bar, o2l, restl, total, note)
            self.calc, self.lb = calc, lb

        with self.beat("b05") as b:
            self.play(FadeOut(self.bar_grp), self.calc.animate.move_to([0.2, 0.75, 0]), run_time=0.6)
            n1 = M(r"n(\ce{O2}) = \frac{V}{V_m} = \frac{17.765\ \text{L}}{24.8\ \text{L mol}^{-1}}", size=EQ_SMALL).next_to(self.calc, DOWN, buff=0.35)
            n2 = M(r"= 0.71633\ldots\ \text{mol} \approx 0.716\ \text{mol}", size=EQ_SMALL).next_to(n1, DOWN, buff=0.3)
            self.play(Write(n1), run_time=1.2)
            b.until(0.55)
            self.play(Write(n2), run_time=1.0)
            rb = result_box(n2)
            chk = T("≈ 0.7 ✓ matches prediction", size=SMALL, color=GOOD).next_to(rb, DOWN, buff=0.15)
            self.play(Create(rb), FadeIn(chk), run_time=0.6)

        with self.beat("b06") as b:
            self.clear(h, req)
            tally = mark_tally([(3, "a. three conversions: 85.0 L, 540 s, 72.0 kJ"),
                                (1, "b. oxygen fraction: 17.765 L of O₂"),
                                (1, "b. n(O₂) = 0.716 mol")], width=6.0).move_to([-3.4, 0.6, 0])
            self.play(FadeIn(tally), run_time=0.8)
            w1 = wrong_panel("Whole air used as oxygen", [M(r"\frac{85.0}{24.8} = 3.43\ \text{mol}", size=EQ_SMALL - 6, color=TEXT)],
                             width=4.6)
            w2 = wrong_panel("m³ treated as mL", [T("volume a million times too small", size=LABEL)], width=4.6)
            ws = VGroup(w1, w2).arrange(DOWN, buff=0.3).move_to([3.5, 0.4, 0])
            b.until(0.3)
            self.play(FadeIn(w1), run_time=0.7)
            b.until(0.62)
            self.play(FadeIn(w2), run_time=0.7)
            b.until(0.85)
            fin = T("In both cases, the prediction would have warned you.", size=LABEL, color=UNKNOWN).move_to([0, -2.35, 0])
            self.play(FadeIn(fin), run_time=0.6)


# =====================================================================================
class E01S09_Recap(NarratedScene):
    def construct(self):
        h = header("Choosing the relationship")
        rows = [["You have…", "Use", "Unit condition"],
                ["a mass", "n = m ÷ M", "grams with g mol⁻¹"],
                ["a solution", "n = c × V", "V in litres"],
                ["a gas at SLC", "n = V ÷ 24.8", "V in litres; 25 °C, 100 kPa"],
                ["a balanced equation", "mole ratio", "coefficients relate mol, not g"]]
        tb = table(rows, [4.0, 3.4, 5.8], size=BODY - 2, row_h=0.75).move_to([0, 0.1, 0])
        grid, cells = tb[0], tb[1]
        with self.beat("b01") as b:
            self.play(FadeIn(h), Create(grid), run_time=0.8)
            per = len(rows[0])
            self.play(FadeIn(VGroup(*cells[:per])), run_time=0.5)
            for i in range(1, len(rows)):
                b.until(0.12 + 0.2 * i)
                self.play(FadeIn(VGroup(*cells[i * per:(i + 1) * per]), shift=0.1 * RIGHT), run_time=0.6)

        with self.beat("b02") as b:
            self.play(FadeOut(tb), run_time=0.5)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN),
                       T("What are the units of molar volume?", size=LABEL + 4),
                       T("At what temperature and pressure does 24.8 apply?", size=LABEL + 4)).arrange(DOWN, buff=0.35)
            q.move_to([0, 0.9, 0])
            self.play(FadeIn(q), run_time=0.8)
            self.q = q

        with self.beat("b03") as b:
            a = VGroup(M(r"V_m:\ \text{L mol}^{-1}", size=EQ, color=VOL_C),
                       T("24.8 L mol⁻¹ at 25 °C and 100 kPa (SLC)", size=LABEL + 2, color=GOOD)).arrange(DOWN, buff=0.3)
            a.next_to(self.q, DOWN, buff=0.5)
            self.play(FadeIn(a), run_time=0.8)
            b.until(0.55)
            nxt = T("Next: Episode 02 · Where reaction energy comes from", size=LABEL, color=MUTED).move_to([0, -2.35, 0])
            self.play(FadeIn(nxt), run_time=0.6)


EPISODE_SCENES = ["E01S01_Welcome", "E01S02_Labels", "E01S03_ThreeRoutes", "E01S04_Ladder", "E01S05_Recipe",
                  "E01S06_Rounding", "E01S07_Q01", "E01S08_Q02", "E01S09_Recap"]
