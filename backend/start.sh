#!/bin/bash

# Exit on any error
set -e

echo "=== Starting CalloutRacing backend ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.get_version())')"

# Check if migrations need to be run
echo "=== Checking migration status ==="
python manage.py showmigrations || echo "Failed to show migrations"

# Run migrations with enhanced logging and fallback
echo "=== Running database migrations ==="
if python manage.py migrate --noinput --verbosity=2; then
    echo "=== Migrations completed successfully ==="
else
    echo "=== Standard migration failed, trying alternative method ==="
    python migrate_db.py
fi

# Collect static files (in case they weren't collected during build)
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

# Start the server
echo "=== Starting Django server on port $PORT ==="
python manage.py runserver 0.0.0.0:$PORT 