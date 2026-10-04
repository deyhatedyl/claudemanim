"""Export a checked narrated episode with captions visible in every player."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('episode')
    args = parser.parse_args()
    ep = args.episode.upper()
    report = json.loads((ROOT / 'logs' / f'assemble_{ep}_1080p30.json').read_text())
    if not report['final'] or not report['narrated']:
        raise ValueError('A complete narrated 1080p30 assembly is required')
    if report['problems']:
        raise ValueError(f"Assembly verification failed: {report['problems']}")
    output_dir = ROOT / 'delivery' / ep
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f'{ep}-Chemistry-Narrated-1080p.mp4'
    caption = report['captions'][0]
    style = ('FontName=Inter,FontSize=15,PrimaryColour=&H00F8F1EE,'
             'OutlineColour=&H001E110C,BorderStyle=1,Outline=1,Shadow=0,MarginV=10')
    subprocess.check_call([
        'ffmpeg', '-y', '-v', 'error', '-i', str(ROOT / report['output']),
        '-vf', f"subtitles={caption}:force_style='{style}'",
        '-map', '0:v:0', '-map', '0:a:0', '-sn',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-threads', '3',
        '-c:a', 'copy', '-movflags', '+faststart', str(output)
    ], cwd=ROOT)
    for name in report['captions'] + [report['transcript']]:
        path = ROOT / name
        shutil.copyfile(path, output_dir / path.name)
    print(output, flush=True)


if __name__ == '__main__':
    main()
