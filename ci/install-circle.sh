#!/bin/bash

set -e
set -eo pipefail

apt-get update; apt-get install -y make
conda config --set always_yes true --set changeps1 false --set quiet true
conda update -q conda
conda env create -f environment-dev.yml --name=${ENV_NAME} --quiet
conda env list
source activate ${ENV_NAME}
pip install pip --upgrade
pip install --no-deps --quiet -e .
conda list -n ${ENV_NAME}