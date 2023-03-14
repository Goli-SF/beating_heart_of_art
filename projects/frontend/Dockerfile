# FROM --platform=linux/amd64 python:3.11-slim-buster
FROM python:3.10-buster

ARG PREDICTION_URL=http://localhost:8000/uploader
ENV PREDICTION_URL=${PREDICTION_URL}

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Install poetry
RUN pip install --no-cache-dir poetry && poetry install


# copy the project
COPY . .

# Run the application
CMD ["poetry", "run", "streamlit", "run", "app/app.py"]