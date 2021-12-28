FROM python:3.8-slim AS base
RUN apt-get update && apt-get install --no-install-recommends --yes python3
RUN python3 -m pip install --upgrade pip
RUN pip install -U discord.py
RUN pip install -U python-dotenv 
RUN pip install -U pika

ENV PYTHONUNBUFFERED=TRUE

COPY . discord/

CMD ["python","discord/bot.py"]
