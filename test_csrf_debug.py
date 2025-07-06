#!/usr/bin/env python3
"""
Debug script to test CSRF token issues
"""

import requests
import json

# Configuration
BASE_URL = "https://calloutracing-backend-production.up.railway.app/api"
LOGIN_URL = f"{BASE_URL}/auth/login/"
REGISTER_URL = f"{BASE_URL}/auth/register/"
CHECK_USER_URL = f"{BASE_URL}/auth/check-user/"
CSRF_URL = f"{BASE_URL}/auth/csrf/"

def test_csrf_debug():
    """Test CSRF token handling in detail"""
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("=== CSRF Debug Test ===")
    
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
    
    # Step 2: Check cookies
    print("\n2. Checking cookies...")
    cookies = session.cookies
    print(f"   All cookies: {dict(cookies)}")
    
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
    
    # Step 3: Test check-user endpoint (which is failing in your logs)
    print("\n3. Testing check-user endpoint...")
    check_user_data = {
        "username": "testuser"
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_cookie if csrf_cookie else ''
    }
    
    print(f"   Headers: {headers}")
    
    try:
        check_response = session.post(CHECK_USER_URL, json=check_user_data, headers=headers)
        print(f"   Status: {check_response.status_code}")
        print(f"   Response: {check_response.text}")
        
        if check_response.status_code == 200:
            print("   ✓ Check-user successful")
        elif check_response.status_code == 403:
            print("   ✗ Check-user failed with 403 - CSRF issue")
        else:
            print(f"   ? Unexpected status: {check_response.status_code}")
    except Exception as e:
        print(f"   ✗ Error during check-user: {e}")
    
    # Step 4: Test register endpoint (which is also failing)
    print("\n4. Testing register endpoint...")
    register_data = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        register_response = session.post(REGISTER_URL, json=register_data, headers=headers)
        print(f"   Status: {register_response.status_code}")
        print(f"   Response: {register_response.text}")
        
        if register_response.status_code == 201:
            print("   ✓ Register successful")
        elif register_response.status_code == 403:
            print("   ✗ Register failed with 403 - CSRF issue")
        elif register_response.status_code == 400:
            print("   ✓ Register failed as expected (user exists)")
        else:
            print(f"   ? Unexpected status: {register_response.status_code}")
    except Exception as e:
        print(f"   ✗ Error during register: {e}")
    
    # Step 5: Test login endpoint
    print("\n5. Testing login endpoint...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        login_response = session.post(LOGIN_URL, json=login_data, headers=headers)
        print(f"   Status: {login_response.status_code}")
        print(f"   Response: {login_response.text}")
        
        if login_response.status_code == 200:
            print("   ✓ Login successful")
        elif login_response.status_code == 401:
            print("   ✓ Login failed as expected (invalid credentials)")
        elif login_response.status_code == 403:
            print("   ✗ Login failed with 403 - CSRF issue")
        else:
            print(f"   ? Unexpected status: {login_response.status_code}")
    except Exception as e:
        print(f"   ✗ Error during login: {e}")
    
    print("\n=== Test completed! ===")
    print("\nIf you see 403 errors, the issue is likely:")
    print("1. CSRF token not being sent correctly")
    print("2. CSRF token validation failing on the backend")
    print("3. Session/cookie domain issues")

if __name__ == "__main__":
    test_csrf_debug() 