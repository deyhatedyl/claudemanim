#!/usr/bin/env bash
# Recreate the render environment in a fresh Ubuntu 24.04 container (about 5 minutes).
#   bash energy_fuels_calorimetry/tools/setup_env.sh
set -euo pipefail
cd "$(dirname "$0")/../.."          # repository root
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q --no-install-recommends texlive-xetex texlive-latex-base texlive-latex-extra texlive-fonts-recommended \
  texlive-science dvisvgm cm-super libcairo2-dev libpango1.0-dev pkg-config python3-dev python3-venv \
  fonts-inter fonts-dejavu fonts-noto-core sox ffmpeg
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -r energy_fuels_calorimetry/requirements.txt
.venv/bin/python -c "import manim; print('manim', manim.__version__)"
