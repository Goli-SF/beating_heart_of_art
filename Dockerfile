
# FROM --platform=linux/amd64  python:3.10-buster
FROM python:3.10-buster

ARG UVICORN_PORT=local
ENV UVICORN_PORT=${UVICORN_PORT}

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY projects /projects

# install local dependencies
COPY requirements-local.txt /requirements-local.txt
RUN pip install -r requirements-local.txt

COPY database /database
COPY resources /resources

CMD uvicorn projects.api.api:app --host 0.0.0.0 --port ${UVICORN_PORT}
