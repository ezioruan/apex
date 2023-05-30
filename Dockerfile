# Pull base image
FROM python:3.11

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.in-project false
RUN poetry install --no-interaction --no-ansi --no-dev

COPY . /code
