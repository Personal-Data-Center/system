FROM python

COPY run.sh /run.sh

RUN mkdir system

RUN pip3 install django-admin djangorestframework mysqlclient

CMD ["/run.sh"]
