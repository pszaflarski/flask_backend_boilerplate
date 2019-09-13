#!/usr/bin/env bash
export FLASK_CONFIG=development
export ROOT_USER=admin@example.com
export ROOT_PASSWORD=Abcd1234!

python manage.py runserver
