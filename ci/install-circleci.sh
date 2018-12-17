#!/bin/bash

set -e

echo
echo "[install dependencies]"
conda env update -f environment-dev.yml
source activate intake-cmip5-dev
conda list

echo
echo "[install intake-cmip5]"
pip install --no-deps -e .

echo "[finished install]"

exit 0