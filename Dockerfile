# Clean Dockerfile for CalloutRacing Backend
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=calloutracing.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend project
COPY backend/ .

# Copy start script and make it executable
COPY backend/start-railway.sh /app/start-railway.sh
RUN dos2unix /app/start-railway.sh
RUN chmod +x /app/start-railway.sh

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media

# Collect static files
RUN python manage.py collectstatic --noinput

# Railway uses PORT environment variable
EXPOSE $PORT

# Run the application
CMD ["bash", "/app/start-railway.sh"] 