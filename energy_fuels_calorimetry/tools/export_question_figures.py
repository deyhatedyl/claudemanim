"""Export question-only temperature graphs from the same data used in the videos."""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from questions.bank import BANK


def export():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator

    out = ROOT / "questions/figures"
    out.mkdir(parents=True, exist_ok=True)
    for q in BANK:
        spec = q.get("visual", {})
        if spec.get("type") != "temperature":
            continue
        pts = spec["points"]
        ymin = math.floor(min([p[1] for p in pts] + [spec["baseline"]])) - 1
        ymax = math.ceil(max(p[1] for p in pts)) + 1
        with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 11,
                             "svg.hashsalt": q["id"]}):
            fig, ax = plt.subplots(figsize=(7.5, 4.7), layout="constrained")
            ax.set(xlim=(0, max(p[0] for p in pts) + 60), ylim=(ymin, ymax),
                   xlabel="Time (s)", ylabel="Temperature (°C)")
            ax.xaxis.set_major_locator(MultipleLocator(60))
            ax.yaxis.set_major_locator(MultipleLocator(1))
            ax.yaxis.set_minor_locator(MultipleLocator(0.2))
            ax.grid(which="major", color="#c3c3c3", linewidth=0.7)
            ax.grid(which="minor", color="#e4e4e4", linewidth=0.4)
            ax.set_axisbelow(True)
            ax.scatter(*zip(*pts), color="black", s=24, zorder=3)
            ax.plot([0, spec["mixing_time"]], [spec["baseline"]] * 2,
                    color="#666666", linewidth=1)
            ax.axvline(spec["mixing_time"], color="#333333", linestyle="--", linewidth=1)
            ax.text(spec["mixing_time"] + 5, ymax - 0.25,
                    f"Mixing at {spec['mixing_time']} s", va="top", fontsize=10)
            fig.savefig(out / f"{q['id']}-temperature.svg", metadata={"Date": None})
            plt.close(fig)
    return out


if __name__ == "__main__":
    print(export())
