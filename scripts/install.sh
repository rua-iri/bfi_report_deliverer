#!/bin/bash
set -e

VENV=".venv"
PYTHON="${VENV}/bin/python3"
PIP="${VENV}/bin/pip3"

python3 -m venv ${VENV}
$PIP install -r requirements.txt

sudo apt install wkhtmltopdf

$PYTHON setup.py
