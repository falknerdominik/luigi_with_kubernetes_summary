# FROM python
FROM tensorflow/tensorflow:latest-py3

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
# RUN pip install tensorflow
COPY ./src /clc
COPY ./test /clc/test
