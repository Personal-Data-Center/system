#! /bin/sh

cd system
python3 /launcher/manage.py migrate && python3 /launcher/manage.py runserver 0.0.0.0:80
