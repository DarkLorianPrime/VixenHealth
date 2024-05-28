FROM python:3.11-slim-buster as base

COPY app /application
WORKDIR /application

RUN pip install poetry
RUN poetry config virtualenvs.create false

FROM base as debug
RUN poetry -C deployment install --no-root --only dev,main


FROM base as production
RUN poetry -C deployment install --no-root --only main
