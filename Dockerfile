FROM python:3
ADD . /restapi
WORKDIR /restapi
RUN pip install -r requirements.txt