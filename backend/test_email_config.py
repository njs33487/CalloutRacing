#!/usr/bin/env python
"""
Test script to check email configuration and identify issues with email verification.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend

def test_email_config():
    """Test email configuration and identify issues."""
    print("=== Email Configuration Test ===\n")
    
    # Check email settings
    print("Email Settings:")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'Not set'}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"FRONTEND_URL: {settings.FRONTEND_URL}")
    print()
    
    # Check if email credentials are configured
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("❌ ERROR: Email credentials are not configured!")
        print("   - EMAIL_HOST_USER is not set")
        print("   - EMAIL_HOST_PASSWORD is not set")
        print()
        print("To fix this, you need to:")
        print("1. Set up Gmail App Password (if using Gmail)")
        print("2. Add EMAIL_HOST_USER and EMAIL_HOST_PASSWORD to your environment variables")
        print("3. Or create a .env file with these settings")
        return False
    
    # Test email backend connection
    print("Testing email backend connection...")
    try:
        backend = EmailBackend(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            use_ssl=settings.EMAIL_USE_SSL,
            fail_silently=False
        )
        
        # Test connection
        backend.open()
        print("✅ Email backend connection successful!")
        backend.close()
        
    except Exception as e:
        print(f"❌ Email backend connection failed: {str(e)}")
        print()
        print("Common issues:")
        print("1. Gmail App Password not set up correctly")
        print("2. 2FA not enabled on Gmail account")
        print("3. Incorrect email credentials")
        print("4. Network/firewall blocking SMTP")
        return False
    
    # Test sending a simple email
    print("\nTesting email sending...")
    try:
        send_mail(
            subject='Test Email - CalloutRacing',
            message='This is a test email to verify email configuration.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # Send to self for testing
            fail_silently=False,
        )
        print("✅ Test email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test email failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_email_config() 