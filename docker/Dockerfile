FROM python:3.12-slim

ARG REQUIREMENTS_PATH=requirements.txt # set default requirements path

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY $REQUIREMENTS_PATH /tmp/$REQUIREMENTS_PATH
RUN apt-get update && \
    apt-get install -y nano curl gcc

# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --no-cache-dir -r /tmp/$REQUIREMENTS_PATH

COPY ./app /app
WORKDIR /app
