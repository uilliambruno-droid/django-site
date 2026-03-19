#!/usr/bin/env bash
set -o errexit

cd mysite

pip install --upgrade poetry
poetry install --no-root --only main

poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate
