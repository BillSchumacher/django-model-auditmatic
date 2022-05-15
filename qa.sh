#!/bin/bash
set -euf -o pipefail
isort .
black --exclude='.*\/*(settings|migrations|venv|node_modules|frontend)\/*.*' .
flake8 .
DJANGO_SETTINGS_MODULE=django_model_auditmatic.settings pylint django_model_auditmatic django_auditmatic
