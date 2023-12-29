#!/bin/bash

set -eux

mypy runs
isort runs test_runs.py
black runs test_runs.py
ruff check --fix runs test_runs.py
coverage run $(which pytest)
coverage html
