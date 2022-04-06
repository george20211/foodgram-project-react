FROM python:3.7-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn wsgi:application --bind 0.0.0.0:8000