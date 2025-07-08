#!/usr/bin/env python
"""
Test script to check if authentication classes are causing the 403 error
"""
import requests
import json

# Test configuration
BASE_URL = "https://calloutracing-backend-production.up.railway.app/api"

def test_with_different_auth_headers():
    """Test with different authentication headers"""
    print("Testing with different authentication headers...")
    
    session = requests.Session()
    
    # Get CSRF token first
    csrf_response = session.get(f"{BASE_URL}/auth/csrf/")
    csrf_token = csrf_response.cookies.get('csrftoken')
    
    # Test cases
    test_cases = [
        {
            "name": "No auth headers",
            "headers": {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token
            }
        },
        {
            "name": "With Authorization header",
            "headers": {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
                "Authorization": "Bearer dummy-token"
            }
        },
        {
            "name": "With session cookie",
            "headers": {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token
            },
            "cookies": {"sessionid": "dummy-session"}
        },
        {
            "name": "With both session and auth",
            "headers": {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
                "Authorization": "Bearer dummy-token"
            },
            "cookies": {"sessionid": "dummy-session"}
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        try:
            response = session.post(
                f"{BASE_URL}/auth/check-user/",
                json={"username": "testuser"},
                headers=test_case["headers"],
                cookies=test_case.get("cookies", {})
            )
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:100]}")
            
            if response.status_code == 403:
                print("   ❌ 403 Forbidden")
            elif response.status_code == 200:
                print("   ✅ Success")
            else:
                print(f"   ⚠️  Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"   Error: {e}")

def test_other_endpoints():
    """Test other endpoints to see if they have the same issue"""
    print("\n" + "="*50)
    print("Testing other endpoints...")
    
    session = requests.Session()
    
    # Get CSRF token
    csrf_response = session.get(f"{BASE_URL}/auth/csrf/")
    csrf_token = csrf_response.cookies.get('csrftoken')
    
    endpoints = [
        "/auth/csrf/",
        "/auth/sso-config/",
        "/auth/check-user/",
        "/sponsored-content/",
        "/events/upcoming/"
    ]
    
    for endpoint in endpoints:
        print(f"\nTesting: {endpoint}")
        try:
            if endpoint == "/auth/check-user/":
                # POST request
                response = session.post(
                    f"{BASE_URL}{endpoint}",
                    json={"username": "testuser"},
                    headers={
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrf_token
                    }
                )
            else:
                # GET request
                response = session.get(
                    f"{BASE_URL}{endpoint}",
                    headers={"X-CSRFToken": csrf_token}
                )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 403:
                print("   ❌ 403 Forbidden")
            elif response.status_code == 200:
                print("   ✅ Success")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
                
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    test_with_different_auth_headers()
    test_other_endpoints() 