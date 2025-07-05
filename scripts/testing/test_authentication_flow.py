#!/usr/bin/env python3
"""
Test Authentication Flow
Tests the complete authentication flow including login, profile access, and session management.
"""

import requests
import json
import sys

# Configuration
BASE_URL = "https://calloutracing-backend-production.up.railway.app/api"
LOGIN_URL = f"{BASE_URL}/auth/login/"
PROFILE_URL = f"{BASE_URL}/auth/profile/"
SSO_CONFIG_URL = f"{BASE_URL}/auth/sso-config/"

def test_authentication_flow():
    """Test the complete authentication flow."""
    print("🔐 Testing Authentication Flow")
    print("=" * 50)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Test 1: Check SSO config (should work without auth)
    print("\n1. Testing SSO Config (no auth required)...")
    try:
        response = session.get(SSO_CONFIG_URL)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ SSO config accessible")
        else:
            print(f"   ❌ SSO config failed: {response.text}")
    except Exception as e:
        print(f"   ❌ SSO config error: {e}")
    
    # Test 2: Try to access profile without authentication
    print("\n2. Testing Profile Access (no auth)...")
    try:
        response = session.get(PROFILE_URL)
        print(f"   Status: {response.status_code}")
        if response.status_code == 403:
            print("   ✅ Profile correctly requires authentication")
        else:
            print(f"   ❌ Unexpected status: {response.text}")
    except Exception as e:
        print(f"   ❌ Profile access error: {e}")
    
    # Test 3: Login with valid credentials
    print("\n3. Testing Login...")
    login_data = {
        "username": "njs_33487@outlook.com",
        "password": "123qweQWE$$"
    }
    
    try:
        response = session.post(LOGIN_URL, json=login_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Login successful")
            user_data = response.json()
            print(f"   User: {user_data.get('user', {}).get('username', 'Unknown')}")
        else:
            print(f"   ❌ Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    # Test 4: Try to access profile after login
    print("\n4. Testing Profile Access (after login)...")
    try:
        response = session.get(PROFILE_URL)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Profile accessible after login")
            profile_data = response.json()
            print(f"   User: {profile_data.get('username', 'Unknown')}")
        else:
            print(f"   ❌ Profile access failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Profile access error: {e}")
        return False
    
    # Test 5: Test session persistence
    print("\n5. Testing Session Persistence...")
    try:
        response = session.get(PROFILE_URL)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Session persists across requests")
        else:
            print(f"   ❌ Session lost: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Session test error: {e}")
        return False
    
    # Test 6: Logout
    print("\n6. Testing Logout...")
    try:
        logout_url = f"{BASE_URL}/auth/logout/"
        response = session.post(logout_url)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Logout successful")
        else:
            print(f"   ❌ Logout failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Logout error: {e}")
    
    # Test 7: Try to access profile after logout
    print("\n7. Testing Profile Access (after logout)...")
    try:
        response = session.get(PROFILE_URL)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 403:
            print("   ✅ Profile correctly requires authentication after logout")
        else:
            print(f"   ❌ Unexpected status after logout: {response.text}")
    except Exception as e:
        print(f"   ❌ Post-logout test error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Authentication flow test completed successfully!")
    return True

def test_cors_headers():
    """Test CORS headers."""
    print("\n🌐 Testing CORS Headers")
    print("=" * 30)
    
    session = requests.Session()
    
    # Test OPTIONS request
    print("\n1. Testing CORS Preflight...")
    try:
        response = session.options(LOGIN_URL)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"     {header}: {value}")
    except Exception as e:
        print(f"   ❌ CORS test error: {e}")
    
    # Test actual request
    print("\n2. Testing CORS on actual request...")
    try:
        response = session.post(LOGIN_URL, json={
            "username": "njs_33487@outlook.com",
            "password": "123qweQWE$$"
        })
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"     {header}: {value}")
    except Exception as e:
        print(f"   ❌ CORS test error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Authentication Tests")
    print("=" * 50)
    
    # Test authentication flow
    auth_success = test_authentication_flow()
    
    # Test CORS headers
    test_cors_headers()
    
    if auth_success:
        print("\n🎉 All tests passed! Authentication is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the authentication configuration.")
        sys.exit(1) 