#!/usr/bin/env python
"""
Comprehensive authentication flow test for CalloutRacing
This script tests the entire auth flow to identify issues
"""

import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calloutracing.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

def test_backend_health():
    """Test if backend is responding"""
    print("=== Testing Backend Health ===")
    try:
        response = requests.get('https://calloutracing-backend-production.up.railway.app/')
        print(f"Backend root response: {response.status_code}")
        print(f"Response content: {response.text[:200]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\n=== Testing Auth Endpoints ===")
    base_url = 'https://calloutracing-backend-production.up.railway.app/api/auth'
    
    # Test SSO config endpoint
    try:
        response = requests.get(f'{base_url}/sso-config/')
        print(f"SSO config response: {response.status_code}")
        if response.status_code == 200:
            print(f"SSO config: {response.json()}")
    except Exception as e:
        print(f"❌ SSO config failed: {e}")
    
    # Test check-user endpoint
    try:
        data = {'username': 'testuser', 'email': 'test@example.com'}
        response = requests.post(f'{base_url}/check-user/', json=data)
        print(f"Check user response: {response.status_code}")
        if response.status_code == 200:
            print(f"Check user result: {response.json()}")
    except Exception as e:
        print(f"❌ Check user failed: {e}")

def test_registration():
    """Test user registration"""
    print("\n=== Testing Registration ===")
    base_url = 'https://calloutracing-backend-production.up.railway.app/api/auth'
    
    # Test registration with new user
    test_data = {
        'username': 'testuser123',
        'email': 'testuser123@example.com',
        'password': 'TestPassword123!',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    try:
        response = requests.post(f'{base_url}/register/', json=test_data)
        print(f"Registration response: {response.status_code}")
        print(f"Registration result: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return test_data
        else:
            print("❌ Registration failed!")
            return None
    except Exception as e:
        print(f"❌ Registration request failed: {e}")
        return None

def test_login():
    """Test user login"""
    print("\n=== Testing Login ===")
    base_url = 'https://calloutracing-backend-production.up.railway.app/api/auth'
    
    # Test login with test user
    login_data = {
        'username': 'testuser123',
        'password': 'TestPassword123!'
    }
    
    try:
        response = requests.post(f'{base_url}/login/', json=login_data)
        print(f"Login response: {response.status_code}")
        print(f"Login result: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            return response.json()
        else:
            print("❌ Login failed!")
            return None
    except Exception as e:
        print(f"❌ Login request failed: {e}")
        return None

def test_database_connection():
    """Test database connection and user model"""
    print("\n=== Testing Database Connection ===")
    
    try:
        # Test if we can query users
        user_count = User.objects.count()
        print(f"Total users in database: {user_count}")
        
        # Test if we can create a user
        test_user, created = User.objects.get_or_create(
            username='db_test_user',
            defaults={
                'email': 'dbtest@example.com',
                'password': 'pbkdf2_sha256$600000$dummy_hash_for_demo'
            }
        )
        
        if created:
            print("✅ Database user creation successful!")
            # Clean up test user
            test_user.delete()
            print("✅ Test user cleaned up!")
        else:
            print("✅ Database user query successful!")
            
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_settings():
    """Test Django settings"""
    print("\n=== Testing Django Settings ===")
    
    print(f"AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}")
    print(f"INSTALLED_APPS: {[app for app in settings.INSTALLED_APPS if 'auth' in app or 'token' in app]}")
    print(f"REST_FRAMEWORK auth classes: {settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']}")
    
    # Check if authtoken is removed
    if 'rest_framework.authtoken' in settings.INSTALLED_APPS:
        print("❌ authtoken is still in INSTALLED_APPS!")
    else:
        print("✅ authtoken removed from INSTALLED_APPS")
    
    # Check authentication classes
    if 'rest_framework.authentication.TokenAuthentication' in settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']:
        print("❌ TokenAuthentication is still in auth classes!")
    else:
        print("✅ TokenAuthentication removed from auth classes")

def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive Authentication Flow Test")
    print("=" * 60)
    
    # Test 1: Backend health
    backend_ok = test_backend_health()
    
    # Test 2: Django settings
    test_settings()
    
    # Test 3: Database connection
    db_ok = test_database_connection()
    
    # Test 4: Auth endpoints
    test_auth_endpoints()
    
    # Test 5: Registration
    if backend_ok and db_ok:
        test_user = test_registration()
        
        # Test 6: Login
        if test_user:
            test_login()
    
    print("\n" + "=" * 60)
    print("🏁 Authentication Flow Test Complete")
    
    if not backend_ok:
        print("❌ Backend is not responding - check deployment")
    if not db_ok:
        print("❌ Database connection failed - check database")
    if backend_ok and db_ok:
        print("✅ Backend and database are working")

if __name__ == '__main__':
    main() 