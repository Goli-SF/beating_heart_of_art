FROM python:3.10.10-slim-buster

COPY projects /projects
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD uvicorn projects.api.api:app --host 0.0.0.0 --port $PORT
