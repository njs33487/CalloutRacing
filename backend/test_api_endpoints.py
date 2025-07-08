#!/usr/bin/env python
"""
Test script to check API endpoints that were failing
"""
import requests
import json

# Test configuration
BASE_URL = "https://calloutracing-backend-production.up.railway.app/api"

def test_endpoint(endpoint, method="GET", data=None, headers=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        print(f"{method} {endpoint}: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"  ✅ Success - Response length: {len(str(result))}")
            except:
                print(f"  ✅ Success - Non-JSON response")
        elif response.status_code == 403:
            print(f"  ⚠️  Forbidden (expected for unauthenticated requests)")
        elif response.status_code == 404:
            print(f"  ❌ Not Found")
        elif response.status_code == 500:
            print(f"  ❌ Server Error")
            try:
                error_detail = response.json()
                print(f"  Error details: {error_detail}")
            except:
                print(f"  Error text: {response.text[:200]}")
        else:
            print(f"  ❓ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")

def main():
    """Test all the endpoints that were failing"""
    print("Testing API endpoints that were previously failing...")
    print("=" * 60)
    
    # Test endpoints that were returning 500 errors
    endpoints_to_test = [
        "/events/upcoming/",
        "/callouts/",
        "/callouts/?status=pending&limit=5",
        "/social/feed/?page=1",
        "/sponsored-content/?display_location=homepage",
        "/profiles/64/",
    ]
    
    for endpoint in endpoints_to_test:
        test_endpoint(endpoint)
        print()
    
    # Test authentication endpoints
    print("Testing authentication endpoints...")
    print("=" * 60)
    
    auth_endpoints = [
        "/auth/login/",
        "/auth/logout/",
        "/auth/csrf/",
    ]
    
    for endpoint in auth_endpoints:
        if endpoint == "/auth/login/":
            # Test with sample data
            test_endpoint(endpoint, method="POST", data={
                "username": "test@example.com",
                "password": "testpassword"
            })
        else:
            test_endpoint(endpoint)
        print()

if __name__ == "__main__":
    main() 