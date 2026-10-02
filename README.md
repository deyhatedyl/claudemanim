# VCE Maths Methods: Tangents to a Trig Graph (Manim)

A step-by-step Manim video for this applications-of-calculus question (based on 2016 Exam 2):

> $g : [-4\pi, 8\pi] \to \mathbb{R},\quad g(x) = 3\sin\big(\tfrac{1}{2}(x+\pi)\big) + \tfrac{\pi}{2}$
>
> **a.** State the period and range of $g(x)$. *(2 marks)*
> **b.** Find the equation of the tangent to $g$ at $x = 5\pi$. *(2 marks)*
> **c.** Find the equations of the tangents to $g$ where the gradient is $\tfrac{3}{2}$. *(3 marks)*

The finished video is at **`output/VCE_Q3_Tangents.mp4`** (1080p60, about 8 minutes, no audio).
It has on-screen explanations only.

## What the video covers

| Scene | Content |
|---|---|
| `Intro` | Reads the question |
| `DecodeFunction` | What each number in $a\sin(n(x-h))+k$ does (amplitude, period, shift, middle line) |
| `PartA` | Period $= 2\pi/n = 4\pi$, a stretch visual, the middle, top and bottom lines on the graph, and a check that the domain covers 3 full waves |
| `PartB` | What a tangent is (a sliding-tangent demo), point–gradient form, $g(5\pi)$ with a unit-circle check, the chain rule, $g'(5\pi)$, the final line on the graph, and the CAS commands |
| `PartC` | "gradient" means $g'(x)$, solving $\cos\theta = 1$ with a picture of the allowed $\theta$-window, converting back to $x$, the three parallel tangents, and why there are only three |
| `Recap` | All answers, common mistakes, and the tangent recipe |

## Answers

- **a.** Period $= 4\pi$, Range $= \left[\tfrac{\pi}{2} - 3,\ \tfrac{\pi}{2} + 3\right]$
- **b.** $y = -\tfrac{3}{2}x + 8\pi$
- **c.** $y = \tfrac{3}{2}x + 2\pi,\quad y = \tfrac{3}{2}x - 4\pi,\quad y = \tfrac{3}{2}x - 10\pi$

## Rendering it yourself

You need Python 3.10+, ffmpeg, a LaTeX install (with `dvisvgm`), and the Cairo/Pango dev libraries.
See the [Manim install guide](https://docs.manim.community/en/stable/installation.html).

```bash
pip install -r requirements.txt
./render.sh        # 1080p60 -> output/VCE_Q3_Tangents.mp4
./render.sh l      # fast 480p preview
manim -pql vce_q3_tangents.py PartB   # preview a single scene
```
