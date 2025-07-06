#!/usr/bin/env python3
"""
Verify test user email for testing
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models.auth import UserProfile

User = get_user_model()

def verify_test_user():
    """Verify the test user's email"""
    print("🔍 Verifying Test User Email")
    print("=" * 50)
    
    # Get test user
    user = User.objects.get(email="test@example.com")
    print(f"✅ Found test user: {user.username}")
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        print(f"✅ Created user profile for: {user.username}")
    else:
        print(f"✅ Found existing profile for: {user.username}")
    
    # Verify email
    profile.email_verified = True
    profile.save()
    print(f"✅ Email verified for: {user.username}")
    
    # Check verification status
    print(f"  - Email verified: {profile.email_verified}")
    print(f"  - User active: {user.is_active}")
    print(f"  - Username: {user.username}")

if __name__ == "__main__":
    verify_test_user() 