FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app/backend

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD sh -c 'echo "Apply database migrations"; python manage.py migrate;     echo "Collect static files"; python manage.py collectstatic --noinput;     echo "Starting server"; gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile -'