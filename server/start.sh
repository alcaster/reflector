#!/usr/bin/env bash
sudo pigpiod
source .venv/bin/activate
export PYTHONPATH=`pwd`/src
python src/app.py "$@"
