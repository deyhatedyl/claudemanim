"""
VCE Maths Methods - Applications of Calculus
Question 3 (based on 2016 Exam 2)

    g : [-4pi, 8pi] -> R,   g(x) = 3 sin( (1/2)(x + pi) ) + pi/2

    a. State the period and range of g.
    b. Find the equation of the tangent to g at x = 5pi.
    c. Find the equations of the tangents to g where the gradient is 3/2.

Render every scene and stitch them together with ./render.sh
(or render one scene, e.g. `manim -pql vce_q3_tangents.py PartB`).
"""

from manim import *
import numpy as np

# ------------------------------------------------------------------
# Colour code (kept the same for the whole video)
# ------------------------------------------------------------------
AMP_C = YELLOW      # the 3      -> amplitude
N_C = GREEN         # the 1/2    -> controls the period
H_C = TEAL          # the + pi   -> slide left
K_C = ORANGE        # the + pi/2 -> middle line
CURVE_C = BLUE
TAN_C = RED
PT_C = YELLOW
GRAD_C = PINK
NOTE_C = GREY_A
BOX_C = GREEN

FONT = "DejaVu Sans"

X_MIN, X_MAX = -4 * PI, 8 * PI


def g(x):
    return 3 * np.sin(0.5 * (x + PI)) + PI / 2


def dg(x):
    return 1.5 * np.cos(0.5 * (x + PI))


# ------------------------------------------------------------------
# Small helpers
# ------------------------------------------------------------------
def T(s, size=30, color=WHITE, **kw):
    """Plain-English text."""
    return Text(s, font=FONT, font_size=size, color=color, **kw)


def M(*s, size=44, color=WHITE, **kw):
    """Maths."""
    return MathTex(*s, font_size=size, color=color, **kw)


def mixed(*parts, size=30, color=WHITE, buff=0.14):
    """A line mixing plain text and $maths$ pieces, e.g. mixed("Range is", "$[a,b]$")."""
    row = VGroup()
    for p in parts:
        if isinstance(p, Mobject):
            row.add(p)
        elif p.startswith("$") and p.endswith("$"):
            row.add(MathTex(p[1:-1], font_size=size * 1.3, color=color))
        else:
            row.add(T(p, size, color))
    row.arrange(RIGHT, buff=buff)
    return row


def header(title):
    t = T(title, 38, WHITE, weight=BOLD).to_corner(UL, buff=0.35)
    ul = Line(t.get_corner(DL), t.get_corner(DR), color=YELLOW, stroke_width=4)
    ul.shift(0.12 * DOWN)
    return VGroup(t, ul)


def boxed(mob, color=BOX_C, buff=0.25):
    box = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.15)
    box.set_fill(color, opacity=0.10)
    return VGroup(box, mob)


def note_card(*rows, color=NOTE_C, width=None, buff=0.18):
    """A rounded 'side note' card."""
    content = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    card = RoundedRectangle(
        corner_radius=0.2,
        width=(width or content.width + 0.6),
        height=content.height + 0.5,
        stroke_color=color,
        stroke_width=2,
        fill_color=BLACK,
        fill_opacity=0.85,
    )
    card.move_to(content)
    return VGroup(card, content)


def align_eq(rows, buff=0.32):
    """Arrange MathTex rows downwards and line up their '=' signs.

    rows: list of (MathTex, index_of_equals_submobject)
    """
    group = VGroup(*[r for r, _ in rows]).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    x_eq = rows[0][0][rows[0][1]].get_center()[0]
    for r, i in rows:
        r.shift((x_eq - r[i].get_center()[0]) * RIGHT)
    return group


def pi_label(k):
    """LaTeX label for k*pi."""
    if k == 0:
        return "0"
    if k == 1:
        return r"\pi"
    if k == -1:
        return r"-\pi"
    return rf"{k}\pi"


def build_graph(x_length=12.6, y_length=4.4, y_range=(-2.6, 5.4), label_every=1,
                show_curve=True):
    """Axes from -4pi to 8pi with pi-labelled ticks, plus the graph of g."""
    ax = Axes(
        x_range=[X_MIN - 0.35 * PI, X_MAX + 0.45 * PI, PI],
        y_range=[y_range[0], y_range[1], 1],
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={"stroke_width": 2, "color": GREY_B, "tick_size": 0.06},
    )
    labels = VGroup()
    for k in range(-4, 9):
        if k == 0 or k % label_every:
            continue
        lab = M(pi_label(k), size=22, color=GREY_B)
        lab.next_to(ax.c2p(k * PI, 0), DOWN, buff=0.12)
        labels.add(lab)
    curve = ax.plot(g, x_range=[X_MIN, X_MAX, 0.05], color=CURVE_C, stroke_width=4)
    ends = VGroup(
        Dot(ax.c2p(X_MIN, g(X_MIN)), radius=0.06, color=CURVE_C),
        Dot(ax.c2p(X_MAX, g(X_MAX)), radius=0.06, color=CURVE_C),
    )
    return ax, labels, curve, ends


def coloured_g(size=50):
    """g(x) = 3 sin(1/2 (x + pi)) + pi/2 with every 'ingredient' coloured."""
    eq = M(
        "g(x)", "=", "3", r"\sin", r"\Big(", r"\tfrac{1}{2}", r"(x", r"+\pi", r")",
        r"\Big)", "+", r"\frac{\pi}{2}",
        size=size,
    )
    eq[2].set_color(AMP_C)
    eq[5].set_color(N_C)
    eq[7].set_color(H_C)
    eq[11].set_color(K_C)
    return eq


# ==================================================================
# Scene 1 - Intro: read the question
# ==================================================================
class Intro(Scene):
    def construct(self):
        title = T("Applications of Calculus", 52, WHITE, weight=BOLD)
        sub = T("Tangents to a trig graph — explained step by step", 30, YELLOW)
        tag = T("VCE Maths Methods · Question 3 (based on 2016 Exam 2)", 24, NOTE_C)
        VGroup(title, sub, tag).arrange(DOWN, buff=0.35)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.play(FadeIn(tag))
        self.wait(2)
        self.play(FadeOut(VGroup(title, sub, tag)))

        # The question
        q_head = header("The question")
        fn = M(
            r"g : [-4\pi,\ 8\pi] \to \mathbb{R},\qquad",
            r"g(x) = 3\sin\Big(\tfrac{1}{2}(x+\pi)\Big) + \frac{\pi}{2}",
            size=44,
        ).shift(UP * 1.6)
        parts = VGroup(
            mixed("a.", "State the period and range of", "$g(x)$", size=25),
            mixed("b.", "Find the equation of the tangent to", "$g$", "at", "$x = 5\\pi$", size=25),
            mixed("c.", "Find the equations of the tangents to", "$g$", "where the gradient is",
                  "$\\tfrac{3}{2}$", size=25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(fn, DOWN, buff=0.8).to_edge(LEFT, buff=0.7)
        marks = VGroup(
            T("2 marks", 20, NOTE_C), T("2 marks", 20, NOTE_C), T("3 marks", 20, NOTE_C)
        )
        for m, p in zip(marks, parts):
            m.move_to(p).to_edge(RIGHT, buff=0.5)

        self.play(FadeIn(q_head))
        self.play(Write(fn), run_time=2.5)
        self.wait(1)
        for p, m in zip(parts, marks):
            self.play(FadeIn(p, shift=RIGHT * 0.3), FadeIn(m), run_time=0.9)
            self.wait(0.8)
        self.wait(2)

        calm = boxed(
            T("Don't panic! We'll break it into tiny, easy steps.", 30, WHITE),
            color=YELLOW,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(calm, shift=UP * 0.2))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ==================================================================
# Scene 2 - Decode the function (what each number does)
# ==================================================================
class DecodeFunction(Scene):
    def construct(self):
        head = header("Step 0: Decode the function")
        self.play(FadeIn(head))

        recipe_lbl = T("Every sine graph follows the same recipe:", 30, NOTE_C)
        recipe = M(r"y =", r"a", r"\sin\big(", r"n", r"(x - h)", r"\big)", r"+", r"k", size=54)
        recipe[1].set_color(AMP_C)
        recipe[3].set_color(N_C)
        recipe[4].set_color(H_C)
        recipe[7].set_color(K_C)
        VGroup(recipe_lbl, recipe).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.3).set_x(0)
        self.play(FadeIn(recipe_lbl))
        self.play(Write(recipe))
        self.wait(1.5)

        ours_lbl = T("Ours:", 30, NOTE_C)
        ours = coloured_g(54)
        VGroup(ours_lbl, ours).arrange(RIGHT, buff=0.4).next_to(recipe, DOWN, buff=0.45)
        self.play(FadeIn(ours_lbl), Write(ours))
        self.wait(1.5)

        # Explain each ingredient
        rows = [
            (ours[2], AMP_C, "a = 3", "Amplitude: the wave goes 3 above and 3 below its middle"),
            (ours[5], N_C, "n = ½", "Controls the period (how long one full wave takes)"),
            (ours[7], H_C, "+π", "Slides the graph π to the LEFT (doesn't change period or range)"),
            (ours[11], K_C, "k = π/2", "Lifts the whole wave up, so the middle line is y = π/2"),
        ]
        table = VGroup()
        for _, col, sym, desc in rows:
            sym_m = T(sym, 28, col, weight=BOLD)
            desc_m = T(desc, 26, WHITE)
            desc_m.move_to(sym_m.get_left() + RIGHT * 2.0, aligned_edge=LEFT)
            table.add(VGroup(sym_m, desc_m))
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        table.next_to(ours, DOWN, buff=0.5).set_x(0)

        for (part, col, _, _), r in zip(rows, table):
            ring = SurroundingRectangle(part, color=col, buff=0.08)
            self.play(Create(ring), run_time=0.6)
            self.play(FadeIn(r, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(2.2)
            self.play(FadeOut(ring), run_time=0.4)

        dom = boxed(
            mixed("The domain", "$[-4\\pi,\\ 8\\pi]$", "means: only draw the graph from",
                  "$x=-4\\pi$", "to", "$x = 8\\pi$", size=26),
            color=NOTE_C, buff=0.18,
        ).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(dom, shift=UP * 0.2))
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ==================================================================
# Scene 3 - Part a: period and range
# ==================================================================
class PartA(Scene):
    def construct(self):
        head = header("Part a: Period and Range")
        self.play(FadeIn(head))

        # ---------------- Period ----------------
        p_title = T("PERIOD", 34, N_C, weight=BOLD)
        p_meaning = T("= how far along the x-axis before the wave repeats itself", 26, WHITE)
        VGroup(p_title, p_meaning).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(p_title), FadeIn(p_meaning))
        self.wait(1.5)

        rule = M(r"\text{Period} = \frac{2\pi}{", r"n", r"}", size=50)
        rule[1].set_color(N_C)
        rule_note = T("(n is the number in front of x, inside the brackets)", 24, NOTE_C)
        VGroup(rule, rule_note).arrange(RIGHT, buff=0.5).next_to(p_title, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        self.play(Write(rule))
        self.play(FadeIn(rule_note))
        self.wait(2)

        work = VGroup(
            M(r"n = ", r"\tfrac{1}{2}", size=46),
            M(r"\text{Period} = \frac{2\pi}{\,\tfrac{1}{2}\,}", size=46),
            M(r"= 2\pi \times 2", size=46),
            M(r"= 4\pi", size=50),
        )
        work[0][1].set_color(N_C)
        work.arrange(RIGHT, buff=0.5).next_to(rule, DOWN, buff=0.55).to_edge(LEFT, buff=1.0)
        flip = T("Dividing by ½ is the same as multiplying by 2", 24, NOTE_C).next_to(work, DOWN, buff=0.3).align_to(work[1], LEFT)
        self.play(FadeIn(work[0]))
        self.wait(1)
        self.play(Write(work[1]))
        self.wait(1)
        self.play(Write(work[2]), FadeIn(flip))
        self.wait(2)
        self.play(Write(work[3]))
        period_ans = boxed(M(r"\text{Period} = 4\pi", size=50, color=WHITE))
        period_ans.next_to(work, RIGHT, buff=0.6)
        self.play(TransformFromCopy(work[3], period_ans[1]), Create(period_ans[0]))
        self.wait(2.5)

        # Visual: sin x vs sin(x/2)
        vis_ax = Axes(
            x_range=[0, 4 * PI + 0.3, PI], y_range=[-1.4, 1.4, 1],
            x_length=8, y_length=1.9, tips=False,
            axis_config={"stroke_width": 2, "color": GREY_B, "tick_size": 0.05},
        ).to_edge(DOWN, buff=0.75).to_edge(LEFT, buff=1.0)
        vis_labels = VGroup(*[
            M(pi_label(k), size=24, color=GREY_B).next_to(vis_ax.c2p(k * PI, 0), DOWN, buff=0.1)
            for k in range(1, 5)
        ])
        s1 = vis_ax.plot(np.sin, x_range=[0, 2 * PI], color=GREY_A, stroke_width=3)
        s2 = vis_ax.plot(lambda x: np.sin(x / 2), x_range=[0, 4 * PI], color=N_C, stroke_width=4)
        lab1 = M(r"\sin x", size=30, color=GREY_A).next_to(vis_ax.c2p(PI / 2, 1), UP, buff=0.1)
        lab2 = M(r"\sin\big(\tfrac{1}{2}x\big)", size=30, color=N_C).next_to(vis_ax.c2p(2 * PI, 1), UP, buff=0.1)
        b1 = BraceBetweenPoints(vis_ax.c2p(0, -1.2), vis_ax.c2p(2 * PI, -1.2), DOWN, color=GREY_A)
        b2 = BraceBetweenPoints(vis_ax.c2p(0, -1.2), vis_ax.c2p(4 * PI, -1.2), DOWN, color=N_C)
        b1t = M(r"2\pi", size=28, color=GREY_A).next_to(b1, DOWN, buff=0.05)
        b2t = M(r"4\pi", size=28, color=N_C).next_to(b2, DOWN, buff=0.05)
        stretch = T("The ½ stretches the wave\nto twice as wide:\none wave now takes 4π", 26, N_C)
        stretch.next_to(vis_ax, RIGHT, buff=0.5)
        self.play(FadeOut(flip), Create(vis_ax), FadeIn(vis_labels))
        self.play(Create(s1), FadeIn(lab1))
        self.wait(0.8)
        self.play(TransformFromCopy(s1, s2), FadeIn(lab2), run_time=2)
        self.play(FadeIn(stretch))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects if m is not head])

        # ---------------- Range ----------------
        r_title = T("RANGE", 34, K_C, weight=BOLD)
        r_meaning = T("= every y-value the graph actually reaches (lowest to highest)", 26, WHITE)
        VGroup(r_title, r_meaning).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(r_title), FadeIn(r_meaning))
        self.wait(1.5)

        steps = VGroup(
            mixed("Middle line:", "$y = \\tfrac{\\pi}{2}$", size=28),
            mixed("Top:", "$\\tfrac{\\pi}{2} + 3$", "(middle + amplitude)", size=28),
            mixed("Bottom:", "$\\tfrac{\\pi}{2} - 3$", "(middle − amplitude)", size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(r_title, DOWN, buff=0.45).align_to(r_title, LEFT).shift(RIGHT * 0.3)
        steps[0][1].set_color(K_C)
        steps[1][1].set_color(AMP_C)
        steps[2][1].set_color(AMP_C)
        for s in steps:
            self.play(FadeIn(s, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(1.4)

        # graph in the lower part of the screen
        ax, labels, curve, ends = build_graph(x_length=11.2, y_length=3.6)
        VGroup(ax, labels, curve, ends).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.3)
        mid = DashedLine(ax.c2p(X_MIN, PI / 2), ax.c2p(X_MAX, PI / 2), color=K_C, stroke_width=2)
        top = DashedLine(ax.c2p(X_MIN, PI / 2 + 3), ax.c2p(X_MAX, PI / 2 + 3), color=AMP_C, stroke_width=2)
        bot = DashedLine(ax.c2p(X_MIN, PI / 2 - 3), ax.c2p(X_MAX, PI / 2 - 3), color=AMP_C, stroke_width=2)
        mid_lab = M(r"y = \tfrac{\pi}{2}", size=28, color=K_C).next_to(mid, RIGHT, buff=0.5)
        top_lab = M(r"y = \tfrac{\pi}{2} + 3", size=28, color=AMP_C).next_to(top, RIGHT, buff=0.5)
        bot_lab = M(r"y = \tfrac{\pi}{2} - 3", size=28, color=AMP_C).next_to(bot, RIGHT, buff=0.5)
        self.play(Create(ax), FadeIn(labels))
        self.play(Create(mid), TransformFromCopy(steps[0][1], mid_lab))
        self.play(Create(top), Create(bot), TransformFromCopy(steps[1][1], top_lab),
                  TransformFromCopy(steps[2][1], bot_lab))
        self.play(Create(curve), FadeIn(ends), run_time=3)
        arr_up = DoubleArrow(ax.c2p(5 * PI, PI / 2), ax.c2p(5 * PI, PI / 2 + 3), buff=0, color=AMP_C,
                             stroke_width=3, tip_length=0.15)
        arr_dn = DoubleArrow(ax.c2p(PI, PI / 2), ax.c2p(PI, PI / 2 - 3), buff=0, color=AMP_C,
                             stroke_width=3, tip_length=0.15)
        three1 = M("3", size=28, color=AMP_C).next_to(arr_up, RIGHT, buff=0.08)
        three2 = M("3", size=28, color=AMP_C).next_to(arr_dn, RIGHT, buff=0.08)
        self.play(GrowFromCenter(arr_up), GrowFromCenter(arr_dn), FadeIn(three1), FadeIn(three2))
        self.wait(2)
        # the steps now live on the graph, so clear the space above it
        self.play(FadeOut(steps))

        # one period brace on the graph
        pb = BraceBetweenPoints(ax.c2p(-PI, PI / 2 + 3.15), ax.c2p(3 * PI, PI / 2 + 3.15), UP, color=N_C)
        pbt = M(r"\text{one period} = 4\pi", size=28, color=N_C).next_to(pb, UP, buff=0.05)
        self.play(GrowFromCenter(pb), FadeIn(pbt))
        self.wait(2.5)
        self.play(FadeOut(pb), FadeOut(pbt))

        check = note_card(
            T("Does the graph really reach the top & bottom?", 22, YELLOW),
            mixed("Domain width", "$= 8\\pi-(-4\\pi) = 12\\pi$", "= 3 full waves of", "$4\\pi$",
                  size=22, color=WHITE),
            T("So yes — it hits both, many times ✔", 22, GREEN),
            buff=0.14,
        ).next_to(r_title, DOWN, buff=0.35).set_x(0)
        self.play(FadeIn(check))
        self.wait(5)
        self.play(FadeOut(check))

        rng = boxed(
            M(r"\text{Range} = \left[\tfrac{\pi}{2} - 3,\ \tfrac{\pi}{2} + 3\right]", size=46),
        ).next_to(r_title, DOWN, buff=0.4).set_x(-2.2)
        approx = T("≈ [−1.43, 4.57]", 24, NOTE_C)
        brk = T("Square brackets [ ] mean the\nend values ARE included", 22, NOTE_C)
        VGroup(approx, brk).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(rng, RIGHT, buff=0.5)
        self.play(FadeIn(rng, scale=0.9))
        self.play(FadeIn(approx), FadeIn(brk))
        self.wait(3.5)

        # Final answer card for part a
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head])
        ans = VGroup(
            T("Answer to part a", 32, BOX_C, weight=BOLD),
            M(r"\text{Period} = 4\pi", size=54),
            M(r"\text{Range} = \left[\tfrac{\pi}{2} - 3,\ \tfrac{\pi}{2} + 3\right]", size=54),
        ).arrange(DOWN, buff=0.5)
        self.play(FadeIn(boxed(ans, buff=0.45), scale=0.95))
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ==================================================================
# Scene 4 - Part b: tangent at x = 5pi
# ==================================================================
class PartB(Scene):
    def unit_circle_note(self):
        """Mini unit circle: spin 3pi (1.5 turns) and land on (-1, 0)."""
        r = 1.0
        circ = Circle(radius=r, color=GREY_B, stroke_width=2)

        def centre():
            return circ.get_center()

        xax = Line(LEFT * (r + 0.35), RIGHT * (r + 0.35), color=GREY_C, stroke_width=1.5)
        yax = Line(DOWN * (r + 0.35), UP * (r + 0.35), color=GREY_C, stroke_width=1.5)
        one = M("1", size=24, color=GREY_B).next_to(RIGHT * r, DR, buff=0.04)
        mone = M("-1", size=24, color=GREY_B).next_to(LEFT * r, DL, buff=0.04)
        angle = ValueTracker(0)
        dot = always_redraw(lambda: Dot(
            centre() + r * np.array([np.cos(angle.get_value()), np.sin(angle.get_value()), 0]),
            color=PT_C, radius=0.09))
        spoke = always_redraw(lambda: Line(
            centre(), centre() + r * np.array([np.cos(angle.get_value()), np.sin(angle.get_value()), 0]),
            color=PT_C, stroke_width=2))
        # spiral trace so you can see the 1.5 turns
        trace = always_redraw(lambda: ParametricFunction(
            lambda t: centre() + (0.2 + 0.06 * t) * np.array([np.cos(t), np.sin(t), 0]),
            t_range=[0, max(angle.get_value(), 0.01), 0.05], color=GRAD_C, stroke_width=2))
        title = T("Unit circle check", 24, NOTE_C, weight=BOLD)
        pic = VGroup(circ, xax, yax, one, mone)
        grp = VGroup(title, pic).arrange(DOWN, buff=0.25)
        return grp, angle, dot, spoke, trace

    def construct(self):
        head = header("Part b: Tangent at x = 5π")
        self.play(FadeIn(head))

        # -------- What is a tangent? (sliding demo) --------
        what = mixed("A", "tangent", "is a straight line that touches the curve at one point", size=28)
        what[1].set_color(TAN_C)
        what2 = T("and is exactly as steep as the curve is right there.", 28, WHITE)
        VGroup(what, what2).arrange(DOWN, buff=0.15).next_to(head, DOWN, buff=0.45).set_x(0)
        self.play(FadeIn(what), FadeIn(what2))

        ax, labels, curve, ends = build_graph(x_length=12.4, y_length=3.9)
        VGroup(ax, labels, curve, ends).to_edge(DOWN, buff=0.4)
        self.play(Create(ax), FadeIn(labels), Create(curve), FadeIn(ends), run_time=2)

        xt = ValueTracker(-3 * PI)

        def tangent_at(x0, half=2.4, color=TAN_C, width=4):
            m = dg(x0)
            # keep the visible line roughly the same length
            h = half / np.sqrt(1 + (m * 0.8) ** 2)
            return Line(ax.c2p(x0 - h, g(x0) - m * h), ax.c2p(x0 + h, g(x0) + m * h),
                        color=color, stroke_width=width)

        slider = always_redraw(lambda: tangent_at(xt.get_value()))
        sdot = always_redraw(lambda: Dot(ax.c2p(xt.get_value(), g(xt.get_value())), color=PT_C, radius=0.08))
        self.play(Create(slider), FadeIn(sdot))
        self.play(xt.animate.set_value(7.5 * PI), run_time=7, rate_func=there_and_back_with_pause)
        self.wait(0.5)
        self.play(FadeOut(slider), FadeOut(sdot))
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head])

        # -------- The recipe for any straight line --------
        need = T("To write the equation of ANY straight line you need just 2 things:", 28, WHITE)
        need.next_to(head, DOWN, buff=0.6).set_x(0)
        ing = VGroup(
            mixed("①", "a point", "$(x_1,\\ y_1)$", size=30, color=PT_C),
            mixed("②", "a gradient (steepness)", "$m$", size=30, color=GRAD_C),
        ).arrange(RIGHT, buff=1.2).next_to(need, DOWN, buff=0.5)
        formula = M(r"y - y_1 = m\,(x - x_1)", size=60)
        formula_lbl = T("point–gradient form (memorise this!)", 24, NOTE_C)
        fgrp = boxed(VGroup(formula, formula_lbl).arrange(DOWN, buff=0.2), color=WHITE)
        fgrp.next_to(ing, DOWN, buff=0.6)
        plan = VGroup(
            mixed("Our plan:", size=28, color=NOTE_C),
            mixed("Step 1 – find the point:  put", "$x=5\\pi$", "into", "$g(x)$", size=26),
            mixed("Step 2 – find the gradient function", "$g'(x)$", "(differentiate)", size=26),
            mixed("Step 3 – find the gradient at", "$x = 5\\pi$", ":", "$m = g'(5\\pi)$", size=26),
            mixed("Step 4 – substitute into", "$y - y_1 = m(x-x_1)$", size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(fgrp, DOWN, buff=0.45)
        self.play(FadeIn(need))
        self.play(FadeIn(ing[0], shift=UP * 0.2))
        self.play(FadeIn(ing[1], shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeIn(fgrp))
        self.wait(2)
        for p in plan:
            self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(0.9)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head])

        # -------- Step 1: the point --------
        s1 = mixed("Step 1: Find the point — substitute", "$x = 5\\pi$", "into", "$g(x)$", size=28, color=PT_C)
        s1.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(s1))
        rows = [
            (M(r"g(5\pi)", "=", r"3\sin\Big(\tfrac{1}{2}(", r"5\pi", r"+\pi)\Big) + \frac{\pi}{2}", size=40), 1),
            (M("=", r"3\sin\Big(\tfrac{1}{2}\times 6\pi\Big) + \frac{\pi}{2}", size=40), 0),
            (M("=", r"3\sin(3\pi) + \frac{\pi}{2}", size=40), 0),
            (M("=", r"3\times 0 + \frac{\pi}{2}", size=40), 0),
            (M("=", r"\frac{\pi}{2}", size=40), 0),
        ]
        rows[0][0][3].set_color(PT_C)
        work = align_eq(rows, buff=0.26).next_to(s1, DOWN, buff=0.35).to_edge(LEFT, buff=0.8)
        comments = [
            T("swap every x for 5π", 22, NOTE_C),
            T("5π + π = 6π", 22, NOTE_C),
            T("half of 6π is 3π", 22, NOTE_C),
            T("sin(3π) = 0", 22, NOTE_C),
        ]
        for (r, _), c in zip(rows, comments):
            c.next_to(r, RIGHT, buff=0.5)
        cx = max(c.get_left()[0] for c in comments)
        for c in comments:
            c.set_x(cx, direction=LEFT)
        comments.append(None)

        for i, ((r, _), c) in enumerate(zip(rows, comments)):
            self.play(Write(r), run_time=1.2)
            if c is not None:
                self.play(FadeIn(c), run_time=0.5)
            self.wait(1.6)
            if i == 2:
                # unit-circle side note for sin(3pi) and cos(3pi)
                uc, angle, dot, spoke, trace = self.unit_circle_note()
                uc.to_edge(RIGHT, buff=1.0).align_to(work, UP)
                self.play(FadeIn(uc))
                self.add(trace, spoke, dot)
                self.play(angle.animate.set_value(3 * PI), run_time=4, rate_func=smooth)
                land = M(r"(-1,\ 0)", size=30, color=PT_C).next_to(uc[1][0].get_left(), LEFT, buff=0.12).shift(UP * 0.3)
                turns = T("3π = 1½ turns → land on (−1, 0)", 22, GRAD_C).next_to(uc, DOWN, buff=0.15)
                facts = VGroup(
                    M(r"\sin(3\pi) = y\text{-coord} = 0", size=30, color=WHITE),
                    M(r"\cos(3\pi) = x\text{-coord} = -1", size=30, color=WHITE),
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(turns, DOWN, buff=0.2)
                for mob in (turns, facts):
                    if mob.get_right()[0] > 6.8:
                        mob.shift((mob.get_right()[0] - 6.8) * LEFT)
                self.play(FadeIn(land), FadeIn(turns))
                self.play(FadeIn(facts[0]))
                self.wait(1)
                self.play(FadeIn(facts[1]))
                keep = T("(we'll need the cos one in Step 3!)", 20, NOTE_C).next_to(facts, DOWN, buff=0.1)
                self.play(FadeIn(keep))
                self.wait(2.5)
                circle_note = VGroup(uc, dot, spoke, trace, land, turns, facts, keep)

        point = boxed(mixed("Point:", "$\\left(5\\pi,\\ \\tfrac{\\pi}{2}\\right)$", size=34, color=PT_C), color=PT_C)
        point.next_to(rows[4][0], RIGHT, buff=0.9)
        self.play(FadeIn(point, scale=0.9))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (head,)], )

        # keep the point in the top-right corner from now on
        point_small = boxed(mixed("Point:", "$\\left(5\\pi,\\ \\tfrac{\\pi}{2}\\right)$", size=26, color=PT_C), color=PT_C, buff=0.15)
        point_small.to_corner(UR, buff=0.35)
        self.play(FadeIn(point_small))

        # -------- Step 2: differentiate --------
        s2 = mixed("Step 2: Differentiate to get the gradient function", "$g'(x)$", size=28, color=GRAD_C)
        s2.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(s2))

        chain = boxed(VGroup(
            T("Chain rule for sine:", 24, NOTE_C),
            M(r"\frac{d}{dx}\Big[\sin(\text{inside})\Big] = \cos(\text{inside}) \times (\text{inside})'", size=38),
        ).arrange(DOWN, buff=0.15), color=GRAD_C, buff=0.2)
        chain.next_to(s2, DOWN, buff=0.3).set_x(0)
        self.play(FadeIn(chain))
        self.wait(3)

        inside = VGroup(
            mixed("The inside is", "$\\tfrac{1}{2}(x+\\pi) = \\tfrac{1}{2}x + \\tfrac{\\pi}{2}$",
                  "so its derivative is", "$\\tfrac{1}{2}$", size=26),
            mixed("The", "$+\\tfrac{\\pi}{2}$", "on the end is a constant, so its derivative is", "$0$",
                  size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(chain, DOWN, buff=0.3).to_edge(LEFT, buff=0.8)
        inside[0][3].set_color(N_C)
        inside[1][1].set_color(K_C)
        self.play(FadeIn(inside[0], shift=RIGHT * 0.2))
        self.wait(2.5)
        self.play(FadeIn(inside[1], shift=RIGHT * 0.2))
        self.wait(2.5)

        d_rows = [
            (M(r"g'(x)", "=", r"3\times\cos\Big(\tfrac{1}{2}(x+\pi)\Big)\times", r"\tfrac{1}{2}", size=42), 1),
            (M("=", r"\tfrac{3}{2}\cos\Big(\tfrac{1}{2}(x+\pi)\Big)", size=42), 0),
        ]
        d_rows[0][0][3].set_color(N_C)
        dwork = align_eq(d_rows, buff=0.25).next_to(inside, DOWN, buff=0.35).set_x(-0.6)
        self.play(Write(d_rows[0][0]), run_time=1.5)
        self.wait(1.5)
        self.play(Write(d_rows[1][0]), run_time=1.2)
        warn = T("⚠ Don't forget the ½ from the inside — the most common mistake!", 22, RED)
        warn.next_to(dwork, DOWN, buff=0.25)
        self.play(FadeIn(warn))
        self.wait(3.5)

        # move g'(x) to a small card under the point card
        gprime_small = boxed(M(r"g'(x) = \tfrac{3}{2}\cos\Big(\tfrac{1}{2}(x+\pi)\Big)", size=28), color=GRAD_C, buff=0.15)
        gprime_small.next_to(point_small, DOWN, buff=0.15).align_to(point_small, RIGHT)
        self.play(
            *[FadeOut(m) for m in self.mobjects if m not in (head, point_small, d_rows[1][0])],
        )
        self.play(ReplacementTransform(d_rows[1][0], gprime_small))
        self.wait(0.5)

        # -------- Step 3: gradient at 5pi --------
        s3 = mixed("Step 3: Gradient at", "$x = 5\\pi$", "— substitute into", "$g'(x)$", size=28, color=GRAD_C)
        s3.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(s3))
        m_rows = [
            (M(r"m = g'(5\pi)", "=", r"\tfrac{3}{2}\cos\Big(\tfrac{1}{2}(5\pi+\pi)\Big)", size=44), 1),
            (M("=", r"\tfrac{3}{2}\cos(3\pi)", size=44), 0),
            (M("=", r"\tfrac{3}{2}\times(-1)", size=44), 0),
            (M("=", r"-\tfrac{3}{2}", size=48), 0),
        ]
        mwork = align_eq(m_rows).next_to(s3, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        m_comments = [
            T("same inside as before", 22, NOTE_C),
            T("½ × 6π = 3π", 22, NOTE_C),
            T("cos(3π) = −1  (from the unit circle)", 22, NOTE_C),
            T("negative → the tangent slopes DOWNHILL", 22, NOTE_C),
        ]
        for (r, _), c in zip(m_rows, m_comments):
            c.next_to(r, RIGHT, buff=0.5)
        cx = max(c.get_left()[0] for c in m_comments)
        for c in m_comments:
            c.set_x(cx, direction=LEFT)
        for (r, _), c in zip(m_rows, m_comments):
            self.play(Write(r), run_time=1.1)
            self.play(FadeIn(c), run_time=0.5)
            self.wait(1.6)
        m_card = boxed(M(r"m = -\tfrac{3}{2}", size=30, color=GRAD_C), color=GRAD_C, buff=0.15)
        m_card.next_to(gprime_small, DOWN, buff=0.15).align_to(gprime_small, RIGHT)
        self.wait(1.5)
        self.play(
            *[FadeOut(m) for m in self.mobjects
              if m not in (head, point_small, gprime_small, m_rows[3][0])]
        )
        self.play(ReplacementTransform(m_rows[3][0], m_card))

        # -------- Step 4: point-gradient form --------
        s4 = mixed("Step 4: Substitute into", "$y - y_1 = m(x - x_1)$", size=28, color=WHITE)
        s4.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(s4))
        subs = M(r"x_1 = 5\pi,", r"\quad y_1 = \tfrac{\pi}{2},", r"\quad m = -\tfrac{3}{2}", size=38)
        subs[0].set_color(PT_C)
        subs[1].set_color(PT_C)
        subs[2].set_color(GRAD_C)
        subs.next_to(s4, DOWN, buff=0.35).to_edge(LEFT, buff=1.0)
        self.play(FadeIn(subs))
        t_rows = [
            (M(r"y - ", r"\tfrac{\pi}{2}", "=", r"-\tfrac{3}{2}", r"\,(x - ", r"5\pi", ")", size=46), 2),
            (M(r"y - \tfrac{\pi}{2}", "=", r"-\tfrac{3}{2}x + \tfrac{15\pi}{2}", size=46), 1),
            (M(r"y", "=", r"-\tfrac{3}{2}x + \tfrac{15\pi}{2} + \tfrac{\pi}{2}", size=46), 1),
            (M(r"y", "=", r"-\tfrac{3}{2}x + \tfrac{16\pi}{2}", size=46), 1),
            (M(r"y", "=", r"-\tfrac{3}{2}x + 8\pi", size=50), 1),
        ]
        t_rows[0][0][1].set_color(PT_C)
        t_rows[0][0][5].set_color(PT_C)
        t_rows[0][0][3].set_color(GRAD_C)
        twork = align_eq(t_rows).next_to(subs, DOWN, buff=0.45).to_edge(LEFT, buff=1.4)
        t_comments = [
            T("plug in the three numbers", 22, NOTE_C),
            T("expand: −3/2 × −5π = +15π/2", 22, NOTE_C),
            T("add π/2 to both sides", 22, NOTE_C),
            T("15π/2 + π/2 = 16π/2", 22, NOTE_C),
            T("16π/2 = 8π", 22, NOTE_C),
        ]
        for (r, _), c in zip(t_rows, t_comments):
            c.next_to(r, RIGHT, buff=0.5)
        cx = max(c.get_left()[0] for c in t_comments)
        for c in t_comments:
            c.set_x(cx, direction=LEFT)
        for (r, _), c in zip(t_rows, t_comments):
            self.play(Write(r), run_time=1.1)
            self.play(FadeIn(c), run_time=0.5)
            self.wait(1.6)
        final_b = SurroundingRectangle(t_rows[4][0], color=BOX_C, buff=0.2, corner_radius=0.12)
        self.play(Create(final_b))
        self.wait(2.5)

        # -------- See it on the graph --------
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head])
        see = T("Let's check it on the graph", 28, NOTE_C).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        ax, labels, curve, ends = build_graph(x_length=12.4, y_length=4.3)
        VGroup(ax, labels, curve, ends).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(see), Create(ax), FadeIn(labels), Create(curve), FadeIn(ends), run_time=2)
        P = ax.c2p(5 * PI, PI / 2)
        pdot = Dot(P, color=PT_C, radius=0.1)
        plab = M(r"\left(5\pi,\ \tfrac{\pi}{2}\right)", size=30, color=PT_C).next_to(P, UR, buff=0.12)
        self.play(FadeIn(pdot, scale=2), FadeIn(plab))
        tline = ax.plot(lambda x: -1.5 * x + 8 * PI, x_range=[5 * PI - 2.4, 5 * PI + 2.4], color=TAN_C, stroke_width=5)
        tlab = M(r"y = -\tfrac{3}{2}x + 8\pi", size=32, color=TAN_C).next_to(ax.c2p(5 * PI + 2.4, PI / 2 - 3.6), RIGHT, buff=0.1)
        self.play(Create(tline), run_time=1.5)
        self.play(FadeIn(tlab))
        down = T("Touches the curve at one point and slopes downhill ✔", 24, GREEN)
        down.next_to(see, DOWN, buff=0.2).align_to(see, LEFT)
        self.play(FadeIn(down))
        self.wait(3)

        cas = note_card(
            T("CAS check (Exam 2 lets you use it):", 21, NOTE_C, weight=BOLD),
            mixed("TI-Nspire:", "$\\texttt{tangentLine}(g(x),\\ x,\\ 5\\pi)$", size=21),
            mixed("ClassPad:", "$\\texttt{tanLine}(g(x),\\ x,\\ 5\\pi)$", size=21),
            T("Make sure the calculator is in RADIAN mode!", 21, RED),
            buff=0.12,
        ).next_to(head, DOWN, buff=0.15).to_edge(LEFT, buff=0.5)
        self.play(FadeOut(see), FadeOut(down))
        self.play(FadeIn(cas))
        self.wait(5)
        self.play(*[FadeOut(m) for m in self.mobjects])

        ans = VGroup(
            T("Answer to part b", 32, BOX_C, weight=BOLD),
            M(r"y = -\tfrac{3}{2}x + 8\pi", size=60),
        ).arrange(DOWN, buff=0.5)
        self.play(FadeIn(boxed(ans, buff=0.45), scale=0.95))
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ==================================================================
# Scene 5 - Part c: tangents with gradient 3/2
# ==================================================================
class PartC(Scene):
    def construct(self):
        head = header("Part c: Gradient = 3/2")
        self.play(FadeIn(head))

        # -------- Translate the words --------
        key = boxed(VGroup(
            T("KEY IDEA", 26, YELLOW, weight=BOLD),
            T("“Gradient” just means the derivative.", 28),
            mixed("So “the gradient is", "$\\tfrac{3}{2}$", "” means:", size=28),
            M(r"g'(x) = \tfrac{3}{2}", size=60, color=GRAD_C),
        ).arrange(DOWN, buff=0.3), color=YELLOW, buff=0.35)
        key.next_to(head, DOWN, buff=0.6).set_x(0)
        self.play(FadeIn(key, scale=0.95))
        self.wait(3)
        reuse = mixed("We already found", "$g'(x) = \\tfrac{3}{2}\\cos\\Big(\\tfrac{1}{2}(x+\\pi)\\Big)$",
                      "in part b.", size=28)
        reuse.next_to(key, DOWN, buff=0.6).set_x(0)
        self.play(FadeIn(reuse))
        self.wait(2.5)
        self.play(FadeOut(key), FadeOut(reuse))

        # -------- Solve g'(x) = 3/2 --------
        s1 = T("Step 1: Solve the equation", 28, GRAD_C)
        s1.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(s1))
        rows = [
            (M(r"\tfrac{3}{2}\cos\Big(\tfrac{1}{2}(x+\pi)\Big)", "=", r"\tfrac{3}{2}", size=46), 1),
            (M(r"\cos\Big(\tfrac{1}{2}(x+\pi)\Big)", "=", r"1", size=46), 1),
        ]
        sw = align_eq(rows).next_to(s1, DOWN, buff=0.45).to_edge(LEFT, buff=1.0)
        c0 = T("set g′(x) equal to 3/2", 22, NOTE_C).next_to(rows[0][0], RIGHT, buff=0.6)
        c1 = T("divide both sides by 3/2", 22, NOTE_C).next_to(rows[1][0], RIGHT, buff=0.6)
        c1.align_to(c0, LEFT)
        self.play(Write(rows[0][0]))
        self.play(FadeIn(c0))
        self.wait(1.5)
        self.play(Write(rows[1][0]))
        self.play(FadeIn(c1))
        self.wait(2)

        theta = mixed("To make it less scary, call the inside", "$\\theta$", ":", size=26)
        theta_def = M(r"\theta = \tfrac{1}{2}(x+\pi)", r"\qquad\Longrightarrow\qquad", r"\cos\theta = 1", size=44)
        theta_def[2].set_color(YELLOW)
        VGroup(theta, theta_def).arrange(DOWN, buff=0.3).next_to(sw, DOWN, buff=0.6).set_x(0)
        self.play(FadeIn(theta))
        self.play(Write(theta_def))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head])

        # -------- When is cos(theta) = 1? --------
        s2 = mixed("Step 2: When does", "$\\cos\\theta = 1$", "?", size=28, color=GRAD_C)
        s2.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(s2))
        cax = Axes(
            x_range=[-2.6 * PI, 6.6 * PI, PI / 2], y_range=[-1.5, 1.6, 1],
            x_length=11.6, y_length=2.4, tips=False,
            axis_config={"stroke_width": 2, "color": GREY_B, "tick_size": 0.04},
        ).next_to(s2, DOWN, buff=0.6).set_x(0.55)
        cos_labels = VGroup()
        for k in range(-2, 7):
            if k == 0:
                continue
            cos_labels.add(M(pi_label(k), size=22, color=GREY_B).next_to(cax.c2p(k * PI, 0), DOWN, buff=0.1))
        cos_labels.add(M("0", size=22, color=GREY_B).next_to(cax.c2p(0, 0), DL, buff=0.06))
        cos_curve = cax.plot(np.cos, x_range=[-2.6 * PI, 6.6 * PI, 0.05], color=GREY_A, stroke_width=3)
        cos_lab = M(r"y = \cos\theta", size=28, color=GREY_A).next_to(cax, UP, buff=0.05).to_edge(RIGHT, buff=0.5)
        one_line = DashedLine(cax.c2p(-2.6 * PI, 1), cax.c2p(6.6 * PI, 1), color=YELLOW, stroke_width=2)
        one_lab = M("y = 1", size=26, color=YELLOW).next_to(one_line, LEFT, buff=0.1)
        self.play(Create(cax), FadeIn(cos_labels))
        self.play(Create(cos_curve), FadeIn(cos_lab), run_time=2)
        self.play(Create(one_line), FadeIn(one_lab))
        peaks = VGroup(*[Dot(cax.c2p(k * PI, 1), color=YELLOW, radius=0.08) for k in (-2, 0, 2, 4, 6)])
        self.play(LaggedStart(*[FadeIn(p, scale=2) for p in peaks], lag_ratio=0.25))
        peaks_txt = mixed("cos θ = 1 at the tops:", "$\\theta = \\dots,\\,-2\\pi,\\ 0,\\ 2\\pi,\\ 4\\pi,\\ 6\\pi,\\dots$",
                          "(every full turn)", size=24)
        peaks_txt.next_to(cax, DOWN, buff=0.55).set_x(0)
        self.play(FadeIn(peaks_txt))
        self.wait(3)

        # -------- Domain restriction for theta --------
        self.play(FadeOut(peaks_txt))
        but = mixed("BUT", "$x$", "is only allowed in", "$[-4\\pi,\\ 8\\pi]$", ". So what values can", "$\\theta$",
                    "take?", size=24)
        but[0].set_color(RED)
        but.next_to(cax, DOWN, buff=0.45).set_x(0)
        self.play(FadeIn(but))
        self.wait(1.5)
        lims = VGroup(
            M(r"x = -4\pi:\quad \theta = \tfrac{1}{2}(-4\pi + \pi) = -\tfrac{3\pi}{2}", size=34),
            M(r"x = 8\pi:\quad \theta = \tfrac{1}{2}(8\pi + \pi) = \tfrac{9\pi}{2}", size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(but, DOWN, buff=0.3).set_x(-2.3)
        self.play(Write(lims[0]))
        self.wait(1)
        self.play(Write(lims[1]))
        self.wait(1)
        trange = boxed(M(r"\theta \in \left[-\tfrac{3\pi}{2},\ \tfrac{9\pi}{2}\right]", size=38, color=WHITE),
                       color=YELLOW, buff=0.18)
        trange.next_to(lims, RIGHT, buff=0.7)
        self.play(FadeIn(trange))
        self.wait(1.5)

        window = Rectangle(
            width=cax.c2p(4.5 * PI, 0)[0] - cax.c2p(-1.5 * PI, 0)[0],
            height=cax.y_length + 0.2,
            stroke_width=0, fill_color=YELLOW, fill_opacity=0.12,
        ).move_to(cax.c2p(1.5 * PI, 0.05))
        w_edges = VGroup(
            DashedLine(cax.c2p(-1.5 * PI, -1.5), cax.c2p(-1.5 * PI, 1.6), color=YELLOW, stroke_width=2),
            DashedLine(cax.c2p(4.5 * PI, -1.5), cax.c2p(4.5 * PI, 1.6), color=YELLOW, stroke_width=2),
        )
        self.play(FadeIn(window), Create(w_edges))
        self.play(peaks[0].animate.set_color(GREY_D), peaks[4].animate.set_color(GREY_D))
        cross0 = Cross(peaks[0], stroke_width=4, scale_factor=1.6, stroke_color=RED)
        cross4 = Cross(peaks[4], stroke_width=4, scale_factor=1.6, stroke_color=RED)
        self.play(Create(cross0), Create(cross4))
        good = VGroup(peaks[1], peaks[2], peaks[3])
        self.play(*[Indicate(p, scale_factor=1.8, color=GREEN) for p in good])
        self.play(good.animate.set_color(GREEN))
        self.wait(1)
        self.play(FadeOut(but), FadeOut(lims), FadeOut(trange))
        sols = mixed("Inside the window:", "$\\theta = 0,\\ 2\\pi,\\ 4\\pi$",
                     "  (−2π and 6π are outside, so they don't count)", size=24)
        sols[1].set_color(GREEN)
        sols.next_to(cax, DOWN, buff=0.55).set_x(0)
        self.play(FadeIn(sols))
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head])

        # -------- Convert theta back to x --------
        s3 = mixed("Step 3: Turn each", "$\\theta$", "back into an", "$x$", size=28, color=GRAD_C)
        s3.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(s3))
        undo = mixed("$\\tfrac{1}{2}(x+\\pi) = \\theta$", "→ double both sides →",
                     "$x + \\pi = 2\\theta$", "→ subtract π →", "$x = 2\\theta - \\pi$", size=26)
        undo[4].set_color(YELLOW)
        undo.next_to(s3, DOWN, buff=0.45).set_x(0)
        self.play(FadeIn(undo))
        self.wait(3)
        conv = VGroup(
            M(r"\theta = 0", r"\ \Rightarrow\ ", r"x = 2(0) - \pi", "=", r"-\pi", size=42),
            M(r"\theta = 2\pi", r"\ \Rightarrow\ ", r"x = 2(2\pi) - \pi", "=", r"3\pi", size=42),
            M(r"\theta = 4\pi", r"\ \Rightarrow\ ", r"x = 2(4\pi) - \pi", "=", r"7\pi", size=42),
        ).arrange(DOWN, buff=0.35)
        for r in conv[1:]:
            r.shift((conv[0][1].get_center()[0] - r[1].get_center()[0]) * RIGHT)
        conv.next_to(undo, DOWN, buff=0.55).set_x(-0.5)
        for r in conv:
            r[4].set_color(PT_C)
            self.play(Write(r), run_time=1.2)
            self.wait(1.2)
        allin = T("All three are inside [−4π, 8π] ✔", 24, GREEN).next_to(conv, DOWN, buff=0.4)
        self.play(FadeIn(allin))
        self.wait(2.5)
        xs_card = boxed(M(r"x = -\pi,\ 3\pi,\ 7\pi", size=30, color=PT_C), color=PT_C, buff=0.15)
        xs_card.to_corner(UR, buff=0.35)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (head,)], FadeIn(xs_card))

        # -------- y-values --------
        s4 = mixed("Step 4: Find the y-value at each point", size=28, color=GRAD_C)
        s4.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(s4))
        ys = VGroup(
            M(r"g(-\pi) = 3\sin(0) + \tfrac{\pi}{2} = 0 + \tfrac{\pi}{2} = \tfrac{\pi}{2}", size=40),
            M(r"g(3\pi) = 3\sin(2\pi) + \tfrac{\pi}{2} = 0 + \tfrac{\pi}{2} = \tfrac{\pi}{2}", size=40),
            M(r"g(7\pi) = 3\sin(4\pi) + \tfrac{\pi}{2} = 0 + \tfrac{\pi}{2} = \tfrac{\pi}{2}", size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(s4, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        hint = T("The inside ½(x + π) is just θ, and sin(0) = sin(2π) = sin(4π) = 0", 22, NOTE_C)
        hint.next_to(ys, DOWN, buff=0.35).align_to(ys, LEFT)
        for r in ys:
            self.play(Write(r), run_time=1.3)
            self.wait(1)
        self.play(FadeIn(hint))
        self.wait(2)
        pts = boxed(mixed("Points:", "$\\left(-\\pi,\\tfrac{\\pi}{2}\\right),\\ \\left(3\\pi,\\tfrac{\\pi}{2}\\right),\\ \\left(7\\pi,\\tfrac{\\pi}{2}\\right)$",
                          size=30, color=PT_C), color=PT_C)
        pts.next_to(hint, DOWN, buff=0.45).set_x(0)
        self.play(FadeIn(pts, scale=0.95))
        same = T("All on the middle line y = π/2 — where the wave is climbing fastest!", 22, NOTE_C)
        same.next_to(pts, DOWN, buff=0.25)
        self.play(FadeIn(same))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (head,)])

        # -------- Tangent equations --------
        s5 = mixed("Step 5: Use", "$y - y_1 = m(x - x_1)$", "with", "$m = \\tfrac{3}{2}$", "for each point",
                   size=28, color=WHITE)
        s5[3].set_color(GRAD_C)
        s5.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(s5))

        blocks = VGroup()
        specs = [
            (r"(-\pi,\ \tfrac{\pi}{2})", r"y - \tfrac{\pi}{2} = \tfrac{3}{2}(x + \pi)",
             r"y = \tfrac{3}{2}x + \tfrac{3\pi}{2} + \tfrac{\pi}{2}", r"y = \tfrac{3}{2}x + 2\pi"),
            (r"(3\pi,\ \tfrac{\pi}{2})", r"y - \tfrac{\pi}{2} = \tfrac{3}{2}(x - 3\pi)",
             r"y = \tfrac{3}{2}x - \tfrac{9\pi}{2} + \tfrac{\pi}{2}", r"y = \tfrac{3}{2}x - 4\pi"),
            (r"(7\pi,\ \tfrac{\pi}{2})", r"y - \tfrac{\pi}{2} = \tfrac{3}{2}(x - 7\pi)",
             r"y = \tfrac{3}{2}x - \tfrac{21\pi}{2} + \tfrac{\pi}{2}", r"y = \tfrac{3}{2}x - 10\pi"),
        ]
        for p, l1, l2, l3 in specs:
            b = VGroup(
                M(r"\text{At }" + p, size=40, color=PT_C),
                M(l1, size=38),
                M(l2, size=38),
                M(l3, size=44, color=TAN_C),
            ).arrange(DOWN, buff=0.38)
            blocks.add(b)
        blocks.arrange(RIGHT, buff=0.6, aligned_edge=UP).next_to(s5, DOWN, buff=0.6).set_x(0)
        if blocks.width > 13.4:
            blocks.scale_to_fit_width(13.4)
        for b in blocks:
            for row in b:
                self.play(Write(row), run_time=0.9)
                self.wait(0.6)
            self.play(Create(SurroundingRectangle(b[3], color=BOX_C, buff=0.12, corner_radius=0.1)))
            self.wait(1.2)
        tip = T("Tip: −π is “minus a minus”, so (x − (−π)) becomes (x + π)", 22, NOTE_C)
        tip.next_to(blocks, DOWN, buff=0.7)
        self.play(FadeIn(tip))
        self.wait(3.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head])

        # -------- See it on the graph --------
        see = T("On the graph: three parallel tangents (same gradient = parallel!)", 26, NOTE_C)
        see.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        ax, labels, curve, ends = build_graph(x_length=12.4, y_length=3.8)
        VGroup(ax, labels, curve, ends).to_edge(DOWN, buff=0.45)
        mid = DashedLine(ax.c2p(X_MIN, PI / 2), ax.c2p(X_MAX, PI / 2), color=K_C, stroke_width=1.5)
        self.play(FadeIn(see), Create(ax), FadeIn(labels), Create(curve), FadeIn(ends), run_time=2)
        self.play(Create(mid))
        lines = VGroup()
        dots = VGroup()
        eq_labels = VGroup()
        texts = [r"y = \tfrac{3}{2}x + 2\pi", r"y = \tfrac{3}{2}x - 4\pi", r"y = \tfrac{3}{2}x - 10\pi"]
        for x0, tx in zip((-PI, 3 * PI, 7 * PI), texts):
            dots.add(Dot(ax.c2p(x0, PI / 2), color=PT_C, radius=0.09))
            ln = ax.plot(lambda x, x0=x0: 1.5 * (x - x0) + PI / 2, x_range=[x0 - 2.3, x0 + 2.3],
                         color=TAN_C, stroke_width=5)
            lines.add(ln)
            lab = M(tx, size=28, color=TAN_C).next_to(ax.c2p(x0 + 2.3, PI / 2 + 3.45), LEFT, buff=0.12)
            eq_labels.add(lab)
        for d, ln, lab in zip(dots, lines, eq_labels):
            self.play(FadeIn(d, scale=2))
            self.play(Create(ln), FadeIn(lab), run_time=1.2)
            self.wait(0.8)
        self.wait(1)
        why = note_card(
            T("Why only these three?", 21, YELLOW, weight=BOLD),
            mixed("The biggest gradient g′(x) can ever have is", "$\\tfrac{3}{2}$", size=21),
            T("(when cos = 1). That only happens where the wave", 21),
            T("crosses its middle line going UP — the steepest spots.", 21),
            buff=0.1,
        ).next_to(head, DOWN, buff=0.2).set_x(0)
        self.play(FadeOut(see))
        self.play(FadeIn(why))
        self.wait(6)
        self.play(*[FadeOut(m) for m in self.mobjects])

        ans = VGroup(
            T("Answer to part c", 32, BOX_C, weight=BOLD),
            M(r"y = \tfrac{3}{2}x + 2\pi", size=54),
            M(r"y = \tfrac{3}{2}x - 4\pi", size=54),
            M(r"y = \tfrac{3}{2}x - 10\pi", size=54),
        ).arrange(DOWN, buff=0.4)
        self.play(FadeIn(boxed(ans, buff=0.45), scale=0.95))
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ==================================================================
# Scene 6 - Recap + common mistakes
# ==================================================================
class Recap(Scene):
    def construct(self):
        head = header("Summary")
        self.play(FadeIn(head))

        a = VGroup(
            T("a.", 30, YELLOW, weight=BOLD),
            M(r"\text{Period} = 4\pi,\qquad \text{Range} = \left[\tfrac{\pi}{2}-3,\ \tfrac{\pi}{2}+3\right]", size=40),
        ).arrange(RIGHT, buff=0.4)
        b = VGroup(T("b.", 30, YELLOW, weight=BOLD), M(r"y = -\tfrac{3}{2}x + 8\pi", size=40)).arrange(RIGHT, buff=0.4)
        c = VGroup(
            T("c.", 30, YELLOW, weight=BOLD),
            M(r"y = \tfrac{3}{2}x + 2\pi,\quad y = \tfrac{3}{2}x - 4\pi,\quad y = \tfrac{3}{2}x - 10\pi", size=40),
        ).arrange(RIGHT, buff=0.4)
        answers = VGroup(a, b, c).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55).to_edge(LEFT, buff=0.8)
        for r in answers:
            self.play(FadeIn(r, shift=RIGHT * 0.3))
            self.wait(1.2)
        self.play(Create(SurroundingRectangle(answers, color=BOX_C, buff=0.25, corner_radius=0.15)))
        self.wait(2)

        mist_t = T("Common mistakes to avoid", 30, RED, weight=BOLD)
        mistakes = VGroup(
            T("✘  Forgetting the ½ from the chain rule when differentiating", 24),
            T("✘  Stopping after ONE answer in part c — check the whole domain", 24),
            T("✘  Leaving the CAS in degree mode (always use RADIANS)", 24),
            T("✘  Mixing up the point (x₁, y₁) — y₁ comes from g(x), not g′(x)", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        mgrp = VGroup(mist_t, mistakes).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        mgrp.next_to(answers, DOWN, buff=0.75).align_to(answers, LEFT)
        self.play(FadeIn(mist_t))
        for m in mistakes:
            self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(1.3)
        self.wait(2.5)

        recipe = boxed(VGroup(
            T("The tangent recipe", 34, YELLOW, weight=BOLD),
            T("1. Point:  y₁ = g(x₁)", 32),
            T("2. Gradient:  m = g′(x₁)", 32),
            T("3. Plug into  y − y₁ = m(x − x₁)", 32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18), color=YELLOW, buff=0.3)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not head])
        self.play(FadeIn(recipe, scale=0.95))
        self.wait(4)
        bye = T("You've got this! Good luck in the exam.", 34, WHITE).next_to(recipe, DOWN, buff=0.7)
        self.play(FadeIn(bye, shift=UP * 0.2))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])
