#!/usr/bin/env python3
"""
Test script to verify authentication fix
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api"
LOGIN_URL = f"{BASE_URL}/auth/login/"
PROFILE_URL = f"{BASE_URL}/auth/profile/"
CSRF_URL = f"{BASE_URL}/auth/csrf/"

def test_authentication_flow():
    """Test the authentication flow to ensure 403 errors are resolved"""
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("Testing authentication flow...")
    
    # Step 1: Get CSRF token
    print("1. Getting CSRF token...")
    try:
        csrf_response = session.get(CSRF_URL)
        print(f"   CSRF Response: {csrf_response.status_code}")
        if csrf_response.status_code == 200:
            print("   ✓ CSRF token obtained successfully")
        else:
            print(f"   ✗ Failed to get CSRF token: {csrf_response.text}")
    except Exception as e:
        print(f"   ✗ Error getting CSRF token: {e}")
        return
    
    # Step 2: Try to login with test credentials
    print("2. Testing login with test credentials...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        login_response = session.post(LOGIN_URL, json=login_data)
        print(f"   Login Response: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("   ✓ Login successful")
            user_data = login_response.json()
            print(f"   User: {user_data.get('user', {}).get('username', 'Unknown')}")
        elif login_response.status_code == 401:
            print("   ✓ Login failed as expected (invalid credentials)")
        elif login_response.status_code == 403:
            print("   ✗ Login failed with 403 Forbidden - this is the issue we're fixing")
        else:
            print(f"   ? Unexpected status code: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
    except Exception as e:
        print(f"   ✗ Error during login: {e}")
    
    # Step 3: Check profile (should work if authenticated)
    print("3. Checking profile...")
    try:
        profile_response = session.get(PROFILE_URL)
        print(f"   Profile Response: {profile_response.status_code}")
        
        if profile_response.status_code == 200:
            print("   ✓ Profile accessible")
        elif profile_response.status_code == 401:
            print("   ✓ Profile requires authentication (as expected)")
        else:
            print(f"   ? Unexpected profile status: {profile_response.status_code}")
    except Exception as e:
        print(f"   ✗ Error checking profile: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_authentication_flow() 