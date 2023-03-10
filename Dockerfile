FROM --platform=linux/amd64  python:3.10-buster

COPY projects /projects
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD uvicorn projects.api.fastapi:app --host 0.0.0.0 --port 8000
