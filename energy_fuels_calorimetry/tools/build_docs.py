"""
Build the learner documents and project indexes from their single sources.

    python tools/build_docs.py

Writes
  questions/worksheet.md            prompts only (no answers), grouped by episode
  solutions/worked_solutions.md     working per part, indicative marks per step, traps, where taught
  coverage_matrix.md                brief coverage IDs -> episodes, anchor questions, scenes
  series_index.md                   viewing order, durations, file paths, status

Sources: questions/bank.py (prompts, answers, traps), scripts/epNN.md (titles, scenes, coverage tags),
scenes/epNN.py (the mark tallies shown on screen, read with ast so the documents match the videos),
logs/assemble_*.json and checks/qa_status.json (durations and status).
solutions/formula_and_method_sheet.md is written by hand and not touched here.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "questions"))

from bank import BANK, BY_ID, SHARED_DATA, marks_total  # noqa: E402
from shared.script_parser import load_episode  # noqa: E402

EPISODES = [f"E{i:02d}" for i in range(1, 15)]
NOTICE = ("All questions are original practice questions written for this series. They are not official "
          "VCAA examination questions, and the marks shown are indicative only, not an official marking scheme.")

# Questions whose mark split is narrated rather than drawn as a tally on screen (wording follows the narration).
MANUAL_TALLIES = {
    "Q10": [(2, "a: energy per 100 g for each food"), (2, "b: energy in one serving of each food"),
            (1, "c: both comparisons stated, each on its basis")],
    "Q23": [(2, "fuel energy input for each fuel"), (2, "mass of each fuel"),
            (2, "lifecycle emissions for each fuel"), (1, "evaluation of the mass-based claim")],
    "Q24": [(2, "a: first supported comparison (feedstock; circular use)"),
            (2, "b: second supported comparison (listed energy and water)"),
            (1, "c: a trade-off or data limit"), (1, "d: recommendation consistent with stated priorities")],
}


def md(s: str) -> str:
    """Bank text -> Markdown (true subscript for ΔH_c)."""
    return s.replace("ΔH_c", "ΔH<sub>c</sub>").replace("V_m", "V<sub>m</sub>")


def episode_info():
    info = {}
    for ep in EPISODES:
        e = load_episode(ep)
        title = e.title.split(" ", 1)[1]
        anchors = [a.strip() for a in e.meta.get("anchors", "").split(",") if a.strip()]
        cover = [c.strip() for c in e.meta.get("coverage", "").split(",") if c.strip()]
        info[ep] = dict(title=title, anchors=anchors, coverage=cover, target=e.meta.get("target", ""),
                        scenes=[(s.id, s.title, s.meta) for s in e.scenes])
    return info


def scene_tallies() -> dict[str, list[tuple[int, str]]]:
    """Mark tallies drawn in the practice scenes, keyed by question ID."""
    out = {}
    for f in sorted((ROOT / "scenes").glob("ep*.py")):
        tree = ast.parse(f.read_text())
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            for node in ast.walk(cls):
                if not (isinstance(node, ast.Call) and getattr(node.func, "id", "") == "mark_tally"):
                    continue
                rows = ast.literal_eval(node.args[0])
                title = next((ast.literal_eval(k.value) for k in node.keywords if k.arg == "title"), "")
                m = re.search(r"Q\d\d", title or "") or re.search(r"Q\d\d", cls.name)
                if m:
                    out[m.group(0)] = rows
    out.update({k: v for k, v in MANUAL_TALLIES.items() if k not in out})
    return out


def assemble_log(ep: str) -> dict | None:
    for tag in ("1080p30", "720p30", "480p15"):
        p = ROOT / "logs" / f"assemble_{ep}_{tag}.json"
        if p.exists():
            return json.loads(p.read_text())
    return None


def where_taught(qid: str, info, logs) -> list[str]:
    out = []
    for ep, e in info.items():
        for sid, title, meta in e["scenes"]:
            if qid in title or qid in meta.get("onscreen", ""):
                t = ""
                lg = logs.get(ep)
                if lg:
                    st = next((s["start"] for s in lg["scenes"] if s["scene"] == sid), None)
                    if st is not None:
                        t = f" (≈{int(st // 60)}:{int(st % 60):02d} in the draft)"
                out.append(f"{sid} “{title}”{t}")
    return out


def mmss(sec: float) -> str:
    return f"{int(sec // 60)}:{int(round(sec % 60)):02d}"


# --------------------------------------------------------------------------------------------- worksheet
def build_worksheet(info):
    L = ["# Worksheet: Energy, fuels and calorimetry (questions only)", "",
         f"> {NOTICE}", "",
         "Attempt each question before watching its worked solution. Show every quantity with its unit, "
         "keep unrounded values until the final answer, and check that each answer is plausible.", "",
         f"**Data for all questions.** {md(SHARED_DATA)}", "",
         f"Total: {len(BANK)} questions, {sum(marks_total(q['id']) for q in BANK)} marks.", ""]
    for ep in EPISODES:
        qs = [q for q in BANK if q["episode"] == int(ep[1:])]
        if not qs:
            continue
        L += [f"## Episode {ep[1:]}: {info[ep]['title']}", ""]
        for q in qs:
            L += [f"### {q['id']}. {md(q['title'])} ({marks_total(q['id'])} marks)", "", md(q["stem"]), ""]
            visual = q.get("visual", {})
            if visual.get("type") == "table":
                rows = visual["rows"]
                L += ["| " + " | ".join(md(str(c)).replace("|", "\\|") for c in rows[0]) + " |",
                      "|" + "---|" * len(rows[0])]
                L += ["| " + " | ".join(md(str(c)).replace("|", "\\|") for c in row) + " |"
                      for row in rows[1:]]
                L += [""]
            elif visual.get("type") == "temperature":
                L += [f"![{q['id']}: measured temperatures; no solution fit](figures/{q['id']}-temperature.svg)", "",
                      "| Time (s) | Temperature (°C) |", "|---|---|"]
                L += [f"| {t} | {temp:.1f} |" for t, temp in visual["points"]
                      if t >= visual["cooling_start"]]
                L += [""]
            for lab, txt, mk in q["parts"]:
                L += [f"**{lab}.** {md(txt)} *[{mk} mark{'s' if mk > 1 else ''}]*", "",
                      "&nbsp;", ""]
            L += [""]
    (ROOT / "questions" / "worksheet.md").write_text("\n".join(L).rstrip() + "\n")


# --------------------------------------------------------------------------------------------- solutions
def build_solutions(info, tallies, logs):
    L = ["# Worked solutions with indicative marks and traps", "",
         f"> {NOTICE}", "",
         "Each solution gives the working for every part, the indicative mark allocation shown in the "
         "video (each mark is attached to an observable step), the main trap, and where the question is "
         "worked in the series. Numerical values are recomputed independently in "
         "`checks/verify_anchors.py` (see `checks/numerical_check_record.md`).", "",
         f"**Data for all questions.** {md(SHARED_DATA)}", ""]
    for ep in EPISODES:
        qs = [q for q in BANK if q["episode"] == int(ep[1:])]
        if not qs:
            continue
        L += [f"## Episode {ep[1:]}: {info[ep]['title']}", ""]
        for q in qs:
            qid = q["id"]
            L += [f"### {qid}. {md(q['title'])} ({marks_total(qid)} marks)", "",
                  f"**Question.** {md(q['stem'])}", ""]
            for (lab, txt, mk), ans in zip(q["parts"], q["answers"]):
                body = re.sub(r"^[a-z]\.\s*", "", ans)
                L += [f"**{lab}.** {md(txt)} *[{mk}]*", "", f"> {md(body)}", ""]
            rows = tallies.get(qid)
            if rows:
                assert sum(r[0] for r in rows) == marks_total(qid), f"{qid}: tally does not match part marks"
                L += ["**Indicative marks**", "", "| Marks | Observable step |", "|---|---|"]
                L += [f"| {m} | {md(t)} |" for m, t in rows]
                L += [f"| **{marks_total(qid)}** | **total** |", ""]
            L += [f"**Trap.** {md(q['trap'])}", ""]
            wt = where_taught(qid, info, logs)
            if wt:
                L += ["**Worked in:** " + "; ".join(wt), ""]
    (ROOT / "solutions" / "worked_solutions.md").write_text("\n".join(L).rstrip() + "\n")


# --------------------------------------------------------------------------------------------- coverage
def build_coverage(info):
    ids = [f"C{i:02d}" for i in range(1, 29)]
    by_c = {c: [] for c in ids}
    for ep, e in info.items():
        for c in e["coverage"]:
            by_c.setdefault(c, []).append(ep)
    L = ["# Coverage matrix", "",
         "Maps each coverage item of the production brief (`brief/production_brief.md`, items C01–C28) to the "
         "episodes that teach or revisit it and to those episodes' anchor questions. Item wording is "
         "defined in the brief and is not repeated here. Generated by `tools/build_docs.py` from the "
         "`coverage=` tags in `scripts/epNN.md`.", "",
         "| Item | Episodes | Anchor questions in those episodes | Status |", "|---|---|---|---|"]
    gaps = []
    for c in ids:
        eps = by_c.get(c, [])
        qs = sorted({q for ep in eps for q in info[ep]["anchors"]})
        status = "covered" if eps else "**not tagged in any episode: check against the brief**"
        if not eps:
            gaps.append(c)
        L.append(f"| {c} | {', '.join(eps) or '–'} | {', '.join(qs) or '–'} | {status} |")
    L += ["", "## By episode", "", "| Episode | Title | Coverage items | Anchor questions |", "|---|---|---|---|"]
    for ep, e in info.items():
        L.append(f"| {ep} | {e['title']} | {', '.join(e['coverage'])} | {', '.join(e['anchors'])} |")
    if gaps:
        L += ["", f"**Open check:** {', '.join(gaps)} carr{'ies' if len(gaps) == 1 else 'y'} no episode tag. "
              "Confirm against the brief whether the item is taught under another tag or needs a scene."]
    (ROOT / "coverage_matrix.md").write_text("\n".join(L).rstrip() + "\n")
    return gaps


# --------------------------------------------------------------------------------------------- index
def build_index(info, logs):
    qa = json.loads((ROOT / "checks" / "qa_status.json").read_text())
    L = ["# Series index", "",
         "Viewing order and latest local outputs. E01–E03 were delivered earlier and are unchanged in "
         "this continuation. E04–E14 have silent 720p30 previews with estimated timing; narrated "
         "1080p30 finals await the learner's audio. Future MP4s contain no burned-in captions or "
         "embedded subtitles. Optional captions and transcripts are separate files.", "",
         "| # | Episode | Runtime | Anchor questions | Video | Separate captions | Transcript | Visual QA |",
         "|---|---|---|---|---|---|---|---|"]
    total = 0.0
    for ep, e in info.items():
        lg = logs.get(ep)
        if lg:
            total += lg["duration"]
            vid = lg["output"]
            stem = vid[:-4]
            row = (f"| {ep[1:]} | {e['title']} | {mmss(lg['duration'])} | {', '.join(e['anchors'])} | "
                   f"`{vid}` | `{Path(stem).name}.srt` / `.vtt` | `{Path(stem).name}_transcript.md` | "
                   f"{qa.get(ep, {}).get('draft_visual_qa', '–')} |")
        elif qa.get(ep, {}).get("delivery_status") == "earlier_delivery":
            row = (f"| {ep[1:]} | {e['title']} | earlier delivery | {', '.join(e['anchors'])} | "
                   "keep previously delivered MP4 | earlier delivery | earlier delivery | unchanged |")
        else:
            row = f"| {ep[1:]} | {e['title']} | – | {', '.join(e['anchors'])} | not rendered | – | – | – |"
        L.append(row)
    L += ["", f"Current local output runtime (excludes earlier deliveries): {int(total // 3600)} h {int(total % 3600 // 60):02d} min "
               f"({total / 60:.1f} min) at an estimated 145 words per minute, including scripted pauses.", "",
          "Learner documents: `questions/worksheet.md` (questions only), `solutions/worked_solutions.md`, "
          "`solutions/formula_and_method_sheet.md`. Project status: `progress.json`, `logs/known_issues.md`."]
    (ROOT / "series_index.md").write_text("\n".join(L).rstrip() + "\n")
    return total


def main():
    info = episode_info()
    from tools.export_question_figures import export
    export()
    logs = {ep: lg for ep in EPISODES if (lg := assemble_log(ep))}
    tallies = scene_tallies()
    missing = [q["id"] for q in BANK if q["id"] not in tallies]
    build_worksheet(info)
    build_solutions(info, tallies, logs)
    gaps = build_coverage(info)
    total = build_index(info, logs)
    print(f"worksheet: {len(BANK)} questions; solutions: tallies for {len(BANK) - len(missing)}/{len(BANK)}"
          f"{' (missing ' + ', '.join(missing) + ')' if missing else ''}")
    print(f"coverage gaps: {gaps or 'none'}; draft runtime {total / 60:.1f} min")


if __name__ == "__main__":
    main()
