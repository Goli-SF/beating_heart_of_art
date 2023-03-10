# FROM --platform=linux/amd64 python:3.11-slim-buster
FROM python:3.11-slim-buster

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Install poetry
RUN pip install poetry && poetry install

# copy the project
COPY . .

# Run the application
CMD ["poetry", "run", "streamlit", "run", "app/app.py"]