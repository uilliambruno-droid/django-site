#!/usr/bin/env bash
# Exit on error

set -o errexit

pip install --upgrade poetry
poetry install --no-root --only main

poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate