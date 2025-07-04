#!/usr/bin/env python
"""
Temporary fix to auto-verify all users for testing
Run this to verify all existing users without email
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from core.models.auth import UserProfile

def auto_verify_all_users():
    """Auto-verify all users for testing purposes"""
    profiles = UserProfile.objects.all()
    count = 0
    
    for profile in profiles:
        if not profile.email_verified:
            profile.email_verified = True
            profile.save()
            count += 1
            print(f"Auto-verified user: {profile.user.email}")
    
    print(f"\n✅ Auto-verified {count} users!")
    print("Users can now log in without email verification.")

if __name__ == '__main__':
    auto_verify_all_users() 