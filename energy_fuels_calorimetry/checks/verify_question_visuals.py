"""Check that question stimuli give the same data and answers as the worked lessons."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from questions.bank import BANK


def constants(name):
    values = {}
    for node in ast.parse((ROOT / "scenes" / name).read_text()).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                values[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    return values


def near(value, expected):
    assert abs(value - expected) < 1e-8, (value, expected)


def main():
    q = {q["id"]: q for q in BANK}
    ep11, ep14 = constants("ep11.py"), constants("ep14.py")
    v21, v27 = q["Q21"]["visual"], q["Q27"]["visual"]
    assert v21["points"] == ep11["PRE"] + ep11["POST"]
    assert [p for p in v21["points"] if p[0] >= v21["cooling_start"]] == ep11["COOL"]
    assert v27["points"] == ep14["COOL"]
    near(v27["baseline"], ep14["BASE"])
    for visual, target in [(v21, 26.3), (v27, 24.8)]:
        cool = [p for p in visual["points"] if p[0] >= visual["cooling_start"]]
        t0, y0 = cool[0]
        t1, y1 = cool[-1]
        slope = (y1 - y0) / (t1 - t0)
        for t, y in cool:
            near(y, y0 + slope * (t - t0))
        near(y0 + slope * (visual["mixing_time"] - t0), target)
    rows = q["Q09"]["visual"]["rows"][1:]
    near(sum(float(r[1]) * float(r[2]) for r in rows), 1638)
    rows = q["Q10"]["visual"]["rows"]
    for col, total, serving in [(1, 1414, 1131.2), (2, 1455, 727.5)]:
        energy = sum(float(rows[i + 1][col]) * factor for i, factor in enumerate([16, 17, 37]))
        near(energy, total)
        near(energy * float(rows[4][col]) / 100, serving)
    rows = q["Q23"]["visual"]["rows"]
    for col, mass, emissions in [(1, 1 / 0.35 / 43, 80 / 0.35),
                                 (2, 1 / 0.28 / 29, 45 / 0.28)]:
        input_energy = 100 / float(rows[2][col])
        near(input_energy / float(rows[1][col]), mass)
        near(input_energy * float(rows[3][col]), emissions)
    rows = q["Q26"]["visual"]["rows"]
    for col, per_gram, direct_co2 in [(1, 726 / 32, 44 / 181.5),
                                    (2, 1370 / 46, 88 / 548)]:
        heat = abs(float(str(rows[2][col]).replace("−", "-")))
        near(heat / float(rows[1][col]), per_gram)
        near(float(rows[3][col]) * 44 / (heat * float(rows[4][col]) / 100), direct_co2)
    assert "visual" not in q["Q06"], "Episode 3 must retain its existing question display"
    for qid in ["Q09", "Q10", "Q21", "Q23", "Q24", "Q26", "Q27"]:
        assert q[qid]["visual"]["prompt"]
    print(json.dumps({"question_stimuli": 7, "graph_data_match_worked_scenes": True,
                      "visible_numeric_givens_reproduce_answers": True}))


if __name__ == "__main__":
    main()
