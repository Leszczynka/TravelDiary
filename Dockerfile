FROM python:3.10.6-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /traveldiary
WORKDIR /traveldiary
COPY requirements.txt /traveldiary/
COPY . /traveldiary/
RUN pip install -r requirements.txt
