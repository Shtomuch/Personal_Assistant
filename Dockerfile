ARG PYTHON_VERSION=3.12.1-slim-bullseye

FROM python:$PYTHON_VERSION AS requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:${PYTHON_VERSION} AS django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PGSSLCERT /tmp/postgresql.crt
RUN mkdir -p /app
WORKDIR /app
RUN apt-get update && apt-get install -y git gettext build-essential libffi-dev libpcre3-dev libpq-dev libssl-dev gettext ffmpeg
COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --clear
CMD ["gunicorn", "-c", "/app/config/gunicorn.py", "config.wsgi"]