FROM python:3.11

RUN mkdir /src


COPY ./AI_devs /src
RUN apt-get update

WORKDIR /src
RUN ls


ENV PYTHONPATH=${PYTHONPATH}:ai_devs
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

RUN poetry install

RUN echo "Current working directory: $(pwd)"

RUN ls
ENTRYPOINT ["/bin/sh", "ai_devs/docker-entrypoint.sh"]

