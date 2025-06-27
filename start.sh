#!/bin/bash
set -e

# Change to backend directory
cd backend

# Use PORT environment variable or default to 8000
PORT=${PORT:-8000}

# Run Django development server
echo "Starting Django server on port $PORT..."
python manage.py runserver 0.0.0.0:$PORT 