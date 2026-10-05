"""
Assemble one episode from its rendered scenes: concatenate video, lay narration clips at the
frame-accurate times recorded in the scene timelines, normalise loudness, write separate
SRT/VTT captions and a transcript, and export an MP4 without subtitles.

    python tools/assemble.py E01 -q l      # draft
    python tools/assemble.py E01 -q h      # final (requires narration for every beat)

Outputs
  final:  renders/final/E01_<slug>.mp4, captions/E01_<slug>.srt|.vtt, captions/E01_<slug>_transcript.md
  draft:  renders/draft/E01_<slug>__<tag>__narrated|SILENT-estimated-timing.mp4 (+ .srt/.vtt beside it)
A draft without narration has NO audio stream and is never labelled final.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared import config as C  # noqa: E402
from shared.script_parser import load_episode  # noqa: E402
from tools.render import QUALITY, episode_scenes  # noqa: E402

FFMPEG = "ffmpeg"


def ffprobe_duration(p: Path) -> float:
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "default=nw=1:nk=1", str(p)])
    return float(out)


def slug(title: str) -> str:
    t = re.sub(r"^E\d\d\s+", "", title)
    return re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_")


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p), "rb") as w:
        if w.getframerate() != C.AUDIO_RATE or w.getnchannels() != 1 or w.getsampwidth() != 2:
            raise ValueError(f"{p}: expected {C.AUDIO_RATE} Hz mono 16-bit")
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def write_wav(p: Path, x: np.ndarray) -> None:
    y = np.clip(x, -1, 1)
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(C.AUDIO_RATE)
        w.writeframes((y * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- captions
def chunk_text(text: str, max_chars: int = 84) -> list[str]:
    sents = re.split(r"(?<=[.?!])\s+", text.strip())
    out = []
    for s in sents:
        while len(s) > max_chars:
            cut = max((m.end() for m in re.finditer(r"[,;:]\s", s[:max_chars])), default=0)
            if cut < max_chars * 0.4:
                cut = s.rfind(" ", 0, max_chars) + 1
            out.append(s[:cut].strip())
            s = s[cut:].strip()
        if s:
            out.append(s)
    return out


def two_lines(s: str, width: int = 42) -> str:
    if len(s) <= width:
        return s
    mid = len(s) // 2
    cands = [m.start() for m in re.finditer(" ", s)]
    best = min(cands, key=lambda i: abs(i - mid))
    return s[:best] + "\n" + s[best + 1:]


def fmt_ts(t: float, sep: str = ",") -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def build_cues(beats_abs: list[dict], word_timings: dict | None = None) -> list[tuple[float, float, str]]:
    cues = []
    for b in beats_abs:
        chunks = chunk_text(b["text"])
        if word_timings is not None:
            words = word_timings[b["key"]]
            if [w["word"] for w in words] != b["text"].split():
                raise ValueError(f"{b['key']}: caption alignment does not match narration")
            cursor = 0
            for c in chunks:
                selected = words[cursor:cursor + len(c.split())]
                if [w["word"] for w in selected] != c.split():
                    raise ValueError(f"{b['key']}: caption chunk has incomplete word coverage")
                s = b["abs_start"] + max(0, selected[0]["start"] - 0.06)
                e = b["abs_start"] + min(b["speech"], selected[-1]["end"] + 0.15)
                if e <= s:
                    raise ValueError(f"{b['key']}: invalid aligned caption interval")
                cues.append((s, e, two_lines(c)))
                cursor += len(selected)
            continue
        total = sum(len(c) for c in chunks)
        t = b["abs_start"]
        for c in chunks:
            d = b["speech"] * len(c) / total
            cues.append((t, t + max(d, 0.8), two_lines(c)))
            t += d
    # never overlap
    fixed = []
    for i, (s, e, txt) in enumerate(cues):
        if i + 1 < len(cues):
            e = min(e, cues[i + 1][0] - 0.04)
        fixed.append((s, e, txt))
    return fixed


def write_srt(p: Path, cues):
    p.write_text("\n".join(f"{i}\n{fmt_ts(s)} --> {fmt_ts(e)}\n{t}\n" for i, (s, e, t) in enumerate(cues, 1)))


def write_vtt(p: Path, cues):
    p.write_text("WEBVTT\n\n" + "\n".join(f"{fmt_ts(s, '.')} --> {fmt_ts(e, '.')}\n{t}\n" for s, e, t in cues))


def mmss(t: float) -> str:
    return f"{int(t // 60):02d}:{int(t % 60):02d}"


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("-q", "--quality", default="l", choices=QUALITY)
    ap.add_argument("--word-timings", type=Path,
                    help="Optional local word alignment JSON for measured caption timing")
    a = ap.parse_args()
    ep = a.episode.upper()
    tag = QUALITY[a.quality][1]
    script = load_episode(ep)
    classes = episode_scenes(ep)
    vid_dir = C.RENDERS / "media" / "videos" / f"ep{ep[1:].lower()}" / tag
    tl_dir = C.TIMELINES / tag

    offset = 0.0
    beats_abs, scene_rows, problems = [], [], []
    audio_parts, have_audio, n_beats = [], 0, 0
    videos = []
    for cls in classes:
        sid = cls.split("_")[0]
        v = vid_dir / f"{cls}.mp4"
        tl = json.loads((tl_dir / f"{sid}.json").read_text())
        vd = ffprobe_duration(v)
        if abs(vd - tl["duration"]) > 2.0 / tl["fps"]:
            problems.append(f"{sid}: video {vd:.3f}s vs timeline {tl['duration']:.3f}s")
        # script/timeline drift: the timeline must contain exactly the current script text
        cur = [b.text for b in script.scene(sid).beats]
        if cur != [b["text"] for b in tl["beats"]]:
            problems.append(f"{sid}: timeline is stale relative to the script; re-render")
        buf = np.zeros(int(round(vd * C.AUDIO_RATE)), dtype=np.float32)
        for b in tl["beats"]:
            n_beats += 1
            beats_abs.append(dict(b, abs_start=offset + b["start"], scene=sid))
            if b["audio"]:
                clip = read_wav(ROOT / b["audio"])
                i0 = int(round(b["start"] * C.AUDIO_RATE))
                seg = clip[: max(0, len(buf) - i0)]
                buf[i0:i0 + len(seg)] += seg
                have_audio += 1
            if b["overrun"] > 0.75:
                problems.append(f"{b['key']}: visuals overrun narration by {b['overrun']:.2f}s")
        audio_parts.append(buf)
        scene_rows.append(dict(scene=sid, title=tl["title"], start=offset, duration=vd))
        videos.append(v)
        offset += vd

    narrated = have_audio == n_beats and n_beats > 0
    final = narrated and a.quality == "h"
    base = f"{ep}_{slug(script.title)}"
    if final:
        out_mp4 = C.RENDERS / "final" / f"{base}.mp4"
        cap_base = C.CAPTIONS / base
    else:
        kind = "narrated" if narrated else "SILENT-estimated-timing"
        out_mp4 = C.RENDERS / "draft" / f"{base}__{tag}__{kind}.mp4"
        cap_base = out_mp4.with_suffix("")
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    cap_base.parent.mkdir(parents=True, exist_ok=True)

    word_timings = json.loads(a.word_timings.read_text()) if a.word_timings else None
    cues = build_cues(beats_abs, word_timings)
    srt, vtt = cap_base.with_suffix(".srt"), cap_base.with_suffix(".vtt")
    write_srt(srt, cues)
    write_vtt(vtt, cues)
    tr = [f"# {script.title}", "", f"Runtime {mmss(offset)}. Narration transcript (matches the captions).", ""]
    for row in scene_rows:
        tr += [f"## [{mmss(row['start'])}] {row['scene']} {row['title']}", ""]
        tr += [b["text"] + ("  *(pause)*" if b["pause"] else "") for b in beats_abs if b["scene"] == row["scene"]]
        tr.append("")
    tr_path = Path(str(cap_base) + "_transcript.md")
    tr_path.write_text("\n".join(tr))

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        lst = td / "list.txt"
        lst.write_text("".join(f"file '{v}'\n" for v in videos))
        vcat = td / "video.mp4"
        subprocess.check_call([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                               "-c", "copy", str(vcat)])
        cmd = [FFMPEG, "-y", "-v", "error", "-i", str(vcat)]
        if narrated:
            raw = td / "raw.wav"
            write_wav(raw, np.concatenate(audio_parts))
            meas = subprocess.run([FFMPEG, "-i", str(raw), "-af",
                                   f"loudnorm=I={C.TARGET_LUFS}:TP={C.TRUE_PEAK}:LRA=11:print_format=json",
                                   "-f", "null", "-"], capture_output=True, text=True).stderr
            m = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
            norm = td / "norm.wav"
            subprocess.check_call([FFMPEG, "-y", "-v", "error", "-i", str(raw), "-af",
                                   f"loudnorm=I={C.TARGET_LUFS}:TP={C.TRUE_PEAK}:LRA=11:"
                                   f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
                                   f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
                                   f"offset={m['target_offset']}:linear=true", "-ar", "48000", str(norm)])
            cmd += ["-i", str(norm), "-map", "0:v:0", "-map", "1:a:0", "-sn",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k"]
        else:
            cmd += ["-map", "0:v:0", "-an", "-sn", "-c:v", "copy"]
        cmd += ["-metadata", f"title={script.title}",
                "-movflags", "+faststart", str(out_mp4)]
        subprocess.check_call(cmd)

    dur = ffprobe_duration(out_mp4)
    report = dict(episode=ep, quality=tag, output=str(out_mp4.relative_to(ROOT)), final=final,
                  narrated=narrated, beats=n_beats, beats_with_audio=have_audio, duration=round(dur, 2),
                  scenes=scene_rows, captions=[str(srt.relative_to(ROOT)), str(vtt.relative_to(ROOT))],
                  transcript=str(tr_path.relative_to(ROOT)), problems=problems)
    rep = C.LOGS / f"assemble_{ep}_{tag}.json"
    rep.write_text(json.dumps(report, indent=1))
    print(json.dumps({k: report[k] for k in ("output", "final", "narrated", "beats", "beats_with_audio", "duration")}))
    for p in problems:
        print("PROBLEM:", p)


if __name__ == "__main__":
    main()
