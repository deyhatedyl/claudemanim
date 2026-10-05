"""Export clean text for manually generated narration, with stable scene/beat IDs."""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.config import GEMINI_TTS_STYLE
from shared.script_parser import load_episode
from shared.tts import estimate_duration, manual_text_hash

PROMPT = (
    GEMINI_TTS_STYLE + "\n\n"
    "Read only the supplied narration text, exactly as written, without adding an introduction, "
    "summary, commentary or music. Keep the same voice across every file. Aim for about 145 words "
    "per minute, with natural short pauses at sentence boundaries. Read decimal numbers digit by "
    "digit after the point and articulate chemical names and units clearly. Do not add long "
    "thinking pauses: these are inserted separately in the video. Do not speak filenames, scene "
    "identifiers, beat identifiers, markdown or this direction."
)


def export(episodes: list[str], dest: Path):
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "Voice-direction.txt").write_text(PROMPT + "\n")
    index = []
    for episode in episodes:
        ep = load_episode(episode.upper())
        folder = dest / ep.id
        (folder / "scenes").mkdir(parents=True, exist_ok=True)
        (folder / "beats").mkdir(exist_ok=True)
        all_text = []
        for scene in ep.scenes:
            scene_text = "\n\n".join(b.text for b in scene.beats)
            (folder / "scenes" / f"{scene.id}.txt").write_text(scene_text + "\n")
            all_text.append(scene_text)
            for b in scene.beats:
                (folder / "beats" / f"{b.key}.txt").write_text(b.text + "\n")
                index.append({"episode": ep.id, "scene": scene.id, "scene_title": scene.title,
                              "key": b.key, "text": b.text, "text_hash": manual_text_hash(b.text),
                              "estimated_speech_seconds": round(estimate_duration(b.text), 3),
                              "thinking_pause_after_seconds": b.pause})
        (folder / f"{ep.id}-Full-narration.txt").write_text("\n\n".join(all_text) + "\n")
    (dest / "beat-index.json").write_text(json.dumps(index, indent=2))
    names = ", ".join(episodes)
    counts = "; ".join(f"{ep}: {len(load_episode(ep).scenes)} scenes" for ep in episodes)
    readme = f"""# Narration for {names}

Use Voice-direction.txt as the voice/style instruction. The narration text is already written in
spoken form: chemical formulas, numbers and units are spelled out for the voice.

Choose one of these equivalent recording formats:

* **Scene files (recommended):** generate one audio file per text in each episode's scenes folder.
  Keep its scene ID as the WAV name. Short chunks are easier to regenerate
  and align accurately. Scene counts: {counts}.
* **Whole episodes:** use each episode's Full-narration.txt and return its episode ID as the
  WAV name. These need speech alignment before the narration beats
  can be timed precisely. The preview's estimated timestamps are not final audio timestamps.
* **Beat files:** use the smaller files in each beats folder and preserve filenames such as
  {episodes[0]}S01.b01.wav. These can be imported directly without speech alignment.

WAV is preferred; MP3 or M4A is also usable. Keep exactly the script's words and the same voice.
Don't read identifiers or instructions aloud, add background music, or add long thinking pauses.
The renderer adds the question-attempt and retrieval pauses separately, using beat-index.json.

Send the audio files back in this chat (a ZIP is convenient). Whole-scene or whole-episode audio
will be split using speech alignment and checked against the script, then the scenes will be
re-rendered using the measured beat durations and muxed with captions. The silent preview is
for visual review; simply laying a full narration file over it will not produce correct sync.
"""
    (dest / "README.md").write_text(readme)
    zip_path = dest.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(dest.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(dest))
    print(json.dumps({"zip": str(zip_path), "episodes": episodes, "beats": len(index)}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="*", default=["E01", "E02", "E03"])
    ap.add_argument("--output", type=Path, default=ROOT / "delivery/Narration-E01-E03")
    a = ap.parse_args()
    export(a.episodes, a.output)


if __name__ == "__main__":
    main()
