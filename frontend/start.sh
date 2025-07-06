#!/bin/bash

# Frontend start script for Railway deployment
set -e

echo "=== Starting CalloutRacing Frontend ==="
echo "Current directory: $(pwd)"

# Use PORT environment variable or default to 3000
PORT=${PORT:-3000}
echo "Starting on port: $PORT"

# Check if dist directory exists
if [ ! -d "dist" ]; then
    echo "Building application..."
    npm run build
fi

# Start the application
echo "=== Starting frontend server on port $PORT ==="
npx serve -s dist -l $PORT 