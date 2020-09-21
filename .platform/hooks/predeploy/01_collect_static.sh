#!/bin/bash
source /var/app/venv/*/bin/activate
python manage.py migrate
python manage.py createsu
python manage.py collectstatic --noinput