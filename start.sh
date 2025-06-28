#!/bin/bash

# Exit on any error
set -e

echo "=== Starting CalloutRacing backend ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.get_version())')"

# Change to backend directory
cd backend
echo "Changed to backend directory: $(pwd)"

# Use PORT environment variable or default to 8000
PORT=${PORT:-8000}

# Test database connection
echo "=== Testing database connection ==="
python manage.py check --database default

# Run migrations
echo "=== Running database migrations ==="
python manage.py migrate --noinput --verbosity=2

# Collect static files (in case they weren't collected during build)
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

# Start the server
echo "=== Starting Django server on port $PORT ==="
python manage.py runserver 0.0.0.0:$PORT 