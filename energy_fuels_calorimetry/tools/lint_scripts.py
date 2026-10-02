"""
Check narration scripts are TTS-ready and report timing estimates.

    python tools/lint_scripts.py            # all scripts
    python tools/lint_scripts.py ep01       # one script

Flags spoken text that contains written-maths forms a TTS engine may mispronounce:
formula-like tokens (CO2, H2O), bare unit symbols (g, mL, kJ, mol), maths symbols (^ _ = / × ° %),
and raw question IDs (Q01 should be spoken "Q zero one").
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shared.config import SCRIPTS  # noqa: E402
from shared.script_parser import parse_script  # noqa: E402
from shared.tts import estimate_duration  # noqa: E402

RULES = [
    (re.compile(r"\b[A-Z][a-z]?\d+[A-Za-z0-9]*\b"), "formula-like token (spell it out)"),
    (re.compile(r"(?<!['’])\b(?:g|mg|kg|mL|L|kJ|MJ|J|mol|kPa|Pa|s|h|K|V|M|Vm|CF)\b(?![-'’])"), "bare unit/symbol"),
    (re.compile(r"[\^_=/×°%+→⁻¹²³⁴Δ<>]|->"), "maths symbol"),
    (re.compile(r"\bQ\d\d\b"), "question ID as digits (say 'Q zero one')"),
    (re.compile(r"\d[,.]\d{3}[,.]\d"), "ambiguous grouped number"),
    (re.compile(r"\be\.g\.|\bi\.e\.|\betc\b"), "abbreviation"),
]


def lint(path: Path) -> tuple[int, float]:
    ep = parse_script(path)
    issues = 0
    total = 0.0
    print(f"\n== {path.name}: {ep.title}")
    for sc in ep.scenes:
        st = 0.0
        for b in sc.beats:
            est = estimate_duration(b.text)
            st += est + b.pause + 0.45
            for rx, why in RULES:
                for m in rx.finditer(b.text):
                    tok = m.group(0)
                    issues += 1
                    ctx = b.text[max(0, m.start() - 25):m.end() + 25]
                    print(f"  {b.key}: {why}: '{tok}'  …{ctx}…")
        words = sum(b.words for b in sc.beats)
        print(f"  {sc.id} {sc.title[:48]:<48} beats={len(sc.beats):>2} words={words:>4} est={st/60:5.2f} min")
        total += st + 0.6
    print(f"  TOTAL est {total/60:.1f} min ({sum(b.words for b in ep.beats())} words); issues: {issues}")
    return issues, total


def main():
    sel = sys.argv[1:] or None
    paths = sorted(SCRIPTS.glob("ep*.md"))
    if sel:
        paths = [p for p in paths if p.stem in sel]
    bad = 0
    for p in paths:
        bad += lint(p)[0]
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
