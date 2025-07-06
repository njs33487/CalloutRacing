#!/usr/bin/env python3
"""
Check and fix test user credentials
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

def check_user_credentials():
    """Check and fix test user credentials"""
    print("🔍 Checking Test User Credentials")
    print("=" * 50)
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        email="test@example.com",
        defaults={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Created new test user: {user.username}")
    else:
        print(f"✅ Found existing test user: {user.username}")
    
    # Set password
    user.set_password('testpass123')
    user.save()
    print(f"✅ Password set for user: {user.username}")
    
    # Test authentication
    auth_user = authenticate(username='testuser', password='testpass123')
    if auth_user:
        print(f"✅ Authentication successful for: {auth_user.username}")
        print(f"  - Email: {auth_user.email}")
        print(f"  - Active: {auth_user.is_active}")
    else:
        print(f"❌ Authentication failed for: testuser")
    
    # Test with email
    auth_user_email = authenticate(username='test@example.com', password='testpass123')
    if auth_user_email:
        print(f"✅ Email authentication successful for: {auth_user_email.username}")
    else:
        print(f"❌ Email authentication failed for: test@example.com")

if __name__ == "__main__":
    check_user_credentials() 