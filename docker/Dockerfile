FROM python:3.10-slim

ARG REQUIREMENTS_PATH=requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY $REQUIREMENTS_PATH /tmp/$REQUIREMENTS_PATH
RUN pip install --no-cache-dir -r /tmp/$REQUIREMENTS_PATH
RUN apt-get update && \
    apt-get install nano

COPY ./app /app
WORKDIR /app
