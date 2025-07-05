#!/bin/bash

# Production Environment Setup Script for CalloutRacing
# This script helps set up the production environment

set -e

echo "=== CalloutRacing Production Environment Setup ==="

# Function to generate secure random string
generate_random_string() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-50
}

# Function to prompt for input with default
prompt_with_default() {
    local prompt="$1"
    local default="$2"
    local var_name="$3"
    
    if [ -z "$default" ]; then
        read -p "$prompt: " value
    else
        read -p "$prompt [$default]: " value
        value=${value:-$default}
    fi
    
    echo "$var_name=$value" >> .env.production
    export "$var_name=$value"
}

# Create production environment file
create_env_file() {
    echo "Creating production environment file..."
    
    # Clear existing file
    > .env.production
    
    echo "# CalloutRacing Production Environment" >> .env.production
    echo "# Generated on $(date)" >> .env.production
    echo "" >> .env.production
    
    # Django Settings
    echo "# Django Settings" >> .env.production
    prompt_with_default "Enter Django SECRET_KEY (leave empty to generate)" "" "SECRET_KEY"
    if [ -z "$SECRET_KEY" ]; then
        SECRET_KEY=$(generate_random_string)
        echo "SECRET_KEY=$SECRET_KEY" >> .env.production
    fi
    
    echo "DEBUG=False" >> .env.production
    prompt_with_default "Enter ALLOWED_HOSTS (comma-separated)" "your-domain.com,www.your-domain.com" "ALLOWED_HOSTS"
    
    echo "" >> .env.production
    echo "# Database Settings (Railway)" >> .env.production
    prompt_with_default "Enter DATABASE_URL" "postgresql://postgres:QfGzdLFMYTfqmSAiohnrWGJGMMrQEMnK@postgres.railway.internal:5432/railway" "DATABASE_URL"
    prompt_with_default "Enter DATABASE_PUBLIC_URL" "postgresql://postgres:QfGzdLFMYTfqmSAiohnrWGJGMMrQEMnK@caboose.proxy.rlwy.net:33954/railway" "DATABASE_PUBLIC_URL"
    
    echo "" >> .env.production
    echo "# Email Settings" >> .env.production
    prompt_with_default "Enter EMAIL_HOST" "smtp.gmail.com" "EMAIL_HOST"
    prompt_with_default "Enter EMAIL_HOST_USER" "digibin@digitalbinarysolutionsllc.com" "EMAIL_HOST_USER"
    prompt_with_default "Enter EMAIL_HOST_PASSWORD" "" "EMAIL_HOST_PASSWORD"
    echo "EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend" >> .env.production
    prompt_with_default "Enter DEFAULT_FROM_EMAIL" "noreply@calloutracing.com" "DEFAULT_FROM_EMAIL"
    echo "EMAIL_PORT=587" >> .env.production
    echo "EMAIL_USE_TLS=True" >> .env.production
    echo "EMAIL_USE_SSL=False" >> .env.production
    
    echo "" >> .env.production
    echo "# Stripe Settings" >> .env.production
    prompt_with_default "Enter STRIPE_SECRET_KEY" "" "STRIPE_SECRET_KEY"
    prompt_with_default "Enter STRIPE_PUBLISHABLE_KEY" "" "STRIPE_PUBLISHABLE_KEY"
    prompt_with_default "Enter STRIPE_WEBHOOK_SECRET" "" "STRIPE_WEBHOOK_SECRET"
    
    echo "" >> .env.production
    echo "# Frontend Settings" >> .env.production
    echo "NODE_ENV=production" >> .env.production
    prompt_with_default "Enter VITE_API_URL" "https://calloutracing-backend-production.up.railway.app/api" "VITE_API_URL"
    echo "VITE_APP_NAME=CalloutRacing" >> .env.production
    echo "VITE_DEV_MODE=false" >> .env.production
    
    echo "" >> .env.production
    echo "# Redis Settings" >> .env.production
    echo "REDIS_URL=redis://redis:6379" >> .env.production
    
    echo "" >> .env.production
    echo "# Optional Settings" >> .env.production
    echo "POPULATE_DATA=false" >> .env.production
    echo "POPULATE_RAILWAY_DATA=false" >> .env.production
    echo "RECREATE_DB=false" >> .env.production
    
    echo "✅ Production environment file created: .env.production"
}

# Security checklist
security_checklist() {
    echo ""
    echo "=== Security Checklist ==="
    echo "Before deploying to production, ensure:"
    echo ""
    echo "✅ SECRET_KEY is set and secure"
    echo "✅ DEBUG=False"
    echo "✅ ALLOWED_HOSTS includes your domain"
    echo "✅ Database credentials are secure"
    echo "✅ Email credentials are secure"
    echo "✅ Stripe keys are production keys"
    echo "✅ SSL/TLS is configured"
    echo "✅ Firewall rules are set"
    echo "✅ Regular backups are scheduled"
    echo "✅ Monitoring is configured"
    echo ""
    echo "⚠️  IMPORTANT: Review .env.production before deployment!"
}

# Main setup process
main() {
    echo "Starting production environment setup..."
    
    create_env_file
    security_checklist
    
    echo ""
    echo "=== Setup Complete ==="
    echo "Next steps:"
    echo "1. Review .env.production file"
    echo "2. Update domain names and URLs"
    echo "3. Set up SSL certificates"
    echo "4. Configure monitoring"
    echo "5. Run: ./deploy-production.sh"
}

# Run main function
main "$@" 