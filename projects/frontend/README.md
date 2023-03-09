# Frontend

## Local development

### Install dependencies / activate poetry virtual environment

´´´bash
poetry install
poetry shell
´´´

## Run the app

´´´bash

streamlit run app/app.py
´´´

## Build and run with docker

### Build the docker image

´´´bash
docker build -t frontend .
´´´

### Run the docker image

´´´bash
docker run -p 8501:8501 frontend
´´´

### Enter container with bash

´´´bash
docker run -it frontend bash
´´´

## Deploy to GCP

### Build the docker image

´´´bash
docker build -t gcr.io/your-project-id/frontend .
´´´

### Push the docker image to GCP

´´´bash
docker push gcr.io/your-project-id/frontend
´´´

### Deploy the docker image to GCP

´´´bash
gcloud run deploy frontend --image gcr.io/your-project-id/frontend --platform managed --region europe-west1 --allow-unauthenticated
´´´
