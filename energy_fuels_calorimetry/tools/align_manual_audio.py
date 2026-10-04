"""Align exact, locally supplied scene narration to animation beats.

Uses a local TorchAudio 2.8 Wav2Vec2 acoustic model and CTC forced alignment.
Audio stays local. Nothing is sent to a speech service, and estimated preview
timestamps are never used. Source WAVs must match the current narration text.
"""
from __future__ import annotations

import argparse
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import wave

import numpy as np
import torch
import torchaudio

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from shared.script_parser import load_episode


def normalize(word):
    word = word.replace("’", "'").upper()
    return re.sub(r"[^A-Z']", "", word)


def read_audio(path):
    data = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"
    ])
    return torch.from_numpy(np.frombuffer(data, dtype=np.float32).copy())


def emissions(model, waveform):
    """Bound inference memory with 20-second windows and one-second context.

    Every retained frame uses the model's 320-sample stride on a single global
    time grid. Context frames are discarded, not duplicated at window joins.
    """
    rows, times = [], []
    window, context = 20 * 16000, 16000
    with torch.inference_mode():
        for core_start in range(0, len(waveform), window):
            core_end = min(len(waveform), core_start + window)
            begin = max(0, core_start - context)
            end = min(len(waveform), core_end + context)
            logits, _ = model(waveform[begin:end].unsqueeze(0))
            prob = logits[0].log_softmax(-1).cpu()
            centers = (begin + np.arange(len(prob)) * 320 + 200) / 16000
            keep = (centers >= core_start / 16000) & (centers < core_end / 16000)
            rows.append(prob[keep])
            times.extend(centers[keep].tolist())
    times = np.asarray(times)
    if not np.allclose(np.diff(times), 0.02, atol=1e-6):
        raise ValueError("Acoustic frame timestamps are not contiguous")
    return torch.cat(rows), times


def silence_cut(waveform, low, high):
    """Choose a low-energy cut between the last word and the next word."""
    if high < low:
        raise ValueError("Aligned words overlap at a beat boundary")
    if high - low < 0.04:
        return (low + high) / 2
    candidates = np.linspace(low + 0.01, high - 0.01, max(2, int((high-low) / 0.005)))
    samples = waveform.numpy()
    energy = []
    for t in candidates:
        center = int(round(t * 16000))
        s = samples[max(0, center-160):min(len(samples), center+160)]
        energy.append(float(np.mean(s*s)) if len(s) else float("inf"))
    # For equally quiet samples, prefer the midpoint of the natural gap.
    minimum = min(energy)
    quiet = [i for i, e in enumerate(energy) if e <= minimum + 1e-8]
    best = min(quiet, key=lambda i: abs(candidates[i] - (low+high)/2))
    return float(candidates[best])


def align_scene(scene, source, model, labels):
    waveform = read_audio(source)
    duration = len(waveform) / 16000
    dictionary = {c: i for i, c in enumerate(labels)}
    transcript, word_map = [], []
    for beat in scene.beats:
        for word in beat.text.split():
            clean = normalize(word)
            if not clean:
                raise ValueError(f"{beat.key}: cannot align token {word!r}")
            if transcript:
                transcript.append("|")
            start = len(transcript)
            transcript.extend(clean)
            word_map.append({"word": word, "key": beat.key, "first": start, "last": len(transcript)-1})
    transcript = "".join(transcript)
    tokens = [dictionary[c] for c in transcript]
    probs, timestamps = emissions(model, waveform)
    alignment, scores = torchaudio.functional.forced_align(
        probs.unsqueeze(0), torch.tensor([tokens], dtype=torch.int64), blank=0
    )
    spans = torchaudio.functional.merge_tokens(alignment[0], scores[0].exp(), blank=0)
    if len(spans) != len(tokens) or [s.token for s in spans] != tokens:
        raise ValueError(f"{scene.id}: CTC path does not cover the exact transcript")
    words = []
    for row in word_map:
        chars = spans[row["first"]:row["last"]+1]
        start = max(0, float(timestamps[chars[0].start]) - 0.01)
        end = min(duration, float(timestamps[chars[-1].end-1]) + 0.01)
        words.append({"word": row["word"], "key": row["key"], "start": start, "end": end,
                      "score": sum(s.score for s in chars) / len(chars)})
    greedy = torch.unique_consecutive(probs.argmax(-1)).tolist()
    decoded = "".join(labels[t] for t in greedy if t != 0)
    similarity = SequenceMatcher(None, transcript.replace("|", ""), decoded.replace("|", ""), autojunk=False).ratio()
    boundaries = [0.0]
    for previous, following in zip(words, words[1:]):
        if previous["key"] != following["key"]:
            boundaries.append(silence_cut(waveform, previous["end"], following["start"]))
    boundaries.append(duration)
    if len(boundaries) != len(scene.beats) + 1:
        raise ValueError("Missing beat boundary")
    segments, relative, beat_report = {}, {}, []
    for beat, start, end in zip(scene.beats, boundaries, boundaries[1:]):
        if end - start < 0.5:
            raise ValueError(f"{beat.key}: implausibly short clip")
        selected = [w for w in words if w["key"] == beat.key]
        if " ".join(w["word"] for w in selected) != beat.text:
            raise ValueError(f"{beat.key}: word coverage is incomplete")
        segments[beat.key] = {"file": str(source.resolve()), "start": round(start, 6), "end": round(end, 6)}
        relative[beat.key] = [{"word": w["word"], "start": round(w["start"]-start, 6),
                               "end": round(w["end"]-start, 6), "score": round(float(w["score"]), 4)} for w in selected]
        beat_report.append({"key": beat.key, "start": start, "end": end,
                            "first_words": " ".join(w["word"] for w in selected[:5]),
                            "last_words": " ".join(w["word"] for w in selected[-5:]),
                            "mean_word_score": sum(float(w["score"]) for w in selected)/len(selected),
                            "minimum_edge_score": min(float(w["score"]) for w in selected[:3]+selected[-3:])})
    report = {"scene": scene.id, "duration": duration, "words": len(words), "beats": beat_report,
              "greedy_transcription_similarity": round(similarity, 4),
              "greedy_transcription": decoded.replace("|", " "),
              "method": "Local Wav2Vec2 ASR BASE 960H + TorchAudio 2.8 CTC forced alignment"}
    return segments, relative, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--directory", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--threads", type=int, default=2)
    args = ap.parse_args()
    torch.set_num_threads(args.threads)
    ep = load_episode(args.episode.upper())
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    model = bundle.get_model().eval()
    labels = bundle.get_labels()
    args.output.mkdir(parents=True, exist_ok=True)
    segments, words, reports = {}, {}, []
    for scene in ep.scenes:
        t0 = time.monotonic()
        a, w, report = align_scene(scene, args.directory / f"{scene.id}.wav", model, labels)
        segments.update(a)
        words.update(w)
        reports.append(report)
        print(f"{scene.id}: {len(a)} beats, {report['duration']:.2f}s audio, "
              f"recognition similarity {report['greedy_transcription_similarity']:.3f}, "
              f"{time.monotonic()-t0:.1f}s processing", flush=True)
        (args.output / "segments.json").write_text(json.dumps(segments, indent=2))
        (args.output / "words.json").write_text(json.dumps(words, indent=2))
        (args.output / "alignment-review.json").write_text(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
