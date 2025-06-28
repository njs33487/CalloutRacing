#!/bin/bash
set -e

# Change to backend directory
cd backend

# Use PORT environment variable or default to 8000
PORT=${PORT:-8000}

# Reset migration state if needed (for Railway deployment)
echo "Checking migration state..."
python manage.py reset_migrations --noinput || echo "Migration reset not needed"

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run Django development server
echo "Starting Django server on port $PORT..."
python manage.py runserver 0.0.0.0:$PORT 