# Use an official Python runtime as the base image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Copy the lockfile and pyproject.toml
COPY poetry.lock pyproject.toml /

# Install Poetry and dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Install supervisord
RUN pip install supervisor

# Copy the application code
COPY api/ /app/api
COPY client/ /app/client

# Copy the supervisord configuration file
WORKDIR /app/api/app

# Запускаем приложение с помощью supervisord
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
