FROM python:3.8-slim AS base
RUN apt-get update && apt-get install --no-install-recommends --yes python3

RUN pip install pika
RUN pip install -U wikipedia

ENV PYTHONUNBUFFERED 1

COPY ./tictactoe.py ./tictactoe.py
COPY ./manager.py ./manager.py

CMD ["python", "manager.py"]