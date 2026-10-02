"""
Generate (or reuse) narration clips for one or more episodes.

    python tools/gen_audio.py E01                # all beats of Episode 01
    python tools/gen_audio.py E01 E02 --jobs 4
    python tools/gen_audio.py E01 --dry-run      # report what would be generated

Clips are cached by beat key + content hash (see shared/tts.py); unchanged beats are reused, so
re-running after a small script edit only synthesises the edited beats. The manifest is saved
after every clip, so an interrupted run resumes where it stopped.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.script_parser import load_episode  # noqa: E402
from shared.tts import TTSUnavailable, cached_clip, ensure_clip, load_manifest, save_manifest  # noqa: E402

LOCK = threading.Lock()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="+")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    manifest = load_manifest()
    todo = []
    for ep in a.episodes:
        script = load_episode(ep.upper())
        for b in script.beats():
            if not cached_clip(b.key, b.text, manifest):
                todo.append(b)
    total = sum(1 for ep in a.episodes for _ in load_episode(ep.upper()).beats())
    print(f"{total} beats; {total - len(todo)} cached; {len(todo)} to synthesise")
    if a.dry_run or not todo:
        return

    def work(b):
        local = {}
        try:
            e = ensure_clip(b.key, b.text, local)
        except TTSUnavailable as err:
            return b.key, None, str(err)
        with LOCK:
            manifest[b.key] = e
            save_manifest(manifest)
        return b.key, e, None

    errors = []
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for key, e, err in ex.map(work, todo):
            if err:
                errors.append((key, err))
                print(f"ERR {key}: {err[:200]}", flush=True)
            else:
                flag = "" if e["wpm"] and 100 <= e["wpm"] <= 185 else "  <-- unusual rate, listen"
                print(f"OK  {key}: {e['duration']:.1f}s {e['wpm']} wpm{flag}", flush=True)
    if errors:
        print(f"{len(errors)} clips failed; re-run to retry (successful clips are cached)")
        sys.exit(1)


if __name__ == "__main__":
    main()
