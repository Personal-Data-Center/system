FROM python

COPY run.sh /run.sh

RUN chmod +x run.sh

RUN pip3 install django-admin mysqlclient  pdc-dev

RUN mkdir service

CMD ["/run.sh"]
