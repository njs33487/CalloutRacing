#!/usr/bin/env python3
"""
Test script to verify CSRF and authentication fixes
"""

import requests
import json
import time

# Configuration
BASE_URL = "https://calloutracing-backend-production.up.railway.app/api"
LOGIN_URL = f"{BASE_URL}/auth/login/"
PROFILE_URL = f"{BASE_URL}/auth/profile/"
CSRF_URL = f"{BASE_URL}/auth/csrf/"

def test_csrf_and_auth_flow():
    """Test the complete CSRF and authentication flow"""
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("=== Testing CSRF and Authentication Flow ===")
    
    # Step 1: Get CSRF token
    print("\n1. Getting CSRF token...")
    try:
        csrf_response = session.get(CSRF_URL)
        print(f"   Status: {csrf_response.status_code}")
        print(f"   Response: {csrf_response.text}")
        
        if csrf_response.status_code == 200:
            print("   ✓ CSRF token obtained successfully")
        else:
            print(f"   ✗ Failed to get CSRF token")
            return
    except Exception as e:
        print(f"   ✗ Error getting CSRF token: {e}")
        return
    
    # Step 2: Check what cookies we have
    print("\n2. Checking cookies...")
    cookies = session.cookies
    print(f"   Session cookies: {dict(cookies)}")
    
    csrf_cookie = cookies.get('csrftoken')
    session_cookie = cookies.get('sessionid')
    
    if csrf_cookie:
        print(f"   ✓ CSRF cookie found: {csrf_cookie[:20]}...")
    else:
        print("   ✗ No CSRF cookie found")
    
    if session_cookie:
        print(f"   ✓ Session cookie found: {session_cookie[:20]}...")
    else:
        print("   ✓ No session cookie (expected for unauthenticated user)")
    
    # Step 3: Try to login with test credentials
    print("\n3. Testing login with test credentials...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    # Set the CSRF token header
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_cookie if csrf_cookie else ''
    }
    
    try:
        login_response = session.post(LOGIN_URL, json=login_data, headers=headers)
        print(f"   Status: {login_response.status_code}")
        print(f"   Response: {login_response.text}")
        
        if login_response.status_code == 200:
            print("   ✓ Login successful")
            user_data = login_response.json()
            print(f"   User: {user_data.get('user', {}).get('username', 'Unknown')}")
        elif login_response.status_code == 401:
            print("   ✓ Login failed as expected (invalid credentials)")
        elif login_response.status_code == 403:
            print("   ✗ Login failed with 403 Forbidden - CSRF issue")
            print("   This indicates the CSRF token is not being accepted")
        else:
            print(f"   ? Unexpected status code: {login_response.status_code}")
    except Exception as e:
        print(f"   ✗ Error during login: {e}")
    
    # Step 4: Check profile (should work if authenticated)
    print("\n4. Checking profile...")
    try:
        profile_response = session.get(PROFILE_URL)
        print(f"   Status: {profile_response.status_code}")
        print(f"   Response: {profile_response.text}")
        
        if profile_response.status_code == 200:
            print("   ✓ Profile accessible")
        elif profile_response.status_code == 401:
            print("   ✓ Profile requires authentication (as expected)")
        else:
            print(f"   ? Unexpected profile status: {profile_response.status_code}")
    except Exception as e:
        print(f"   ✗ Error checking profile: {e}")
    
    # Step 5: Test with valid credentials (if you have them)
    print("\n5. Testing with valid credentials...")
    # Replace with actual test credentials if available
    valid_credentials = {
        "username": "nojusi334@gmail.com",  # Use the email from your logs
        "password": "your_password_here"    # Replace with actual password
    }
    
    print("   Note: Replace 'your_password_here' with actual password to test")
    print("   Skipping this step for security...")
    
    print("\n=== Test completed! ===")
    print("\nNext steps:")
    print("1. Check the browser console for CSRF token logs")
    print("2. Verify cookies are being set correctly")
    print("3. Test the login flow in the browser")

if __name__ == "__main__":
    test_csrf_and_auth_flow() 