#!/bin/bash
set -euf -o pipefail
flake8 .
echo $?
python run_pylint.py
echo $?