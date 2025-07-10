#!/bin/bash
set -e

VENV=".venv"
PYTHON="${VENV}/bin/python3"
PIP="${VENV}/bin/pip3"

$PYTHON -m unittest -v test.test
