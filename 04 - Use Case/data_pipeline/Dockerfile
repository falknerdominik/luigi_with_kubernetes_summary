#FROM python
# tensorflow braucht sein eigenes Docker image
FROM tensorflow/tensorflow:latest-py3

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY ./src /clc
COPY ./urban_sound_files /clc/urban_sound_files
RUN apt-get update
RUN apt-get install -y libsndfile1
