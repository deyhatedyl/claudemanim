"""Build standalone episode TTS files, transcripts and a return-audio helper.

python tools/build_narration_pack.py E04 E05 --output delivery/Narration-E04-E05
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pprint
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.script_parser import load_episode
from tools.export_narration import export


def build(episodes, dest):
    episodes = [f"E{int(ep.lower().removeprefix('ep').removeprefix('e')):02d}" for ep in episodes]
    if not episodes or any(not 1 <= int(ep[1:]) <= 14 for ep in episodes):
        raise ValueError("Choose episodes 1–14")
    export(episodes, dest)
    template = (ROOT / "tools/narration_runner.py").read_text()
    manifest = {}
    for ep in episodes:
        episode = load_episode(ep)
        beats = [dict(scene=s.id, key=b.key, text=b.text) for s in episode.scenes for b in s.beats]
        script = template.replace("BEATS = []", "BEATS = " + pprint.pformat(beats, width=100, sort_dicts=False))
        script = script.replace("DEFAULT_PREFIX = None", f"DEFAULT_PREFIX = {ep!r}")
        script = script.replace("Episodes 1-14", f"{ep}: {episode.title}")
        script = script.replace("Run: python3.12 narration_tts.py ep1 --lite",
                                f"Run: python3.12 narration_{ep.lower()}.py --lite")
        path = dest / f"narration_{ep.lower()}.py"
        path.write_text(script)
        manifest[ep] = {"title": episode.title, "scenes": {s.id: {
            "text_sha256": hashlib.sha256("\n\n".join(b.text for b in s.beats).encode()).hexdigest(),
            "beats": len(s.beats),
        } for s in episode.scenes}}
    (dest / "scene-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (dest / "zip_audio.py").write_text(ZIP_HELPER)
    (dest / "requirements.txt").write_text("google-genai\n")
    commands = "\n\n".join(
        f"# {ep}: {manifest[ep]['title']}\n"
        f"env -u GEMINI_API_KEY -u GOOGLE_API_KEY python3.12 \\\n"
        f"  ~/Downloads/VCE-Chemistry-Videos/Energy-Fuels-Calorimetry/narration_{ep.lower()}.py --lite\n"
        f"python3.12 ~/Downloads/VCE-Chemistry-Videos/Energy-Fuels-Calorimetry/zip_audio.py {ep}"
        for ep in episodes)
    guide = f"""# Generate narration for {', '.join(episodes)}

Put the contents of this folder in:
`~/Downloads/VCE-Chemistry-Videos/Energy-Fuels-Calorimetry/`

Install once if needed:
```bash
python3.12 -m pip install --upgrade google-genai
```

The Python files include the complete narration; no separate text files are required.
They use your working Gemini request format and your existing **Melb Teacher F1** voice.
Your Electrochemistry `voice_samples_melb/voice_ids.txt` is found automatically.
If that file moved, add `--voice-file /path/to/voice_ids.txt`.
The key prompt is hidden. The commands below clear old key environment variables to avoid
the authentication problem you encountered before. Paste the working key into Terminal.

Each script generates one WAV per scene in `audio/raw/`. Completed valid WAVs are kept
when you rerun or switch models. `--force` regenerates the selected files.
If the daily Lite limit is reached, rerun that episode without `--lite`.
Add `--dry-run` to list the selection without an API call.

## Commands

Run one episode, then package it. The ZIP helper checks that every expected scene is
present, complete and matches the current transcript before making the ZIP.

```bash
{commands}
```

Return the episode audio ZIPs here. The video will be aligned to the actual speech,
and re-rendered at 1080p30 without burned-in or embedded subtitles.
Silent visual previews have estimated timing.
Keep the same transcript and voice, with no music or long thinking pauses;
question-attempt pauses are added separately in the video.

The episode folders contain readable scene and beat transcripts. `beat-index.json`
records the exact words and intended thinking pauses. Do not read those identifiers aloud.
"""
    (dest / "START-HERE.md").write_text(guide)
    (dest / "Commands.txt").write_text(commands + "\n")
    archive = dest.with_suffix(".zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(dest.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                z.write(p, p.relative_to(dest))
    print(json.dumps({"zip": str(archive), "episodes": len(manifest),
                      "scenes": sum(len(v['scenes']) for v in manifest.values())}))


ZIP_HELPER = '''"""Validate and ZIP the audio for one episode. Usage: python3.12 zip_audio.py E04"""
import argparse
import importlib.util
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("episode")
p.add_argument("--input", type=Path, default=ROOT / "audio" / "raw")
a = p.parse_args()
ep = "E" + str(int(a.episode.lower().removeprefix("ep").removeprefix("e"))).zfill(2)
manifest = json.loads((ROOT / "scene-manifest.json").read_text())
if ep not in manifest:
    p.error(f"{ep} is not included in this pack")
spec = importlib.util.spec_from_file_location("episode_tts", ROOT / f"narration_{ep.lower()}.py")
tts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tts)
source = a.input.expanduser().resolve()
jobs = tts.selected_jobs(ep, False)
bad = [sid for sid, text in jobs
       if not (source / f"{sid}.wav.json").is_file()
       or not tts.ready(source / f"{sid}.wav", text)]
if bad:
    p.error("Missing, incomplete or outdated WAVs (or missing transcript metadata): " + ", ".join(bad))
target = ROOT / "audio" / f"{ep}-audio.zip"
target.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
    for sid, _ in jobs:
        z.write(source / f"{sid}.wav", f"{sid}.wav")
        meta = source / f"{sid}.wav.json"
        if meta.is_file():
            z.write(meta, meta.name)
print(f"{len(jobs)}/{len(jobs)} scenes validated. Send {target} here for syncing.")
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("episodes", nargs="+")
    ap.add_argument("--output", type=Path, default=ROOT / "delivery/Narration-E04-E14")
    a = ap.parse_args()
    build(a.episodes, a.output.resolve())


if __name__ == "__main__":
    main()
