#!/usr/bin/env python
"""
Test script to debug the check-user endpoint
"""
import requests
import json

# Test configuration
BASE_URL = "https://calloutracing-backend-production.up.railway.app/api"

def test_check_user():
    """Test the check-user endpoint"""
    print("Testing check-user endpoint...")
    
    # Test 1: Without CSRF token
    print("\n1. Testing without CSRF token:")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/check-user/",
            json={"username": "testuser"},
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: With CSRF token
    print("\n2. Testing with CSRF token:")
    try:
        # First get CSRF token
        csrf_response = requests.get(f"{BASE_URL}/auth/csrf/")
        csrf_token = csrf_response.cookies.get('csrftoken')
        
        if csrf_token:
            response = requests.post(
                f"{BASE_URL}/auth/check-user/",
                json={"username": "testuser"},
                headers={
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrf_token
                },
                cookies={"csrftoken": csrf_token}
            )
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
        else:
            print("   No CSRF token received")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: With session
    print("\n3. Testing with session:")
    try:
        session = requests.Session()
        
        # Get CSRF token
        csrf_response = session.get(f"{BASE_URL}/auth/csrf/")
        
        response = session.post(
            f"{BASE_URL}/auth/check-user/",
            json={"username": "testuser"},
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_check_user() 