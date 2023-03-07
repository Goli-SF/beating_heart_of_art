FROM python:3.10.6-buster

COPY projects /projects
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD uvicorn projects.api.fastapi:app --host 0.0.0.0 --port $PORT
