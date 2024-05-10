FROM python:3.11-slim-buster

COPY app /application
WORKDIR /application

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry -C deployment install --no-root --only main