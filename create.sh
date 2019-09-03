#!/usr/bin/env bash
export FLASK_CONFIG=development
python manage.py adduser --admin admin@example.com --password Abcd1234!
