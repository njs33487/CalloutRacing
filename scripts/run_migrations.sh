#!/bin/bash

# Script to run migrations on Railway
echo "=== Running Django migrations on Railway ==="

# Change to backend directory
cd backend

# Show current migration status
echo "=== Current migration status ==="
python manage.py showmigrations

# Run migrations
echo "=== Running migrations ==="
python manage.py migrate --noinput --verbosity=2

# Show final migration status
echo "=== Final migration status ==="
python manage.py showmigrations

echo "=== Migrations completed ===" 