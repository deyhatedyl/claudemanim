"""
Episode 13 - Exam workshop A: fuels and combustion (Q25, Q26).
Narration: scripts/ep13.md (beat names must match).
Q25 and Q26 are original practice questions written for this series (labelled on screen; not VCAA questions).
Every value shown is recomputed in checks/verify_anchors.py (q25, q26, ep13_workshop_values).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (bullets, mark_tally, question_card, result_box, right_panel, strike, table,  # noqa: E402
                               title_card, wrap, wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.workshop import (BIO, CO2E, WK, X0, XM, attempt_card, blank, boxes_for, mbox, node, number,  # noqa: E402
                             part_tag, requested, tally_text, tick, work)
from shared.style import (BAD, BG, BODY, ENERGY_C, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, LOSS, MASS_C,  # noqa: E402
                          MOL_C, MUTED, PANEL, SMALL, SURR, SYSTEM, TEXT, UNKNOWN, USEFUL, VOL_C, M, T, TB, chip,
                          header, panel)


# =====================================================================================
class E13S01_Retrieval(NarratedScene):
    def construct(self):
        tc = title_card(13, "Exam workshop A: fuels and combustion")
        note = T("Q25 and Q26 are original practice questions written for this series, not VCAA questions.",
                 size=SMALL, color=MUTED).next_to(tc, DOWN, buff=0.45)
        with self.beat("b01") as b:
            self.play(FadeIn(tc, shift=0.2 * UP), run_time=1.5)
            b.until(0.6)
            self.play(FadeIn(note), run_time=0.6)
        with self.beat("b02") as b:
            self.play(FadeOut(tc), FadeOut(note), run_time=0.5)
            h = header("Retrieval check")
            q1 = wrapped("1.  A label says 1650 kJ per 100 g. How much energy is in a 40.0 g bar?", size=LABEL + 4, width=12.2)
            q2 = wrapped("2.  A platinum catalyst lets methane react at a lower temperature. Does it change the energy "
                         "released per mole of methane?", size=LABEL + 4, width=12.2)
            qs = VGroup(q1, q2).arrange(DOWN, buff=1.05, aligned_edge=LEFT).move_to([0, 0.75, 0])
            self.play(FadeIn(h), FadeIn(q1), run_time=0.7)
            b.until(0.45)
            self.play(FadeIn(q2), run_time=0.6)
            self.qs = qs
        with self.beat("b03") as b:
            a1 = M(r"1650 \times \frac{40.0}{100} = 660\ \text{kJ}", size=EQ_SMALL - 4, color=GOOD)
            a1.next_to(self.qs[0], DOWN, buff=0.2).align_to(self.qs[0], LEFT).shift(0.6 * RIGHT)
            a2 = wrapped("No: lower activation energy, but the same reactants, products and states, so ΔH is unchanged",
                         size=LABEL + 2, width=11.0, color=GOOD)
            a2.next_to(self.qs[1], DOWN, buff=0.2).align_to(self.qs[1], LEFT).shift(0.6 * RIGHT)
            self.play(Write(a1), run_time=0.9)
            b.until(0.5)
            self.play(FadeIn(a2), run_time=0.7)


# =====================================================================================
class E13S02_Routine(NarratedScene):
    def construct(self):
        h = header("The routine for every question")
        steps = ["Read", "Annotate", "Choose method", "Work with units", "Check plausibility"]
        cols = [SURR, UNKNOWN, SYSTEM, MOL_C, GOOD]
        strip = VGroup()
        for i, (s, c) in enumerate(zip(steps, cols)):
            n = TB(str(i + 1), size=LABEL + 2, color=c)
            t = VGroup(*[T(l, size=LABEL) for l in wrap(s, LABEL, 1.9)]).arrange(DOWN, buff=0.08)
            g = VGroup(n, t).arrange(DOWN, buff=0.12)
            r = RoundedRectangle(width=2.3, height=1.35, corner_radius=0.14, stroke_color=FAINT, stroke_width=2.5,
                                 fill_color=PANEL, fill_opacity=1)
            g.move_to(r)
            strip.add(VGroup(r, g))
        strip.arrange(RIGHT, buff=0.22).move_to([0, 1.55, 0])
        arrows = VGroup(*[Arrow(strip[i].get_right(), strip[i + 1].get_left(), buff=0.02, stroke_width=3,
                                max_tip_length_to_length_ratio=0.5, color=FAINT) for i in range(4)])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(strip, lag_ratio=0.1), FadeIn(arrows), run_time=1.0)
            for i, f in enumerate((0.05, 0.2, 0.42, 0.62, 0.84)):
                b.until(f)
                self.play(strip[i][0].animate.set_stroke(cols[i], width=3.5), run_time=0.4)
        with self.beat("b02") as b:
            ex = T("hypothetical working (propane, SLC)", size=SMALL, color=MUTED).move_to([0, 0.35, 0]).align_to([X0, 0, 0], LEFT)
            l1 = work(r"n(\ce{C3H8}) = 2.48 \div 24.8 = 0.100\ \text{mol}", -0.3)
            l2 = work(r"n(\ce{CO2}) = 3 \times 0.100 = 0.300\ \text{mol}", -1.05)
            l3 = work(r"m(\ce{CO2}) = 0.300 \times 44.0 = 1.32\ \text{g}", -1.8)
            m1, m2, m3 = boxes_for(l1), boxes_for(l2), boxes_for(l3)
            slip = T("slip: should be 13.2 g", size=SMALL + 1, color=BAD).next_to(l3, RIGHT, buff=0.4)
            note = T("marks are indicative: each visible correct step can earn a mark", size=SMALL + 1, color=GOOD)
            note.move_to([0, -2.45, 0])
            self.play(FadeIn(ex), Write(l1), FadeIn(m1), run_time=0.9)
            self.play(tick(m1), run_time=0.4)
            b.until(0.3)
            self.play(Write(l2), FadeIn(m2), run_time=0.8)
            self.play(tick(m2), run_time=0.4)
            b.until(0.5)
            self.play(Write(l3), FadeIn(m3), run_time=0.8)
            self.play(l3[0][-5:].animate.set_color(BAD), FadeIn(slip), run_time=0.6)
            b.until(0.75)
            self.play(FadeIn(note), run_time=0.6)


# =====================================================================================
class E13S03_Q25Attempt(NarratedScene):
    PAUSE_LABELS = {"b02": "Pause the video now and attempt every part"}
    TIMER_CORNER = DR

    def construct(self):
        qc = attempt_card("Q25")
        with self.beat("b01"):
            self.play(FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        with self.beat("b02") as b:
            self.play(Indicate(qc[1][0][0], color=UNKNOWN), run_time=0.8)


# =====================================================================================
class E13S04_Annotate(NarratedScene):
    def construct(self):
        h = header("Q25: read and annotate")
        rows = [
            ("6.20 L fuel mixture at SLC", "n = V ÷ 24.8 L mol⁻¹", VOL_C, False),
            ("90.0% CH₄, 10.0% CO₂ by volume", "only CH₄ burns; vol % = mol %", UNKNOWN, True),
            ("60.0 L air, 21.0% O₂", "air ≠ oxygen: use 21.0% of 60.0 L", UNKNOWN, True),
            ("ΔH = −890 kJ mol⁻¹ (H₂O(l))", "states fixed: H₂O(l) in the equation", ENERGY_C, False),
            ("800.0 g water, 17.0 → 57.0 °C", "ΔT = 40.0 °C; c = 4.18 J g⁻¹ °C⁻¹", ENERGY_C, False),
            ("fuel CO₂ passes through unchanged", "CO₂ out = new + inlet", UNKNOWN, True),
        ]
        built = VGroup()
        x_arrow = max(T(d, size=LABEL + 1).width for d, *_ in rows) - 6.2 + 0.3
        for i, (d, a, c, trap) in enumerate(rows):
            y = 2.2 - i * 0.82
            dt = T(d, size=LABEL + 1).move_to([0, y, 0]).align_to([-6.2, 0, 0], LEFT)
            ar = Arrow([x_arrow, y, 0], [x_arrow + 0.7, y, 0], buff=0, stroke_width=3, color=FAINT,
                       max_tip_length_to_length_ratio=0.35)
            at = T(a, size=LABEL + 1, color=c).move_to([0, y, 0]).align_to([x_arrow + 0.9, 0, 0], LEFT)
            g = VGroup(dt, ar, at)
            if trap:
                g.add(chip("trap", LOSS, size=SMALL - 2).next_to(at, RIGHT, buff=0.25))
            built.add(g)
        given = T("given", size=SMALL, color=MUTED).next_to(built[0][0], UP, buff=0.22).align_to(built[0][0], LEFT)
        note = T("annotation", size=SMALL, color=MUTED).next_to(built[0][2], UP, buff=0.22).align_to(built[0][2], LEFT)

        def show(i, run=0.8):
            r = built[i]
            anims = [FadeIn(r[0]), GrowArrow(r[1]), FadeIn(r[2], shift=0.1 * RIGHT)]
            if len(r) > 3:
                anims.append(FadeIn(r[3], scale=1.2))
            self.play(*anims, run_time=run)

        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(given), FadeIn(note), run_time=0.6)
            show(0)
            b.until(0.4)
            show(1)
        with self.beat("b02") as b:
            show(2)
            u = Underline(built[2][0], color=UNKNOWN, buff=0.06)
            b.until(0.55)
            self.play(Create(u), run_time=0.5)
        with self.beat("b03") as b:
            show(3)
            b.until(0.5)
            show(4)
        with self.beat("b04") as b:
            show(5)
            traps = VGroup(*[SurroundingRectangle(built[i], color=LOSS, buff=0.08, stroke_width=2) for i in (1, 2, 5)])
            b.until(0.6)
            self.play(LaggedStart(*[Create(t) for t in traps], lag_ratio=0.25), run_time=1.0)


# =====================================================================================
class E13S05_Plan(NarratedScene):
    def construct(self):
        h = header("Q25: plan the methods")
        a = node("a", ["amounts: n = V ÷ 24.8", "CH₄: × 0.900", "O₂: 21.0% of the air"], SYSTEM)
        bb = node("b", ["equation with", "states and ΔH"], MUTED)
        c = node("c", ["mole ratio 1 : 2", "→ excess O₂ → mass"], MOL_C)
        d = node("d", ["E = n × 890", "q = m c ΔT"], ENERGY_C)
        e = node("e", ["efficiency =", "q ÷ E × 100%"], USEFUL)
        f = node("f", ["CO₂ = new + inlet", "V = n × 24.8"], VOL_C)
        g = node("g", ["renewable:", "defined by source"], BIO)
        a.move_to([-4.65, 0.55, 0])
        c.move_to([-0.3, 1.85, 0])
        d.move_to([-0.3, 0.55, 0])
        f.move_to([-0.3, -0.75, 0])
        e.move_to([4.55, 0.55, 0])
        bb.move_to([-4.65, -2.1, 0])
        g.move_to([-0.3, -2.1, 0])
        alone = T("b and g stand alone", size=SMALL + 1, color=MUTED).move_to([4.55, -2.1, 0])
        order = [a, bb, c, d, e, f, g]
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.5)
            for n_, fr in zip(order, (0.02, 0.17, 0.3, 0.47, 0.62, 0.74, 0.88)):
                b.until(fr)
                self.play(FadeIn(n_, shift=0.1 * UP), run_time=0.5)
        with self.beat("b02") as b:
            arr = VGroup(*[Arrow(a.get_right(), t.get_left(), buff=0.08, stroke_width=4, color=SYSTEM,
                                 max_tip_length_to_length_ratio=0.12) for t in (c, d, f)],
                         Arrow(d.get_right(), e.get_left(), buff=0.08, stroke_width=4, color=ENERGY_C,
                               max_tip_length_to_length_ratio=0.12))
            self.play(LaggedStart(*[GrowArrow(x) for x in arr[:3]], lag_ratio=0.25), run_time=1.2)
            b.until(0.3)
            self.play(GrowArrow(arr[3]), FadeIn(alone), run_time=0.8)
            b.until(0.6)
            hl = SurroundingRectangle(a, color=UNKNOWN, buff=0.1, stroke_width=3)
            chk = T("check part a carefully", size=SMALL + 1, color=UNKNOWN).next_to(hl, UP, buff=0.12)
            self.play(Create(hl), FadeIn(chk), run_time=0.7)


# =====================================================================================
class E13S06_PartsAC(NarratedScene):
    def construct(self):
        h = header("Q25 parts a–c")
        tl = tally_text("Q25", 0, 15)
        ys = [2.05, 1.35, 0.65, -0.35, -1.3, -2.05]
        l1 = work(r"n_{\text{mix}} = 6.20 \div 24.8 = 0.250\ \text{mol}", ys[0], MOL_C)
        l2 = work(r"n(\ce{CH4}) = 0.900 \times 0.250 = 0.225\ \text{mol}", ys[1], MOL_C)
        l3 = work(r"n(\ce{O2}) = 0.210 \times 60.0 \div 24.8 = 12.6 \div 24.8 = 0.508\ \text{mol}", ys[2], MOL_C)
        l4 = work(r"\ce{CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)} \qquad \Delta H = -890\ \text{kJ}", ys[3])
        l5 = work(r"n(\ce{O2})_{\text{required}} = 2 \times 0.225 = 0.450\ \text{mol} < 0.508:\ \ce{O2}\ \text{in excess}", ys[4], MOL_C)
        l6 = work(r"(0.5081 - 0.450) = 0.0581\ \text{mol};\quad 0.0581 \times 32.0 = 1.86\ \text{g}", ys[5], MASS_C)
        ta, tb_, tc = part_tag("a", l1), part_tag("b", l4), part_tag("c", l5)
        bx = [boxes_for(l) for l in (l1, l2, l3)] + [boxes_for(l4, 2)] + [boxes_for(l5), boxes_for(l6)]

        def step(line, box, tag=None, run=0.9):
            anims = [Write(line), FadeIn(box)]
            if tag is not None:
                anims.append(FadeIn(tag))
            self.play(*anims, run_time=run)

        def score(box, got):
            new = tally_text("Q25", got, 15)
            self.play(*[tick(x) for x in box], Transform(self.tl, new), run_time=0.4)

        with self.beat("b01") as b:
            self.tl = tl
            self.play(FadeIn(h), FadeIn(tl), run_time=0.5)
            step(l1, bx[0], ta)
            score(bx[0], 1)
            b.until(0.3)
            step(l2, bx[1])
            score(bx[1], 2)
            b.until(0.55)
            step(l3, bx[2], run=1.2)
            score(bx[2], 3)
        with self.beat("b02") as b:
            step(l4, bx[3], tb_, run=1.3)
            b.until(0.55)
            score(bx[3], 5)
        with self.beat("b03") as b:
            step(l5, bx[4], tc, run=1.2)
            score(bx[4], 6)
            b.until(0.62)
            step(l6, bx[5], run=1.1)
            rb = result_box(l6[0][-5:], color=MASS_C)
            self.play(Create(rb), run_time=0.4)
            score(bx[5], 7)


# =====================================================================================
class E13S07_WrongMethane(NarratedScene):
    def construct(self):
        h = header("Wrong solution: all the gas treated as methane")
        sz = EQ_SMALL - 10
        wl = [M(r"\text{a: } n(\ce{CH4}) = 0.250\ \text{mol}", size=sz),
              M(r"\text{c: } \ce{O2}\ \text{needed} = 0.500\ \text{mol};\ \text{excess} = 0.258\ \text{g}", size=sz),
              M(r"\text{d: } E = 0.250 \times 890 = 222.5\ \text{kJ}", size=sz),
              M(r"\text{e: } 133.76 \div 222.5 \times 100\% = 60.1\%", size=sz)]
        rl = [M(r"0.225\ \text{mol}", size=sz, color=GOOD), M(r"0.450\ \text{mol};\ 1.86\ \text{g}", size=sz, color=GOOD),
              M(r"200.25\ \text{kJ}", size=sz, color=GOOD), M(r"66.8\%", size=sz, color=GOOD)]
        wp = wrong_panel("Student's working", wl, width=5.6).move_to([-3.05, 0.65, 0])
        for w_, r_ in zip(wl, rl):            # each correct value level with its wrong line
            r_.move_to([0, w_.get_y(), 0]).align_to([2.4, 0, 0], LEFT)
        rh = VGroup(TB("✓", size=LABEL + 6, color=GOOD), TB("Correct", size=LABEL + 2, color=GOOD)).arrange(RIGHT, buff=0.2)
        rh.move_to([0, wp[2][0].get_y(), 0]).align_to([2.4, 0, 0], LEFT)
        rcol = VGroup(rh, *rl)
        rp = VGroup(panel(rcol, color=GOOD, buff=0.25, stroke=3), rcol)
        rp[0].stretch_to_fit_height(wp[0].height).set_y(wp[0].get_y())
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.5)
            self.play(FadeIn(wp[0]), Create(wp[1]), FadeIn(wp[2][0]), run_time=0.8)
            b.until(0.45)
            self.play(Write(wl[0]), run_time=0.8)
            self.play(wl[0].animate.set_color(BAD), run_time=0.4)
        with self.beat("b02") as b:
            for i, fr in zip((1, 2, 3), (0.0, 0.4, 0.62)):
                b.until(fr)
                self.play(Write(wl[i]), run_time=0.8)
                self.play(wl[i].animate.set_color(BAD), run_time=0.3)
            b.until(0.8)
            self.play(FadeIn(rp), run_time=0.8)
        with self.beat("b03") as b:
            cons = T("Later marks may be consequential, but the part a mark is lost and every value is wrong.",
                     size=SMALL + 1, color=MUTED).move_to([0, -1.75, 0])
            fix = right_panel("Fix: mixture? find the reacting component first",
                              [M(r"n(\ce{CH4}) = 0.900 \times n_{\text{mix}}", size=sz, color=TEXT)], width=7.5, color=UNKNOWN)
            fix.move_to([0, -2.0, 0])
            self.play(FadeIn(cons), run_time=0.6)
            b.until(0.55)
            self.play(FadeOut(cons), FadeIn(fix), run_time=0.7)


# =====================================================================================
class E13S08_PartsDE(NarratedScene):
    def construct(self):
        h = header("Q25 parts d–e")
        tl = tally_text("Q25", 7, 15)
        l1 = work(r"E = 0.225 \times 890 = 200.25\ \text{kJ} \approx 200\ \text{kJ released}", 2.15, ENERGY_C)
        l2 = work(r"q = 800.0 \times 4.18 \times 40.0 = 133\,760\ \text{J} = 133.76\ \text{kJ}", 1.5, USEFUL)
        td, te = part_tag("d", l1), None
        b1, b2 = boxes_for(l1), boxes_for(l2)
        sc = 0.03
        x_left = -3.2
        fuel = Rectangle(width=200.25 * sc, height=0.36, fill_color=ENERGY_C, fill_opacity=0.85, stroke_width=0)
        fuel.move_to([0, 0.82, 0]).align_to([x_left, 0, 0], LEFT)
        water = Rectangle(width=133.76 * sc, height=0.36, fill_color=USEFUL, fill_opacity=0.85, stroke_width=0)
        water.move_to([0, 0.3, 0]).align_to([x_left, 0, 0], LEFT)
        loss = DashedVMobject(Rectangle(width=(200.25 - 133.76) * sc, height=0.36, stroke_color=LOSS, stroke_width=2),
                              num_dashes=18).next_to(water, RIGHT, buff=0)
        lf = T("fuel energy released", size=SMALL + 1).next_to(fuel, LEFT, buff=0.2)
        lw = T("heat gained by water", size=SMALL + 1).next_to(water, LEFT, buff=0.2)
        ll = T("not useful", size=SMALL, color=LOSS).next_to(loss, RIGHT, buff=0.15)
        bars = VGroup(fuel, water, loss, lf, lw, ll)
        l3 = work(r"\text{efficiency} = \frac{133.76}{200.25} \times 100\% = 66.8\%", -0.5, USEFUL)
        tg_e = part_tag("e", l3)
        b3 = boxes_for(l3, 2)
        with self.beat("b01") as b:
            self.tl = tl
            self.play(FadeIn(h), FadeIn(tl), run_time=0.5)
            self.play(Write(l1), FadeIn(td), FadeIn(b1), run_time=1.0)
            self.play(tick(b1), Transform(self.tl, tally_text("Q25", 8, 15)), run_time=0.4)
            self.play(GrowFromEdge(fuel, LEFT), FadeIn(lf), run_time=0.7)
            b.until(0.45)
            self.play(Write(l2), FadeIn(b2), run_time=1.1)
            self.play(GrowFromEdge(water, LEFT), FadeIn(lw), Create(loss), FadeIn(ll), run_time=0.8)
            b.until(0.85)
            self.play(tick(b2), Transform(self.tl, tally_text("Q25", 9, 15)), run_time=0.4)
        with self.beat("b02") as b:
            self.play(Write(l3), FadeIn(tg_e), FadeIn(b3), run_time=1.2)
            self.play(*[tick(x) for x in b3], Transform(self.tl, tally_text("Q25", 11, 15)), run_time=0.4)
            b.until(0.6)
            keep = T("keep 200.25 unrounded; round only the final answer (3 s.f.)", size=SMALL + 1, color=MUTED)
            keep.next_to(l3, DOWN, buff=0.2).align_to(l3, LEFT)
            self.play(FadeIn(keep), run_time=0.5)
            self.keep = keep
        with self.beat("b03") as b:
            d1 = wrong_panel("÷ efficiency?", [T("only to find a required input", size=SMALL)], size=SMALL, width=3.6)
            d2 = right_panel("Plausible?", [T("0 < 66.8% < 100%;  q(water) < E(fuel)", size=SMALL)], size=SMALL,
                             width=4.4)
            VGroup(d1, d2).arrange(RIGHT, buff=0.35).move_to([-0.6, -1.98, 0])
            b4 = mbox().next_to(d1, UP, buff=0.08).align_to(d1, RIGHT)
            self.play(FadeOut(self.keep), FadeIn(d1), run_time=0.7)
            b.until(0.35)
            self.play(FadeIn(d2), run_time=0.7)
            b.until(0.75)
            mk = T("d: 2 marks   e: 3 marks", size=SMALL + 2, color=GOOD).move_to([4.1, -1.15, 0])
            b4.move_to([XM, -1.98, 0])
            self.play(FadeIn(b4), FadeIn(mk), run_time=0.4)
            self.play(tick(b4), Transform(self.tl, tally_text("Q25", 12, 15)), run_time=0.4)


# =====================================================================================
class E13S09_PartsFG(NarratedScene):
    def construct(self):
        h = header("Q25 parts f–g")
        tl = tally_text("Q25", 12, 15)
        new = VGroup(T("new CO₂ from combustion", size=SMALL + 1, color=MUTED),
                     M(r"1 \times 0.225 = 0.225\ \text{mol}", size=WK, color=MOL_C)).arrange(DOWN, buff=0.12)
        inl = VGroup(T("inlet CO₂ (passes through)", size=SMALL + 1, color=MUTED),
                     M(r"0.100 \times 0.250 = 0.0250\ \text{mol}", size=WK, color=MOL_C)).arrange(DOWN, buff=0.12)
        new.move_to([-3.6, 1.85, 0])
        inl.move_to([-3.6, 0.45, 0])
        tot = M(r"0.250\ \text{mol} \times 24.8 = 6.20\ \text{L}", size=WK + 2, color=VOL_C).move_to([2.9, 1.15, 0])
        a1 = Arrow(new.get_right(), tot.get_left() + 0.15 * UP, buff=0.2, color=CO2E, stroke_width=4)
        a2 = Arrow(inl.get_right(), tot.get_left() + 0.15 * DOWN, buff=0.2, color=CO2E, stroke_width=4)
        bf = boxes_for(tot, 2)
        tf = TB("f.", size=LABEL + 2, color=SYSTEM).move_to([-6.3, 1.15, 0])
        with self.beat("b01") as b:
            self.tl = tl
            self.play(FadeIn(h), FadeIn(tl), FadeIn(tf), run_time=0.5)
            self.play(FadeIn(new), run_time=0.7)
            b.until(0.35)
            self.play(FadeIn(inl), run_time=0.7)
            b.until(0.65)
            self.play(GrowArrow(a1), GrowArrow(a2), Write(tot), run_time=1.0)
            self.play(FadeIn(bf), run_time=0.3)
            self.play(*[tick(x) for x in bf], Transform(self.tl, tally_text("Q25", 14, 15)), run_time=0.4)
        with self.beat("b02") as b:
            c_in = M(r"\text{C in: } 0.225 + 0.0250 = 0.250\ \text{mol}", size=WK - 2)
            c_out = M(r"\text{C out: } 0.250\ \text{mol CO}_2", size=WK - 2)
            ok = T("✓ carbon conserved", size=LABEL + 1, color=GOOD)
            cc = VGroup(c_in, c_out, ok).arrange(RIGHT, buff=0.5).move_to([0, -0.85, 0])
            self.play(FadeIn(c_in), run_time=0.6)
            b.until(0.4)
            self.play(FadeIn(c_out), run_time=0.6)
            self.play(FadeIn(ok, scale=1.2), run_time=0.4)
            b.until(0.8)
            dry = T("dry CO₂ isolated: water not counted", size=SMALL + 1, color=MUTED).next_to(cc, DOWN, buff=0.22)
            self.play(FadeIn(dry), run_time=0.5)
            self.cc = VGroup(cc, dry)
        with self.beat("b03") as b:
            gp = right_panel("g. Renewable because of its source",
                             [wrapped("recently grown biomass (food or farm waste), replenished on a human timescale; "
                                      "the CH₄ molecule is identical to fossil methane", size=SMALL + 1, width=9.8)],
                             size=SMALL + 1, width=10.0, color=BIO)
            gp.move_to([-0.3, -1.3, 0])
            self.play(FadeOut(self.cc), FadeIn(gp), run_time=0.8)
            bg = mbox().move_to([XM, -1.3, 0])
            b.until(0.85)
            self.play(FadeIn(bg), run_time=0.3)
            self.play(tick(bg), Transform(self.tl, tally_text("Q25", 15, 15)), run_time=0.4)
        with self.beat("b04") as b:
            self.clear()
            tally = mark_tally([(3, "a: mixture amount, CH₄ amount, O₂ amount"), (2, "b: equation with states; ΔH"),
                                (2, "c: O₂ required; excess mass"), (2, "d: energy released; heat gained"),
                                (3, "e: ratio set up; value; direction explained"), (2, "f: new + inlet CO₂; volume"),
                                (1, "g: source-based reason")], size=SMALL + 1, width=9.4, title="Q25 indicative marks")
            tally.move_to([0, 0.2, 0])
            self.play(FadeIn(tally), run_time=1.0)


# =====================================================================================
class E13S10_SpotError(NarratedScene):
    def construct(self):
        h = header("Checkpoint: spot the error")
        sub = T("three lines from different students' answers to Q25 · one mistake in each", size=SMALL + 1, color=MUTED)
        sub.next_to(h, DOWN, buff=0.25).align_to(h, LEFT)
        ys = [1.45, 0.05, -1.35]
        lines = [work(r"n(\ce{O2}) = 60.0 \div 24.8 = 2.42\ \text{mol}", ys[0], x=-4.9),
                 work(r"V(\ce{CO2}) = 0.225 \times 24.8 = 5.58\ \text{L}", ys[1], x=-4.9),
                 work(r"q = 800.0 \times 4.18 \times 40.0 = 133\,760\ \text{kJ}", ys[2], x=-4.9)]
        nums = VGroup(*[number(i + 1, l) for i, l in enumerate(lines)])
        fixes = [work(r"0.210 \times 60.0 \div 24.8 = 0.508\ \text{mol}\quad(\text{air is not all oxygen})", ys[0] - 0.62,
                      GOOD, size=WK - 4, x=-4.9),
                 work(r"(0.225 + 0.0250) \times 24.8 = 6.20\ \text{L}\quad(\text{add the inlet CO}_2)", ys[1] - 0.62,
                      GOOD, size=WK - 4, x=-4.9),
                 work(r"= 133\,760\ \text{J} = 133.76\ \text{kJ}\quad(\text{g} \times \text{J g}^{-1}\,{}^\circ\text{C}^{-1} \times {}^\circ\text{C} = \text{J})",
                      ys[2] - 0.62, GOOD, size=WK - 4, x=-4.9)]
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(sub), run_time=0.5)
            for i in range(3):
                self.play(FadeIn(nums[i]), Write(lines[i]), run_time=0.8)
        with self.beat("b02") as b:
            c1 = SurroundingRectangle(lines[0][0][6:10], color=BAD, buff=0.06)
            self.play(Create(c1), run_time=0.5)
            b.until(0.35)
            self.play(FadeIn(fixes[0], shift=0.1 * DOWN), run_time=0.8)
        with self.beat("b03") as b:
            c2 = SurroundingRectangle(lines[1][0][7:12], color=BAD, buff=0.06)
            self.play(Create(c2), run_time=0.5)
            b.until(0.3)
            self.play(FadeIn(fixes[1], shift=0.1 * DOWN), run_time=0.8)
        with self.beat("b04") as b:
            unit = lines[2][0][-2:]
            self.play(Create(strike(unit)), run_time=0.5)
            b.until(0.3)
            self.play(FadeIn(fixes[2], shift=0.1 * DOWN), run_time=0.9)
            b.until(0.62)
            warn = M(r"\text{uncorrected: } 133\,760\ \text{kJ} \div 200.25\ \text{kJ} \times 100\% \approx 66\,800\%\ \text{(impossible)}",
                     size=WK - 4, color=BAD).move_to([0, -2.45, 0])
            self.play(FadeIn(warn), run_time=0.7)


# =====================================================================================
class E13S11_LessAir(NarratedScene):
    def construct(self):
        h = header("What if there were less air?")
        old = T("60.0 L air", size=LABEL + 2, color=MUTED)
        new = T("50.0 L air", size=LABEL + 2, color=UNKNOWN)
        q = T("Would all 0.225 mol of CH₄ still burn completely?", size=LABEL + 2)
        row = VGroup(old, Arrow(LEFT, RIGHT, stroke_width=3, color=FAINT).scale(0.4), new).arrange(RIGHT, buff=0.25)
        top = VGroup(row, q).arrange(DOWN, buff=0.35).move_to([0, 1.85, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(old), run_time=0.5)
            b.until(0.3)
            self.play(FadeIn(row[1]), FadeIn(new), Create(strike(old, color=MUTED, width=3)), run_time=0.7)
            b.until(0.6)
            self.play(FadeIn(q), run_time=0.6)
        with self.beat("b02") as b:
            l1 = work(r"n(\ce{O2}) = 0.210 \times 50.0 \div 24.8 = 10.5 \div 24.8 = 0.423\ \text{mol}", 0.55, MOL_C, x=-5.9)
            sc = 8.0
            av = Rectangle(width=0.423 * sc, height=0.38, fill_color=MOL_C, fill_opacity=0.85, stroke_width=0)
            rq = Rectangle(width=0.450 * sc, height=0.38, fill_color=FAINT, fill_opacity=0.9, stroke_width=0)
            av.move_to([0, -0.35, 0]).align_to([-2.2, 0, 0], LEFT)
            rq.move_to([0, -0.9, 0]).align_to([-2.2, 0, 0], LEFT)
            la = T("O₂ available", size=SMALL + 1).next_to(av, LEFT, buff=0.2)
            lr = T("O₂ required", size=SMALL + 1).next_to(rq, LEFT, buff=0.2)
            va = T("0.423 mol", size=SMALL + 1, color=MOL_C).next_to(av, RIGHT, buff=0.15)
            vr = T("2 × 0.225 = 0.450 mol", size=SMALL + 1, color=MUTED).next_to(rq, RIGHT, buff=0.15)
            self.play(Write(l1), run_time=1.2)
            b.until(0.25)
            self.play(GrowFromEdge(av, LEFT), FadeIn(la), FadeIn(va), run_time=0.7)
            self.play(GrowFromEdge(rq, LEFT), FadeIn(lr), FadeIn(vr), run_time=0.7)
            lim = chip("O₂ is now limiting", LOSS, size=SMALL + 2).move_to([0, -1.6, 0])
            b.until(0.42)
            self.play(FadeIn(lim, scale=1.1), run_time=0.5)
            cons = T("CH₄ can't all burn completely  ·  CO or soot possible  ·  less energy released",
                     size=SMALL + 2, color=TEXT).move_to([0, -2.3, 0])
            b.until(0.6)
            self.play(FadeIn(cons), run_time=0.7)


# =====================================================================================
class E13S12_Q26Attempt(NarratedScene):
    PAUSE_LABELS = {"b02": "Pause the video now and attempt every part"}
    TIMER_CORNER = DR

    def construct(self):
        qc = attempt_card("Q26")
        with self.beat("b01"):
            self.play(FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        with self.beat("b02") as b:
            self.play(Indicate(qc[1][0][0], color=UNKNOWN), run_time=0.8)


# =====================================================================================
class E13S13_PartsAB(NarratedScene):
    def construct(self):
        h = header("Q26 parts a–b")
        req = requested("g CO₂ per useful kJ")
        notes = VGroup(chip("ΔH is per mol", ENERGY_C), chip("efficiencies differ: 25.0% vs 40.0%", USEFUL),
                       chip("basis for b: per useful kJ", UNKNOWN)).arrange(RIGHT, buff=0.3).move_to([0, 2.25, 0])
        xm, xe = -3.35, 3.35
        hm = TB("methanol (heater 25.0%)", size=LABEL + 1, color=SURR).move_to([xm, 1.55, 0])
        he = TB("ethanol (heater 40.0%)", size=LABEL + 1, color=SYSTEM).move_to([xe, 1.55, 0])
        div = DashedLine([0, 1.8, 0], [0, -1.55, 0], color=FAINT, dash_length=0.08)

        def col(x, tex, y, c=TEXT):
            return M(tex, size=WK - 2, color=c).move_to([x, y, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for i, fr in enumerate((0.05, 0.3, 0.6)):
                b.until(fr)
                self.play(FadeIn(notes[i], shift=0.1 * DOWN), run_time=0.5)
            self.play(FadeIn(req), run_time=0.4)
        with self.beat("b02") as b:
            a_m = col(xm, r"\text{a: } 726 \div 32.0 = 22.7\ \text{kJ g}^{-1}", 0.95, ENERGY_C)
            a_e = col(xe, r"\text{a: } 1370 \div 46.0 = 29.8\ \text{kJ g}^{-1}", 0.95, ENERGY_C)
            self.play(FadeIn(hm), FadeIn(he), Create(div), run_time=0.6)
            self.play(Write(a_m), run_time=0.8)
            b.until(0.5)
            self.play(Write(a_e), run_time=0.8)
        with self.beat("b03") as b:
            m1 = col(xm, r"1\ \text{mol} \to 1\ \text{mol CO}_2 = 44.0\ \text{g}", 0.25, CO2E)
            m2 = col(xm, r"\text{useful} = 726 \times 0.250 = 181.5\ \text{kJ}", -0.4, USEFUL)
            m3 = col(xm, r"44.0 \div 181.5 = 0.242\ \text{g kJ}^{-1}", -1.1, UNKNOWN)
            self.play(FadeIn(m1), run_time=0.6)
            b.until(0.3)
            self.play(Write(m2), run_time=0.9)
            b.until(0.72)
            self.play(Write(m3), run_time=0.8)
            self.m3 = m3
        with self.beat("b04") as b:
            e1 = col(xe, r"1\ \text{mol} \to 2\ \text{mol CO}_2 = 88.0\ \text{g}", 0.25, CO2E)
            e2 = col(xe, r"\text{useful} = 1370 \times 0.400 = 548\ \text{kJ}", -0.4, USEFUL)
            e3 = col(xe, r"88.0 \div 548 = 0.161\ \text{g kJ}^{-1}", -1.1, UNKNOWN)
            self.play(FadeIn(e1), run_time=0.6)
            b.until(0.3)
            self.play(Write(e2), run_time=0.9)
            b.until(0.6)
            self.play(Write(e3), run_time=0.8)
            win = T("lower direct CO₂ per useful kJ", size=SMALL + 1, color=GOOD).next_to(e3, DOWN, buff=0.3)
            self.play(Create(result_box(e3, GOOD)), FadeIn(win), run_time=0.6)
            mk = T("a: 2 marks   b: 4 marks", size=SMALL + 1, color=GOOD).move_to([0, -2.3, 0])
            b.until(0.85)
            self.play(FadeIn(mk), run_time=0.4)
            self.mk = mk
        with self.beat("b05") as b:
            pl = VGroup(M(r"\text{per kJ released: } 44.0 \div 726 = 0.0606 \quad 88.0 \div 1370 = 0.0642\ \text{(similar)}",
                          size=WK - 4, color=MUTED),
                        M(r"\text{efficiency ratio } 0.400 \div 0.250 = 1.6 \quad \text{vs} \quad 0.242 \div 0.161 \approx 1.5\ \checkmark",
                          size=WK - 4, color=GOOD)).arrange(DOWN, buff=0.14).move_to([0, -2.25, 0])
            self.play(FadeOut(self.mk), FadeIn(pl[0]), run_time=0.7)
            b.until(0.45)
            self.play(FadeIn(pl[1]), run_time=0.7)


# =====================================================================================
class E13S14_WrongBases(NarratedScene):
    def construct(self):
        h = header("Wrong solution: emissions on different bases")
        sz = EQ_SMALL - 10
        w1 = M(r"\text{methanol: } 44.0 \div 181.5 = 0.242", size=sz)
        w2 = M(r"\text{ethanol: } 88.0 \div 1370 = 0.0642", size=sz)
        w3 = T("“ethanol emits nearly 4× less”", size=SMALL + 2, color=BAD)
        t1 = T("per useful kJ", size=SMALL, color=USEFUL)
        t2 = T("per kJ released", size=SMALL, color=BAD)
        r1 = VGroup(w1, t1).arrange(RIGHT, buff=0.25)
        r2 = VGroup(w2, t2).arrange(RIGHT, buff=0.25)
        t2.align_to(t1, LEFT)
        t1.set_opacity(0)
        t2.set_opacity(0)
        wp = wrong_panel("Student's comparison", [r1, r2, w3], size=SMALL + 1, width=5.4).move_to([-3.3, 1.05, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            self.play(FadeIn(wp[0]), Create(wp[1]), FadeIn(wp[2][0]), run_time=0.7)
            self.play(Write(w1), run_time=0.8)
            b.until(0.35)
            self.play(Write(w2), run_time=0.8)
            b.until(0.75)
            self.play(FadeIn(w3), run_time=0.5)
        with self.beat("b02") as b:
            self.play(t1.animate.set_opacity(1), t2.animate.set_opacity(1), run_time=0.6)
            self.play(Indicate(t2, color=BAD), run_time=0.7)
            rp = right_panel("Same basis: per useful kJ",
                             [M(r"\text{methanol } 0.242 \quad \text{ethanol } 0.161", size=sz),
                              M(r"0.242 \div 0.161 \approx 1.5\ \text{(not 4)}", size=sz, color=GOOD)],
                             size=SMALL + 1, width=4.6).move_to([3.85, 1.05, 0])
            b.until(0.5)
            self.play(FadeIn(rp), run_time=0.8)
        with self.beat("b03") as b:
            w4 = wrong_panel("Per mole of fuel: “methanol emits half as much”",
                             [M(r"1\ \text{mol CO}_2 \text{ vs } 2\ \text{mol CO}_2 \text{ per mol of fuel}", size=sz)],
                             note="true per mole, but 1 mol methanol delivers 181.5 kJ useful vs 548 kJ for ethanol",
                             size=SMALL + 1, width=11.6)
            w4.move_to([0, -1.55, 0])
            self.play(FadeIn(w4), run_time=0.8)


# =====================================================================================
class E13S15_PartsCD(NarratedScene):
    def construct(self):
        h = header("Q26 parts c–d")
        claim = T("“Both contain an O–H bond, so they release equal energy per gram.”", size=LABEL + 2)
        claim.move_to([0, 2.15, 0])
        r1 = T("1.  one shared bond can't decide: it depends on the whole molecule's combustion", size=LABEL, color=GOOD)
        r2 = wrapped("2.  oxygen is 50% of methanol's mass but 35% of ethanol's: already partly oxidised, so "
                     "methanol releases less per gram (22.7 vs 29.8 kJ g⁻¹)", size=LABEL, width=12.0, color=GOOD)
        rs = VGroup(r1, r2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([0, 1.05, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(claim), run_time=0.7)
            b.until(0.25)
            self.play(Create(Line(claim.get_left(), claim.get_right(), color=BAD, stroke_width=4)), run_time=0.5)
            b.until(0.4)
            self.play(FadeIn(r1), run_time=0.6)
            b.until(0.75)
            self.play(FadeIn(r2), run_time=0.6)
        with self.beat("b02") as b:
            it = T("combustion CO₂ (calculated)", size=SMALL, color=SYSTEM)
            inner = RoundedRectangle(width=it.width + 0.5, height=0.8, corner_radius=0.12, stroke_color=SYSTEM, stroke_width=3)
            ot = VGroup(T("lifecycle: feedstock · processing · transport", size=SMALL, color=SURR),
                        T("(no data given)", size=SMALL, color=SURR)).arrange(DOWN, buff=0.08)
            outer = DashedVMobject(RoundedRectangle(width=ot.width + 0.6, height=2.3, corner_radius=0.16, stroke_color=SURR,
                                                    stroke_width=2.5), num_dashes=50)
            dia = VGroup(outer, inner, it)
            inner.move_to(outer).shift(0.45 * UP)
            it.move_to(inner)
            ot.next_to(inner, DOWN, buff=0.2)
            dia.add(ot)
            dia.move_to([-3.2, -1.3, 0])
            con = VGroup(TB("d. Lower lifecycle emissions?", size=LABEL + 1, color=UNKNOWN),
                         T("Can't tell: only direct combustion", size=LABEL, color=TEXT),
                         T("CO₂ was counted.", size=LABEL, color=TEXT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            con.move_to([3.4, -1.3, 0])
            self.play(FadeIn(inner), FadeIn(it), FadeIn(con[0]), run_time=0.7)
            b.until(0.35)
            self.play(FadeIn(con[1:]), run_time=0.6)
            b.until(0.55)
            self.play(Create(outer), FadeIn(ot), run_time=1.0)
        with self.beat("b03") as b:
            self.clear(h)
            tally = mark_tally([(2, "a: energy per gram for each fuel"), (4, "b: useful energy and g CO₂ per useful kJ, each fuel"),
                                (2, "c: one bond can't decide; oxygen fraction (already partly oxidised)"), (2, "d: no; lifecycle stages missing")],
                               size=SMALL + 2, width=8.0, title="Q26 indicative marks").move_to([0, 0.1, 0])
            self.play(FadeIn(tally), run_time=0.9)


# =====================================================================================
class E13S16_ErrorLog(NarratedScene):
    PAUSE_LABELS = {"b03": "Write your entry"}

    def construct(self):
        h = header("Your error log")
        rows = [["Question / part", "What I did", "Type of error", "Correct idea", "Check next time"],
                ["Q25 a", "used 0.250 mol as the CH₄", "reading: mixture vs component",
                 "multiply by the volume fraction first", "circle every % in a gas question: “% of what?”"],
                [blank() for _ in range(5)]]
        tb = table(rows, [1.9, 2.5, 2.5, 2.6, 3.1], size=SMALL, row_h=0.62).move_to([0, 0.75, 0])
        grid, cells = tb[0], tb[1]
        your = T("your entry", size=SMALL, color=FAINT).move_to(tb.get_bottom() + 0.31 * UP).align_to(cells[0], LEFT)
        with self.beat("b01") as b:
            self.play(FadeIn(h), Create(grid), run_time=0.9)
            for i, fr in enumerate((0.25, 0.4, 0.55, 0.7, 0.82)):
                b.until(fr)
                self.play(FadeIn(cells[i]), run_time=0.4)
        with self.beat("b02") as b:
            for i, fr in enumerate((0.0, 0.18, 0.4, 0.62, 0.78)):
                b.until(fr)
                self.play(FadeIn(cells[5 + i], shift=0.05 * DOWN), run_time=0.5)
        with self.beat("b03") as b:
            self.play(FadeIn(your), run_time=0.5)
            self.play(Indicate(your, color=UNKNOWN), run_time=0.8)
        with self.beat("b04") as b:
            self.clear(h)
            items = bullets(["Read and annotate: units, conditions, trap words",
                             "Choose the method before calculating",
                             "Show every quantity with units; carry unrounded values",
                             "Check plausibility: conservation, 0–100%, sensible sizes",
                             "Watch for: mixtures, air vs oxygen, inlet vs new CO₂, the basis of every comparison"],
                            size=LABEL + 1, width=11.5).move_to([0, 0.5, 0])
            self.play(FadeIn(items, lag_ratio=0.15), run_time=1.5)
            nxt = T("Next: Episode 14 · Exam workshop B on calorimetry and data evaluation", size=LABEL, color=MUTED)
            nxt.move_to([0, -2.3, 0])
            b.until(0.8)
            self.play(FadeIn(nxt), run_time=0.6)


EPISODE_SCENES = ["E13S01_Retrieval", "E13S02_Routine", "E13S03_Q25Attempt", "E13S04_Annotate", "E13S05_Plan",
                  "E13S06_PartsAC", "E13S07_WrongMethane", "E13S08_PartsDE", "E13S09_PartsFG",
                  "E13S10_SpotError", "E13S11_LessAir", "E13S12_Q26Attempt", "E13S13_PartsAB",
                  "E13S14_WrongBases", "E13S15_PartsCD", "E13S16_ErrorLog"]
