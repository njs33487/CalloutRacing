#!/bin/bash

# Production Deployment Script for CalloutRacing
# This script sets up the production environment with proper security

set -e

echo "=== CalloutRacing Production Deployment ==="

# Check if required environment variables are set
check_env_vars() {
    local required_vars=(
        "SECRET_KEY"
        "DATABASE_URL"
        "EMAIL_HOST_USER"
        "EMAIL_HOST_PASSWORD"
        "STRIPE_SECRET_KEY"
        "STRIPE_PUBLISHABLE_KEY"
        "STRIPE_WEBHOOK_SECRET"
        "ALLOWED_HOSTS"
    )
    
    echo "Checking required environment variables..."
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            echo "❌ ERROR: $var is not set"
            exit 1
        else
            echo "✅ $var is set"
        fi
    done
}

# Generate secure secret key if not provided
generate_secret_key() {
    if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "your-production-secret-key-here-change-this" ]; then
        echo "Generating secure Django secret key..."
        export SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
        echo "✅ Generated new SECRET_KEY"
    fi
}

# Build production images
build_images() {
    echo "Building production Docker images..."
    docker-compose -f docker-compose.prod.yml build --no-cache
    echo "✅ Images built successfully"
}

# Run security checks
security_checks() {
    echo "Running security checks..."
    
    # Check for DEBUG=False
    if [ "$DEBUG" = "True" ]; then
        echo "⚠️  WARNING: DEBUG is set to True in production"
    fi
    
    # Check for weak passwords
    if [ "$STAFF_PASSWORD" = "admin123" ]; then
        echo "❌ ERROR: STAFF_PASSWORD is still using default value"
        exit 1
    fi
    
    echo "✅ Security checks passed"
}

# Deploy services
deploy_services() {
    echo "Deploying production services..."
    docker-compose -f docker-compose.prod.yml up -d
    
    echo "Waiting for services to start..."
    sleep 30
    
    # Check service health
    echo "Checking service health..."
    docker-compose -f docker-compose.prod.yml ps
    
    echo "✅ Services deployed successfully"
}

# Run database migrations
run_migrations() {
    echo "Running database migrations..."
    docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate --noinput
    echo "✅ Migrations completed"
}

# Collect static files
collect_static() {
    echo "Collecting static files..."
    docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
    echo "✅ Static files collected"
}

# Main deployment process
main() {
    echo "Starting production deployment..."
    
    check_env_vars
    generate_secret_key
    security_checks
    build_images
    deploy_services
    run_migrations
    collect_static
    
    echo "=== Production Deployment Complete ==="
    echo "Frontend: http://localhost"
    echo "Backend API: http://localhost:8000"
    echo "Health Check: http://localhost:8000/health/"
}

# Run main function
main "$@" 