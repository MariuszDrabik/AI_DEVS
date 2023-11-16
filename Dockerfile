FROM python:3.11

RUN mkdir /src


COPY ./AI_devs /src
RUN apt-get update

WORKDIR /src


ENV PYTHONPATH=${PYTHONPATH}:ai_devs
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

RUN poetry install
RUN chown 777 ai_devs/docker-entrypoint.sh

CMD ["./ai_devs/docker-entrypoint.sh"]

