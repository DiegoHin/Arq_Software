FROM python:3.8-slim AS base
RUN apt-get update && apt-get install --no-install-recommends --yes python3
RUN python3 -m pip install --upgrade pip
RUN pip install fastapi
RUN pip install sqlalchemy
RUN pip install uvicorn
RUN pip install mysql.connector
RUN pip install fastapi-pagination[sqlalchemy]

COPY api/ api/

CMD ["uvicorn","api.main:app","--reload","--port","12333","--host","0.0.0.0"]