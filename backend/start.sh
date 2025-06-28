#!/bin/bash

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Start the server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:$PORT 