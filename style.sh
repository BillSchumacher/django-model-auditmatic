#!/bin/bash

isort .
black --exclude='.*\/*(settings|migrations|venv|node_modules|frontend)\/*.*' .