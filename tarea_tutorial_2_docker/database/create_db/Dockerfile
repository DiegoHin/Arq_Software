FROM python:3.7.3-slim AS base
RUN apt-get update && apt-get install --no-install-recommends --yes python3

RUN pip install PyMySql
ENV PYTHONUNBUFFERED 1

COPY ./create_db.py ./create_db.py

CMD ["python","./create_db.py"] 