#!/bin/sh

# Set default port if not provided
PORT=${PORT:-8000}

# Start the application
echo "Starting CalloutRacing frontend on port $PORT"
serve -s dist -l $PORT 