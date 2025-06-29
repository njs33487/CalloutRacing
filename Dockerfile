# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy start script first
COPY backend/start.sh .
RUN chmod +x start.sh

# Install Python dependencies
COPY backend/requirements.txt backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy project
COPY backend/ backend/

# Collect static files
RUN cd backend && python manage.py collectstatic --noinput

# Expose port (Railway uses PORT environment variable)
EXPOSE 8080

# Run the application
CMD ["./start.sh"] 