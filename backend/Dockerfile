FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/backend

COPY requirements.txt /app/backend/

# Build psycopg2-binary from source -- add required required dependencies
RUN apk add --virtual .build-deps --no-cache \
        postgresql-dev \
        gcc \
        g++ \
        python3-dev \
        musl-dev \
    && apk add --no-cache \
        libstdc++ \
        libgomp \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY . /app/backend/

EXPOSE 8000
CMD sleep 20 ; echo "Apply database migrations" ; python manage.py migrate ; echo "Starting server" ; python manage.py runserver 0.0.0.0:8000