# Backend Placc Zacc
Backend for Placc Zacc

to build:
- Download and install Docker
- Inside root directory execute `docker-compose up --build`

to run:
- do `docker-compose up`

To use the admin, you must first create a superuser. You do this by opening the terminal of the Docker container and typing the following command: `python manage.py createsuperuser`

Follow the steps, and afterwards you can log in with those credentials at `https://localhost:8000/admin`