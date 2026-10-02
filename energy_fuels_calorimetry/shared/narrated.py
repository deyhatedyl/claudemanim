"""
NarratedScene: a Manim Scene whose timing is driven by narration beats.

    class E01S02_UnitCancel(NarratedScene):
        def construct(self):
            with self.beat("b01") as b:        # narration for beat E01S02.b01 starts here
                self.play(Write(eq), run_time=2)
                b.until(0.6)                     # wait until 60% of the clip has played
                self.play(Indicate(eq[2]))
            # leaving the block waits for the rest of the clip, a short gap, and any
            # scripted thinking pause (shown with an on-screen timer)

* Beat durations come from the measured narration clip (audio/manifest.json) when one exists
  for the exact current text; otherwise a words-per-minute estimate is used and the beat is
  flagged "estimated" (draft previews only).
* Every beat in the scene's script must be used exactly once, in order; the render fails
  otherwise, so scripts and visuals cannot silently drift apart.
* At the end, a timeline JSON (frame-accurate start times) is written to
  renders/timelines/<quality>/<SCENE_ID>.json for audio placement and captions.
  Render with --disable_caching so scene.time counts every written frame.
"""
from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path

from manim import (DOWN, LEFT, RIGHT, UP, UR, Create, FadeIn, FadeOut, Rectangle,
                   RoundedRectangle, Scene, VGroup, config, linear)

from . import config as C
from .script_parser import load_scene
from .style import BG, MUTED, SAFE_BOTTOM, TEXT, T
from .tts import cached_clip, estimate_duration, load_manifest


def quality_tag() -> str:
    return f"{config.pixel_height}p{int(round(config.frame_rate))}"


class _BeatTracker:
    def __init__(self, scene: "NarratedScene", beat, start: float, dur: float):
        self.scene, self.beat, self.start, self.dur = scene, beat, start, dur

    @property
    def elapsed(self) -> float:
        return self.scene.time - self.start

    @property
    def remaining(self) -> float:
        return max(0.0, self.start + self.dur - self.scene.time)

    def until(self, frac: float) -> None:
        """Wait until `frac` of the narration clip has played (no-op if already past)."""
        t = self.start + frac * self.dur - self.scene.time
        if t > 1 / config.frame_rate:
            self.scene.wait(t)

    def rt(self, frac: float, lo: float = 0.4, hi: float = 4.0) -> float:
        """A run_time equal to `frac` of the clip, clamped to [lo, hi] seconds."""
        return min(hi, max(lo, frac * self.dur))


class NarratedScene(Scene):
    SCENE_ID: str = ""

    def setup(self):
        self.camera.background_color = BG
        sid = self.SCENE_ID or type(self).__name__.split("_")[0]
        self.SCENE_ID = sid
        # per-scene TeX cache: parallel renders compiling the same snippet would otherwise race
        tex_dir = C.RENDERS / "media" / "Tex" / sid
        tex_dir.mkdir(parents=True, exist_ok=True)
        config.tex_dir = str(tex_dir)
        text_dir = C.RENDERS / "media" / "texts" / sid
        text_dir.mkdir(parents=True, exist_ok=True)
        config.text_dir = str(text_dir)
        self._script = load_scene(sid)
        self._beats = {b.name: b for b in self._script.beats}
        self._order = [b.name for b in self._script.beats]
        self._used: list[str] = []
        self._timeline: list[dict] = []
        self._manifest = load_manifest()

    # ------------------------------------------------------------ beats
    def beat_duration(self, beat) -> tuple[float, str | None, bool]:
        hit = cached_clip(beat.key, beat.text, self._manifest)
        if hit:
            return float(hit["duration"]), hit["path"], False
        return estimate_duration(beat.text), None, True

    @contextmanager
    def beat(self, name: str, gap: float | None = None):
        if name not in self._beats:
            raise KeyError(f"{self.SCENE_ID}: beat {name} is not in the script")
        expected = self._order[len(self._used)] if len(self._used) < len(self._order) else None
        if name != expected:
            raise RuntimeError(f"{self.SCENE_ID}: beat {name} used out of order (expected {expected})")
        beat = self._beats[name]
        dur, path, est = self.beat_duration(beat)
        start = self.time
        tracker = _BeatTracker(self, beat, start, dur)
        yield tracker
        overrun = self.time - (start + dur)
        if overrun < 0:
            self.wait(-overrun)
        self._used.append(name)
        entry = dict(key=beat.key, start=round(start, 4), speech=round(dur, 4), audio=path,
                     estimated=est, text=beat.text, overrun=round(max(0.0, overrun), 3),
                     pause=beat.pause, layout=self.layout_problems())
        self._timeline.append(entry)
        g = C.BEAT_GAP if gap is None else gap
        if g > 0:
            self.wait(g)
        if beat.pause > 0:
            self.think_timer(beat.pause)

    def think_timer(self, seconds: float, label: str = "Pause and think"):
        """Silent reflection time with a small draining bar in the top-right corner."""
        w = 2.6
        frame = RoundedRectangle(width=w, height=0.16, corner_radius=0.08, stroke_color=MUTED,
                                 stroke_width=2, fill_opacity=0)
        bar = Rectangle(width=w - 0.04, height=0.12, stroke_width=0, fill_color=MUTED, fill_opacity=0.9)
        txt = T(f"{label}  ({int(round(seconds))} s)", size=18, color=MUTED)
        grp = VGroup(txt, VGroup(frame, bar)).arrange(DOWN, buff=0.12)
        grp.to_corner(UR, buff=0.3)
        bar.move_to(frame)
        self.play(FadeIn(grp), run_time=0.3)
        left = bar.get_left()
        self.play(bar.animate.stretch(0.001, 0, about_point=left), run_time=max(0.1, seconds - 0.6),
                  rate_func=linear)
        self.play(FadeOut(grp), run_time=0.3)

    # ------------------------------------------------------------ layout QA
    def layout_problems(self) -> list[str]:
        """Objects outside the frame margins or inside the caption strip at the end of a beat."""
        out = []
        hw = config.frame_width / 2 - 0.15
        hh = config.frame_height / 2 - 0.05
        for m in self.mobjects:
            if not m.get_family() or m.width == 0:
                continue
            l, r = m.get_left()[0], m.get_right()[0]
            bt, tp = m.get_bottom()[1], m.get_top()[1]
            name = type(m).__name__
            txt = getattr(m, "text", None) or getattr(m, "tex_string", None)
            label = f"{name}({txt[:30]!r})" if isinstance(txt, str) else name
            if l < -hw or r > hw or tp > hh:
                out.append(f"off-frame {label} x[{l:.2f},{r:.2f}] y[{bt:.2f},{tp:.2f}]")
            elif bt < SAFE_BOTTOM - 0.02:
                out.append(f"caption-strip {label} bottom {bt:.2f}")
        return out

    # ------------------------------------------------------------ helpers
    def clear(self, *keep, run_time: float = 0.6):
        """Fade out everything on screen except `keep`."""
        keep_ids = set()
        for k in keep:
            keep_ids |= {id(m) for m in k.get_family()}
        gone = [m for m in self.mobjects if id(m) not in keep_ids]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=run_time)

    # ------------------------------------------------------------ teardown
    def tear_down(self):
        self.wait(C.SCENE_TAIL)
        missing = [n for n in self._order if n not in self._used]
        if missing:
            raise RuntimeError(f"{self.SCENE_ID}: beats never narrated: {missing}")
        if not config.write_to_movie:      # still-image renders must not overwrite draft timelines
            return
        out = C.TIMELINES / quality_tag()
        out.mkdir(parents=True, exist_ok=True)
        data = dict(scene=self.SCENE_ID, title=self._script.title, cls=type(self).__name__,
                    fps=config.frame_rate, duration=round(self.time, 4), beats=self._timeline)
        (out / f"{self.SCENE_ID}.json").write_text(json.dumps(data, indent=1))
