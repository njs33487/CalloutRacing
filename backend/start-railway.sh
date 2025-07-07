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

# Check for required environment variables
echo "=== Checking environment variables ==="
if [ -z "$ENCRYPTION_KEY" ]; then
    echo "⚠️  ENCRYPTION_KEY not set. Generating temporary key..."
    export ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
    echo "Generated temporary ENCRYPTION_KEY. Set this in Railway environment variables for production."
fi

if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  SECRET_KEY not set. Using Django default..."
fi

# Test database connection with retries
echo "=== Testing database connection ==="
MAX_RETRIES=5
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if $PYTHON_CMD manage.py check --database default 2>/dev/null; then
        echo "✅ Database connection successful"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        echo "⚠️  Database connection failed (attempt $RETRY_COUNT/$MAX_RETRIES)"
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "Waiting 5 seconds before retry..."
            sleep 5
        fi
    fi
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "❌ Database connection failed after $MAX_RETRIES attempts"
    echo "Check your DATABASE_URL environment variable in Railway"
    exit 1
fi

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

# Create superuser if not exists (for development)
if [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "=== Creating superuser ==="
    $PYTHON_CMD manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"
fi

# Start the server
echo "=== Starting Django server on port $PORT ==="
$PYTHON_CMD manage.py runserver 0.0.0.0:$PORT 