#FROM python:3.10.6-buster

#COPY beatingheart /beatingheart
COPY requirements.txt /requirements.txt
#COPY setup.py /setup.py

RUN pip install -r requirements.txt
RUN pip install .

#CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
