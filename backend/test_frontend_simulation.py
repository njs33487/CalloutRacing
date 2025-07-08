#!/usr/bin/env python
"""
Test script to simulate frontend behavior and reproduce the 403 error
"""
import requests
import json

# Test configuration
BASE_URL = "https://calloutracing-backend-production.up.railway.app/api"

def simulate_frontend_behavior():
    """Simulate exactly what the frontend is doing"""
    print("Simulating frontend behavior...")
    
    session = requests.Session()
    
    # Step 1: Get CSRF token (like frontend does)
    print("\n1. Getting CSRF token...")
    csrf_response = session.get(f"{BASE_URL}/auth/csrf/")
    csrf_token = csrf_response.cookies.get('csrftoken')
    print(f"   CSRF Token: {csrf_token}")
    print(f"   Status: {csrf_response.status_code}")
    
    # Step 2: Make the check-user request (like frontend does)
    print("\n2. Making check-user request...")
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token
    }
    
    # Test with username
    data = {"username": "testuser"}
    print(f"   Request data: {data}")
    print(f"   Headers: {headers}")
    
    try:
        response = session.post(
            f"{BASE_URL}/auth/check-user/",
            json=data,
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 403:
            print("   ❌ 403 Forbidden - This reproduces the frontend issue!")
        elif response.status_code == 200:
            print("   ✅ Success")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 3: Test with email
    print("\n3. Testing with email...")
    data = {"email": "test@example.com"}
    print(f"   Request data: {data}")
    
    try:
        response = session.post(
            f"{BASE_URL}/auth/check-user/",
            json=data,
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 403:
            print("   ❌ 403 Forbidden - This reproduces the frontend issue!")
        elif response.status_code == 200:
            print("   ✅ Success")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"   Error: {e}")

def test_without_csrf():
    """Test without CSRF token to see if that's the issue"""
    print("\n" + "="*50)
    print("Testing without CSRF token...")
    
    session = requests.Session()
    
    # Make request without CSRF token
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {"username": "testuser"}
    
    try:
        response = session.post(
            f"{BASE_URL}/auth/check-user/",
            json=data,
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 403:
            print("   ❌ 403 Forbidden")
        elif response.status_code == 200:
            print("   ✅ Success")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
            
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    simulate_frontend_behavior()
    test_without_csrf() 