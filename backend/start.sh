#!/bin/bash

# Exit on any error
set -e

echo "=== Starting CalloutRacing backend ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.get_version())')"

# Change to root directory where manage.py is located
cd ..
echo "Changed to root directory: $(pwd)"

# Check if migrations need to be run
echo "=== Checking migration status ==="
python manage.py showmigrations || echo "Failed to show migrations"

# Create migrations if needed
echo "=== Creating migrations ==="
python manage.py makemigrations --noinput || echo "No new migrations needed"

# Run migrations with enhanced logging and fallback
echo "=== Running database migrations ==="
if python manage.py migrate --noinput --verbosity=2; then
    echo "=== Migrations completed successfully ==="
    echo "=== Migration status ==="
    python manage.py showmigrations
else
    echo "=== Standard migration failed, trying database fix script ==="
    python scripts/fix_database.py
fi

# Collect static files (in case they weren't collected during build)
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

# Start the server
echo "=== Starting Django server on port $PORT ==="
python manage.py runserver 0.0.0.0:$PORT 