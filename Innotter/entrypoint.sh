#!/bin/bash

python Innotter/manage.py makemigrations
python Innotter/manage.py migrate
python Innotter/manage.py runserver 0.0.0.0:8000