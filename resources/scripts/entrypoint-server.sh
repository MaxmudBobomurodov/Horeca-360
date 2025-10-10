#!/bin/bash
set -e  # xatoda to‘xtash

echo "Waiting for database..."
until python3 manage.py migrate --check; do
  sleep 2
done

echo "Running migrations..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application -b 0.0.0.0:8000 --workers $(($(nproc) * 2 + 1)) --log-level info
