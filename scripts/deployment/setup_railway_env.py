#!/usr/bin/env python3
"""
Railway Environment Setup Script

This script helps set up and validate the Railway deployment environment.
Run this locally to generate the necessary environment variables for Railway.
"""

import os
import secrets
import base64
from cryptography.fernet import Fernet

def generate_encryption_key():
    """Generate a secure encryption key for Railway."""
    return Fernet.generate_key().decode()

def generate_secret_key():
    """Generate a Django secret key."""
    return ''.join([secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

def create_railway_env_template():
    """Create a template for Railway environment variables."""
    template = f"""# Railway Environment Variables Template
# Copy these to your Railway project environment variables

# Django Settings
SECRET_KEY={generate_secret_key()}
DEBUG=False
ALLOWED_HOSTS=*.railway.app,*.up.railway.app,your-domain.com

# Database (Railway provides these automatically)
DATABASE_URL=postgresql://user:password@host:port/database

# Encryption
ENCRYPTION_KEY={generate_encryption_key()}

# Stripe (Replace with your actual keys)
STRIPE_SECRET_KEY=sk_test_your_test_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_test_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Email (Configure your email service)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# OAuth (Optional - for social login)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret

# Other Settings
CSRF_TRUSTED_ORIGINS=https://*.railway.app,https://*.up.railway.app
CORS_ALLOWED_ORIGINS=https://*.railway.app,https://*.up.railway.app
"""
    
    with open('railway_env_template.txt', 'w') as f:
        f.write(template)
    
    print("✅ Created railway_env_template.txt")
    print("📝 Copy the variables from this file to your Railway project environment variables")
    print("🔗 Go to: https://railway.app/dashboard -> Your Project -> Variables")

def validate_railway_deployment():
    """Validate Railway deployment configuration."""
    print("🔍 Validating Railway deployment configuration...")
    
    # Check if start script exists
    if not os.path.exists('backend/start-railway.sh'):
        print("❌ Missing: backend/start-railway.sh")
        return False
    
    # Check if Dockerfile exists
    if not os.path.exists('Dockerfile'):
        print("❌ Missing: Dockerfile")
        return False
    
    # Check if railway.toml exists
    if not os.path.exists('railway.toml'):
        print("❌ Missing: railway.toml")
        return False
    
    print("✅ Railway configuration files found")
    return True

def main():
    """Main function."""
    print("🚀 Railway Environment Setup")
    print("=" * 40)
    
    # Validate configuration
    if not validate_railway_deployment():
        print("\n❌ Railway configuration validation failed")
        return
    
    # Create environment template
    create_railway_env_template()
    
    print("\n📋 Next Steps:")
    print("1. Copy the environment variables from railway_env_template.txt to Railway")
    print("2. Update the Stripe keys with your actual test/live keys")
    print("3. Configure your email settings")
    print("4. Deploy to Railway")
    print("\n🔗 Railway Dashboard: https://railway.app/dashboard")

if __name__ == "__main__":
    main() 