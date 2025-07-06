#!/bin/bash

# Simple Docker start script for CalloutRacing backend
set -e

echo "=== Starting CalloutRacing backend ==="
echo "Current directory: $(pwd)"

# Use PORT environment variable or default to 8000
PORT=${PORT:-8000}

# Run migrations
echo "=== Running database migrations ==="
python manage.py migrate --noinput

# Collect static files
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

# Start the server
echo "=== Starting Django server on port $PORT ==="
python manage.py runserver 0.0.0.0:$PORT 