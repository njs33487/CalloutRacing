#!/usr/bin/env python
"""
Fix authentication configuration to work with custom User model
This script updates the Django settings to remove authtoken and use session auth
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

def fix_authentication():
    """Fix authentication configuration"""
    print("=== Fixing Authentication Configuration ===")
    
    # Check current user model
    print(f"Current AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}")
    print(f"User model: {User}")
    
    # Check if authtoken is in INSTALLED_APPS
    if 'rest_framework.authtoken' in settings.INSTALLED_APPS:
        print("❌ authtoken app is still in INSTALLED_APPS")
        print("This causes conflicts with custom User model")
    else:
        print("✅ authtoken app is not in INSTALLED_APPS")
    
    # Check authentication classes
    print(f"Authentication classes: {settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']}")
    
    # Check if there are any tokens in the database
    try:
        token_count = Token.objects.count()
        print(f"Tokens in database: {token_count}")
        
        if token_count > 0:
            print("⚠️  There are existing tokens in the database")
            print("These will need to be cleaned up")
    except Exception as e:
        print(f"Error checking tokens: {e}")
    
    print("\n=== Recommended Fix ===")
    print("1. Remove 'rest_framework.authtoken' from INSTALLED_APPS")
    print("2. Update authentication classes to use only SessionAuthentication")
    print("3. Clean up any existing tokens in the database")
    print("4. Update login view to not create tokens")

if __name__ == '__main__':
    fix_authentication() 