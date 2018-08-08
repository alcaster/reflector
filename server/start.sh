#!/usr/bin/env bash
sudo pigpiod
source `pwd`/../.venv/bin/activate
export PYTHONPATH=`pwd`/src
python `pwd`/src/app.py "$@"
