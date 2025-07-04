#!/usr/bin/env python
"""
Test email configuration for CalloutRacing
Run this to check if email is properly configured
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_config():
    """Test email configuration"""
    print("=== Email Configuration Test ===")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"EMAIL_HOST_USER: {'SET' if settings.EMAIL_HOST_USER else 'NOT SET'}")
    print(f"EMAIL_HOST_PASSWORD: {'SET' if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"FRONTEND_URL: {settings.FRONTEND_URL}")
    
    # Check if email credentials are configured
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("\n❌ Email credentials are not configured!")
        print("You need to set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD environment variables.")
        print("\nFor Gmail setup:")
        print("1. Enable 2-factor authentication on your Gmail account")
        print("2. Generate an App Password")
        print("3. Set EMAIL_HOST_USER to your Gmail address")
        print("4. Set EMAIL_HOST_PASSWORD to your App Password")
        return False
    
    print("\n✅ Email credentials are configured!")
    
    # Test sending a simple email
    try:
        print("\nTesting email send...")
        send_mail(
            subject='Test Email - CalloutRacing',
            message='This is a test email from CalloutRacing.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['test@example.com'],
            fail_silently=False,
        )
        print("✅ Email test successful!")
        return True
    except Exception as e:
        print(f"❌ Email test failed: {str(e)}")
        return False

if __name__ == '__main__':
    test_email_config() 