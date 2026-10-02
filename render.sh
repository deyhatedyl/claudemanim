#!/usr/bin/env bash
# Render every scene of vce_q3_tangents.py and stitch them into one video.
#
#   ./render.sh        # 1080p60 (default)
#   ./render.sh l      # quick 480p15 preview
#
# Quality letters are manim's: l=480p15, m=720p30, h=1080p60, p=1440p60, k=2160p60.
# Output: output/VCE_Q3_Tangents.mp4
set -euo pipefail
cd "$(dirname "$0")"

Q="${1:-h}"
FILE=vce_q3_tangents.py
SCENES=(Intro DecodeFunction PartA PartB PartC Recap)
MANIM="${MANIM:-manim}"

case "$Q" in
  l) DIR=480p15 ;;
  m) DIR=720p30 ;;
  h) DIR=1080p60 ;;
  p) DIR=1440p60 ;;
  k) DIR=2160p60 ;;
  *) echo "unknown quality '$Q' (use l, m, h, p or k)" >&2; exit 1 ;;
esac

for s in "${SCENES[@]}"; do
  "$MANIM" -q"$Q" "$FILE" "$s"
done

OUT_DIR="media/videos/${FILE%.py}/$DIR"
LIST="$(mktemp)"
trap 'rm -f "$LIST"' EXIT
for s in "${SCENES[@]}"; do
  echo "file '$PWD/$OUT_DIR/$s.mp4'" >> "$LIST"
done

mkdir -p output
ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" -c copy output/VCE_Q3_Tangents.mp4
echo "Done -> output/VCE_Q3_Tangents.mp4"
