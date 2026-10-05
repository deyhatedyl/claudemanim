"""
Episode 04 - Fuels, biofuels and the carbon cycle.
Narration: scripts/ep04.md (beat names must match).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (atom, bullets, flask, mark_tally, mol_C2H5OH, mol_CH4, mol_CO2, molecule,  # noqa: E402
                               question_card, result_box, right_panel, table, title_card, wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (BAD, BG, BODY, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, MASS_C, MOL_C, MUTED,  # noqa: E402
                          PANEL, SMALL, SURR, SYSTEM, TEXT, UNKNOWN, USEFUL, M, T, TB, chip, header, panel)

FOSSIL = "#A1887F"
BIO = "#7BE495"


def requested(text: str) -> VGroup:
    from shared.style import asked_pill
    return asked_pill(text)


def card(title, lines, color, width=3.9):
    t = TB(title, size=LABEL + 2, color=color)
    body = VGroup(*[wrapped(l, size=SMALL + 1, width=width - 0.5) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    g = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    r = RoundedRectangle(width=width, height=g.height + 0.45, corner_radius=0.15, stroke_color=color, stroke_width=2.5,
                         fill_color=PANEL, fill_opacity=0.95).move_to(g)
    g.move_to(r)
    return VGroup(r, g)


# =====================================================================================
class E04S01_Retrieval(NarratedScene):
    def construct(self):
        tc = title_card(4, "Fuels, biofuels and the carbon cycle")
        with self.beat("b01"):
            self.play(FadeIn(tc, shift=0.2 * UP), run_time=1.5)
        with self.beat("b02") as b:
            self.play(FadeOut(tc), run_time=0.5)
            h = header("Retrieval check")
            q1 = T("1.  Does a catalyst change ΔH?", size=BODY)
            q2 = VGroup(T("2.", size=BODY), M(r"2\ce{H2(g)} + \ce{O2(g)} \ce{->} 2\ce{H2O(l)}\quad \Delta H = -572\ \text{kJ}", size=EQ_SMALL - 2))
            q2.arrange(RIGHT, buff=0.3)
            q2b = T("Molar enthalpy of combustion of H₂ = ?", size=BODY)
            qs = VGroup(q1, q2, q2b).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([0, 0.9, 0])
            q2b.shift(0.55 * RIGHT)
            self.play(FadeIn(h), FadeIn(q1), run_time=0.8)
            b.until(0.35)
            self.play(FadeIn(q2), FadeIn(q2b), run_time=0.8)
            self.qs = qs
        with self.beat("b03") as b:
            a1 = T("No: it lowers Ea only", size=BODY, color=GOOD)
            a2 = M(r"-286\ \text{kJ per mol of } \ce{H2}", size=EQ_SMALL, color=GOOD)
            a1.next_to(self.qs[0], RIGHT, buff=0.5)
            a2.next_to(self.qs[2], DOWN, buff=0.3).align_to(self.qs[2], LEFT)
            self.play(FadeIn(a1), run_time=0.6)
            b.until(0.4)
            self.play(Write(a2), run_time=1.0)


# =====================================================================================
class E04S02_Fossil(NarratedScene):
    def construct(self):
        h = header("What counts as a fuel")
        d = VGroup(TB("Fuel", size=BODY, color=UNKNOWN),
                   wrapped("a substance that reacts, usually by combustion with oxygen, to release useful energy, most often as heat",
                           size=LABEL + 2, width=11.5)).arrange(DOWN, buff=0.15)
        d.move_to([0, 2.0, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(d[0]), run_time=0.6)
            self.play(FadeIn(d[1]), run_time=1.0)
        cards = VGroup(card("Coal", ["mostly carbon", "solid"], FOSSIL),
                       card("Natural gas", ["mostly methane, CH₄", "gas"], FOSSIL),
                       card("Petrol", ["mixture of liquid hydrocarbons from crude oil", "e.g. octane, C₈H₁₈"], FOSSIL))
        cards.arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to([0, 0.05, 0])
        with self.beat("b02") as b:
            for i, c in enumerate(cards):
                b.until(0.15 + 0.25 * i)
                self.play(FadeIn(c, shift=0.1 * UP), run_time=0.6)
        with self.beat("b03") as b:
            strip = VGroup(T("ancient organisms", size=LABEL), Arrow(LEFT * 0.6, RIGHT * 0.6, color=FOSSIL, buff=0),
                           T("buried; heat and pressure", size=LABEL), Arrow(LEFT * 0.6, RIGHT * 0.6, color=FOSSIL, buff=0),
                           T("fossil fuel", size=LABEL, color=FOSSIL)).arrange(RIGHT, buff=0.2)
            strip.move_to([0, -1.75, 0])
            tl = T("millions of years  →  used far faster than formed: non-renewable", size=LABEL, color=BAD).move_to([0, -2.4, 0])
            self.play(FadeIn(strip), run_time=1.0)
            b.until(0.55)
            self.play(FadeIn(tl), run_time=0.8)


# =====================================================================================
class E04S03_Timescale(NarratedScene):
    def construct(self):
        h = header("Renewable: replenished on a human timescale")
        base = Line([-6.0, 0, 0], [6.0, 0, 0], color=FAINT)
        long_bar = Rectangle(width=11.6, height=0.45, fill_color=FOSSIL, fill_opacity=0.8, stroke_width=0)
        long_bar.move_to([0.0, 1.9, 0]).align_to([-6.0, 0, 0], LEFT)
        brk = VGroup(Line([3.9, 1.55, 0], [3.7, 2.25, 0], color=BG, stroke_width=10),
                     Line([4.15, 1.55, 0], [3.95, 2.25, 0], color=BG, stroke_width=10))
        long_t = T("fossil fuel formation: millions of years", size=LABEL, color=FOSSIL).next_to(long_bar, UP, buff=0.12).align_to(long_bar, LEFT)
        short_bar = Rectangle(width=0.12, height=0.45, fill_color=BIO, fill_opacity=0.9, stroke_width=0)
        short_bar.move_to([0, 0.7, 0]).align_to([-6.0, 0, 0], LEFT)
        short_t = T("biomass regrowth: months to years", size=LABEL, color=BIO).next_to(short_bar, RIGHT, buff=0.2)
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            self.play(GrowFromEdge(long_bar, LEFT), FadeIn(long_t), run_time=1.2)
            self.play(FadeIn(brk), run_time=0.3)
            b.until(0.35)
            self.play(GrowFromEdge(short_bar, LEFT), FadeIn(short_t), run_time=0.8)
            rule = T("renewable: replenished at least as fast as it is used", size=LABEL + 2, color=UNKNOWN).move_to([0, -0.05, 0])
            b.until(0.7)
            self.play(FadeIn(rule), run_time=0.7)
        bio = VGroup(card("Biogas", ["mainly CH₄ + CO₂", "anaerobic digestion of organic waste"], BIO, 4.0),
                     card("Bioethanol", ["C₂H₅OH", "fermentation of sugars"], BIO, 4.0),
                     card("Biodiesel", ["fatty acid esters", "transesterification of oils and fats"], BIO, 4.0))
        bio.arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to([0, -1.55, 0])
        with self.beat("b02") as b:
            for i, c in enumerate(bio):
                b.until(0.1 + 0.28 * i)
                self.play(FadeIn(c, shift=0.1 * UP), run_time=0.6)
        with self.beat("b03") as b:
            self.clear(h)
            m1, m2 = mol_CH4(1.4), mol_CH4(1.4)
            src1 = card("natural gas reserve", ["formed over millions of years"], FOSSIL, 4.2)
            src2 = card("biogas digester", ["recently grown plant waste"], BIO, 4.2)
            src1.move_to([-3.6, 1.6, 0])
            src2.move_to([3.6, 1.6, 0])
            m1.move_to([-3.6, -0.3, 0])
            m2.move_to([3.6, -0.3, 0])
            eq = TB("=", size=HEAD + 10).move_to([0, -0.3, 0])
            same = T("the same molecule: same energy and same CO₂ per mole burned", size=LABEL + 2, color=UNKNOWN).move_to([0, -1.6, 0])
            diff = T("different origin of the carbon, and how fast it is replaced", size=LABEL, color=MUTED).move_to([0, -2.25, 0])
            self.play(FadeIn(src1), FadeIn(src2), run_time=0.8)
            self.play(FadeIn(m1), FadeIn(m2), run_time=0.6)
            b.until(0.3)
            self.play(FadeIn(eq), FadeIn(same), run_time=0.8)
            b.until(0.7)
            self.play(FadeIn(diff), run_time=0.6)


# =====================================================================================
class E04S04_CarbonCycle(NarratedScene):
    def construct(self):
        h = header("Following the carbon atoms")
        sch = T("schematic", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
        atm = card("Atmosphere", ["carbon dioxide, CO₂"], SURR, 3.6).move_to([-0.5, 1.9, 0])
        plant = card("Plant", ["glucose, C₆H₁₂O₆"], BIO, 3.6).move_to([3.9, 0.15, 0])
        fuel = card("Fuel", ["ethanol, C₂H₅OH"], SYSTEM, 3.6).move_to([-0.5, -1.4, 0])
        a1 = CurvedArrow(atm.get_right() + 0.05 * RIGHT, plant.get_top() + 0.05 * UP, angle=-PI / 3, color=BIO, stroke_width=4)
        a2 = CurvedArrow(plant.get_bottom() + 0.05 * DOWN, fuel.get_right() + 0.05 * RIGHT, angle=-PI / 3, color=SYSTEM, stroke_width=4)
        a3 = CurvedArrow(fuel.get_left() + 0.05 * LEFT, atm.get_left() + 0.05 * LEFT, angle=-PI / 1.6, color=SURR, stroke_width=4)
        l1 = VGroup(T("photosynthesis", size=SMALL + 1, color=BIO), T("light energy in", size=SMALL, color=UNKNOWN)).arrange(DOWN, buff=0.05)
        l1.next_to(a1, UR, buff=-0.2).shift(0.3 * RIGHT)
        l2 = T("fermentation", size=SMALL + 1, color=SYSTEM).next_to(a2, DR, buff=-0.1)
        l3 = VGroup(T("combustion", size=SMALL + 1, color=SURR), T("energy out", size=SMALL, color=USEFUL)).arrange(DOWN, buff=0.05)
        l3.next_to(a3, LEFT, buff=0.1)
        cs = VGroup(*[atom("C", 0.9) for _ in range(3)])
        cs.arrange(RIGHT, buff=0.12).next_to(atm, DOWN, buff=0.08)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(sch), FadeIn(atm), FadeIn(cs), run_time=0.8)
            b.until(0.35)
            self.play(Create(a1), FadeIn(l1), FadeIn(plant), run_time=1.0)
            self.play(cs.animate(path_arc=-PI / 3).next_to(plant, DOWN, buff=0.08), run_time=1.8)
        with self.beat("b02") as b:
            self.play(Create(a2), FadeIn(l2), FadeIn(fuel), run_time=1.0)
            self.play(cs[:2].animate(path_arc=-PI / 3).next_to(fuel, DOWN, buff=0.08), run_time=1.6)
            fco2 = T("one C leaves as CO₂", size=SMALL, color=MUTED).next_to(plant, LEFT, buff=0.25).shift(0.6 * DOWN)
            self.play(cs[2].animate(path_arc=PI / 3).next_to(atm, DOWN, buff=0.08).shift(0.8 * RIGHT), FadeIn(fco2), run_time=1.6)
            self.fco2 = fco2
        with self.beat("b03") as b:
            self.play(Create(a3), FadeIn(l3), run_time=1.0)
            self.play(cs[:2].animate(path_arc=-PI / 1.6).next_to(atm, DOWN, buff=0.08).shift(0.35 * LEFT), run_time=1.8)
            loop = T("recycled over months or years", size=LABEL, color=BIO).move_to([-0.5, 0.05, 0])
            b.until(0.6)
            self.play(FadeIn(loop), run_time=0.6)
        with self.beat("b04") as b:
            fos = card("Fossil carbon", ["stored underground for millions of years"], FOSSIL, 3.4).move_to([-4.9, -0.7, 0])
            fa = Arrow(fos.get_top(), atm.get_left() + 0.3 * DOWN, buff=0.1, color=FOSSIL, stroke_width=5)
            ft = T("adds extra CO₂", size=SMALL + 1, color=FOSSIL).move_to([-4.9, 0.95, 0])
            extra = VGroup(*[atom("C", 0.9) for _ in range(3)]).arrange(RIGHT, buff=0.12).next_to(fos, DOWN, buff=0.08)
            self.play(FadeOut(l3), FadeIn(fos), FadeIn(extra), run_time=0.8)
            self.fossil = VGroup(fos, extra)
            self.play(GrowArrow(fa), FadeIn(ft), run_time=0.8)
            self.fossil.add(fa, ft)
            self.play(extra.animate(path_arc=PI / 6).next_to(atm, LEFT, buff=0.15), run_time=1.8)
        with self.beat("b05") as b:
            warn = wrapped("Not automatically carbon neutral: farming, processing and transport can use fossil energy.",
                           size=SMALL + 1, width=3.6, color=UNKNOWN)
            wb = panel(warn, color=UNKNOWN)
            VGroup(wb, warn).move_to([-4.9, -0.6, 0])
            self.play(FadeOut(self.fossil), run_time=0.5)
            self.play(FadeIn(wb), FadeIn(warn), run_time=0.8)


# =====================================================================================
class E04S05_Photosynthesis(NarratedScene):
    def construct(self):
        h = header("Photosynthesis and respiration")
        ph = M(r"6\ce{CO2(g)} + 6\ce{H2O(l)} \ce{->} \ce{C6H12O6(aq)} + 6\ce{O2(g)}", size=EQ_SMALL).move_to([0, 2.25, 0])
        cnt = T("each side: 6 C, 12 H, 18 O", size=LABEL, color=MUTED).next_to(ph, DOWN, buff=0.15)
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(ph), run_time=1.4)
            b.until(0.5)
            self.play(FadeIn(cnt), run_time=0.6)
        lo = Line([-5.6, -1.6, 0], [-2.6, -1.6, 0], color=TEXT, stroke_width=5)
        hi = Line([-5.6, 0.7, 0], [-2.6, 0.7, 0], color=TEXT, stroke_width=5)
        lo_t = T("6CO₂ + 6H₂O", size=LABEL).next_to(lo, DOWN, buff=0.1)
        hi_t = T("C₆H₁₂O₆ + 6O₂", size=LABEL).next_to(hi, UP, buff=0.1)
        up = Arrow([-4.1, -1.55, 0], [-4.1, 0.65, 0], buff=0, color=UNKNOWN, stroke_width=5)
        sun = VGroup(Circle(radius=0.35, color=UNKNOWN, fill_color=UNKNOWN, fill_opacity=0.9),
                     *[Line(ORIGIN, 0.25 * RIGHT, color=UNKNOWN, stroke_width=3).shift(0.48 * RIGHT).rotate(k * PI / 4, about_point=ORIGIN)
                       for k in range(8)]).move_to([-1.2, 0.0, 0])
        ray = Arrow(sun.get_left(), [-3.9, -0.45, 0], buff=0.1, color=UNKNOWN, stroke_width=4)
        with self.beat("b02") as b:
            self.play(Create(lo), FadeIn(lo_t), Create(hi), FadeIn(hi_t), run_time=1.0)
            self.play(GrowArrow(up), run_time=0.8)
            b.until(0.4)
            self.play(FadeIn(sun), GrowArrow(ray), run_time=0.8)
            lab = VGroup(T("endothermic", size=LABEL, color=UNKNOWN), T("light energy → chemical energy", size=LABEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            lab.move_to([2.6, 0.2, 0]).align_to([0.2, 0, 0], LEFT)
            b.until(0.65)
            self.play(FadeIn(lab), run_time=0.7)
            self.lab = lab
        with self.beat("b03") as b:
            rs = M(r"\ce{C6H12O6(aq)} + 6\ce{O2(g)} \ce{->} 6\ce{CO2(g)} + 6\ce{H2O(l)}", size=EQ_SMALL - 4, color=USEFUL)
            rs.scale_to_fit_width(6.5).move_to([3.2, -0.95, 0])
            e = T("releases ≈ 2.8 × 10³ kJ per mol of glucose", size=LABEL, color=USEFUL).next_to(rs, DOWN, buff=0.2)
            why = T("because strong bonds form in CO₂ and H₂O", size=SMALL + 1, color=MUTED).next_to(e, DOWN, buff=0.12)
            self.play(Write(rs), run_time=1.2)
            self.play(FadeIn(e), run_time=0.6)
            b.until(0.65)
            self.play(FadeIn(why), run_time=0.6)


# =====================================================================================
def glucose_layout(s=1.0):
    """Schematic open-chain glucose: returns dict of named atoms and list of bonds."""
    A = {}
    xs = [-2.75, -1.65, -0.55, 0.55, 1.65, 2.75]
    for i, x in enumerate(xs, 1):
        A[f"C{i}"] = atom("C", s).move_to([x * s, 0, 0])
        A[f"H{i}"] = atom("H", s).move_to([x * s, -0.62 * s, 0])
        A[f"O{i}"] = atom("O", s).move_to([x * s, 0.66 * s, 0])
        if i > 1:
            A[f"HO{i}"] = atom("H", s).move_to([x * s + 0.42 * s, 1.0 * s, 0])
    A["H6b"] = atom("H", s).move_to([(xs[5] + 0.62) * s, 0, 0])
    bonds = []
    for i in range(1, 6):
        bonds.append((f"C{i}", f"C{i+1}", 1))
    for i in range(1, 7):
        bonds.append((f"C{i}", f"H{i}", 1))
        bonds.append((f"C{i}", f"O{i}", 2 if i == 1 else 1))
        if i > 1:
            bonds.append((f"O{i}", f"HO{i}", 1))
    bonds.append(("C6", "H6b", 1))
    return A, bonds


def bond_lines(A, bonds, s=1.0):
    g = VGroup()
    for a, b_, order in bonds:
        p, q = A[a].get_center(), A[b_].get_center()
        d = q - p
        n = np.array([-d[1], d[0], 0])
        n = n / (np.linalg.norm(n) + 1e-9) * 0.06 * s
        for o in ([0] if order == 1 else [-1, 1]):
            g.add(Line(p + n * o, q + n * o, color="#C8D0DA", stroke_width=3.5 * s))
    return g


class E04S06_Ethanol(NarratedScene):
    def construct(self):
        h = header("Making bioethanol")
        eq = M(r"\ce{C6H12O6(aq)} \ce{->} 2\ce{C2H5OH(aq)} + 2\ce{CO2(g)}", size=EQ_SMALL).move_to([0, 2.45, 0])
        s = 0.95
        A, bonds = glucose_layout(s)
        gl = VGroup(*A.values()).move_to([0, 0.75, 0])
        bl = bond_lines(A, bonds, s)
        glab = T("glucose (schematic)", size=SMALL + 1, color=MUTED).next_to(gl, DOWN, buff=0.18)
        # product templates
        eA, eB = mol_C2H5OH(s), mol_C2H5OH(s)
        cA, cB = mol_CO2(s), mol_CO2(s)
        eA.move_to([-4.3, -1.4, 0])
        cA.move_to([-1.35, -1.4, 0])
        cB.move_to([1.35, -1.4, 0])
        eB.move_to([4.3, -1.4, 0])
        # ethanol atom order: C, C, O, H(on O), H, H, H, H, H ; CO2: O, C, O
        mapping = [("C1", eA, 0), ("C2", eA, 1), ("O2", eA, 2), ("HO2", eA, 3), ("H1", eA, 4), ("H2", eA, 5),
                   ("H3", eA, 6), ("HO3", eA, 7), ("H4", eA, 8),
                   ("C3", cA, 1), ("O1", cA, 0), ("O3", cA, 2),
                   ("C4", cB, 1), ("O4", cB, 0), ("O5", cB, 2),
                   ("C5", eB, 0), ("C6", eB, 1), ("O6", eB, 2), ("HO6", eB, 3), ("HO4", eB, 4), ("H5", eB, 5),
                   ("HO5", eB, 6), ("H6", eB, 7), ("H6b", eB, 8)]
        assert len(mapping) == 24 and len({m[0] for m in mapping}) == 24
        counts = T("C 6   H 12   O 6", size=LABEL, color=MUTED)
        cl = counts.copy().move_to([-5.4, 0.75, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(eq), run_time=1.0)
            self.play(FadeIn(gl), Create(bl), FadeIn(glab), FadeIn(cl), run_time=1.0)
            b.until(0.4)
            self.play(FadeOut(bl), FadeOut(glab), run_time=0.5)
            self.play(*[A[k].animate.move_to(mol.atoms[i].get_center()) for k, mol, i in mapping], run_time=2.0)
            self.play(FadeIn(eA.bonds), FadeIn(eB.bonds), FadeIn(cA.bonds), FadeIn(cB.bonds), run_time=0.6)
            names = VGroup(*[T(n, size=SMALL, color=MUTED).next_to(m, DOWN, buff=0.12)
                             for n, m in [("ethanol", eA), ("CO₂", cA), ("CO₂", cB), ("ethanol", eB)]])
            cr = counts.copy().move_to([0, -2.45, 0])
            self.play(FadeIn(names), FadeIn(cr), run_time=0.6)
            self.prod = VGroup(*A.values(), eA.bonds, eB.bonds, cA.bonds, cB.bonds, names, cr, cl)
        with self.beat("b02") as b:
            self.play(FadeOut(self.prod), run_time=0.6)
            cond = VGroup(TB("Conditions", size=LABEL + 2, color=SYSTEM),
                          T("enzymes from yeast (biological catalysts)", size=LABEL),
                          T("no oxygen (anaerobic)", size=LABEL),
                          T("warm: about 30–35 °C", size=LABEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            cond.move_to([-3.2, 0.6, 0])
            self.play(FadeIn(cond[0]), FadeIn(cond[1]), run_time=0.7)
            self.play(FadeIn(cond[2]), FadeIn(cond[3]), run_time=0.7)
            hot = VGroup(TB("Too hot?", size=LABEL + 2, color=BAD),
                         wrapped("the enzyme's shape is permanently changed (denatured), so fermentation slows or stops",
                                 size=LABEL, width=5.4)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            hot.move_to([3.3, 0.6, 0])
            b.until(0.5)
            self.play(FadeIn(hot), run_time=0.9)
            self.cond = VGroup(cond, hot)
        with self.beat("b03") as b:
            note = T("product: a dilute solution, about 10–15% ethanol", size=LABEL + 2, color=UNKNOWN).move_to([0, -1.2, 0])
            self.play(FadeIn(note), run_time=0.8)
            nxt = T("→ separate and concentrate by distillation", size=LABEL + 2).move_to([0, -1.9, 0])
            b.until(0.6)
            self.play(FadeIn(nxt), run_time=0.6)
        with self.beat("b04") as b:
            self.clear(h)
            sch = T("schematic", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
            rb = VGroup(Circle(radius=0.85, color=TEXT, stroke_width=3),
                        Rectangle(width=0.36, height=1.1, color=TEXT, stroke_width=3))
            rb[1].next_to(rb[0], UP, buff=-0.1)
            liq = Circle(radius=0.8, stroke_width=0, fill_color=SURR, fill_opacity=0.35).move_to(rb[0]).shift(0.0 * DOWN)
            liq = Intersection(liq, Rectangle(width=2, height=0.9).move_to(rb[0].get_center() + 0.42 * DOWN),
                               stroke_width=0, fill_color=SURR, fill_opacity=0.45)
            flame = Polygon([-0.25, 0, 0], [0.25, 0, 0], [0, 0.55, 0], stroke_width=0, fill_color=SYSTEM, fill_opacity=0.9)
            still = VGroup(rb, liq).move_to([-4.6, 0.15, 0])
            flame.next_to(rb[0], DOWN, buff=0.12)
            top = rb[1].get_top()
            cond_outer = Polygon(top + [0.2, -0.1, 0], top + [3.6, -1.1, 0], top + [3.6, -1.6, 0], top + [0.2, -0.6, 0],
                                 color=SURR, stroke_width=2.5, fill_color=SURR, fill_opacity=0.12)
            tube = Line(top + [0.0, -0.3, 0], top + [4.1, -1.5, 0], color=TEXT, stroke_width=3)
            recv = flask(width=1.4, height=1.6, liquid=SYSTEM, level=0.25).move_to(top + [4.3, -2.45, 0])
            win = T("cooling water", size=SMALL, color=SURR).move_to([-2.8, 1.55, 0])
            l_mix = wrapped("fermented mixture (about 10–15% ethanol)", size=SMALL + 1, width=4.2)
            l_mix.next_to(flame, DOWN, buff=0.15)
            l_vap = wrapped("vapour richer in ethanol (boils at 78 °C; water 100 °C)", size=SMALL + 1, width=3.4, color=UNKNOWN)
            l_vap.move_to([0.4, 2.08, 0])
            l_dist = wrapped("distillate: much more concentrated, but at most about 95% ethanol, not pure", size=SMALL + 1,
                             width=3.6, color=SYSTEM).next_to(recv, RIGHT, buff=0.25)
            self.play(FadeIn(sch), FadeIn(still), FadeIn(flame), FadeIn(l_mix), run_time=1.0)
            b.until(0.25)
            self.play(Create(tube), FadeIn(cond_outer), FadeIn(win), FadeIn(l_vap), run_time=1.2)
            b.until(0.55)
            self.play(FadeIn(recv), run_time=0.6)
            b.until(0.7)
            self.play(FadeIn(l_dist), run_time=0.8)


# =====================================================================================
class E04S07_Q07(NarratedScene):
    def construct(self):
        h = header("Practice Q07")
        qc = question_card("Q07").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        eq = M(r"\ce{C6H12O6(aq)} \ce{->} 2\ce{C2H5OH(aq)} + 2\ce{CO2(g)}", size=EQ_SMALL).move_to([0, 2.35, 0])
        ratio = T("1 : 2 : 2", size=LABEL + 2, color=MOL_C).next_to(eq, DOWN, buff=0.12)
        req = requested("masses (g)")
        with self.beat("b02") as b:
            self.play(FadeOut(qc), Write(eq), FadeIn(req), run_time=1.2)
            b.until(0.55)
            self.play(FadeIn(ratio), run_time=0.6)
        with self.beat("b03") as b:
            pred = VGroup(TB("Predict first", size=LABEL + 2, color=UNKNOWN),
                          T("270 g ÷ 180 g mol⁻¹ ≈ 1.5 mol glucose", size=LABEL),
                          T("→ at most 3 mol ethanol ≈ 140 g; yield < 100% → a bit over 100 g", size=LABEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            pb = panel(pred, color=UNKNOWN)
            pg = VGroup(pb, pred).move_to([0, 0.55, 0])
            self.play(FadeIn(pb), FadeIn(pred[0]), FadeIn(pred[1]), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(pred[2]), run_time=0.8)
            self.pg = pg
        chain_y = 0.05
        boxes = VGroup(
            VGroup(TB("glucose", size=SMALL + 1, color=MUTED), M(r"1.50\ \text{mol}", size=EQ_SMALL - 6, color=MOL_C)).arrange(DOWN, buff=0.1),
            VGroup(TB("theoretical", size=SMALL + 1, color=MUTED), M(r"3.00\ \text{mol}", size=EQ_SMALL - 6, color=MOL_C)).arrange(DOWN, buff=0.1),
            VGroup(TB("actual (78.0%)", size=SMALL + 1, color=MUTED), M(r"2.34\ \text{mol}", size=EQ_SMALL - 6, color=MOL_C)).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=2.1).move_to([0, chain_y, 0])
        arrs = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.15, color=TEXT, stroke_width=3),
                      Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.15, color=TEXT, stroke_width=3))
        al = VGroup(T("× 2", size=SMALL + 1, color=MOL_C).next_to(arrs[0], UP, buff=0.05),
                    T("× 0.780", size=SMALL + 1, color=UNKNOWN).next_to(arrs[1], UP, buff=0.05))
        with self.beat("b04") as b:
            self.play(FadeOut(self.pg), run_time=0.4)
            c1 = M(r"n(\text{glucose}) = \frac{270.0\ \text{g}}{180.0\ \text{g mol}^{-1}} = 1.50\ \text{mol}", size=EQ_SMALL - 4).move_to([0, 1.1, 0])
            self.play(Write(c1), run_time=1.2)
            self.play(FadeIn(boxes[0]), run_time=0.5)
            b.until(0.55)
            self.play(GrowArrow(arrs[0]), FadeIn(al[0]), FadeIn(boxes[1]), run_time=0.9)
            note = T("ethanol and CO₂ each", size=SMALL, color=MUTED).next_to(boxes[1], DOWN, buff=0.1)
            self.play(FadeIn(note), run_time=0.4)
            self.c1 = VGroup(c1, note)
        with self.beat("b05") as b:
            self.play(GrowArrow(arrs[1]), FadeIn(al[1]), FadeIn(boxes[2]), run_time=1.0)
        with self.beat("b06") as b:
            m1 = M(r"m(\text{ethanol}) = 2.34 \times 46.0 = 107.64\ \text{g} \approx 108\ \text{g}", size=EQ_SMALL - 4, color=MASS_C)
            m2 = M(r"m(\ce{CO2}) = 2.34 \times 44.0 = 102.96\ \text{g} \approx 103\ \text{g}", size=EQ_SMALL - 4, color=MASS_C)
            VGroup(m1, m2).arrange(DOWN, buff=0.3).move_to([0, -1.5, 0])
            self.play(Write(m1), run_time=1.2)
            b.until(0.45)
            self.play(Write(m2), run_time=1.2)
            chk = T("✓ a bit over 100 g, as predicted", size=SMALL + 1, color=GOOD).next_to(m2, DOWN, buff=0.15)
            b.until(0.8)
            self.play(FadeIn(chk), run_time=0.5)
        with self.beat("b07") as b:
            self.clear(h, req, eq, ratio)
            ans = right_panel("c. Full-credit style", [
                "Distillation separates and concentrates the ethanol from the aqueous fermentation mixture, using the "
                "difference in volatility (boiling point) of ethanol and water."], width=11.0)
            ans.move_to([0, 0.4, 0])
            self.play(FadeIn(ans), run_time=1.0)
            self.ans = ans
        with self.beat("b08") as b:
            self.play(FadeOut(self.ans), FadeOut(eq), FadeOut(ratio), run_time=0.4)
            tally = mark_tally([(1, "equation with states"), (1, "1 : 2 ratio → 3.00 mol"), (1, "yield applied once → 2.34 mol"),
                                (2, "masses: 108 g ethanol, 103 g CO₂"), (1, "distillation separates/concentrates")],
                               width=6.0, size=SMALL + 1).move_to([-3.3, 0.2, 0])
            ws = VGroup(wrong_panel("1 : 1 ratio", [T("halves the answer: ≈ 54 g", size=SMALL + 1)], width=4.4, size=SMALL + 1),
                        wrong_panel("Yield applied twice", [T("0.780 × 0.780 × …", size=SMALL + 1)], width=4.4, size=SMALL + 1),
                        wrong_panel("Distillation 'makes' ethanol", [T("it separates; fermentation makes", size=SMALL + 1)], width=4.4, size=SMALL + 1))
            ws.arrange(DOWN, buff=0.18).move_to([3.5, 0.2, 0])
            self.play(FadeIn(tally), run_time=0.8)
            for i, w in enumerate(ws):
                b.until(0.45 + 0.15 * i)
                self.play(FadeIn(w), run_time=0.5)


# =====================================================================================
class E04S08_BiogasBiodiesel(NarratedScene):
    def construct(self):
        h = header("Biogas and biodiesel")
        sch = T("schematic", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
        tank = RoundedRectangle(width=3.4, height=2.2, corner_radius=0.3, color=BIO, stroke_width=3,
                                fill_color=PANEL, fill_opacity=1).move_to([-2.0, 0.2, 0])
        sludge = Rectangle(width=3.2, height=1.1, stroke_width=0, fill_color="#6E5B3E", fill_opacity=0.8).move_to(tank.get_center() + 0.45 * DOWN)
        win = Arrow([-6.3, 0.0, 0], tank.get_left() + 0.0 * UP, buff=0.05, color=TEXT, stroke_width=4)
        win_t = wrapped("organic waste: manure, food scraps, sewage", size=SMALL + 1, width=2.6).next_to(win, UP, buff=0.1)
        gout = Arrow(tank.get_top(), tank.get_top() + 1.0 * UP, buff=0.05, color=UNKNOWN, stroke_width=4)
        gout_t = T("biogas: mainly CH₄ + CO₂", size=LABEL, color=UNKNOWN).next_to(gout, RIGHT, buff=0.15)
        dout = Arrow(tank.get_right() + 0.6 * DOWN, tank.get_right() + 0.6 * DOWN + 1.2 * RIGHT, buff=0.05, color=FOSSIL, stroke_width=4)
        dout_t = T("digestate (fertiliser)", size=SMALL + 1, color=FOSSIL).next_to(dout, RIGHT, buff=0.1)
        cond = T("no oxygen · microbes · days to weeks", size=LABEL, color=BIO).next_to(tank, DOWN, buff=0.3)
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(sch), FadeIn(tank), FadeIn(sludge), run_time=0.8)
            self.play(GrowArrow(win), FadeIn(win_t), run_time=0.7)
            b.until(0.35)
            self.play(FadeIn(cond), run_time=0.5)
            b.until(0.55)
            self.play(GrowArrow(gout), FadeIn(gout_t), run_time=0.7)
            b.until(0.8)
            self.play(GrowArrow(dout), FadeIn(dout_t), run_time=0.6)

        # transesterification (schematic ester exchange)
        R_cols = ["#F5B041", "#5DADE2", "#AF7AC5"]
        back = VGroup(*[T(t, size=LABEL) for t in ["CH₂–O–", "CH–O–", "CH₂–O–"]]).arrange(DOWN, buff=0.55, aligned_edge=RIGHT)
        back.move_to([-4.6, -0.2, 0])
        tails = VGroup(*[T(f"CO–R{i+1}", size=LABEL, color=R_cols[i]) for i in range(3)])
        for t_, bk in zip(tails, back):
            t_.next_to(bk, RIGHT, buff=0.05)
        tri_lab = T("triglyceride (fat or oil)", size=SMALL + 1, color=MUTED).next_to(VGroup(back, tails), DOWN, buff=0.3)
        meths = VGroup(*[VGroup(T("H", size=LABEL, color=UNKNOWN), T("–O–CH₃", size=LABEL)).arrange(RIGHT, buff=0.02) for _ in range(3)])
        meths.arrange(DOWN, buff=0.55).move_to([-0.6, -0.2, 0])
        plus = T("+ 3", size=BODY).next_to(meths, LEFT, buff=0.35)
        m_lab = T("3 methanol", size=SMALL + 1, color=MUTED).next_to(meths, DOWN, buff=0.3)
        arrow = Arrow([0.6, -0.2, 0], [1.9, -0.2, 0], buff=0, color=TEXT, stroke_width=4)
        cat = T("catalyst, e.g. KOH", size=SMALL, color=MUTED).next_to(arrow, UP, buff=0.08)
        with self.beat("b02") as b:
            self.clear(h, sch)
            self.play(FadeIn(back), FadeIn(tails), FadeIn(tri_lab), run_time=1.0)
            b.until(0.5)
            ester = T("ester links", size=SMALL, color=UNKNOWN).next_to(tails, RIGHT, buff=0.3)
            self.play(LaggedStart(*[Indicate(t_) for t_ in tails], lag_ratio=0.2), FadeIn(ester), run_time=1.2)
            self.ester = ester
        with self.beat("b03") as b:
            self.play(FadeOut(self.ester), FadeIn(plus), FadeIn(meths), FadeIn(m_lab), GrowArrow(arrow), FadeIn(cat), run_time=1.0)
            b.until(0.3)
            # products: esters R-CO-O-CH3 on the right; glycerol keeps O and gains H
            prod_y = [0.75, -0.2, -1.15]
            for i in range(3):
                tail_tgt = np.array([4.9, prod_y[i], 0])
                meo = T("CH₃–O–", size=LABEL)
                meo.move_to(tail_tgt + LEFT * (tails[i].width / 2 + meo.width / 2 + 0.02))
                self.play(tails[i].animate.move_to(tail_tgt), Transform(meths[i][1], meo), run_time=0.7)
            hs = [m[0] for m in meths]
            self.play(*[hs[i].animate.next_to(back[i], RIGHT, buff=0.05) for i in range(3)], FadeOut(plus), run_time=0.8)
            fame = T("3 fatty acid methyl esters = biodiesel", size=SMALL + 1, color=BIO).move_to([4.3, -1.95, 0])
            gly = T("glycerol", size=SMALL + 1, color=MUTED).move_to(tri_lab)
            self.play(FadeIn(fame), Transform(tri_lab, gly), FadeOut(m_lab), run_time=0.8)
        with self.beat("b04") as b:
            key = M(r"\text{triglyceride} + 3\,\text{alcohol} \ce{->} 3\,\text{esters} + \text{glycerol}", size=EQ_SMALL - 4, color=UNKNOWN)
            key.move_to([0, 2.15, 0])
            self.play(Write(key), run_time=1.2)
            sig = T("detailed mechanisms: organic chemistry topic", size=SMALL, color=MUTED).move_to([0, -2.45, 0])
            b.until(0.6)
            self.play(FadeIn(sig), run_time=0.5)


# =====================================================================================
class E04S09_Q08(NarratedScene):
    def construct(self):
        h = header("Practice Q08")
        qc = question_card("Q08").move_to([0, -0.10, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        with self.beat("b02") as b:
            self.play(FadeOut(qc), run_time=0.4)
            la = TB("a.", size=LABEL + 2, color=SYSTEM).move_to([-6.2, 2.2, 0])
            eq = M(r"\ce{CH4(g) + 2O2(g) -> CO2(g) + 2H2O(l)}", size=EQ_SMALL - 4).next_to(la, RIGHT, buff=0.3)
            t = wrapped("Identical: same molecule, same reaction → same energy released and 1 mol CO₂ per mol CH₄ burned.",
                        size=LABEL, width=11.4).next_to(eq, DOWN, buff=0.2).align_to(eq, LEFT)
            self.play(FadeIn(la), Write(eq), run_time=1.0)
            b.until(0.4)
            self.play(FadeIn(t), run_time=0.8)
            self.pa = VGroup(la, eq, t)
        with self.beat("b03") as b:
            lb = TB("b.", size=LABEL + 2, color=SYSTEM).move_to([-6.2, 0.75, 0])
            c1 = card("Natural gas", ["non-renewable: formed over millions of years, used far faster than replaced"], FOSSIL, 5.4)
            c2 = card("Biomethane", ["renewable: plant feedstock regrows on a human timescale"], BIO, 5.4)
            VGroup(c1, c2).arrange(RIGHT, buff=0.35, aligned_edge=UP).next_to(lb, RIGHT, buff=0.3, aligned_edge=UP)
            self.play(FadeIn(lb), FadeIn(c1), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(c2), run_time=0.8)
            self.pb = VGroup(lb, c1, c2)
        with self.beat("b04") as b:
            lc = TB("c.", size=LABEL + 2, color=SYSTEM).move_to([-6.2, 0, 0]).set_y(self.pb.get_bottom()[1] - 0.35)
            items = bullets(["methane leakage from digesters and pipes (a potent greenhouse gas)",
                             "energy used in processing", "land and water used to grow feedstock"], size=SMALL + 1, width=11.0, buff=0.1)
            items.next_to(lc, RIGHT, buff=0.3, aligned_edge=UP)
            self.play(FadeIn(lc), FadeIn(items[0]), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(items[1:]), run_time=0.8)
        with self.beat("b05") as b:
            self.clear(h)
            tally = mark_tally([(1, "a. same energy and CO₂ per mol"), (2, "b. classification with timescale reasons"),
                                (1, "c. a lifecycle issue")], width=5.6).move_to([-3.4, 0.3, 0])
            w = wrong_panel("“Biomethane doesn't emit CO₂”", [T("It does: 1 mol CO₂ per mol CH₄", size=LABEL)],
                            note="Its carbon was recently taken from the air.", width=5.0).move_to([3.5, 0.3, 0])
            self.play(FadeIn(tally), run_time=0.8)
            b.until(0.4)
            self.play(FadeIn(w), run_time=0.8)
        with self.beat("b06") as b:
            self.clear(h)
            g = VGroup(TB("Checkpoint", size=BODY, color=UNKNOWN),
                       T("renewable = replenished on a human timescale", size=BODY, color=BIO),
                       T("renewable ≠ emission-free", size=BODY, color=BAD),
                       T("renewable ≠ automatically sustainable", size=BODY, color=BAD)).arrange(DOWN, buff=0.35)
            g.move_to([0, 0.4, 0])
            self.play(FadeIn(g[0]), FadeIn(g[1]), run_time=0.8)
            self.play(FadeIn(g[2]), run_time=0.6)
            self.play(FadeIn(g[3]), run_time=0.6)


# =====================================================================================
class E04S10_Recap(NarratedScene):
    def construct(self):
        h = header("Recap")
        rows = [["Fuel", "Source", "Made by", "Renewable?"],
                ["coal, natural gas, petrol", "ancient organisms", "geological processes", "no"],
                ["biogas", "organic waste", "anaerobic digestion", "yes"],
                ["bioethanol", "sugars, starch", "fermentation, then distillation", "yes"],
                ["biodiesel", "fats and oils", "transesterification", "yes"]]
        tb = table(rows, [3.4, 2.8, 4.2, 2.2], size=LABEL, row_h=0.7).move_to([0, 0.3, 0])
        grid, cells = tb[0], tb[1]
        with self.beat("b01") as b:
            self.play(FadeIn(h), Create(grid), FadeIn(VGroup(*cells[:4])), run_time=0.8)
            for i in range(1, 5):
                b.until(0.1 + 0.18 * i)
                self.play(FadeIn(VGroup(*cells[i * 4:(i + 1) * 4])), run_time=0.5)
            note = T("renewable ≠ sustainable", size=LABEL, color=UNKNOWN).move_to([0, -2.3, 0])
            self.play(FadeIn(note), run_time=0.4)
        with self.beat("b02") as b:
            self.clear(h)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN),
                       T("Balanced equation for the fermentation of glucose?", size=BODY),
                       T("What does distillation do afterwards?", size=BODY)).arrange(DOWN, buff=0.35).move_to([0, 1.0, 0])
            self.play(FadeIn(q), run_time=0.8)
            self.q = q
        with self.beat("b03") as b:
            a = VGroup(M(r"\ce{C6H12O6(aq) -> 2C2H5OH(aq) + 2CO2(g)}", size=EQ_SMALL, color=GOOD),
                       T("separates and concentrates the ethanol (lower boiling point)", size=LABEL + 2, color=GOOD)).arrange(DOWN, buff=0.3)
            a.next_to(self.q, DOWN, buff=0.5)
            self.play(FadeIn(a), run_time=1.0)
            b.until(0.6)
            nxt = T("Next: Episode 05 · Food as a chemical energy source", size=LABEL, color=MUTED).move_to([0, -2.35, 0])
            self.play(FadeIn(nxt), run_time=0.5)


EPISODE_SCENES = ["E04S01_Retrieval", "E04S02_Fossil", "E04S03_Timescale", "E04S04_CarbonCycle", "E04S05_Photosynthesis",
                  "E04S06_Ethanol", "E04S07_Q07", "E04S08_BiogasBiodiesel", "E04S09_Q08", "E04S10_Recap"]
