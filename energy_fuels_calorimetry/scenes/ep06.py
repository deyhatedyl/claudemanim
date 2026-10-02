"""
Episode 06 - Combustion equations and gaseous products.
Narration: scripts/ep06.md (beat names must match).
"""
import re
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from shared.components import (atom, bullets, mark_tally, question_card, result_box, right_panel, table,  # noqa: E402
                               title_card, wrapped, wrong_panel)
from shared.narrated import NarratedScene  # noqa: E402
from shared.style import (ATOM_COLORS, BAD, BG, BODY, EQ, EQ_SMALL, FAINT, GOOD, HEAD, LABEL, MASS_C, MOL_C,  # noqa: E402
                          MUTED, PANEL, SMALL, SURR, SYSTEM, TEXT, UNKNOWN, USEFUL, VOL_C, M, T, TB, chip,
                          header, panel)


def requested(text: str) -> VGroup:
    c = chip("Asked", UNKNOWN)
    t = T(text, size=SMALL + 2, color=UNKNOWN)
    return VGroup(c, t).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.4)


TOK = re.compile(r"([A-Z][a-z]?)(\d*)")


def atoms_of(formula: str) -> dict:
    d = {}
    for el, n in TOK.findall(formula):
        d[el] = d.get(el, 0) + int(n or 1)
    return d


def side_count(terms):
    tot = {"C": Fraction(0), "H": Fraction(0), "O": Fraction(0)}
    for coef, f in terms:
        if coef is None:
            continue
        for el, n in atoms_of(f).items():
            tot[el] = tot.get(el, 0) + Fraction(coef) * n
    return tot


def counter_row(tot, color=TEXT):
    g = VGroup()
    for el in ("C", "H", "O"):
        v = tot.get(el, 0)
        s = f"{float(v):g}" if v != 0 else "0"
        a = atom(el, 0.75)
        g.add(VGroup(a, TB(s, size=LABEL, color=color)).arrange(RIGHT, buff=0.1))
    return g.arrange(RIGHT, buff=0.35)


def coef_tex(c):
    if c is None:
        return r"\boxed{?}"
    if c == 1:
        return r"\phantom{1}"
    f = Fraction(c)
    if f.denominator == 1:
        return str(f.numerator)
    return rf"\tfrac{{{f.numerator}}}{{{f.denominator}}}"


def chem(f):
    return r"\ce{" + f + "}"


def build_eq(reac, prod, size=EQ):
    parts = []
    for i, (c, f) in enumerate(reac):
        if i:
            parts.append("+")
        parts += [coef_tex(c), chem(f)]
    parts.append(r"\ce{->}")
    for i, (c, f) in enumerate(prod):
        if i:
            parts.append("+")
        parts += [coef_tex(c), chem(f)]
    return M(*parts, size=size)


class Balancer:
    """Equation + counters that can be re-rendered after each coefficient change."""

    def __init__(self, scene, reac, prod, y=1.4, size=EQ):
        self.s, self.reac, self.prod, self.y, self.size = scene, [list(t) for t in reac], [list(t) for t in prod], y, size
        self.eq = build_eq(self.reac, self.prod, size).move_to([0, y, 0])
        self.lc, self.rc = self._counters()

    def _counters(self):
        lc = counter_row(side_count(self.reac)).move_to([-3.4, self.y - 1.3, 0])
        rc = counter_row(side_count(self.prod)).move_to([3.4, self.y - 1.3, 0])
        lt = T("reactants", size=SMALL, color=MUTED).next_to(lc, UP, buff=0.12)
        rt = T("products", size=SMALL, color=MUTED).next_to(rc, UP, buff=0.12)
        return VGroup(lt, lc), VGroup(rt, rc)

    def show(self, rt=1.0):
        self.s.play(Write(self.eq), FadeIn(self.lc), FadeIn(self.rc), run_time=rt)

    def set(self, side, idx, value, rt=0.9, flag=None):
        (self.reac if side == "r" else self.prod)[idx][0] = value
        new_eq = build_eq(self.reac, self.prod, self.size).move_to([0, self.y, 0])
        nl, nr = self._counters()
        self.s.play(TransformMatchingTex(self.eq, new_eq) if False else ReplacementTransform(self.eq, new_eq),
                    ReplacementTransform(self.lc, nl), ReplacementTransform(self.rc, nr), run_time=rt)
        self.eq, self.lc, self.rc = new_eq, nl, nr
        if flag:
            el = flag
            l = side_count(self.reac).get(el, 0)
            r = side_count(self.prod).get(el, 0)
            ok = l == r
            idx_el = ["C", "H", "O"].index(el)
            boxes = VGroup(SurroundingRectangle(self.lc[1][idx_el], color=GOOD if ok else BAD, buff=0.08),
                           SurroundingRectangle(self.rc[1][idx_el], color=GOOD if ok else BAD, buff=0.08))
            self.s.play(Create(boxes), run_time=0.4)
            self.s.play(FadeOut(boxes), run_time=0.3)


# =====================================================================================
class E06S01_Retrieval(NarratedScene):
    def construct(self):
        tc = title_card(6, "Combustion equations and gaseous products")
        with self.beat("b01"):
            self.play(FadeIn(tc, shift=0.2 * UP), run_time=1.5)
        with self.beat("b02") as b:
            self.play(FadeOut(tc), run_time=0.5)
            h = header("Retrieval check")
            q1 = VGroup(T("1.", size=BODY), M(r"2\ce{H2} + \ce{O2} \ce{->} 2\ce{H2O}", size=EQ_SMALL),
                        T(": water from 0.30 mol O₂?", size=BODY)).arrange(RIGHT, buff=0.2)
            q2 = T("2.  Does burning biomethane produce CO₂?", size=BODY)
            qs = VGroup(q1, q2).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([0, 0.9, 0])
            self.play(FadeIn(h), FadeIn(q1), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(q2), run_time=0.6)
            self.qs = qs
        with self.beat("b03") as b:
            a1 = T("O₂ : H₂O = 1 : 2  →  0.60 mol", size=BODY, color=GOOD).next_to(self.qs[0], DOWN, buff=0.15).align_to(self.qs[0], LEFT).shift(0.6 * RIGHT)
            a2 = T("yes: 1 mol CO₂ per mol CH₄", size=BODY, color=GOOD).next_to(self.qs[1], DOWN, buff=0.15).align_to(self.qs[1], LEFT).shift(0.6 * RIGHT)
            self.play(FadeIn(a1), run_time=0.6)
            b.until(0.4)
            self.play(FadeIn(a2), run_time=0.6)


# =====================================================================================
class E06S02_Balance(NarratedScene):
    def construct(self):
        h = header("Balancing: C, then H, then O")
        bal = Balancer(self, [[None, "CH3OH"], [None, "O2"]], [[None, "CO2"], [None, "H2O"]], y=1.5)
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            note = T("complete combustion: all C → CO₂, all H → H₂O", size=LABEL, color=MUTED).move_to([0, 2.55, 0])
            self.play(FadeIn(note), run_time=0.5)
            bal.reac[0][0] = 1
            bal.eq = build_eq(bal.reac, bal.prod).move_to([0, 1.5, 0])
            bal.lc, bal.rc = bal._counters()
            b.until(0.4)
            bal.show(1.2)
            ox = T("methanol already contains an O atom", size=LABEL, color=UNKNOWN).move_to([0, -1.2, 0])
            b.until(0.7)
            self.play(FadeIn(ox), run_time=0.6)
            self.ox = ox
        with self.beat("b02") as b:
            self.play(FadeOut(self.ox), run_time=0.3)
            step = T("1. Carbon: 1 C → 1 CO₂", size=LABEL + 2, color=TEXT).move_to([0, -1.2, 0])
            self.play(FadeIn(step), run_time=0.4)
            bal.set("p", 0, 1, flag="C")
            self.step = step
        with self.beat("b03") as b:
            st = T("2. Hydrogen: 4 H in CH₃OH → 2 H₂O", size=LABEL + 2, color=TEXT).move_to([0, -1.2, 0])
            self.play(Transform(self.step, st), run_time=0.5)
            b.until(0.4)
            bal.set("p", 1, 2, flag="H")
        with self.beat("b04") as b:
            st = T("3. Oxygen last: products 2 + 2 = 4 O; methanol gives 1; O₂ gives 3 → 1½ O₂", size=LABEL + 2).move_to([0, -1.2, 0])
            self.play(Transform(self.step, st), run_time=0.6)
            b.until(0.55)
            bal.set("r", 1, Fraction(3, 2), flag="O")
        with self.beat("b05") as b:
            fin = M(r"2\ce{CH3OH} + 3\ce{O2} \ce{->} 2\ce{CO2} + 4\ce{H2O}", size=EQ, color=GOOD).move_to([0, -2.05, 0])
            lab = T("× 2 for whole numbers", size=SMALL + 1, color=MUTED).next_to(fin, UP, buff=0.12)
            self.play(FadeOut(self.step), run_time=0.3)
            self.play(Write(fin), FadeIn(lab), run_time=1.2)
            chk = T("each side: 2 C, 8 H, 8 O ✓", size=LABEL, color=GOOD).move_to([0, -2.6, 0])
            b.until(0.6)
            self.play(FadeIn(chk), run_time=0.5)


# =====================================================================================
class E06S03_Octane(NarratedScene):
    def construct(self):
        h = header("A hydrocarbon from petrol")
        bal = Balancer(self, [[1, "C8H18"], [None, "O2"]], [[None, "CO2"], [None, "H2O"]], y=1.5)
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            bal.show(1.0)
            bal.set("p", 0, 8, rt=0.8, flag="C")
            b.until(0.6)
            bal.set("p", 1, 9, rt=0.8, flag="H")
        with self.beat("b02") as b:
            st = T("O in products: 16 + 9 = 25 atoms, all from O₂ → 12½ O₂", size=LABEL + 2).move_to([0, -1.2, 0])
            self.play(FadeIn(st), run_time=0.6)
            bal.set("r", 1, Fraction(25, 2), rt=0.8, flag="O")
            fin = M(r"2\ce{C8H18} + 25\ce{O2} \ce{->} 16\ce{CO2} + 18\ce{H2O}", size=EQ, color=GOOD).move_to([0, -2.1, 0])
            b.until(0.6)
            self.play(Write(fin), run_time=1.2)


# =====================================================================================
class E06S04_Incomplete(NarratedScene):
    def construct(self):
        h = header("Incomplete combustion")
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            items = bullets(["limited oxygen: some carbon → carbon monoxide, CO (toxic)",
                             "or → solid carbon, C (soot)",
                             "hydrogen still forms water"], size=LABEL + 2, width=11.0, buff=0.25).move_to([0, 1.6, 0])
            for i, it in enumerate(items):
                b.until(0.15 + 0.25 * i)
                self.play(FadeIn(it), run_time=0.5)
            self.items = items
        cols = [(r"\ce{CH4 + 2O2 -> CO2 + 2H2O}", "complete", 2.0, GOOD),
                (r"\ce{2CH4 + 3O2 -> 2CO + 4H2O}", "to carbon monoxide", 1.5, UNKNOWN),
                (r"\ce{CH4 + O2 -> C + 2H2O}", "to soot", 1.0, BAD)]
        built = VGroup()
        for tex, name, o2, col in cols:
            e = M(tex, size=EQ_SMALL - 8)
            n = TB(name, size=LABEL, color=col)
            bar = Rectangle(width=o2 * 1.4, height=0.35, fill_color=col, fill_opacity=0.8, stroke_width=0)
            bl = T(f"{o2:g} mol O₂ per mol CH₄", size=SMALL, color=col)
            g = VGroup(n, e, bar, bl).arrange(DOWN, buff=0.18)
            built.add(g)
        built.arrange(RIGHT, buff=0.45).move_to([0, -0.55, 0])
        with self.beat("b02") as b:
            self.play(FadeOut(self.items), run_time=0.4)
            for i, g in enumerate(built):
                b.until(0.1 + 0.2 * i)
                self.play(FadeIn(g[:2]), run_time=0.6)
            b.until(0.62)
            self.play(*[GrowFromEdge(g[2], LEFT) for g in built], *[FadeIn(g[3]) for g in built], run_time=0.9)
            less = T("less O₂, less energy released: carbon less fully oxidised", size=LABEL, color=MUTED).move_to([0, 1.55, 0])
            self.play(FadeIn(less), run_time=0.5)
            self.less = less
        with self.beat("b03") as b:
            self.play(FadeOut(self.less), run_time=0.3)
            warn = wrapped("“Limited oxygen” alone doesn't decide which equation applies. Real flames give a mixture. "
                           "Write an incomplete-combustion equation only when the products (or enough data) are given.",
                           size=LABEL, width=11.6, color=UNKNOWN)
            wp = panel(warn, color=UNKNOWN)
            VGroup(wp, warn).move_to([0, 1.6, 0])
            self.play(FadeIn(wp), FadeIn(warn), run_time=1.0)
            self.warn = VGroup(wp, warn)
        with self.beat("b04") as b:
            self.play(FadeOut(self.warn), run_time=0.4)
            l1 = M(r"1.00\ \text{mol}\ \ce{CH4} + 1.60\ \text{mol}\ \ce{O2}:\ \text{complete needs } 2.00\ \text{mol}"
                   r"\ \Rightarrow\ \text{must be incomplete}", size=EQ_SMALL - 8, color=UNKNOWN).move_to([0, 1.95, 0])
            l2 = M(r"\text{no soot} \Rightarrow\ 0.20\ \ce{CO2} + 0.80\ \ce{CO} + 2.00\ \ce{H2O}\ \ (\text{mol})",
                   size=EQ_SMALL - 8, color=GOOD).move_to([0, 1.2, 0])
            self.play(Write(l1), run_time=1.2)
            b.until(0.55)
            self.play(Write(l2), run_time=1.1)


# =====================================================================================
class E06S05_Q11(NarratedScene):
    def construct(self):
        h = header("Practice Q11")
        qc = question_card("Q11").move_to([0, 0.3, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        sk = M(r"\ce{C2H5OH}", "+", r"2.5\,\ce{O2}", r"\ce{->}", r"x\,\ce{CO2}", "+", r"y\,\ce{CO}", "+", r"z\,\ce{H2O}", size=EQ).move_to([0, 2.3, 0])
        req = requested("amounts of each product")
        with self.beat("b02") as b:
            self.play(FadeOut(qc), FadeIn(req), run_time=0.5)
            self.play(Write(sk), run_time=1.4)
            given = T("all ethanol and O₂ react · only CO₂, CO, H₂O · no soot", size=LABEL, color=MUTED).next_to(sk, DOWN, buff=0.2)
            self.play(FadeIn(given), run_time=0.6)
            self.given = given
        lines_x = -5.6

        def line(lbl, tex, y, col=TEXT):
            l = TB(lbl, size=LABEL + 2, color=col).move_to([0, y, 0]).align_to([lines_x, 0, 0], LEFT)
            m = M(tex, size=EQ_SMALL - 2).next_to(l, RIGHT, buff=0.4)
            return VGroup(l, m)
        Hl = line("H:", r"6 = 2z \;\Rightarrow\; z = 3", 0.75, ATOM_COLORS["H"])
        Cl = line("C:", r"x + y = 2", -0.05, "#AEB6BF")
        Ol = line("O:", r"1 + 5 = 2x + y + 3 \;\Rightarrow\; 2x + y = 3", -0.85, ATOM_COLORS["O"])
        with self.beat("b03") as b:
            self.play(FadeOut(self.given), Write(Hl), run_time=1.0)
        with self.beat("b04") as b:
            self.play(Write(Cl), run_time=0.9)
        with self.beat("b05") as b:
            hl = T("1 from ethanol!", size=SMALL + 1, color=UNKNOWN)
            self.play(Write(Ol), run_time=1.6)
            hl.next_to(Ol[1][0][0], DOWN, buff=0.15)
            self.play(FadeIn(hl), Indicate(Ol[1][0][0], color=UNKNOWN), run_time=0.8)
            self.hl = hl
        with self.beat("b06") as b:
            sol = M(r"(2x + y) - (x + y) = 3 - 2 \;\Rightarrow\; x = 1,\; y = 1", size=EQ_SMALL - 2, color=GOOD).move_to([0, -1.75, 0])
            self.play(Write(sol), run_time=1.4)
            amts = T("1.00 mol CO₂ · 1.00 mol CO · 3.00 mol H₂O", size=LABEL + 2, color=GOOD).move_to([0, -2.4, 0])
            b.until(0.6)
            self.play(FadeIn(amts), run_time=0.6)
        with self.beat("b07") as b:
            self.clear(h, req)
            fin = M(r"\ce{C2H5OH(l)} + 2\tfrac{1}{2}\ce{O2(g)} \ce{->} \ce{CO2(g)} + \ce{CO(g)} + 3\ce{H2O(g)}", size=EQ_SMALL, color=GOOD)
            fin.move_to([0, 1.3, 0])
            comp = M(r"\text{complete: } \ce{C2H5OH} + 3\ce{O2} \ce{->} 2\ce{CO2} + 3\ce{H2O}", size=EQ_SMALL - 4).move_to([0, 0.1, 0])
            diff = T("3.00 mol O₂ needed for complete combustion; only 2.50 mol here", size=LABEL, color=UNKNOWN).move_to([0, -0.8, 0])
            self.play(Write(fin), run_time=1.4)
            b.until(0.5)
            self.play(Write(comp), run_time=1.0)
            self.play(FadeIn(diff), run_time=0.6)
        with self.beat("b08") as b:
            self.clear(h, req)
            tally = mark_tally([(1, "H balance: 3 H₂O"), (2, "C and O balances: x = y = 1"), (1, "balanced equation"),
                                (1, "complete needs 3.00 mol O₂")], width=5.6, size=SMALL + 2).move_to([-3.4, 0.4, 0])
            w = wrong_panel("Ethanol's own O forgotten", [M(r"2x + y = 2 \Rightarrow x = 0,\ y = 2", size=EQ_SMALL - 8, color=TEXT)],
                            note="“All CO” looks like the textbook answer, but it's wrong for these data.", width=5.0, size=SMALL + 2)
            w.move_to([3.4, 0.4, 0])
            self.play(FadeIn(tally), run_time=0.8)
            b.until(0.4)
            self.play(FadeIn(w), run_time=0.8)


# =====================================================================================
GAS = {"CO₂": "#AEB6BF", "H₂O": "#5DADE2", "N₂": "#AF7AC5", "O₂": "#E74C3C"}


def gas_dot(name, r=0.2):
    c = Circle(radius=r, fill_color=GAS[name], fill_opacity=0.9, stroke_width=1.5, stroke_color=WHITE)
    t = T(name, size=12, color=BG, weight="BOLD").move_to(c)
    if t.width > 2 * r - 0.04:
        t.scale((2 * r - 0.04) / t.width)
    g = VGroup(c, t)
    g.gas = name
    return g


class E06S06_Exhaust(NarratedScene):
    def construct(self):
        h = header("Hot exhaust and dry gas")
        sch = T("schematic", size=SMALL, color=MUTED).to_corner(UR, buff=0.45)
        burner = RoundedRectangle(width=1.8, height=1.4, corner_radius=0.15, color=SYSTEM, stroke_width=3,
                                  fill_color=PANEL, fill_opacity=1).move_to([-5.4, 1.0, 0])
        flame = Polygon([-0.25, 0, 0], [0.25, 0, 0], [0, 0.6, 0], stroke_width=0, fill_color=SYSTEM, fill_opacity=0.9).move_to(burner)
        bl = T("combustion", size=SMALL + 1, color=SYSTEM).next_to(burner, DOWN, buff=0.12)
        pipe1 = Rectangle(width=3.4, height=1.1, color=SYSTEM, stroke_width=2).next_to(burner, RIGHT, buff=0).set_y(1.0)
        hot = T("hot exhaust, > 100 °C", size=SMALL + 1, color=SYSTEM).next_to(pipe1, UP, buff=0.1)
        names = ["CO₂", "H₂O", "N₂", "H₂O", "O₂", "N₂", "CO₂", "H₂O", "N₂"]
        dots = VGroup(*[gas_dot(n) for n in names])
        for i, d in enumerate(dots):
            d.move_to(pipe1.get_left() + RIGHT * (0.4 + 0.33 * i) + UP * (0.22 if i % 2 else -0.22))
        with self.beat("b01") as b:
            self.play(FadeIn(h), FadeIn(sch), FadeIn(burner), FadeIn(flame), FadeIn(bl), run_time=0.8)
            self.play(Create(pipe1), FadeIn(hot), run_time=0.6)
            b.until(0.3)
            self.play(LaggedStart(*[FadeIn(d, shift=0.2 * RIGHT) for d in dots], lag_ratio=0.1), run_time=1.6)
            key = VGroup(*[VGroup(gas_dot(n, 0.16), T(lbl, size=SMALL, color=MUTED)).arrange(RIGHT, buff=0.12)
                           for n, lbl in [("CO₂", "carbon dioxide"), ("H₂O", "water vapour"), ("N₂", "nitrogen (from air)"),
                                          ("O₂", "excess oxygen")]]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            key.move_to([4.6, 2.0, 0])
            b.until(0.65)
            self.play(FadeIn(key), run_time=0.6)
        cooler = RoundedRectangle(width=2.2, height=1.5, corner_radius=0.15, color=SURR, stroke_width=3,
                                  fill_color=SURR, fill_opacity=0.12).next_to(pipe1, RIGHT, buff=0).set_y(1.0)
        cl = T("cooler (to 25 °C)", size=SMALL + 1, color=SURR).next_to(cooler, UP, buff=0.1)
        trap = VGroup(Line(cooler.get_bottom(), cooler.get_bottom() + 0.9 * DOWN, color=SURR, stroke_width=3),
                      RoundedRectangle(width=1.4, height=0.7, corner_radius=0.1, color=SURR, stroke_width=2.5).move_to(cooler.get_bottom() + 1.25 * DOWN))
        tl = T("liquid water removed", size=SMALL + 1, color=SURR).next_to(trap[1], DOWN, buff=0.1)
        dry = RoundedRectangle(width=1.9, height=1.2, corner_radius=0.15, color=GOOD, stroke_width=3).move_to([5.6, -0.6, 0])
        dl = wrapped("dry gas measured at SLC", size=SMALL + 1, width=2.2, color=GOOD).next_to(dry, DOWN, buff=0.1)
        p2 = Line(cooler.get_right(), [dry.get_left()[0] - 0.2, 1.0, 0], color=GOOD, stroke_width=3)
        p3 = Arrow([dry.get_left()[0] - 0.2, 1.0, 0], [dry.get_center()[0], dry.get_top()[1], 0], buff=0, color=GOOD, stroke_width=3)
        with self.beat("b02") as b:
            self.play(FadeOut(key), FadeIn(cooler), FadeIn(cl), run_time=0.6)
            self.play(dots.animate.shift(2.6 * RIGHT), run_time=1.2)
            self.play(FadeIn(trap), FadeIn(tl), run_time=0.5)
            waters = [d for d in dots if d.gas == "H₂O"]
            others = [d for d in dots if d.gas != "H₂O"]
            drops = VGroup(*[Circle(radius=0.13, fill_color=GAS["H₂O"], fill_opacity=1, stroke_width=0) for _ in waters])
            for i, dr in enumerate(drops):
                dr.move_to(trap[1].get_center() + RIGHT * (i - 1) * 0.32)
            self.play(*[ReplacementTransform(w, dr) for w, dr in zip(waters, drops)], run_time=1.2)
            b.until(0.55)
            self.play(Create(p2), GrowArrow(p3), FadeIn(dry), FadeIn(dl), run_time=0.8)
            self.play(*[o.animate.move_to(dry.get_center() + np.array([((i % 3) - 1) * 0.45, (i // 3 - 0.5) * 0.45, 0]))
                        for i, o in enumerate(others)], run_time=1.4)
        cols = VGroup(VGroup(TB("Formed by the reaction", size=LABEL, color=SYSTEM),
                             T("CO₂(g)", size=LABEL), T("H₂O(g)  (vapour, hot)", size=LABEL)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                      VGroup(TB("Measured after cooling", size=LABEL, color=GOOD),
                             T("CO₂(g) at SLC", size=LABEL), T("water removed as liquid", size=LABEL, color=MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        cols.arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([-1.9, -2.0, 0])
        with self.beat("b03") as b:
            self.play(FadeOut(tl), FadeIn(cols[0]), run_time=0.7)
            b.until(0.3)
            self.play(FadeIn(cols[1]), run_time=0.7)
        with self.beat("b04") as b:
            self.clear(h)
            v1 = VGroup(TB("25 °C, 100 kPa", size=LABEL + 2, color=VOL_C), M(r"V_m = 24.8\ \text{L mol}^{-1}", size=EQ_SMALL))
            v2 = VGroup(TB("600 °C, 100 kPa", size=LABEL + 2, color=SYSTEM), T("about 3 × the volume per mole", size=LABEL + 2))
            for v in (v1, v2):
                v.arrange(DOWN, buff=0.25)
            VGroup(v1, v2).arrange(RIGHT, buff=2.0).move_to([0, 0.9, 0])
            box1 = Square(side_length=0.9, color=VOL_C, fill_opacity=0.2).next_to(v1, DOWN, buff=0.4)
            box2 = Rectangle(width=2.7, height=0.9, color=SYSTEM, fill_opacity=0.2).next_to(v2, DOWN, buff=0.4)
            self.play(FadeIn(v1), FadeIn(box1), run_time=0.8)
            b.until(0.45)
            self.play(FadeIn(v2), FadeIn(box2), run_time=0.8)
            nb = T("never apply 24.8 L mol⁻¹ to a hot gas", size=LABEL + 2, color=BAD).move_to([0, -1.6, 0])
            b.until(0.75)
            self.play(FadeIn(nb), run_time=0.5)


# =====================================================================================
class E06S07_Q12(NarratedScene):
    def construct(self):
        h = header("Practice Q12")
        qc = question_card("Q12").move_to([0, 0.3, 0])
        with self.beat("b01"):
            self.play(FadeIn(h), FadeIn(qc, shift=0.1 * UP), run_time=1.0)
        eq = M(r"\ce{CH4(g) + 2O2(g) -> CO2(g) + 2H2O(g)}", size=EQ_SMALL).move_to([0, 2.35, 0])
        tag = T("water is a gas at 600 °C", size=SMALL + 1, color=MUTED).next_to(eq, DOWN, buff=0.1)
        with self.beat("b02") as b:
            self.play(FadeOut(qc), Write(eq), FadeIn(tag), run_time=1.2)
            r = VGroup(M(r"n(\ce{CO2}) = 0.250\ \text{mol}\ (1:1)", size=EQ_SMALL - 6, color=MOL_C),
                       M(r"n(\ce{H2O}) = 0.500\ \text{mol}\ (1:2)", size=EQ_SMALL - 6, color=MOL_C)).arrange(RIGHT, buff=0.8)
            r.move_to([0, 1.2, 0])
            b.until(0.5)
            self.play(Write(r), run_time=1.2)
        left = VGroup(TB("Hot stream (formed)", size=LABEL, color=SYSTEM),
                      M(r"\ce{CO2}: 0.250 \times 44.0 = 11.0\ \text{g}", size=EQ_SMALL - 8),
                      M(r"\ce{H2O}: 0.500 \times 18.0 = 9.00\ \text{g}", size=EQ_SMALL - 8),
                      M(r"\text{total} = 20.0\ \text{g}", size=EQ_SMALL - 6, color=MASS_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        right = VGroup(TB("Cooled, dried, at SLC (measured)", size=LABEL, color=GOOD),
                       M(r"V(\ce{CO2}) = 0.250 \times 24.8", size=EQ_SMALL - 8),
                       M(r"= 6.20\ \text{L}", size=EQ_SMALL - 6, color=VOL_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        VGroup(left, right).arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to([0, -0.7, 0])
        with self.beat("b03") as b:
            self.play(FadeIn(left[0]), Write(left[1]), run_time=1.0)
            b.until(0.4)
            self.play(Write(left[2]), run_time=1.0)
            b.until(0.75)
            self.play(Write(left[3]), run_time=0.7)
        with self.beat("b04") as b:
            self.play(FadeIn(right[0]), Write(right[1]), run_time=1.0)
            self.play(Write(right[2]), run_time=0.7)
        with self.beat("b05") as b:
            self.clear(h)
            tally = mark_tally([(1, "mole ratios"), (2, "masses: 11.0 g and 9.00 g"), (1, "total 20.0 g"), (1, "6.20 L at SLC")],
                               width=5.4).move_to([-3.4, 0.4, 0])
            ws = VGroup(wrong_panel("Hot water vapour left out", [T("11.0 g instead of 20.0 g", size=LABEL)], width=4.6),
                        wrong_panel("24.8 L mol⁻¹ used at 600 °C", [T("SLC molar volume on a hot gas", size=LABEL)], width=4.6))
            ws.arrange(DOWN, buff=0.3).move_to([3.4, 0.4, 0])
            self.play(FadeIn(tally), run_time=0.8)
            b.until(0.5)
            self.play(FadeIn(ws), run_time=0.8)
        with self.beat("b06") as b:
            self.clear(h)
            q = VGroup(TB("Changed condition", size=BODY, color=UNKNOWN),
                       T("The same CO₂ measured at 600 °C and 100 kPa: more or less than 6.20 L?", size=LABEL + 2)).arrange(DOWN, buff=0.3)
            q.move_to([0, 0.9, 0])
            self.play(FadeIn(q), run_time=0.8)
            self.q = q
        with self.beat("b07") as b:
            a = T("More: higher temperature, same pressure → larger volume for the same amount", size=LABEL + 2, color=GOOD)
            a.next_to(self.q, DOWN, buff=0.5)
            self.play(FadeIn(a), run_time=0.8)


# =====================================================================================
class E06S08_MolesNotGrams(NarratedScene):
    def construct(self):
        h = header("Moles, not grams")
        eq = M(r"\ce{CH4 + 2O2 -> CO2 + 2H2O}", size=EQ).move_to([0, 2.3, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), Write(eq), run_time=1.0)
            q = T("Twice the moles of water: twice the mass?", size=BODY, color=UNKNOWN).move_to([0, 1.55, 0])
            self.play(FadeIn(q), run_time=0.6)
        bars = VGroup()
        specs = [("CO₂", 1, 44, "#AEB6BF"), ("H₂O", 2, 36, "#5DADE2")]
        for i, (n, mol, g, col) in enumerate(specs):
            y = 0.35 - 0.6 * i
            lab = T(n, size=LABEL + 2).move_to([-5.4, y, 0])
            mb = Rectangle(width=mol * 1.5, height=0.4, fill_color=MOL_C, fill_opacity=0.85, stroke_width=0).move_to([0, y, 0]).align_to([-4.6, 0, 0], LEFT)
            mt = T(f"{mol} mol", size=LABEL, color=MOL_C).next_to(mb, RIGHT, buff=0.15)
            gb = Rectangle(width=g * 0.06, height=0.4, fill_color=MASS_C, fill_opacity=0.85, stroke_width=0).move_to([0, y, 0]).align_to([1.2, 0, 0], LEFT)
            gt = T(f"{g} g", size=LABEL, color=MASS_C).next_to(gb, RIGHT, buff=0.15)
            bars.add(VGroup(lab, mb, mt, gb, gt))
        hd = VGroup(T("amount", size=LABEL, color=MOL_C).move_to([-3.4, 0.85, 0]), T("mass", size=LABEL, color=MASS_C).move_to([2.4, 0.85, 0]))
        with self.beat("b02") as b:
            self.play(FadeIn(hd[0]), *[FadeIn(bb[:3]) for bb in bars], run_time=0.9)
            b.until(0.35)
            self.play(FadeIn(hd[1]), *[GrowFromEdge(bb[3], LEFT) for bb in bars], *[FadeIn(bb[4]) for bb in bars], run_time=1.0)
            msg = T("coefficients → mole ratios; masses also need molar masses", size=LABEL + 2, color=UNKNOWN).move_to([0, -1.25, 0])
            b.until(0.75)
            self.play(FadeIn(msg), run_time=0.6)
        with self.beat("b03") as b:
            box = VGroup(VGroup(TB("“Carbon emissions”", size=LABEL, color=TEXT), T("CO₂ (or the mass of C it contains)", size=SMALL + 1)).arrange(DOWN, buff=0.08),
                         VGroup(TB("“Greenhouse gases”", size=LABEL, color=TEXT), T("CO₂, water vapour, unburnt CH₄, …", size=SMALL + 1)).arrange(DOWN, buff=0.08)).arrange(RIGHT, buff=1.0)
            bp = panel(box)
            VGroup(bp, box).move_to([0, -2.15, 0])
            self.play(FadeIn(bp), FadeIn(box), run_time=1.0)


# =====================================================================================
class E06S09_Propane(NarratedScene):
    def construct(self):
        h = header("Checkpoint: propane")
        bal = Balancer(self, [[1, "C3H8"], [None, "O2"]], [[None, "CO2"], [None, "H2O"]], y=1.5)
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            bal.show(1.0)
            st = T("complete combustion, with states, at SLC", size=LABEL + 1, color=UNKNOWN).move_to([0, -1.2, 0])
            self.play(FadeIn(st), run_time=0.5)
            self.st = st
        with self.beat("b02") as b:
            self.play(FadeOut(self.st), run_time=0.3)
            bal.set("p", 0, 3, rt=0.8, flag="C")
            b.until(0.25)
            bal.set("p", 1, 4, rt=0.8, flag="H")
            b.until(0.45)
            ox = T("O in products: 6 + 4 = 10 atoms → 5 O₂", size=LABEL + 1).move_to([0, -1.2, 0])
            self.play(FadeIn(ox), run_time=0.5)
            bal.set("r", 1, 5, rt=0.8, flag="O")
            fin = M(r"\ce{C3H8(g) + 5O2(g) -> 3CO2(g) + 4H2O(l)}", size=EQ, color=GOOD).move_to([0, -2.0, 0])
            b.until(0.75)
            self.play(Write(fin), run_time=1.1)
            nt = T("water is a liquid at SLC", size=SMALL + 1, color=MUTED).next_to(fin, DOWN, buff=0.15)
            self.play(FadeIn(nt), run_time=0.4)


# =====================================================================================
class E06S10_Recap(NarratedScene):
    def construct(self):
        h = header("Recap")
        items = bullets(["Balance C, then H, then O; include O already in the fuel",
                         "Incomplete combustion (CO, C): only when products or data are given",
                         "States match the conditions: H₂O(g) in hot exhaust, H₂O(l) at SLC",
                         "Formed ≠ measured: dry gas after cooling; 24.8 L mol⁻¹ only at SLC"], size=LABEL + 2, width=12.0, buff=0.35)
        items.move_to([0, 0.3, 0])
        with self.beat("b01") as b:
            self.play(FadeIn(h), run_time=0.4)
            for i, it in enumerate(items):
                b.until(0.05 + 0.22 * i)
                self.play(FadeIn(it, shift=0.1 * RIGHT), run_time=0.6)
        with self.beat("b02") as b:
            self.play(FadeOut(items), run_time=0.4)
            q = VGroup(TB("Closing recall", size=BODY, color=UNKNOWN),
                       T("Balance the complete combustion of propane, C₃H₈", size=BODY)).arrange(DOWN, buff=0.35).move_to([0, 1.0, 0])
            self.play(FadeIn(q), run_time=0.7)
            self.q = q
        with self.beat("b03") as b:
            a = M(r"\ce{C3H8 + 5O2 -> 3CO2 + 4H2O}", size=EQ, color=GOOD).next_to(self.q, DOWN, buff=0.5)
            steps = T("3 C → 3 CO₂ · 8 H → 4 H₂O · 6 + 4 = 10 O → 5 O₂", size=LABEL, color=MUTED).next_to(a, DOWN, buff=0.25)
            self.play(Write(a), FadeIn(steps), run_time=1.2)
            b.until(0.6)
            nxt = T("Next: Episode 07 · Limiting reactants, excess fuel and gas mixtures", size=LABEL, color=MUTED).move_to([0, -2.35, 0])
            self.play(FadeIn(nxt), run_time=0.5)


EPISODE_SCENES = ["E06S01_Retrieval", "E06S02_Balance", "E06S03_Octane", "E06S04_Incomplete", "E06S05_Q11",
                  "E06S06_Exhaust", "E06S07_Q12", "E06S08_MolesNotGrams", "E06S09_Propane", "E06S10_Recap"]
