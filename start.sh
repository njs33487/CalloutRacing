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
        # Create core_user table directly with SQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS core_user (
                id BIGSERIAL PRIMARY KEY,
                password VARCHAR(128) NOT NULL,
                last_login TIMESTAMP WITH TIME ZONE,
                is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
                first_name VARCHAR(150) NOT NULL DEFAULT \'\',
                last_name VARCHAR(150) NOT NULL DEFAULT \'\',
                is_staff BOOLEAN NOT NULL DEFAULT FALSE,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                email_verified BOOLEAN NOT NULL DEFAULT FALSE,
                email_verification_token UUID DEFAULT gen_random_uuid(),
                email_verification_sent_at TIMESTAMP WITH TIME ZONE,
                email_verification_expires_at TIMESTAMP WITH TIME ZONE,
                email VARCHAR(254) NOT NULL UNIQUE,
                username VARCHAR(150) NOT NULL UNIQUE
            );
        ''')
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS core_user_username_idx ON core_user(username);')
        cursor.execute('CREATE INDEX IF NOT EXISTS core_user_email_idx ON core_user(email);')
        # Insert migration record
        cursor.execute('''
            INSERT INTO django_migrations (app, name, applied) 
            VALUES (\'core\', \'0001_initial\', NOW())
            ON CONFLICT (app, name) DO NOTHING;
        ''')
        print('core_user table created successfully')
"
fi

# Collect static files (in case they weren't collected during build)
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

# Start the server
echo "=== Starting Django server on port $PORT ==="
python manage.py runserver 0.0.0.0:$PORT 