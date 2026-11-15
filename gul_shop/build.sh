#!/usr/bin/env bash
# Render ар бир deploy'до ушуну иштетет
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py ensure_admin
python manage.py seed_demo
