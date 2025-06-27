#!/bin/sh

# Set default port if not provided
PORT=${PORT:-8080}

# Start the application
echo "Starting CalloutRacing frontend on port $PORT"
echo "Environment: $NODE_ENV"
echo "API URL: $VITE_API_URL"

serve -s dist -l $PORT 