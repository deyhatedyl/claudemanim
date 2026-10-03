"""
Episode 02 - Where reaction energy comes from.
Narration: scripts/ep02.md (beat names must match).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (bullets, calorimeter, dH_arrow, enthalpy_axis, ledger, level, mark_tally,  # noqa: E402
                               mol_CH3OH, mol_CH4, mol_CO2, mol_H2, number_badge, question_card, result_box,
                               right_panel, title_card, wrapped, wrong_panel, atom)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, LOSS, MUTED, PANEL,  # noqa: E402
                          SMALL, SURR, SYSTEM, TEXT, UNKNOWN, USEFUL, M, T, TB, chip, header, panel)


def requested(text: str) -> VGroup:
    from shared.style import asked_pill
    return asked_pill(text)


def flow_arrows(center, r_in: float, r_out: float, inward: bool, color: str, n: int = 4, stroke: float = 6):
    """Arrows crossing a circular boundary (outward for exothermic, inward for endothermic)."""
    g = VGroup()
    for k in range(n):
        ang = np.pi / 4 + k * 2 * np.pi / n
        d = np.array([np.cos(ang), np.sin(ang), 0])
        a, b = center + d * r_in, center + d * r_out
        g.add(Arrow(b, a, buff=0, color=color, stroke_width=stroke, max_tip_length_to_length_ratio=0.35) if inward
              else Arrow(a, b, buff=0, color=color, stroke_width=stroke, max_tip_length_to_length_ratio=0.35))
    return g


def mini_molecules(center, scale=0.5):
    ms = VGroup(mol_H2(scale), mol_CH4(scale * 0.8), mol_H2(scale))
    ms.arrange(RIGHT, buff=0.12).move_to(center)
    return ms


# =====================================================================================
class E02S01_Retrieval(NarratedScene):
    def construct(self):
        card = title_card(2, "Where reaction energy comes from")
        with self.beat("b01"):
            self.play(FadeIn(card, shift=0.2 * UP), run_time=1.5)

        with self.beat("b02") as b:
            self.play(FadeOut(card), run_time=0.5)
            h = header("Retrieval check")
            eq = M(r"2\,\ce{H2}", "+", r"\ce{O2}", r"\ce{->}", r"2\,\ce{H2O}", size=EQ + 4).move_to([0, 1.6, 0])
            q = T("0.500 mol of H₂ reacts completely. What amount of water forms?", size=BODY).move_to([0, 0.2, 0])
            self.play(FadeIn(h), Write(eq), run_time=1.0)
            b.until(0.5)
            self.play(FadeIn(q), run_time=0.8)
            self.eq, self.q, self.h = eq, q, h

        with self.beat("b03") as b:
            r1 = M(r"\ce{H2} : \ce{H2O} = 2 : 2 = 1 : 1", size=EQ_SMALL).move_to([0, -0.9, 0])
            r2 = M(r"n(\ce{H2O}) = 0.500\ \text{mol}", size=EQ, color=GOOD).move_to([0, -1.9, 0])
            self.play(Indicate(self.eq[0]), Indicate(self.eq[4]), run_time=1.0)
            self.play(Write(r1), run_time=1.0)
            b.until(0.5)
            self.play(Write(r2), Create(result_box(r2)), run_time=1.0)

        with self.beat("b04") as b:
            self.clear(self.h)
            self.play(ReplacementTransform(self.h, header("The big question")), run_time=0.5)
            big = TB("When a fuel burns, where does the energy come from?", size=BODY + 4).move_to([0, 1.5, 0])
            claim = VGroup(T("A common belief:", size=LABEL, color=MUTED),
                           T("“Energy is stored in bonds and is released when bonds break.”", size=BODY))
            claim.arrange(DOWN, buff=0.2)
            cb = panel(claim, color=UNKNOWN)
            cg = VGroup(cb, claim).move_to([0, -0.2, 0])
            stamp = TB("We'll test this claim", size=BODY, color=UNKNOWN).move_to([0, -1.9, 0])
            self.play(Write(big), run_time=1.2)
            b.until(0.3)
            self.play(FadeIn(cg), run_time=0.8)
            b.until(0.55)
            self.play(FadeIn(stamp, scale=1.1), run_time=0.6)


# =====================================================================================
class E02S02_System(NarratedScene):
    def construct(self):
        h = header("System and surroundings")
        cal = calorimeter(width=3.4, height=2.8, system=True).move_to([-3.6, 0.0, 0])
        mols = mini_molecules(cal.system.get_center(), 0.42)
        sys_lab = TB("System", size=BODY, color=SYSTEM)
        sys_sub = T("the reacting chemicals", size=LABEL, color=SYSTEM)
        sg = VGroup(sys_lab, sys_sub).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([1.4, 1.4, 0]).align_to([0.4, 0, 0], LEFT)
        sur_lab = TB("Surroundings", size=BODY, color=SURR)
        sur_sub = wrapped("everything else: water, cup, thermometer, air", size=LABEL, width=5.7, color=SURR)
        ug = VGroup(sur_lab, sur_sub).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([1.4, 0.0, 0]).align_to([0.4, 0, 0], LEFT)
        p1 = Line(sg.get_left() + 0.1 * LEFT, cal.system.get_right() + 0.05 * RIGHT, color=SYSTEM, stroke_width=2)
        p2 = Line(ug.get_left() + 0.1 * LEFT, cal.water.get_right() + 0.3 * LEFT + 0.2 * DOWN, color=SURR, stroke_width=2)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(cal.cup), FadeIn(cal.water), FadeIn(cal.lid), FadeIn(cal.thermo),
                      FadeIn(cal.stirrer), run_time=0.8)
            self.play(Create(cal.system), FadeIn(mols), run_time=0.8)
            self.play(FadeIn(sg), Create(p1), run_time=0.6)
            b.until(0.55)
            self.play(FadeIn(ug), Create(p2), run_time=0.6)

        arrows = flow_arrows(cal.system.get_center(), 0.62, 1.15, inward=False, color=SYSTEM)
        with self.beat("b02") as b:
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.2)
            heat = VGroup(TB("Heat", size=BODY, color=UNKNOWN),
                          wrapped("energy transferred because of a temperature difference", size=LABEL, width=6.0),
                          T("a transfer, not a substance", size=LABEL, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            heat.move_to([1.4, -1.5, 0]).align_to([0.4, 0, 0], LEFT)
            b.until(0.4)
            self.play(FadeIn(heat[:2]), run_time=0.8)
            b.until(0.75)
            self.play(FadeIn(heat[2]), run_time=0.5)
            self.heat = heat

        with self.beat("b03") as b:
            self.play(FadeOut(VGroup(sg, ug, p1, p2)), run_time=0.4)
            temp = VGroup(TB("Temperature", size=BODY, color="#F1948A"),
                          T("how hot something is", size=LABEL),
                          wrapped("reflects the average kinetic energy of the particles", size=LABEL, width=6.0),
                          T("not the total energy it contains", size=LABEL, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            temp.move_to([1.4, 1.1, 0]).align_to([0.4, 0, 0], LEFT)
            self.play(FadeIn(temp[:2]), run_time=0.6)
            b.until(0.35)
            self.play(FadeIn(temp[2]), run_time=0.6)
            b.until(0.7)
            self.play(FadeIn(temp[3]), run_time=0.5)

        with self.beat("b04") as b:
            self.clear(h)
            cup = VGroup(RoundedRectangle(width=1.0, height=1.1, corner_radius=0.1, stroke_color=TEXT, stroke_width=3),
                         Rectangle(width=0.92, height=0.8, stroke_width=0, fill_color="#B9770E", fill_opacity=0.7))
            cup[1].align_to(cup[0], DOWN).shift(0.04 * UP)
            bath = VGroup(RoundedRectangle(width=5.0, height=1.6, corner_radius=0.3, stroke_color=TEXT, stroke_width=3),
                          RoundedRectangle(width=4.8, height=1.2, corner_radius=0.25, stroke_width=0, fill_color=SURR,
                                           fill_opacity=0.45))
            bath[1].align_to(bath[0], DOWN).shift(0.08 * UP)
            cup.move_to([-4.3, 0.8, 0])
            bath.move_to([1.8, 0.8, 0])
            l1 = VGroup(T("cup of tea, 80 °C", size=LABEL), T("hotter", size=LABEL, color="#F1948A")).arrange(DOWN, buff=0.1).next_to(cup, DOWN, buff=0.3)
            l2 = VGroup(T("bath, 40 °C", size=LABEL), T("far more water: far more thermal energy", size=LABEL, color=SURR)).arrange(DOWN, buff=0.1).next_to(bath, DOWN, buff=0.3)
            self.play(FadeIn(cup), FadeIn(l1), run_time=0.8)
            b.until(0.25)
            self.play(FadeIn(bath), FadeIn(l2), run_time=0.8)
            key = TB("Higher temperature does not mean more energy", size=BODY, color=UNKNOWN).move_to([0, -1.6, 0])
            b.until(0.55)
            self.play(Write(key), run_time=1.0)
            note = T("Calorimetry uses a temperature change to work out how much heat was transferred.",
                     size=LABEL, color=MUTED).move_to([0, -2.3, 0])
            b.until(0.78)
            self.play(FadeIn(note), run_time=0.6)


# =====================================================================================
class E02S03_ExoEndo(NarratedScene):
    def construct(self):
        h = header("Exothermic and endothermic")
        calL = calorimeter(width=2.5, height=2.0, system=True).move_to([-3.4, 0.7, 0])
        calR = calorimeter(width=2.5, height=2.0, system=True).move_to([3.4, 0.7, 0])
        tL = TB("Exothermic", size=BODY, color=SYSTEM).next_to(calL, UP, buff=0.2)
        tR = TB("Endothermic", size=BODY, color=SURR).next_to(calR, UP, buff=0.2)
        outA = flow_arrows(calL.system.get_center(), 0.48, 0.95, inward=False, color=SYSTEM, stroke=5)
        inA = flow_arrows(calR.system.get_center(), 0.48, 0.95, inward=True, color=SURR, stroke=5)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(calL), FadeIn(tL), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(a) for a in outA], lag_ratio=0.15), run_time=1.0)
            b.until(0.35)
            self.play(calL.thermo.level.animate.set_value(0.75), run_time=1.6)
            lL = VGroup(T("energy: system → surroundings", size=LABEL), T("water warms; reading rises", size=LABEL, color=MUTED),
                        T("e.g. combustion of a fuel", size=LABEL, color=MUTED)).arrange(DOWN, buff=0.08)
            lL.next_to(calL, DOWN, buff=0.2)
            b.until(0.7)
            self.play(FadeIn(lL), run_time=0.8)

        with self.beat("b02") as b:
            self.play(FadeIn(calR), FadeIn(tR), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(a) for a in inA], lag_ratio=0.15), run_time=1.0)
            b.until(0.35)
            self.play(calR.thermo.level.animate.set_value(0.12), run_time=1.6)
            lR = VGroup(T("energy: surroundings → system", size=LABEL), T("water cools; reading falls", size=LABEL, color=MUTED),
                        T("e.g. an instant cold pack", size=LABEL, color=MUTED)).arrange(DOWN, buff=0.08)
            lR.next_to(calR, DOWN, buff=0.2)
            b.until(0.7)
            self.play(FadeIn(lR), run_time=0.8)
            self.lL, self.lR = lL, lR

        with self.beat("b03") as b:
            rule = VGroup(T("energy gained:", size=LABEL, color=UNKNOWN), T("positive", size=LABEL, color=UNKNOWN),
                          T("energy lost:", size=LABEL, color=UNKNOWN), T("negative", size=LABEL, color=UNKNOWN)).arrange(DOWN, buff=0.1)
            rule.move_to([0, 0.6, 0])
            self.play(FadeIn(rule), run_time=0.6)
            sL = M(r"q_{\text{system}} < 0,\quad q_{\text{surr}} > 0", size=EQ_SMALL - 4).next_to(self.lL, DOWN, buff=0.15)
            sR = M(r"q_{\text{system}} > 0,\quad q_{\text{surr}} < 0", size=EQ_SMALL - 4).next_to(self.lR, DOWN, buff=0.15)
            b.until(0.45)
            self.play(Write(sL), run_time=1.0)
            self.play(Write(sR), run_time=1.0)
            self.signs = VGroup(sL, sR)

        with self.beat("b04") as b:
            bal = M(r"q_{\text{system}} = -\,q_{\text{surroundings}}", size=EQ_SMALL, color=GOOD)
            note = T("(no energy escapes elsewhere)", size=SMALL, color=MUTED)
            bg = VGroup(bal, note).arrange(RIGHT, buff=0.3)
            bb = panel(bg, color=GOOD, buff=0.15)
            VGroup(bb, bg).move_to([0, -1.45, 0])
            self.play(FadeOut(self.lL), FadeOut(self.lR), run_time=0.5)
            self.play(FadeIn(bb), Write(bal), run_time=1.0)
            self.play(FadeIn(note), run_time=0.5)


# =====================================================================================
class E02S04_Bonds(NarratedScene):
    def construct(self):
        h = header("Breaking and making bonds")
        sch = T("schematic", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
        m1 = mol_H2(2.4).move_to([-3.6, 1.0, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(sch), FadeIn(m1), run_time=0.8)
            ein = VGroup(Arrow([-3.6, 2.6, 0], [-3.6, 1.35, 0], buff=0, color=SYSTEM, stroke_width=7,
                               max_tip_length_to_length_ratio=0.3),
                         T("energy in", size=LABEL, color=SYSTEM))
            ein[1].next_to(ein[0], RIGHT, buff=0.15)
            b.until(0.45)
            self.play(GrowArrow(ein[0]), FadeIn(ein[1]), run_time=0.8)
            self.play(FadeOut(m1.bonds), m1.atoms[0].animate.shift(1.0 * LEFT), m1.atoms[1].animate.shift(1.0 * RIGHT),
                      run_time=1.2)
            cap1 = TB("Breaking a bond absorbs energy", size=BODY, color=SYSTEM).move_to([-3.6, -0.4, 0])
            self.play(FadeIn(cap1), run_time=0.6)
            self.left = VGroup(m1, ein, cap1)

        a1, a2 = atom("H", 2.4).move_to([2.2, 1.0, 0]), atom("H", 2.4).move_to([5.0, 1.0, 0])
        with self.beat("b02") as b:
            self.play(FadeIn(a1), FadeIn(a2), run_time=0.6)
            target = mol_H2(2.4).move_to([3.6, 1.0, 0])
            self.play(a1.animate.move_to(target.atoms[0]), a2.animate.move_to(target.atoms[1]), run_time=1.2)
            self.play(FadeIn(target.bonds), run_time=0.4)
            eout = VGroup(Arrow([3.6, 1.35, 0], [3.6, 2.6, 0], buff=0, color=USEFUL, stroke_width=7,
                                max_tip_length_to_length_ratio=0.3), T("energy out", size=LABEL, color=USEFUL))
            eout[1].next_to(eout[0], RIGHT, buff=0.15)
            self.play(GrowArrow(eout[0]), FadeIn(eout[1]), run_time=0.8)
            cap2 = TB("Making a bond releases energy", size=BODY, color=USEFUL).move_to([3.6, -0.4, 0])
            b.until(0.6)
            self.play(FadeIn(cap2), run_time=0.6)

        def magnet(flip=False):
            n = Rectangle(width=0.7, height=0.5, fill_color=BAD, fill_opacity=0.85, stroke_width=0)
            s = Rectangle(width=0.7, height=0.5, fill_color=SURR, fill_opacity=0.85, stroke_width=0)
            g = VGroup(n, s).arrange(RIGHT, buff=0)
            tn, ts = TB("N", size=SMALL, color=BG).move_to(n), TB("S", size=SMALL, color=BG).move_to(s)
            g.add(tn, ts)
            return g.rotate(PI) if flip else g
        with self.beat("b03") as b:
            mA, mB = magnet(), magnet()
            pair = VGroup(mA, mB).arrange(RIGHT, buff=0).move_to([-3.6, -1.7, 0])
            self.play(FadeIn(pair), run_time=0.5)
            t1 = T("pulling apart takes effort", size=LABEL, color=SYSTEM).next_to(pair, DOWN, buff=0.15)
            self.play(mA.animate.shift(0.6 * LEFT), mB.animate.shift(0.6 * RIGHT), FadeIn(t1), run_time=1.0)
            b.until(0.4)
            mC, mD = magnet(), magnet()
            pair2 = VGroup(mC, mD).arrange(RIGHT, buff=1.2).move_to([3.6, -1.7, 0])
            self.play(FadeIn(pair2), run_time=0.4)
            t2 = T("snapping together gives energy out", size=LABEL, color=USEFUL).next_to(pair2, DOWN, buff=0.15)
            self.play(mC.animate.shift(0.6 * RIGHT), mD.animate.shift(0.6 * LEFT), FadeIn(t2), run_time=0.8)

        with self.beat("b04") as b:
            self.clear(h)
            e1 = VGroup(T("Overall energy change", size=BODY), T("=", size=BODY),
                        T("energy in", size=BODY, color=SYSTEM), T("(breaking reactant bonds)", size=LABEL, color=SYSTEM),
                        T("−", size=BODY), T("energy out", size=BODY, color=USEFUL),
                        T("(forming product bonds)", size=LABEL, color=USEFUL))
            row1 = VGroup(e1[0], e1[1]).arrange(RIGHT, buff=0.25)
            row2 = VGroup(VGroup(e1[2], e1[3]).arrange(DOWN, buff=0.08), e1[4], VGroup(e1[5], e1[6]).arrange(DOWN, buff=0.08)).arrange(RIGHT, buff=0.5)
            blk = VGroup(row1, row2).arrange(DOWN, buff=0.4).move_to([0, 0.8, 0])
            self.play(FadeIn(row1), run_time=0.6)
            self.play(FadeIn(row2), run_time=1.0)
            concl = TB("More energy out than in  →  exothermic overall", size=BODY, color=UNKNOWN).move_to([0, -1.2, 0])
            b.until(0.65)
            self.play(Write(concl), run_time=1.0)


# =====================================================================================
class E02S05_Q03(NarratedScene):
    def construct(self):
        h = header("Practice Q03")
        card = question_card("Q03").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(card, shift=0.1 * UP), run_time=1.0)

        eq = M(r"\ce{H2(g) + Cl2(g) -> 2HCl(g)}", size=EQ).move_to([0, 2.45, 0])
        req = requested("ΔH for the equation as written")
        with self.beat("b02") as b:
            self.play(FadeOut(card), run_time=0.5)
            self.play(Write(eq), FadeIn(req), run_time=1.0)
            asw = T("1 mol H₂ + 1 mol Cl₂ → 2 mol HCl", size=LABEL, color=MUTED).next_to(eq, DOWN, buff=0.15)
            self.play(FadeIn(asw), run_time=0.6)
            model = M(r"\Delta H \approx \textstyle\sum(\text{bonds broken}) - \sum(\text{bonds formed})", size=EQ_SMALL - 2)
            model.next_to(asw, DOWN, buff=0.3)
            b.until(0.55)
            self.play(Write(model), run_time=1.2)
            self.asw, self.model = asw, model

        led = ledger([("1 × H–H", "436"), ("1 × Cl–Cl", "243")], [("2 × H–Cl", "2 × 431")], "679 kJ", "862 kJ",
                     width=5.4)
        led.move_to([0, -0.55, 0])
        L, R = led.left, led.right
        with self.beat("b03") as b:
            self.play(FadeIn(L.box), FadeIn(L.head), run_time=0.6)
            self.play(FadeIn(L.rows[0]), run_time=0.6)
            b.until(0.45)
            self.play(FadeIn(L.rows[1]), run_time=0.6)
            b.until(0.75)
            self.play(Create(L.line), FadeIn(L.total), run_time=0.6)

        with self.beat("b04") as b:
            self.play(FadeIn(R.box), FadeIn(R.head), run_time=0.6)
            self.play(FadeIn(R.rows[0]), run_time=0.6)
            b.until(0.6)
            self.play(Create(R.line), FadeIn(R.total), run_time=0.6)
            two = SurroundingRectangle(R.rows[0][0][0], color=UNKNOWN, buff=0.06)
            self.play(Create(two), Indicate(eq), run_time=0.8)
            self.two = two

        with self.beat("b05") as b:
            pred = T("Predict: out (862) > in (679)  →  exothermic, ΔH < 0", size=LABEL + 2, color=UNKNOWN)
            pred.move_to([0, -2.35, 0])
            self.play(FadeOut(self.two), FadeIn(pred), run_time=0.8)
            self.pred = pred

        with self.beat("b06") as b:
            self.play(FadeOut(self.asw), FadeOut(self.model), FadeOut(self.pred), run_time=0.4)
            calc = M(r"\Delta H \approx 679 - 862 = -183\ \text{kJ}", size=EQ, color=GOOD).move_to([0, 1.35, 0])
            self.play(Write(calc), run_time=1.2)
            box = result_box(calc)
            self.play(Create(box), run_time=0.4)
            basis = T("per mole of reaction as written  ·  an estimate: average bond enthalpies", size=LABEL, color=MUTED)
            basis.move_to([0, -2.35, 0])
            b.until(0.6)
            self.play(FadeIn(basis), run_time=0.6)
            self.calc_grp = VGroup(calc, box, basis)

        with self.beat("b07") as b:
            self.play(FadeOut(led), FadeOut(self.calc_grp[2]), run_time=0.5)
            good = right_panel("Full-credit style", [
                "Exothermic because more energy is released forming the two H–Cl bonds (862 kJ) than is absorbed "
                "breaking the H–H and Cl–Cl bonds (679 kJ)."], width=11.5)
            good.move_to([0, -0.15, 0])
            self.play(FadeIn(good), run_time=0.8)
            weak = wrong_panel("Misses the comparison", ['"Exothermic because bonds are formed."'], width=11.5)
            weak.next_to(good, DOWN, buff=0.3)
            b.until(0.62)
            self.play(FadeIn(weak), run_time=0.8)

        with self.beat("b08") as b:
            self.clear(h, req, eq)
            tally = mark_tally([(1, "bonds broken total: 679 kJ"), (1, "bonds formed total: 862 kJ"),
                                (1, "ΔH ≈ −183 kJ (subtraction, correct sign)"),
                                (1, "explanation compares energy released and absorbed")], width=8.5)
            tally.move_to([0, 0.0, 0])
            self.play(FadeIn(tally), run_time=1.0)

        with self.beat("b09") as b:
            self.clear(h, req, eq)
            w1 = wrong_panel("Adding everything", [M(r"436 + 243 + 862 = 1541\ \text{kJ}", size=EQ_SMALL - 6, color=TEXT)],
                             note="No physical meaning", width=5.0)
            w2 = wrong_panel("Breaking treated as release", [M(r"862 - 679 = +183\ \text{kJ}", size=EQ_SMALL - 6, color=TEXT)],
                             note="Sign flipped", width=5.0)
            ws = VGroup(w1, w2).arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to([0, 0.6, 0])
            self.play(FadeIn(w1), run_time=0.7)
            b.until(0.4)
            self.play(FadeIn(w2), run_time=0.7)
            first = T("First wrong step in both: not separating energy in (broken) from energy out (formed).",
                      size=LABEL, color=UNKNOWN).move_to([0, -1.5, 0])
            b.until(0.75)
            self.play(FadeIn(first), run_time=0.6)

        with self.beat("b10") as b:
            self.clear(h, req, eq)
            p = VGroup(TB("Changed condition", size=BODY, color=UNKNOWN),
                       T("Suppose forming the two new bonds released only 600 kJ in total.", size=LABEL + 2),
                       T("Still exothermic?", size=LABEL + 2)).arrange(DOWN, buff=0.25).move_to([0, 0.9, 0])
            self.play(FadeIn(p), run_time=0.8)

        with self.beat("b11") as b:
            a = M(r"\Delta H \approx 679 - 600 = +79\ \text{kJ}", size=EQ, color=BAD).move_to([0, -0.7, 0])
            t = T("Endothermic: the sign depends on the balance of breaking and forming.", size=LABEL + 2).move_to([0, -1.7, 0])
            self.play(Write(a), run_time=1.0)
            b.until(0.5)
            self.play(FadeIn(t), run_time=0.6)


# =====================================================================================
class E02S06_Enthalpy(NarratedScene):
    def construct(self):
        h = header("Enthalpy and ΔH")
        with self.beat("b01") as b:
            d = VGroup(TB("Enthalpy, H", size=BODY + 2, color=UNKNOWN),
                       T("the total chemical energy (heat content) of a system at constant pressure", size=LABEL),
                       T("we can't measure H itself, only changes in it: ΔH", size=LABEL, color=MUTED)).arrange(DOWN, buff=0.15)
            d.move_to([0, 0.6, 0])
            self.play(FadeIn(h), FadeIn(d[0]), run_time=0.6)
            self.play(FadeIn(d[1]), run_time=0.8)
            b.until(0.6)
            self.play(FadeIn(d[2]), run_time=0.6)
            self.d = d

        ax = enthalpy_axis(4.6).move_to([-5.6, -0.1, 0])
        rl = level(3.2, "H₂(g) + Cl₂(g)").move_to([-2.4, 1.4, 0])
        pl = level(3.2, "2HCl(g)").move_to([-2.4, -1.5, 0])
        rl.label.next_to(rl.line, UP, buff=0.12)
        pl.label.next_to(pl.line, DOWN, buff=0.12)
        with self.beat("b02") as b:
            self.play(FadeOut(self.d), run_time=0.4)
            self.play(FadeIn(ax), run_time=0.5)
            self.play(Create(rl.line), FadeIn(rl.label), run_time=0.7)
            f = M(r"\Delta H = H_{\text{products}} - H_{\text{reactants}}", size=EQ_SMALL).move_to([3.2, 2.0, 0])
            self.play(Write(f), run_time=1.0)
            b.until(0.6)
            self.play(Create(pl.line), FadeIn(pl.label), run_time=0.7)
            self.f = f

        arr = dH_arrow(1.4, -1.5, -0.45, "ΔH = −183 kJ", color=UNKNOWN, side=LEFT)
        with self.beat("b03") as b:
            self.play(GrowArrow(arr[0]), FadeIn(arr[1]), run_time=1.0)
            out = VGroup(T("products lower  →  ΔH negative", size=LABEL),
                         wrapped("energy transferred out of the system: exothermic", size=LABEL, width=6.0, color=SYSTEM),
                         T("ΔH positive: products higher, endothermic", size=LABEL, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            out.move_to([0, 0.3, 0]).align_to([0.3, 0, 0], LEFT)
            b.until(0.3)
            self.play(FadeIn(out[0]), run_time=0.6)
            self.play(FadeIn(out[1]), run_time=0.6)
            b.until(0.75)
            self.play(FadeIn(out[2]), run_time=0.6)
            self.out = out

        with self.beat("b04") as b:
            self.play(FadeOut(self.out), FadeOut(self.f), run_time=0.4)
            c1 = right_panel("Signed, describes the system", [M(r"\Delta H = -183\ \text{kJ}", size=EQ_SMALL, color=TEXT)], width=4.3)
            c2 = right_panel("Positive amount released", [T("183 kJ of energy is released", size=LABEL)], width=4.3)
            c3 = wrong_panel("Double negative", [T("“−183 kJ released”", size=LABEL)], note="would mean energy absorbed", width=4.3)
            cs = VGroup(c1, c2, c3).arrange(DOWN, buff=0.22).move_to([3.4, 0.05, 0])
            self.play(FadeIn(c1), run_time=0.7)
            b.until(0.4)
            self.play(FadeIn(c2), run_time=0.7)
            b.until(0.7)
            self.play(FadeIn(c3), run_time=0.7)

        with self.beat("b05") as b:
            self.clear(h)
            new_h = header("Checkpoint")
            sa = VGroup(TB("Student A", size=LABEL, color=MUTED), M(r"\Delta H = -50\ \text{kJ}", size=EQ))
            sb = VGroup(TB("Student B", size=LABEL, color=MUTED), T("50 kJ of energy is released", size=BODY))
            for s_ in (sa, sb):
                s_.arrange(DOWN, buff=0.25)
            VGroup(sa, sb).arrange(RIGHT, buff=1.6).move_to([0, 0.9, 0])
            q = T("Same reaction?", size=BODY, color=UNKNOWN).move_to([0, -0.6, 0])
            self.play(ReplacementTransform(h, new_h), FadeIn(sa), run_time=0.7)
            self.play(FadeIn(sb), run_time=0.7)
            self.play(FadeIn(q), run_time=0.5)
            self.q = q

        with self.beat("b06") as b:
            a = VGroup(TB("Yes.", size=BODY, color=GOOD),
                       T("Both: exothermic; 50 kJ leaves the system.", size=LABEL + 2),
                       T("A uses a signed enthalpy change; B uses the positive size of the energy released.", size=LABEL)).arrange(DOWN, buff=0.18)
            a.next_to(self.q, DOWN, buff=0.35)
            self.play(FadeIn(a[0]), FadeIn(a[1]), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(a[2]), run_time=0.7)


# =====================================================================================
class E02S07_Q04(NarratedScene):
    def construct(self):
        h = header("Practice Q04")
        card = question_card("Q04").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(card, shift=0.1 * UP), run_time=1.0)

        cal = calorimeter(width=3.0, height=2.6, system=True).move_to([-4.3, 0.2, 0])
        cal.thermo.level.set_value(0.6)
        inA = flow_arrows(cal.system.get_center(), 0.55, 1.05, inward=True, color=SURR, stroke=5)
        lab = wrapped("endothermic: energy into the system", size=LABEL, width=4.8, color=SURR).next_to(cal, DOWN, buff=0.3)
        with self.beat("b02") as b:
            self.play(FadeOut(card), FadeIn(cal), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(a) for a in inA], lag_ratio=0.15), run_time=1.0)
            self.play(FadeIn(lab), run_time=0.5)

        with self.beat("b03") as b:
            la = TB("a.", size=LABEL + 2, color=SYSTEM).move_to([-1.3, 1.9, 0])
            l1 = M(r"q_{\text{system}} = +18.0\ \text{kJ mol}^{-1} \times 0.0250\ \text{mol}", size=EQ_SMALL - 4)
            l2 = M(r"= +0.450\ \text{kJ}", size=EQ_SMALL - 2, color=SYSTEM)
            g = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(la, RIGHT, buff=0.25, aligned_edge=UP)
            self.play(FadeIn(la), Write(l1), run_time=1.2)
            b.until(0.55)
            self.play(Write(l2), run_time=0.8)
            why = T("positive: the system gains energy", size=LABEL, color=MUTED).next_to(l2, RIGHT, buff=0.4)
            self.play(FadeIn(why), run_time=0.5)

        with self.beat("b04") as b:
            lb = TB("b.", size=LABEL + 2, color=SYSTEM).move_to([-1.3, 0.2, 0])
            l3 = M(r"q_{\text{calorimeter}} = -0.450\ \text{kJ}", size=EQ_SMALL - 2, color=SURR)
            l3.next_to(lb, RIGHT, buff=0.25)
            self.play(FadeIn(lb), Write(l3), run_time=1.0)
            lc = TB("c.", size=LABEL + 2, color=SYSTEM).move_to([-1.3, -1.0, 0])
            l4 = T("the temperature falls", size=BODY, color=SURR).next_to(lc, RIGHT, buff=0.25)
            b.until(0.5)
            self.play(FadeIn(lc), FadeIn(l4), cal.thermo.level.animate.set_value(0.3), run_time=1.4)

        with self.beat("b05") as b:
            self.clear(h)
            tally = mark_tally([(1, "a. q(system) = +0.450 kJ"), (1, "b. q(calorimeter) = −0.450 kJ"),
                                (1, "c. temperature falls")], width=5.6).move_to([-3.3, 0.4, 0])
            w = wrong_panel("Same sign on both sides", [T("q(system) = q(cal) = +0.450 kJ", size=LABEL)],
                            note="Ask: who gains energy, who loses it?", width=5.2).move_to([3.4, 0.4, 0])
            self.play(FadeIn(tally), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(w), run_time=0.8)

        with self.beat("b06") as b:
            self.clear(h)
            t1 = TB("Endothermic does not mean energy disappears", size=BODY, color=UNKNOWN).move_to([0, 1.4, 0])
            t2 = T("Every kilojoule the system absorbs comes from the surroundings.", size=LABEL + 2).move_to([0, 0.5, 0])
            t3 = VGroup(T("Twice the solute:", size=LABEL + 2), M(r"0.900\ \text{kJ}", size=EQ_SMALL - 2),
                        T("transferred, about twice the temperature drop (same calorimeter)", size=LABEL)).arrange(RIGHT, buff=0.2)
            t3.move_to([0, -0.7, 0])
            self.play(Write(t1), run_time=1.0)
            self.play(FadeIn(t2), run_time=0.8)
            b.until(0.6)
            self.play(FadeIn(t3), run_time=0.8)


# =====================================================================================
class E02S08_Oxygen(NarratedScene):
    def construct(self):
        h = header("Oxygen counts too")
        eq = M(r"\ce{CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)}", size=EQ).move_to([0, 2.20, 0])
        led = ledger([("4 × C–H", ""), ("2 × O=O", "")], [("2 × C=O", ""), ("4 × O–H", "")],
                     "energy in", "energy out", width=5.0).move_to([0, 0.05, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(eq), run_time=1.0)
            self.play(FadeIn(led.left.box), FadeIn(led.left.head), FadeIn(led.left.rows[0]), run_time=0.8)
            self.play(FadeIn(led.left.rows[1]), run_time=0.6)
            ox = SurroundingRectangle(led.left.rows[1], color=UNKNOWN, buff=0.08)
            oxl = T("don't forget oxygen", size=SMALL, color=UNKNOWN).next_to(led.left, DOWN, buff=0.12)
            self.play(Create(ox), FadeIn(oxl), run_time=0.6)
            b.until(0.6)
            self.play(FadeIn(led.right.box), FadeIn(led.right.head), FadeIn(led.right.rows), run_time=0.8)
            self.play(FadeIn(led.left.line), FadeIn(led.left.total), FadeIn(led.right.line), FadeIn(led.right.total), run_time=0.6)
            self.extra = VGroup(ox, oxl)

        with self.beat("b02") as b:
            hl = SurroundingRectangle(led.right.rows, color=USEFUL, buff=0.1)
            t = T("very strong bonds in CO₂ and H₂O: forming them releases a lot of energy", size=LABEL, color=USEFUL)
            t.move_to([0, -2.3, 0])
            self.play(Create(hl), FadeIn(t), run_time=1.0)
            self.extra.add(hl, t)

        ms = VGroup(mol_CH4(1.0), mol_CH3OH(1.0), mol_CO2(1.0)).arrange(RIGHT, buff=2.4).move_to([0, 1.25, 0])
        names = VGroup(*[T(n, size=LABEL) for n in ["methane, CH₄", "methanol, CH₃OH", "carbon dioxide, CO₂"]])
        oxn = VGroup(*[T(n, size=LABEL, color=UNKNOWN) for n in ["C: −4", "C: −2", "C: +4"]])
        for n_, o_, m_ in zip(names, oxn, ms):
            n_.next_to(m_, DOWN, buff=0.3)
            o_.next_to(n_, DOWN, buff=0.12)
        more = Arrow([-4.5, 2.08, 0], [4.5, 2.08, 0], buff=0, color=SYSTEM, stroke_width=4)
        more_t = T("more oxidised  →", size=SMALL + 1, color=SYSTEM).next_to(more, UP, buff=0.08)
        with self.beat("b03") as b:
            self.play(FadeOut(led), FadeOut(self.extra), FadeOut(eq), run_time=0.6)
            self.play(GrowArrow(more), FadeIn(more_t), run_time=0.6)
            for i in range(3):
                self.play(FadeIn(ms[i]), FadeIn(names[i]), run_time=0.6)
            b.until(0.62)
            self.play(LaggedStart(*[FadeIn(o) for o in oxn], lag_ratio=0.3), run_time=1.2)
            done = T("cannot burn further", size=SMALL, color=MUTED).next_to(oxn[2], DOWN, buff=0.1)
            self.play(FadeIn(done), run_time=0.4)

        with self.beat("b04") as b:
            data = VGroup(M(r"\Delta H_c(\ce{CH4}) = -890\ \text{kJ mol}^{-1}", size=EQ_SMALL - 4),
                          M(r"\Delta H_c(\ce{CH3OH}) = -726\ \text{kJ mol}^{-1}", size=EQ_SMALL - 4)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            note = T("one carbon each; products CO₂ and liquid water", size=SMALL, color=MUTED)
            dg = VGroup(data, note).arrange(DOWN, buff=0.15)
            db = panel(dg)
            VGroup(db, dg).move_to([-3.4, -1.5, 0])
            b.until(0.45)
            self.play(FadeIn(db), FadeIn(dg), run_time=0.9)

        with self.beat("b05") as b:
            caut = VGroup(TB("Qualitative idea, not a shortcut", size=LABEL, color=UNKNOWN),
                          wrapped("Exact comparisons need the full balanced equation, the product states, and one "
                                  "basis (per mol or per g).", size=SMALL + 1, width=5.3)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            cb = panel(caut, color=UNKNOWN)
            VGroup(cb, caut).move_to([3.4, -1.5, 0])
            self.play(FadeIn(cb), FadeIn(caut), run_time=0.9)


# =====================================================================================
class E02S09_Recap(NarratedScene):
    def construct(self):
        h = header("Recap")
        cards = [("System and surroundings", "reacting chemicals | everything else", SYSTEM),
                 ("Heat vs temperature", "energy transferred | how hot", "#F1948A"),
                 ("Bonds", "breaking absorbs | making releases", USEFUL),
                 ("ΔH = H(products) − H(reactants)", "negative: energy released", UNKNOWN)]
        grid = VGroup()
        for t, s, c in cards:
            body = VGroup(TB(t, size=LABEL + 2, color=c), T(s, size=LABEL)).arrange(DOWN, buff=0.15)
            r = RoundedRectangle(width=6.0, height=1.5, corner_radius=0.15, stroke_color=c, stroke_width=2.5,
                                 fill_color=PANEL, fill_opacity=0.95)
            grid.add(VGroup(r, body.move_to(r)))
        grid.arrange_in_grid(2, 2, buff=0.35).move_to([0, 0.3, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for i, c in enumerate(grid):
                b.until(0.05 + 0.22 * i)
                self.play(FadeIn(c, shift=0.1 * UP), run_time=0.6)

        with self.beat("b02") as b:
            self.play(FadeOut(grid), run_time=0.5)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN),
                       T("Why does burning a fuel release energy?", size=BODY),
                       T("Use the words “broken” and “formed”.", size=LABEL + 2, color=MUTED)).arrange(DOWN, buff=0.3)
            q.move_to([0, 1.0, 0])
            self.play(FadeIn(q), run_time=0.8)
            self.q = q

        with self.beat("b03") as b:
            a = right_panel("A strong answer", [
                "More energy is released when the bonds in the products are formed than is absorbed when the "
                "bonds in the reactants are broken."], width=10.5)
            a.next_to(self.q, DOWN, buff=0.4)
            self.play(FadeIn(a), run_time=0.8)
            b.until(0.6)
            nxt = T("Next: Episode 03 · Energy profiles and thermochemical equations", size=LABEL, color=MUTED).move_to([0, -2.35, 0])
            self.play(FadeIn(nxt), run_time=0.6)


EPISODE_SCENES = ["E02S01_Retrieval", "E02S02_System", "E02S03_ExoEndo", "E02S04_Bonds", "E02S05_Q03",
                  "E02S06_Enthalpy", "E02S07_Q04", "E02S08_Oxygen", "E02S09_Recap"]
