"""
Parser for narration scripts (scripts/epNN.md).

Format
------
    # E01 Episode title
    meta: target=10-14 min; anchors=Q01,Q02; coverage=C01

    ## E01S01 | Scene title
    objective: what the learner should be able to do after this scene
    onscreen: the main objects shown
    transitions: how the scene enters/leaves
    checks: answer/source checks relevant to this scene

    [b01] Spoken narration. Written as it should be SAID: symbols, subscripts and units
    are spelled out ("kilojoules per mole", "C O two").
    [b02 pause=10] A beat followed by a silent 10-second thinking pause.

Lines beginning with % are comments. A beat runs until the next [bNN] or ## heading.
Beat keys are "<SCENEID>.<beat>", e.g. "E01S01.b02".
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from .config import SCRIPTS

BEAT_RE = re.compile(r"^\[(b\d+[a-z]?)((?:\s+\w+=[\w.]+)*)\]\s*(.*)$")
SCENE_RE = re.compile(r"^##\s+(E\d\d[A-Z]?S\d\d[a-z]?)\s*\|\s*(.+)$")


@dataclass
class Beat:
    key: str
    scene: str
    name: str
    text: str
    pause: float = 0.0
    opts: dict = field(default_factory=dict)

    @property
    def words(self) -> int:
        return len(self.text.split())


@dataclass
class SceneScript:
    id: str
    title: str
    meta: dict = field(default_factory=dict)
    beats: list[Beat] = field(default_factory=list)


@dataclass
class EpisodeScript:
    id: str
    title: str
    meta: dict
    scenes: list[SceneScript]
    path: Path

    def beats(self):
        for s in self.scenes:
            yield from s.beats

    def scene(self, sid: str) -> SceneScript:
        for s in self.scenes:
            if s.id == sid:
                return s
        raise KeyError(sid)


def parse_script(path: Path) -> EpisodeScript:
    title, ep_id, meta = "", "", {}
    scenes: list[SceneScript] = []
    cur_scene: SceneScript | None = None
    cur_beat: Beat | None = None

    def close_beat():
        nonlocal cur_beat
        if cur_beat is not None:
            cur_beat.text = " ".join(cur_beat.text.split())
            if not cur_beat.text:
                raise ValueError(f"{path.name}: empty beat {cur_beat.key}")
            cur_scene.beats.append(cur_beat)
            cur_beat = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("%"):
            continue
        if line.startswith("# ") and not ep_id:
            title = line[2:].strip()
            ep_id = title.split()[0]
            continue
        m = SCENE_RE.match(line)
        if m:
            close_beat()
            cur_scene = SceneScript(m.group(1), m.group(2).strip())
            scenes.append(cur_scene)
            continue
        m = BEAT_RE.match(line)
        if m:
            close_beat()
            if cur_scene is None:
                raise ValueError(f"{path.name}: beat before any scene heading")
            opts = dict(kv.split("=") for kv in m.group(2).split())
            pause = float(opts.pop("pause", 0))
            name = m.group(1)
            cur_beat = Beat(f"{cur_scene.id}.{name}", cur_scene.id, name, m.group(3), pause, opts)
            continue
        if cur_beat is not None:
            cur_beat.text += " " + line.strip()
            continue
        kv = re.match(r"^(\w+):\s*(.*)$", line)
        if kv:
            target = cur_scene.meta if cur_scene is not None else meta
            if kv.group(1) == "meta":
                for item in kv.group(2).split(";"):
                    if "=" in item:
                        k, v = item.split("=", 1)
                        meta[k.strip()] = v.strip()
            else:
                target[kv.group(1)] = kv.group(2)
    close_beat()
    keys = [b.key for s in scenes for b in s.beats]
    dup = {k for k in keys if keys.count(k) > 1}
    if dup:
        raise ValueError(f"{path.name}: duplicate beat keys {sorted(dup)}")
    return EpisodeScript(ep_id, title, meta, scenes, path)


@lru_cache(maxsize=None)
def load_episode(ep_id: str) -> EpisodeScript:
    """ep_id like 'E01' -> scripts/ep01.md"""
    return parse_script(SCRIPTS / f"ep{ep_id[1:].lower()}.md")


def load_scene(scene_id: str) -> SceneScript:
    ep = re.match(r"(E\d\d[A-Z]?)S", scene_id).group(1)
    return load_episode(ep).scene(scene_id)
