#! /bin/sh

cd system
python3 /system/manage.py migrate && python3 /system/manage.py runserver 0.0.0.0:80
