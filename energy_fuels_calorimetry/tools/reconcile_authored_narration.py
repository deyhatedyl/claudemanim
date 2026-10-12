"""Import the learner's deliberately revised narration from local TTS scripts.

The original external narration_eNN.py files and their scene WAVs are private
assets; this script does not copy them to git. It validates that each archived
WAV sidecar identifies the exact authored scene transcript before modifying
the project script. A small known list of audit-corrected beats deliberately
retains the CURRENT corrected wording and requires a narration retake.

Usage:
 python tools/reconcile_authored_narration.py \
   --source ../../Energy-Fuels-Calorimetry --episodes E04 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14
 Add --apply to write the reviewed changes.
"""
from __future__ import annotations

import argparse
import ast
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.script_parser import load_episode

AUDITED_RETAKES = {
    "E06S04.b04", "E07S12.b01", "E08S06.b06",
    "E12S02.b01", "E12S02.b02", "E12S04.b01", "E12S09.b03",
    "E14S17.b03", "E14S18.b02",
}
LINE_RE = re.compile(r"^(\[(b\d\d)(?:\s+[^]]+)?\]\s*)(.*)$")


def authored_beats(source: Path, episode: str) -> dict[str, str]:
    path = source / f"narration_{episode.lower()}.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    assignments = [
        node.value for node in tree.body if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "BEATS" for target in node.targets)
    ]
    if len(assignments) != 1:
        raise ValueError(f"{path}: expected one BEATS definition")
    beats = ast.literal_eval(assignments[0])
    grouped: dict[str, list[str]] = defaultdict(list)
    for beat in beats:
        grouped[beat["scene"]].append(beat["text"])
    for scene, texts in grouped.items():
        sidecar = source / "audio" / "raw" / f"{scene}.wav.json"
        wav = source / "audio" / "raw" / f"{scene}.wav"
        if not sidecar.is_file() or not wav.is_file():
            raise FileNotFoundError(f"{scene}: original recording or sidecar missing")
        actual = json.loads(sidecar.read_text())["text_sha256"]
        expected = hashlib.sha256("\n\n".join(texts).encode("utf-8")).hexdigest()
        if actual != expected:
            raise ValueError(f"{scene}: authored recording SHA does not match the transcript")
    return {beat["key"]: beat["text"] for beat in beats}


def reconcile(source: Path, episodes: list[str], apply: bool) -> dict:
    summary: dict = {"apply": apply, "episodes": {}, "retakes": []}
    for ep in episodes:
        path = ROOT / "scripts" / f"ep{ep[1:]}.md"
        authored = authored_beats(source, ep)
        existing = load_episode(ep)
        repo_keys = {b.key for b in existing.beats()}
        if set(authored) != repo_keys:
            raise ValueError(f"{ep}: beat key mismatch: authored-only={sorted(set(authored)-repo_keys)}; "
                             f"script-only={sorted(repo_keys-set(authored))}")
        scene = None
        updated = 0
        retained = 0
        out = []
        for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
            header = re.match(r"^##\s+(E\d\dS\d\d)\b", line)
            if header:
                scene = header.group(1)
            beat = LINE_RE.match(line.rstrip("\r\n"))
            if not beat or scene is None:
                out.append(line)
                continue
            key = f"{scene}.{beat.group(2)}"
            old = beat.group(3)
            replacement = old if key in AUDITED_RETAKES else authored[key]
            if key in AUDITED_RETAKES and old != authored[key]:
                summary["retakes"].append(key)
                retained += 1
            if replacement != old:
                updated += 1
            out.append(beat.group(1) + replacement + ("\n" if line.endswith("\n") else ""))
        summary["episodes"][ep] = {"scene_count": len({k.split(".")[0] for k in authored}),
                                    "beats": len(authored), "updated": updated,
                                    "audit_retakes": retained}
        if apply:
            path.write_text("".join(out), encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--episodes", nargs="+", default=[f"E{i:02d}" for i in range(4, 15)])
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    print(json.dumps(reconcile(args.source.resolve(), [x.upper() for x in args.episodes],
                               args.apply), indent=2))
