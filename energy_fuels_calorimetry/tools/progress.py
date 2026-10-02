"""
Rebuild progress.json from the files on disk (never hand-edit progress.json).

    python tools/progress.py            # writes progress.json and prints a summary

Stage ladder per episode:
  not-started -> scripted -> scenes-coded -> draft-rendered -> narrated (all clips cached)
  -> final-rendered (1080p30 narrated MP4 assembled) -> verified (final QA recorded in checks/qa_status.json)
Hand-entered QA results live in checks/qa_status.json; everything else is derived.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared import config as C  # noqa: E402
from shared.script_parser import parse_script  # noqa: E402
from shared.tts import cached_clip, estimate_duration, load_manifest  # noqa: E402

EPISODES = {
    "E01": "Mole calculations and units that unlock the topic",
    "E02": "Where reaction energy comes from",
    "E03": "Energy profiles and thermochemical equations",
    "E04": "Fuels, biofuels and the carbon cycle",
    "E05": "Food as a chemical energy source",
    "E06": "Combustion equations and gaseous products",
    "E07": "Limiting reactants, excess fuel and gas mixtures",
    "E08": "Measuring combustion energy and efficiency",
    "E09": "Why calorimeters need calibration",
    "E10": "Reaction calorimetry and molar enthalpy",
    "E11": "Temperature graphs, correction and experimental reasoning",
    "E12": "Fair fuel comparisons and sustainability",
    "E13": "Exam workshop A on fuels and combustion",
    "E14": "Exam workshop B on calorimetry and data evaluation",
}


def sha(p: Path) -> str | None:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.exists() else None


def main():
    manifest = load_manifest()
    qa = json.loads((ROOT / "checks" / "qa_status.json").read_text()) if (ROOT / "checks" / "qa_status.json").exists() else {}
    have_key = bool(C.gemini_api_key())
    out = dict(updated=time.strftime("%Y-%m-%dT%H:%M:%S"), tts=dict(provider=C.TTS_PROVIDER, model=C.GEMINI_TTS_MODEL,
               voice=C.GEMINI_TTS_VOICE, api_key_present=have_key), blockers=[], episodes={})
    if not have_key:
        out["blockers"].append("TTS: GEMINI_API_KEY not set in this environment; narration, narrated drafts and "
                               "final renders cannot be produced. Add it as an environment variable and start a new "
                               "session, then run tools/tts_probe.py.")
    total_est = 0.0
    for ep, title in EPISODES.items():
        n = ep[1:].lower()
        spath, cpath = ROOT / "scripts" / f"ep{n}.md", ROOT / "scenes" / f"ep{n}.py"
        e = dict(title=title, script=None, scenes_code=None, stage="not-started", scenes=[])
        if spath.exists():
            sc = parse_script(spath)
            beats = list(sc.beats())
            est = sum(estimate_duration(b.text) + b.pause + C.BEAT_GAP for b in beats) + C.SCENE_TAIL * len(sc.scenes)
            total_est += est
            e["script"] = dict(path=str(spath.relative_to(ROOT)), sha=sha(spath), beats=len(beats),
                               words=sum(b.words for b in beats), est_minutes=round(est / 60, 1),
                               anchors=sc.meta.get("anchors"), coverage=sc.meta.get("coverage"))
            e["stage"] = "scripted"
            audio_ready = sum(1 for b in beats if cached_clip(b.key, b.text, manifest))
            e["audio"] = dict(ready=audio_ready, total=len(beats),
                              seconds=round(sum(manifest[b.key]["duration"] for b in beats
                                                if cached_clip(b.key, b.text, manifest)), 1))
            if cpath.exists():
                e["scenes_code"] = dict(path=str(cpath.relative_to(ROOT)), sha=sha(cpath))
                e["stage"] = "scenes-coded"
            draft_ok = True
            for s in sc.scenes:
                row = dict(id=s.id, title=s.title, beats=len(s.beats),
                           audio_ready=sum(1 for b in s.beats if cached_clip(b.key, b.text, manifest)))
                for tag in ("480p15", "1080p30"):
                    tl = C.TIMELINES / tag / f"{s.id}.json"
                    if tl.exists():
                        d = json.loads(tl.read_text())
                        fresh = [b.text for b in s.beats] == [b["text"] for b in d["beats"]]
                        row[tag] = dict(duration=d["duration"], fresh=fresh,
                                        estimated_beats=sum(1 for b in d["beats"] if b["estimated"]),
                                        layout_warnings=sum(len(b.get("layout", [])) for b in d["beats"]))
                if not row.get("480p15", {}).get("fresh"):
                    draft_ok = False
                e["scenes"].append(row)
            for tag in ("480p15", "1080p30"):
                rep = C.LOGS / f"assemble_{ep}_{tag}.json"
                if rep.exists():
                    e[f"assembled_{tag}"] = {k: v for k, v in json.loads(rep.read_text()).items()
                                             if k in ("output", "final", "narrated", "duration", "captions",
                                                      "transcript", "problems")}
            if e["scenes_code"] and draft_ok and e.get("assembled_480p15"):
                e["stage"] = "draft-rendered"
            if e["audio"]["ready"] == e["audio"]["total"] and e["stage"] == "draft-rendered":
                e["stage"] = "narrated"
            fin = e.get("assembled_1080p30")
            if fin and fin.get("final") and e["stage"] == "narrated":
                e["stage"] = "final-rendered"
                if qa.get(ep, {}).get("final_qa") == "pass":
                    e["stage"] = "verified"
        e["qa"] = qa.get(ep, {})
        out["episodes"][ep] = e
    out["series_est_minutes"] = round(total_est / 60, 1)
    C.PROGRESS.write_text(json.dumps(out, indent=1))
    for ep, e in out["episodes"].items():
        a = e.get("audio", {})
        print(f"{ep} {e['stage']:<15} est {e.get('script', {}) and e['script']['est_minutes']} min  "
              f"audio {a.get('ready', 0)}/{a.get('total', 0)}  {e['title']}")
    print("blockers:", out["blockers"] or "none")


if __name__ == "__main__":
    main()
