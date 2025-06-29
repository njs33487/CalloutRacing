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
    echo "=== Standard migration failed, trying alternative method ==="
    echo "=== Checking if core_user table exists ==="
    python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = \'public\' AND table_name = \'core_user\');')
    exists = cursor.fetchone()[0]
    print(f'core_user table exists: {exists}')
    if not exists:
        print('Table missing, creating core_user table...')
        # Read and execute the SQL script
        with open('../scripts/create_core_user_table.sql', 'r') as f:
            sql_script = f.read()
        cursor.execute(sql_script)
        print('core_user table created successfully')
"
fi

# Collect static files (in case they weren't collected during build)
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

# Start the server
echo "=== Starting Django server on port $PORT ==="
python manage.py runserver 0.0.0.0:$PORT 