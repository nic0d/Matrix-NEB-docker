FROM python:2.7-alpine

# Maintainer
MAINTAINER Nicolas Dumont <nicolas.dumont.fr@gmail.com>


RUN pip install flask \
    && pip install python-dateutil \
    && apk update \
    && apk add git
WORKDIR /app
RUN git clone https://github.com/matrix-org/Matrix-NEB.git && git clone https://github.com/matrix-org/matrix-python-sdk.git

WORKDIR /app/matrix-python-sdk 
RUN python setup.py install

ADD add/neb.py /app/Matrix-NEB/neb.py
ADD add/neb.conf /app/neb.conf
ADD add/plugins/TAIBot.py /app/Matrix-NEB/plugins/TAIBot.py
ADD add/plugins/sample.py /app/Matrix-NEB/plugins/sample.py

WORKDIR /app/Matrix-NEB
RUN python setup.py install

EXPOSE 8500

CMD python neb.py -c /app/neb.conf
