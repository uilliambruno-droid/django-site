#!/usr/bin/env bash
set -o errexit

cd mysite

poetry run gunicorn mysite.wsgi:application --bind 0.0.0.0:"${PORT:-8000}"
