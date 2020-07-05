FROM python:3.6.11-buster

RUN apt-get update --yes

RUN pip3 install flask
RUN pip3 install mysql-connector-python
RUN pip3 install sqlalchemy

RUN groupadd -g 1000 mygroup
RUN useradd -u 1000 -ms /bin/bash -g mygroup me

RUN mkdir -p /var/www/bd2_labs
WORKDIR /var/www/bd2_labs

COPY --chown=me:mygroup . /var/www/bd2_labs
USER me

CMD ["python3", "index.py"]