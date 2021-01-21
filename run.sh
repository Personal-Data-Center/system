#! /bin/sh

cd service
python3 /service/manage.py migrate && python3 /service/manage.py runserver 0.0.0.0:80
