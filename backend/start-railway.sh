#!/bin/bash

# Railway-optimized start script for CalloutRacing backend
set -e

echo "=== Starting CalloutRacing backend on Railway ==="
echo "Current directory: $(pwd)"

# Check Python availability
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "Using python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "Using python"
else
    echo "ERROR: Python not found"
    exit 1
fi

echo "Python version: $($PYTHON_CMD --version)"
echo "Django version: $($PYTHON_CMD -c 'import django; print(django.get_version())')"

# Use Railway's PORT environment variable
PORT=${PORT:-8000}
echo "Starting on port: $PORT"

# Test database connection
echo "=== Testing database connection ==="
$PYTHON_CMD manage.py check --database default

# Check if migrations need to be run
echo "=== Checking migration status ==="
$PYTHON_CMD manage.py showmigrations || echo "Failed to show migrations"

# Create migrations if needed
echo "=== Creating migrations ==="
$PYTHON_CMD manage.py makemigrations --noinput || echo "No new migrations needed"

# Run migrations
echo "=== Running database migrations ==="
$PYTHON_CMD manage.py migrate --noinput

# Collect static files
echo "=== Collecting static files ==="
$PYTHON_CMD manage.py collectstatic --noinput

# Start the server
echo "=== Starting Django server on port $PORT ==="
$PYTHON_CMD manage.py runserver 0.0.0.0:$PORT 