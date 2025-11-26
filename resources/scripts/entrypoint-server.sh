#!/bin/bash
set -e  # xato bo‘lsa to‘xtaydi

echo "Waiting for PostgreSQL..."

# Postgres tayyor bo‘lguncha kutish
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "Database is unavailable - sleeping"
  sleep 2
done

echo "Database is up!"

echo "Running migrations..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8080
  # <-- bu yerni 8080 g
