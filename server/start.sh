#!/usr/bin/env bash
sudo pigpiod
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source $DIR/.venv/bin/activate
export PYTHONPATH=$DIR/src
python $DIR/src/app.py "$@"
