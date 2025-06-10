FROM mcr.microsoft.com/azure-functions/python:4-python3.9

RUN apt-get update && apt-get install -y ffmpeg

ENV PYTHONUNBUFFERED=1
ENV IMAGEIO_FFMPEG_EXE=/usr/bin/ffmpeg

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY . /home/site/wwwroot
