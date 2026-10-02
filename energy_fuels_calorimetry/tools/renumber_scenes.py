"""
Renumber an episode's scenes so new scenes can be inserted in teaching order.

    python tools/renumber_scenes.py E10 5:6 6:8 7:9 8:10 9:11

Each OLD:NEW pair renames scene ENN S<OLD> to ENN S<NEW> in scripts/epNN.md (headings) and
scenes/epNN.py (class names, EPISODE_SCENES). Pairs are applied highest-first through a temporary
name, so overlapping ranges are safe. Draft timelines for the episode are deleted because their
scene IDs no longer match; re-render the episode afterwards. No narration exists yet, so no clip
cache entries are affected (beat keys contain the scene ID).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ep = sys.argv[1].upper()
    pairs = [tuple(int(x) for x in p.split(":")) for p in sys.argv[2:]]
    script = ROOT / "scripts" / f"ep{ep[1:].lower()}.md"
    scenes = ROOT / "scenes" / f"ep{ep[1:].lower()}.py"
    s_txt, c_txt = script.read_text(), scenes.read_text()
    for old, new in sorted(pairs, reverse=True):
        a, tmp = f"{ep}S{old:02d}", f"{ep}T{new:02d}"
        s_txt = re.sub(rf"^## {a} \|", f"## {tmp} |", s_txt, flags=re.M)
        c_txt = re.sub(rf"\b{a}_", f"{tmp}_", c_txt)
    s_txt = re.sub(rf"^## {ep}T(\d\d) \|", rf"## {ep}S\1 |", s_txt, flags=re.M)
    c_txt = re.sub(rf"\b{ep}T(\d\d)_", rf"{ep}S\1_", c_txt)
    script.write_text(s_txt)
    scenes.write_text(c_txt)
    for p in (ROOT / "renders" / "timelines").glob(f"*/{ep}S*.json"):
        p.unlink()
    print(f"{ep}: renumbered {len(pairs)} scenes; timelines cleared")


if __name__ == "__main__":
    main()
